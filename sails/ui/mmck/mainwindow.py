import json
import os
import traceback
from collections import defaultdict
from time import strftime

import io
from PyQt5.QtCore import pyqtSlot, Qt, QTimer
from PyQt5.QtWidgets import QFileDialog, QProgressDialog
from PyQt5.uic import loadUiType

from arrow import now
import numpy as np
import rv.api as rv
from rv.cmidmap import MidiMessageType
from rv.modules.metamodule import MAX_USER_DEFINED_CONTROLLERS
from rv.note import NOTE, NOTECMD
from sails.midi.ccmappings import cc_mappings
from sails.ui import App
from sails.ui.mainmenubar import MainMenuBar
from sails.ui.mmck.ccmapper import CCMapper
from sails.ui.mmck.controllers.manager import ControllersManager, Group
from sails.ui.mmck.filewatcher import FileWatcher
from sails.ui.mmck.noteplayer import NotePlayer
from sails.ui.mmck.parameters.manager import ParametersManager
from sails.ui.mmck.sunvoxprocess import SunvoxProcess
from sails.ui.mmck.udcmanager import UdcManager
from sails.ui.outputcatcher import OutputCatcher

try:
    from scipy.io import wavfile
except ImportError:
    wavfile = None
from sf.mmck.controllers import Controller
from sf.mmck.kit import Kit
from sunvox.api import Slot
from sunvox.buffered import BufferedProcess, float32


UIC_NAME = "mainwindow.ui"
UIC_PATH = os.path.join(os.path.dirname(__file__), UIC_NAME)

Ui_MmckMainWindow, MmckMainWindowBase = loadUiType(UIC_PATH)

EMPTY_GROUP = Group()

CONTROLLER_AUTOSAVE_TIMEOUT = 250


class MmckMainMenuBar(MainMenuBar):
    def create_menus(self):
        super().create_menus()
        self.edit_menu = self.addMenu("&Edit")
        self.transport_menu = self.addMenu("&Transport")
        self.view_menu = self.addMenu("&View")
        self.insertMenu(self.edit_menu.menuAction(), self.edit_menu)
        self.insertMenu(self.transport_menu.menuAction(), self.transport_menu)
        self.insertMenu(self.view_menu.menuAction(), self.view_menu)


class MmckMainWindow(MmckMainWindowBase, Ui_MmckMainWindow):
    def __init__(self):
        super(MmckMainWindow, self).__init__(None)
        self.clear_midi_mapping()
        self.clear_udc_assignments()
        self.loaded_path = None
        self.kit = Kit()
        self.setupUi(self)
        self.play_started = False

    def setupUi(self, ui):
        super(MmckMainWindow, self).setupUi(ui)
        self.setMenuBar(MmckMainMenuBar())
        self.setup_catcher()
        self.setup_menus()
        self.setup_parameters_manager()
        self.setup_udc_manager()
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
        self.setup_edit_menus(menubar)
        self.setup_transport_menus(menubar)

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
            self.action_import_parameter_values,
            self.action_reset_parameter_values,
            self.action_save,
            self.action_save_as,
            self.action_export_metamodule,
            self.action_export_project,
            self.action_export_wav,
        ]:
            menubar.file_menu.insertAction(sep, action)

    def setup_edit_menus(self, menubar):
        for action in [
            self.action_copy_to_sunvox_clipboard,
            self.action_paste_from_sunvox_clipboard,
            self.action_restore_controller_values,
        ]:
            menubar.edit_menu.addAction(action)

    def setup_transport_menus(self, menubar):
        for action in [
            self.action_play_from_beginning,
            self.action_stop,
        ]:
            menubar.transport_menu.addAction(action)

    def setup_parameters_manager(self):
        self.parameters_manager = ParametersManager(
            parent=self.parameters_scrollarea,
            layout=self.parameters_layout,
            parameters={},
            values=self.kit.parameter_values,
        )
        self.parameters_manager.valuesChanged.connect(
            self.on_parameters_manager_valuesChanged
        )

    def setup_udc_manager(self):
        self.udc_manager = UdcManager(
            parent=self.udc_scrollarea,
            layout=self.udc_layout,
            assignments=self.udc_assignments,
        )

    def setup_controllers_manager(self):
        self.controllers_manager = ControllersManager(
            parent=self.controllers_scrollarea,
            layout=self.controllers_layout,
            root_group=EMPTY_GROUP,
        )
        self.controllers_manager.mappingChanged.connect(
            self.on_controllers_manager_mappingChanged
        )
        self.controllers_manager.valueChanged.connect(
            self.on_controllers_manager_valueChanged
        )
        self.controllers_manager.udcChanged.connect(
            self.on_controllers_manager_udcChanged
        )

    def setup_file_watcher(self):
        self.file_watcher = FileWatcher(self)
        self.file_watcher.fileChanged.connect(self.on_file_watcher_fileChanged)

    def setup_sunvox_process(self):
        self.sunvox_process = SunvoxProcess(self)

    def setup_note_player(self):
        self.note_player = NotePlayer(self)
        self.note_player.noteOn.connect(self.on_note_player_noteOn)
        self.note_player.noteOff.connect(self.on_note_player_noteOff)

    def setup_cc_mapper(self):
        self.cc_mapper = CCMapper(self)
        self.cc_mapper.controlValueChanged.connect(
            self.on_cc_mapper_controlValueChanged
        )

    @property
    def slot(self):
        return self.sunvox_process.slot

    def clear_midi_mapping(self):
        self.controller_aliases = defaultdict(set)
        self.alias_controllers = defaultdict(set)

    def clear_udc_assignments(self):
        self.udc_assignments = [set() for _ in range(MAX_USER_DEFINED_CONTROLLERS)]
        if hasattr(self, "udc_manager"):
            self.udc_manager.assignments = self.udc_assignments

    def prune_udc_assignments(self):
        for names in self.udc_assignments:
            for name in names.copy():
                if name not in self.kit.controllers:
                    names.remove(name)
        self.udc_manager.assignments = self.udc_assignments

    def update_udc_assignments(self, assignments):
        for existing, new in zip(self.udc_assignments, assignments):
            existing.update({new} if isinstance(new, str) else new)
        if hasattr(self, "udc_manager"):
            self.udc_manager.assignments = self.udc_assignments
        self.controllers_manager.restore_udc_assignments(self.udc_assignments)

    # noinspection PyBroadException
    def load_file(self, path):
        self.loaded_path = path
        self.kit.name = os.path.basename(path)[: -len(".mmckpy")]
        self.setWindowTitle(path)
        self.parameters_manager.clear_widgets()
        with self.catcher:
            try:
                with open(path, "r") as f:
                    self.kit.py_source = f.read()
                self.load_kit_parameter_values()
                self.parameters_manager.parameters = self.kit.parameters
                self.rebuild_project()
                self.clear_udc_assignments()
                if hasattr(self.kit.py_module, "udc_assignments"):
                    self.update_udc_assignments(
                        self.kit.py_module.udc_assignments(self.kit.parameter_values)
                    )
            except Exception:
                print(traceback.format_exc())
                return
            else:
                print("Finished loading at {}".format(strftime("%c")))
        self.file_watcher.paths = [path] + self.kit.watch_paths

    def auto_map_controllers(self):
        for alias, (name, w) in zip(
            cc_mappings.options[1:], self.controllers_manager.controller_widgets.items()
        ):
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
        values = self.controllers_manager.save_values()
        del self.kit.project
        project = self.kit.project
        self.sunvox_process.slot.load(project)
        self.controllers_manager.root_group = self.kit.controllers
        self.controllers_manager.restore_values(values)
        self.prune_udc_assignments()
        self.controllers_manager.restore_udc_assignments(self.udc_assignments)
        self.auto_map_controllers()

    def reset_parameter_values(self):
        for name, param in self.kit.parameters.items():
            self.kit.parameter_values[name] = param.default

    def load_kit_parameter_values(self):
        App.settings.beginGroup("mmck_params")
        try:
            saved_params = App.settings.value(self.kit.name)
            if saved_params:
                self.kit.parameter_values.update(saved_params)
        finally:
            App.settings.endGroup()

    def save_kit_parameter_values(self):
        App.settings.beginGroup("mmck_params")
        try:
            App.settings.setValue(self.kit.name, dict(self.kit.parameter_values))
        finally:
            App.settings.endGroup()

    def load_controller_values(self):
        App.settings.beginGroup("mmck_controllers")
        try:
            values = dict(App.settings.value(self.kit.name))
            self.controllers_manager.restore_values(values)
        finally:
            App.settings.endGroup()

    def save_controller_values(self):
        values = self.controllers_manager.save_values()
        App.settings.beginGroup("mmck_controllers")
        try:
            App.settings.setValue(
                self.kit.name, dict(self.controllers_manager.save_values())
            )
        finally:
            App.settings.endGroup()

    def exportable_project(self):
        # make a clone of the project as we may be modifying it
        with io.BytesIO() as f:
            project = self.kit.project.write_to(f)
            f.seek(0)
            project = rv.read_sunvox_file(f)
        # store MMCK metadata
        mmckdata = project.new_module(
            rv.m.Sampler,
            name="mmckdata",
            layer=7,
            x=project.output.x,
            y=project.output.y,
        )
        s1 = mmckdata.samples[-1] = mmckdata.Sample()
        s1.data = self.kit.py_source.encode("utf8")
        s1.format = mmckdata.Format.int8
        s1.channels = mmckdata.Channels.mono
        s2 = mmckdata.samples[-2] = mmckdata.Sample()
        s2.data = json.dumps(self.kit.parameter_values).encode("utf8")
        s2.format = mmckdata.Format.int8
        s2.channels = mmckdata.Channels.mono
        s3 = mmckdata.samples[-3] = mmckdata.Sample()
        s3.data = json.dumps(
            list(self.kit.controllers.all_items()),
            default=Controller.to_json,
        ).encode("utf8")
        s3.format = mmckdata.Format.int8
        s3.channels = mmckdata.Channels.mono
        return project

    def export_metamodule(self, filename=None):
        project = self.exportable_project()
        metamod = rv.m.MetaModule(
            project=project, name=project.name, apply_velocity_to_project=True
        )
        assignments = self.udc_assignments[:]
        while assignments and not assignments[-1]:
            assignments.pop()
        metamod.user_defined_controllers = len(assignments)
        for i, names in enumerate(assignments):
            mapping = metamod.mappings.values[i]
            if len(names) == 0:
                mapping.module = 0
                mapping.controller = 1
                metamod.user_defined[i].label = ""
            elif len(names) == 1:
                # direct connection
                name = list(names).pop()
                grpname, ctlname = name.split(".")
                controller = self.kit.controllers[grpname][ctlname]
                mapping.module = controller.module.index
                mapping.controller = controller.ctl.number
                metamod.user_defined[i].label = name
            else:
                # bundle into multictl
                c = self.kit.controllers
                macro = rv.m.MultiCtl.macro(
                    project,
                    *[(c[name].module, c[name].ctl) for name in names],
                    name="macro-{}".format(i + 1),
                    layer=7,
                    x=i * 80,
                    y=-80,
                )
                mapping.module = macro.index
                mapping.controller = 1
                metamod.user_defined[i].label = ",".join(sorted(names))
        synth = rv.Synth(metamod)
        if filename is None:
            slug = project.name.lower().replace(" ", "-")
            timestamp = now().strftime("%Y%m%d%H%M%S")
            filename = "{}-{}-{}.sunsynth".format(self.loaded_path, slug, timestamp)
        with open(filename, "wb") as f:
            synth.write_to(f)
        print("Exported synth to {}".format(filename))

    def reset_save_timer(self):
        if not hasattr(self, "save_timer"):
            t = self.save_timer = QTimer(self)
            t.setSingleShot(True)
            t.setInterval(CONTROLLER_AUTOSAVE_TIMEOUT)
            t.timeout.connect(self.on_save_timer_timeout)
        self.save_timer.start()

    @pyqtSlot()
    def on_save_timer_timeout(self):
        self.save_controller_values()

    @pyqtSlot(str, str)
    def on_controllers_manager_mappingChanged(self, alias, name):
        # first remove existing controller/alias mappings
        for a in list(self.controller_aliases[name]):
            if name in self.alias_controllers[a]:
                self.alias_controllers[a].remove(name)
            if a in self.controller_aliases[name]:
                self.controller_aliases[name].remove(a)
        self.alias_controllers[alias].add(name)
        self.controller_aliases[name].add(alias)

    @pyqtSlot(int, str)
    def on_controllers_manager_valueChanged(self, value, name):
        c = self.controllers_manager.root_group
        if not c:
            return
        controller = c[name]
        mod = controller.module
        ctl = controller.ctl
        pvalue = ctl.pattern_value(mod, value)
        setattr(mod, ctl.name, value)
        with self.catcher.more:
            print(f"{ctl.number=} {value=} {pvalue=}")
        self.slot.send_event(0, 0, 0, mod.index + 1, ctl.number << 8, pvalue)
        self.reset_save_timer()

    @pyqtSlot(int, str)
    def on_controllers_manager_udcChanged(self, pos, name):
        pos -= 1
        if pos < 0 or pos > 26:
            return
        for names in self.udc_assignments:
            if name in names:
                names.remove(name)
        self.udc_assignments[pos].add(name)
        self.udc_manager.assignments = self.udc_assignments

    # noinspection PyBroadException
    @pyqtSlot()
    def on_parameters_manager_valuesChanged(self):
        with self.catcher:
            try:
                self.rebuild_project()
                if self.kit.name:
                    self.save_kit_parameter_values()
            except Exception:
                print(traceback.format_exc())
                return
            else:
                print("Rebuilt project at {}".format(strftime("%c")))

    @pyqtSlot()
    def on_file_watcher_fileChanged(self):
        if self.loaded_path:
            self.load_file(self.loaded_path)

    @pyqtSlot(str, int)
    def on_cc_mapper_controlValueChanged(self, name, value):
        self.controllers_manager.set_ctl_value(name, value)

    @pyqtSlot(int, int, int)
    def on_note_player_noteOn(self, track, note, velocity):
        note += 1
        with self.catcher.more:
            print("Note On: {!r}, {}".format(NOTE(note), velocity))
            module = 2
            self.slot.send_event(track, note, velocity, module, 0, 0)

    @pyqtSlot(int)
    def on_note_player_noteOff(self, track):
        self.slot.send_event(track, NOTECMD.NOTE_OFF, 0, 0, 0, 0)

    @pyqtSlot()
    def on_action_copy_to_sunvox_clipboard_triggered(self):
        with self.catcher.more:
            workspace_paths = App.settings.value("sunvox/workspace_paths")
            if len(workspace_paths) == 0:
                print(
                    "To copy to SunVox clipboard, set a workspace path in app settings"
                )
            else:
                path = workspace_paths[0]
                filename = os.path.join(path, ".sunvox_clipboard.sunsynth")
                self.export_metamodule(filename)

    @pyqtSlot()
    def on_action_paste_from_sunvox_clipboard_triggered(self):
        pass

    @pyqtSlot()
    def on_action_export_metamodule_triggered(self, filename=None):
        if self.loaded_path:
            with self.catcher.more:
                self.export_metamodule()

    @pyqtSlot()
    def on_action_export_project_triggered(self):
        path = self.loaded_path
        if path:
            with self.catcher.more:
                project = self.exportable_project()
                slug = project.name.lower().replace(" ", "-")
                timestamp = now().strftime("%Y%m%d%H%M%S")
                filename = "{}-{}-{}.sunvox".format(path, slug, timestamp)
                with open(filename, "wb") as f:
                    project.write_to(f)
                print("Exported project to {}".format(filename))

    @pyqtSlot()
    def on_action_export_wav_triggered(self):
        if wavfile is None:
            with self.catcher.more:
                print("WAV export only available on MacOS (for now!)")
                return
        path = self.loaded_path
        if path:
            with self.catcher.more:
                project = self.exportable_project()
                slug = project.name.lower().replace(" ", "-")
                timestamp = now().strftime("%Y%m%d%H%M%S")
                bpm = project.initial_bpm / (project.initial_tpl / 6)
                filename = "{}-{}-{}bpm-{}.wav".format(path, slug, bpm, timestamp)
                freq = 44100
                size = freq
                channels = 2
                data_type = float32
                p = BufferedProcess(
                    freq=freq, size=size, channels=channels, data_type=data_type
                )
                slot = Slot(project, process=p)
                length = slot.get_song_length_frames()
                output = np.zeros((length, 2), data_type)
                position = 0
                slot.play_from_beginning()
                dialog = QProgressDialog(
                    "Writing WAV to {}".format(filename), "Cancel", 0, length, self
                )
                dialog.setWindowModality(Qt.WindowModal)
                dialog.forceShow()
                cancelled = False
                while position < length:
                    if dialog.wasCanceled():
                        cancelled = True
                        break
                    buffer = p.fill_buffer()
                    end_pos = min(position + freq, length)
                    copy_size = end_pos - position
                    output[position:end_pos] = buffer[:copy_size]
                    position = end_pos
                    dialog.setValue(position)
                if not cancelled:
                    wavfile.write(filename, freq, output)
                    print("Exported project to {}".format(filename))
                else:
                    print("Cancelled export")
                p.deinit()
                p.kill()
                dialog.close()

    @pyqtSlot()
    def on_action_play_from_beginning_triggered(self):
        with self.catcher.more:
            print("Play from beginning")
            self.slot.play_from_beginning()
            self.play_started = True

    @pyqtSlot()
    def on_action_stop_triggered(self):
        with self.catcher.more:
            self.slot.stop()
            self.slot.send_event(0, NOTECMD.ALL_NOTES_OFF, 0, 0, 0, 0)
            if not self.play_started:
                print("Clean synths")
                self.slot.send_event(0, NOTECMD.CLEAN_SYNTHS, 0, 0, 0, 0)
            else:
                print("Stop")
                self.play_started = False

    @pyqtSlot()
    def on_action_restore_controller_values_triggered(self):
        with self.catcher.more:
            print("Restoring controller values")
            self.load_controller_values()

    @pyqtSlot()
    def on_action_import_parameter_values_triggered(self):
        with self.catcher.more:
            filename, _ = QFileDialog.getOpenFileName(
                parent=self,
                caption="Import Parameter Values",
                directory=".",
                filter="Supported Files (*.sunsynth *.sunvox)",
            )
            if filename:
                obj = rv.read_sunvox_file(filename)
                if isinstance(obj, rv.Project):
                    project = obj
                elif isinstance(obj, rv.Synth) and isinstance(
                    obj.module, rv.m.MetaModule
                ):
                    project = obj.module.project
                else:
                    print("{} is not a project or metamodule".format(filename))
                    return
                mmckdata = None
                for mod in reversed(project.modules):
                    if mod.name == "mmckdata":
                        mmckdata = mod
                        break
                if not mmckdata:
                    print("Could not find mmckdata module in {}".format(filename))
                    return
                params = json.loads(mmckdata.samples[-2].data.decode("utf8"))
                self.kit.parameter_values.update(params)
                self.parameters_manager.parameters = self.kit.parameters
                self.rebuild_project()
                self.save_kit_parameter_values()
                if hasattr(self.kit.py_module, "udc_assignments"):
                    self.update_udc_assignments(
                        self.kit.py_module.udc_assignments(self.kit.parameter_values)
                    )
                print("Imported parameter values from {}".format(filename))

    @pyqtSlot()
    def on_action_reset_parameter_values_triggered(self):
        with self.catcher.more:
            self.reset_parameter_values()
            self.parameters_manager.parameters = self.kit.parameters
