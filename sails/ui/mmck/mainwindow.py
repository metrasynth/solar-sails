import os
import traceback
from collections import defaultdict
from time import strftime

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QFileDialog
from PyQt5.uic import loadUiType

from arrow import now
import rv.api as rv
from rv.cmidmap import MidiMessageType
from sails.midi.ccmappings import cc_mappings
from sails.ui import App
from sails.ui.mmck.ccmapper import CCMapper
from sails.ui.mmck.filewatcher import FileWatcher
from sails.ui.mmck.noteplayer import NotePlayer
from sails.ui.mmck.sunvoxprocess import SunvoxProcess
from sails.ui.outputcatcher import OutputCatcher
from sf.mmck.kit import Kit

from sails.ui.mainmenubar import MainMenuBar
from sails.ui.mmck.parameters.manager import ParametersManager
from sails.ui.mmck.controllers.manager import ControllersManager, Group
from sf.mmck.parameters import ParameterValues

UIC_NAME = 'mainwindow.ui'
UIC_PATH = os.path.join(os.path.dirname(__file__), UIC_NAME)

Ui_MmckMainWindow, MmckMainWindowBase = loadUiType(UIC_PATH)

EMPTY_GROUP = Group()


class MmckMainMenuBar(MainMenuBar):

    def create_menus(self):
        super().create_menus()
        self.view_menu = self.addMenu('&View')
        self.insertMenu(self.tools_menu.menuAction(), self.view_menu)


class MmckMainWindow(MmckMainWindowBase, Ui_MmckMainWindow):

    def __init__(self):
        super(MmckMainWindow, self).__init__(None)
        self.clear_midi_mapping()
        self.loaded_path = None
        self.kit = Kit()
        self.setupUi(self)

    def setupUi(self, ui):
        super(MmckMainWindow, self).setupUi(ui)
        self.setMenuBar(MmckMainMenuBar())
        self.setup_catcher()
        self.setup_menus()
        self.setup_parameters_manager()
        self.setup_controllers_manager()
        self.setup_file_watcher()
        self.setup_sunvox_process()
        self.setup_note_player()
        self.setup_cc_mapper()

    def setup_catcher(self):
        self.catcher = OutputCatcher(self.output_textedit)

    def setup_menus(self):
        menubar = self.menuBar()
        self.setup_dockwidget_menus(menubar)
        self.setup_file_menus(menubar)

    def setup_dockwidget_menus(self, menubar):
        for action in [
            self.action_view_output,
            self.action_view_parameters,
            self.action_view_udc,
        ]:
            menubar.view_menu.addAction(action)

    def setup_file_menus(self, menubar):
        sep = menubar.file_menu.insertSeparator(menubar.file_settings)
        for action in [
            self.action_save,
            self.action_save_as,
            self.action_export_metamodule,
            self.action_export_project,
        ]:
            menubar.file_menu.insertAction(sep, action)

    def setup_parameters_manager(self):
        self.parameters_manager = ParametersManager(
            parent=self.parameters_scrollarea,
            layout=self.parameters_layout,
            parameters={},
            values=self.kit.parameter_values,
        )
        self.parameters_manager.valuesChanged.connect(
            self.on_parameters_manager_valuesChanged)

    def setup_controllers_manager(self):
        self.controllers_manager = ControllersManager(
            parent=self.controllers_scrollarea,
            layout=self.controllers_layout,
            root_group=EMPTY_GROUP,
        )
        self.controllers_manager.mapping_changed.connect(
            self.on_controllers_manager_mapping_changed)
        self.controllers_manager.value_changed.connect(
            self.on_controllers_manager_value_changed)
        self.controllers_manager.udc_changed.connect(
            self.on_controllers_manager_udc_changed)

    def setup_file_watcher(self):
        self.file_watcher = FileWatcher(self)
        self.file_watcher.fileChanged.connect(self.on_file_watcher_fileChanged)

    def setup_sunvox_process(self):
        self.sunvox_process = SunvoxProcess(self)

    def setup_note_player(self):
        self.note_player = NotePlayer(self.sunvox_process.slot, self)

    def setup_cc_mapper(self):
        self.cc_mapper = CCMapper(self.sunvox_process.slot, self)
        self.cc_mapper.controlValueChanged.connect(self.on_cc_mapper_controlValueChanged)

    @property
    def slot(self):
        return self.sunvox_process.slot

    def clear_midi_mapping(self):
        self.controller_aliases = defaultdict(set)
        self.alias_controllers = defaultdict(set)

    # noinspection PyBroadException
    def load_file(self, path):
        self.loaded_path = path
        self.kit.name = os.path.basename(path)[:-len('.mmck.py')]
        self.setWindowTitle(path)
        self.parameters_manager.clear_widgets()
        with self.catcher:
            try:
                with open(path, 'r') as f:
                    self.kit.py_source = f.read()
                self.load_kit_parameter_values()
                self.parameters_manager.parameters = self.kit.parameters
                self.rebuild_project()
                self.auto_map_controllers()
            except Exception:
                print(traceback.format_exc())
                return
            else:
                print('Finished loading at {}'.format(strftime('%c')))
        self.file_watcher.path = path

    def auto_map_controllers(self):
        for alias, (name, w) in zip(cc_mappings.options[1:], self.controllers_manager.controller_widgets.items()):
            try:
                w.set_cc_alias(alias)
            except (SystemError, RuntimeError):
                continue
            mod = w.module
            ctl = w.ctl
            ccs = cc_mappings.alias_ccs[alias]
            if ccs:
                cc = list(sorted(ccs))[0]
                midmap = mod.controller_midi_maps[ctl.name]
                midmap.message_type = MidiMessageType.control_change
                midmap.message_parameter = cc

    def rebuild_project(self):
        project, root_group = self.kit.project
        self.sunvox_process.slot.load(project)
        self.controllers_manager.root_group = root_group

    def load_kit_parameter_values(self):
        App.settings.beginGroup('mmck_params')
        try:
            saved_params = App.settings.value(self.kit.name)
            if saved_params:
                self.kit.parameter_values.update(saved_params)
        finally:
            App.settings.endGroup()

    def save_kit_parameter_values(self):
        App.settings.beginGroup('mmck_params')
        try:
            App.settings.setValue(self.kit.name, dict(self.kit.parameter_values))
        finally:
            App.settings.endGroup()

    @pyqtSlot(str, str)
    def on_controllers_manager_mapping_changed(self, alias, name):
        # first remove existing controller/alias mappings
        for a in list(self.controller_aliases[name]):
            if name in self.alias_controllers[a]:
                self.alias_controllers[a].remove(name)
            if a in self.controller_aliases[name]:
                self.controller_aliases[name].remove(a)
        self.alias_controllers[alias].add(name)
        self.controller_aliases[name].add(alias)

    @pyqtSlot(int, str)
    def on_controllers_manager_value_changed(self, value, name):
        c = self.controllers_manager.root_group
        if c:
            controller = c[name]
            mod = controller.module.index + 1
            ctl = controller.ctl.number
            pvalue = controller.ctl.pattern_value(value)
            self.slot.send_event(0, 0, 0, mod, ctl << 8, pvalue)

    @pyqtSlot(bool, str)
    def on_controllers_manager_udc_changed(self, state, name):
        pass
        # if state and name not in self.udc_list:
        #     self.udc_list.append(name)
        # elif not state and name in self.udc_list:
        #     self.udc_list.remove(name)
        # self.update_udc_widgets()

    # noinspection PyBroadException
    @pyqtSlot()
    def on_parameters_manager_valuesChanged(self):
        with self.catcher:
            try:
                self.rebuild_project()
                self.auto_map_controllers()
            except Exception:
                print(traceback.format_exc())
                return
            else:
                print('Rebuilt project at {}'.format(strftime('%c')))
        if self.kit.name:
            self.save_kit_parameter_values()

    @pyqtSlot()
    def on_file_watcher_fileChanged(self):
        if self.loaded_path:
            self.load_file(self.loaded_path)

    @pyqtSlot(str, int)
    def on_cc_mapper_controlValueChanged(self, name, value):
        print(name, value)
        self.controllers_manager.set_ctl_value(name, value)

    @pyqtSlot()
    def on_action_export_metamodule_triggered(self):
        path = self.loaded_path
        if path:
            project, c = self.kit.project
            metamod = rv.m.MetaModule(project=project)
            # udc_list = self.main_widget.udc_list
            # metamod.user_defined_controllers = min(27, len(udc_list))
            # for i, name in zip(range(0, 27), udc_list):
            #     grpname, ctlname = name.split('.')
            #     ctl = self.main_widget.kit.project_module.c[grpname][ctlname]
            #     mapping = metamod.mappings.values[i]
            #     mapping.module = ctl.module.index
            #     mapping.controller = ctl.ctl.number
            #     metamod.user_defined[i].label = name
            synth = rv.Synth(metamod)
            slug = project.name.lower().replace(' ', '-')
            timestamp = now().strftime('%Y%m%d%H%M%S')
            filename = '{}-{}-{}.sunsynth'.format(path, slug, timestamp)
            with open(filename, 'wb') as f:
                synth.write_to(f)

    @pyqtSlot()
    def on_action_export_project_triggered(self):
        path = self.loaded_path
        if path:
            project, c = self.kit.project
            slug = project.name.lower().replace(' ', '-')
            timestamp = now().strftime('%Y%m%d%H%M%S')
            filename = '{}-{}-{}.sunvox'.format(path, slug, timestamp)
            with open(filename, 'wb') as f:
                project.write_to(f)

    # @pyqtSlot()
    # def on_action_save_triggered(self):
    #     path = self.loaded_path
    #     if not path:
    #         self.on_action_save_as_triggered()
    #     else:
    #         with open(path, 'w') as f:
    #             f.write(self.main_widget.kit.to_json())
    #
    # @pyqtSlot()
    # def on_action_save_as_triggered(self):
    #     path, _ = QFileDialog.getSaveFileName(
    #         parent=self,
    #         caption='Save MMCK file',
    #         directory='.',
    #         filter=MmckOpener.filter(),
    #     )
    #     if path:
    #         self.setWindowFilePath(path)
    #         self.on_action_save_triggered()
