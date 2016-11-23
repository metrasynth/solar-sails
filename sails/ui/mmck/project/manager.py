from enum import Enum

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QGroupBox, QLabel, QVBoxLayout, QWidget
from rv.controller import Range
from sf.mmck.project import Controller, Group

from .enum import EnumWidget
from .range import RangeWidget


class ControllersManager(QObject):

    _root_group = None

    def __init__(self, parent, layout, root_group):
        super().__init__(parent)
        self.widgets = {}
        self.root_layout = layout
        self.root_group = root_group

    @property
    def root_group(self):
        return self._root_group

    @root_group.setter
    def root_group(self, value):
        if value is not self._root_group:
            self.clear_widgets()
            self._root_group = value
            self.create_widgets()

    def clear_widgets(self):
        for w in self.widgets.values():
            w.close()
            w.deleteLater()
        while self.root_layout.takeAt(0):
            continue
        self.widgets = {}

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
            if isinstance(value, Controller):
                widget = ControllerWidget(
                    parent=group_widget,
                    name=key,
                    controller=value,
                )
                layout.addWidget(widget)
                self.widgets[key] = widget
            elif isinstance(value, Group):
                subprefix = name + '.'
                groupbox = GroupWidget(
                    parent=group_widget,
                    name=key,
                    group=value,
                )
                layout.addWidget(groupbox)
                self.widgets[key] = groupbox
                self.create_widgets(
                    prefix=subprefix,
                    group=value,
                    group_widget=groupbox,
                    layout=layout,
                )
        if layout is self.root_layout:
            layout.addStretch(1)


class ControllerWidget(QWidget):

    def __init__(self, parent, name, controller):
        super().__init__(parent)
        module = controller.module
        ctl = controller.ctl
        value = controller.value
        t = ctl.value_type
        if isinstance(t, Range):
            widget_class = RangeWidget
        elif isinstance(t, type) and issubclass(t, Enum):
            widget_class = EnumWidget
        else:
            widget_class = None
        if widget_class:
            layout = QVBoxLayout(self)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(5)
            self.setLayout(layout)
            label = QLabel(name.split('.')[-1], self)
            w = widget_class(parent=self, value_type=t, initial_value=value)
            layout.addWidget(label)
            layout.addWidget(w)


class GroupWidget(QGroupBox):

    def __init__(self, parent, name, group):
        super().__init__(parent)
        self.setTitle(name.split('.')[-1])
        self.setLayout(QVBoxLayout(self))
