from collections import OrderedDict
from enum import Enum

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QGroupBox, QLabel, QVBoxLayout, QWidget, QHBoxLayout
from rv.controller import Range
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

    def set_ctl_value(self, name, value):
        self.widgets[name].set_ctl_value(value)

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
            hlayout.addWidget(udc_combobox)
            hlayout.addSpacing(5)
            hlayout.addWidget(label, 1)
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

    def set_ctl_value(self, value):
        self.managed_widget.set_ctl_value(value)


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
