from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QLabel


PARAMETER_WIDGETS = {
    # param_type: widget_class,
}


def widget_class_for(param_type):
    def wrapper(cls):
        PARAMETER_WIDGETS[param_type] = cls
        return cls
    return wrapper


class ParametersManager(QObject):

    _parameters = None

    valuesChanged = pyqtSignal()

    def __init__(self, parent, layout, parameters, values):
        super().__init__(parent)
        self.layout = layout
        self.parameter_widgets = {}
        self.parameters = parameters
        self.values = values

    @property
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self, value):
        if value is not self._parameters:
            self.clear_widgets()
            self._parameters = value
            self.create_widgets()

    def clear_widgets(self):
        for w in self.parameter_widgets.values():
            w.close()
            w.deleteLater()
        self.parameter_widgets = {}
        while self.layout.takeAt(0):
            continue

    def create_widgets(self):
        for name, parameter in self.parameters.items():
            if name in self.values:
                value = self.values[name]
            else:
                value = parameter.default
            widget_class = PARAMETER_WIDGETS[type(parameter)]
            widget = widget_class(self.parent(), name, parameter, value)
            widget.valueChanged.connect(self.on_parameter_widget_valueChanged)
            self.layout.addWidget(widget)
            self.parameter_widgets[name] = widget
        self.layout.addStretch(1)

    @pyqtSlot('PyQt_PyObject', str)
    def on_parameter_widget_valueChanged(self, value, name):
        self.values[name] = value
        self.valuesChanged.emit()
