from collections import OrderedDict
from enum import Enum

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QGroupBox, QLabel, QVBoxLayout, QWidget, QHBoxLayout
from rv.controller import Range
from rv.modules.metamodule import UserDefinedProxy
from sf.mmck.controllers import Controller, Group

from sails.midi.ccmappings import cc_mappings
from .enum import EnumWidget
from .range import RangeWidget


class BoolEnum(Enum):
    on = False
    off = True


class ControllersManager(QObject):

    mappingChanged = pyqtSignal(str, str)  # alias, name
    valueChanged = pyqtSignal(int, str)  # value, name
    udcChanged = pyqtSignal(int, str)  # position, name

    def __init__(self, parent, layout, root_group):
        super().__init__(parent)
        self._root_group = None
        self.widgets = OrderedDict()
        self.controller_widgets = OrderedDict()
        self.root_layout = layout
        self.root_group = root_group

    @property
    def root_group(self):
        return self._root_group

    @root_group.setter
    def root_group(self, value):
        self.clear_widgets()
        self._root_group = value
        self.create_widgets()

    def set_ctl_value(self, name, value, value_type=None):
        self.widgets[name].set_ctl_value(value, value_type)

    def clear_widgets(self):
        for w in self.widgets.values():
            w.close()
            w.deleteLater()
        while self.root_layout.takeAt(0):
            continue
        self.widgets = OrderedDict()
        self.controller_widgets = OrderedDict()

    def create_widgets(self, prefix='', group=None, group_widget=None,
                       layout=None):
        if group is None:
            group = self.root_group
        if group_widget is None:
            group_widget = self.parent()
            layout = self.root_layout
        else:
            layout = group_widget.layout()
        for name, value in group.items():
            key = prefix + name
            if layout is self.root_layout:
                wlayout = QVBoxLayout()
                layout.addLayout(wlayout)
            else:
                wlayout = layout
            if isinstance(value, Controller):
                widget = ControllerWidget(
                    parent=group_widget,
                    name=key,
                    controller=value,
                )
                wlayout.addWidget(widget)
                self.widgets[key] = widget
                self.controller_widgets[key] = widget
                widget.mappingChanged.connect(self.mappingChanged)
                widget.valueChanged.connect(self.valueChanged)
                widget.udcChanged.connect(self.udcChanged)
            elif isinstance(value, Group):
                subprefix = name + '.'
                groupbox = GroupWidget(
                    parent=group_widget,
                    name=key,
                    group=value,
                )
                wlayout.addWidget(groupbox)
                self.widgets[key] = groupbox
                self.create_widgets(
                    prefix=subprefix,
                    group=value,
                    group_widget=groupbox,
                    layout=wlayout,
                )
            if layout is self.root_layout:
                wlayout.addStretch(1)
        if layout is self.root_layout:
            layout.addStretch(1)

    def _save_values(self, prefix='', group=None):
        if group is None:
            group = self.root_group
        for key, x in group.items():
            if isinstance(x, Group):
                prefix2 = '{}.'.format(key)
                for key2, value2 in self._save_values(prefix2, x):
                    yield key2, value2
            else:
                yield '{}{}'.format(prefix, key), (x.value, x.ctl.value_type)

    def save_values(self):
        return OrderedDict(self._save_values())

    def restore_values(self, values):
        set_values = []
        for key, (value, value_type) in values.items():
            if key in self.widgets:
                if hasattr(value, 'value'):
                    value = value.value
                set_values.append((key, value, value_type))
        if set_values:
            def set_ctl_values():
                for k, v, vt in set_values:
                    self.set_ctl_value(k, v, vt)
            QTimer.singleShot(0, set_ctl_values)

    def restore_udc_assignments(self, assignments):
        for i, names in enumerate(assignments, 1):
            for name in names:
                widget = self.widgets[name]
                widget.udc_combobox.setCurrentText(str(i))


class ControllerWidget(QWidget):

    mappingChanged = pyqtSignal(str, str)  # alias, name
    valueChanged = pyqtSignal(int, str)  # value, name
    udcChanged = pyqtSignal(int, str)  # position, name

    def __init__(self, parent, name, controller):
        super().__init__(parent)
        self.name = name
        module = self.module = controller.module
        ctl = self.ctl = controller.ctl
        value = controller.value
        self.cc_combobox = None
        if isinstance(ctl, UserDefinedProxy):
            ctl = module.user_defined[ctl.number - 6]
        t = ctl.value_type
        if t is bool:
            t = BoolEnum
            value = BoolEnum(value)
        if isinstance(t, Range):
            widget_class = RangeWidget
        elif isinstance(t, type) and issubclass(t, Enum):
            widget_class = EnumWidget
        else:
            widget_class = None
        if widget_class:
            vlayout = QVBoxLayout(self)
            vlayout.setContentsMargins(0, 0, 0, 0)
            vlayout.setSpacing(5)
            self.setLayout(vlayout)
            hlayout = QHBoxLayout()
            hlayout.setContentsMargins(0, 0, 0, 0)
            hlayout.setSpacing(5)
            udc_combobox = self.udc_combobox = UdcComboBox(self)
            label = QLabel(name.split('.')[-1], self)
            cc_combobox = self.cc_combobox = QComboBox(self)
            cc_combobox.addItems(cc_mappings.options)
            cc_combobox.setEditable(True)
            self.managed_widget = w = widget_class(parent=self, value_type=t, initial_value=value)
            hlayout.addWidget(label, 1)
            hlayout.addSpacing(5)
            hlayout.addWidget(udc_combobox)
            hlayout.addWidget(cc_combobox)
            vlayout.addItem(hlayout)
            vlayout.addWidget(w)
            udc_combobox.currentTextChanged.connect(self.on_udc_combobox_currentTextChanged)
            cc_combobox.currentTextChanged.connect(self.on_cc_combobox_currentTextChanged)
            w.value_changed.connect(self.on_child_valueChanged)

    def on_cc_combobox_currentTextChanged(self, text):
        self.mappingChanged.emit(text, self.name)

    def on_udc_combobox_currentTextChanged(self, text):
        self.udcChanged.emit(None if text == '' else int(text), self.name)

    def on_child_valueChanged(self, value):
        self.valueChanged.emit(value, self.name)

    def set_cc_alias(self, alias):
        if self.cc_combobox:
            self.cc_combobox.setCurrentText(alias)
            self.mappingChanged.emit(alias, self.name)

    def set_ctl_value(self, value, value_type=None):
        if not value_type or value_type == self.managed_widget.value_type:
            self.managed_widget.set_ctl_value(value)
        else:
            print('INFO: {} expected {}, got {}'.format(
                self.name, self.managed_widget.value_type, value_type))


class GroupWidget(QGroupBox):

    def __init__(self, parent, name, group):
        super().__init__(parent)
        self.setTitle(name.split('.')[-1])
        self.setLayout(QVBoxLayout(self))


class UdcComboBox(QComboBox):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.addItem('')
        self.addItems(list(map(str, range(1, 28))))
