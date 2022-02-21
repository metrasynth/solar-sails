from enum import Enum

from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtCore import pyqtSignal

from rv.controller import DependentRange, Range
from sails import midi
from sails.midi.ccmappings import cc_mappings


class CCMapper(QObject):

    controlValueChanged = pyqtSignal(str, int, bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        midi.listener.message_received.connect(self.on_midi_listener_message_received)

    @pyqtSlot(str, "PyQt_PyObject")
    def on_midi_listener_message_received(self, port_name, message):
        cc = message.type == "control_change"
        if not cc:
            return
        cc_key = (message.channel, message.control)
        for alias, options in cc_mappings.cc_aliases[cc_key]:
            for name in self.parent().alias_controllers[alias]:
                # map message.value to controller range
                c = self.parent().controllers_manager.root_group
                if not c or name not in c:
                    continue
                controller = c[name]
                ctl = controller.ctl
                value_type = ctl.value_type
                if isinstance(value_type, DependentRange):
                    value_type = value_type.parent(controller.module)
                if isinstance(value_type, Range):
                    min_value, max_value = value_type.min, value_type.max
                elif isinstance(value_type, type) and issubclass(value_type, Enum):
                    min_value, max_value = 0, len(value_type)
                elif value_type is bool:
                    min_value, max_value = 0, 1
                else:
                    print("Unknown value_type {}".format(value_type))
                    continue
                range = max_value - min_value
                factor = range / 127.0
                is_relative = "relative" in options
                if is_relative:
                    value = int(message.value) - 0x40
                else:
                    value = int(message.value * factor)
                    value += min_value
                self.controlValueChanged.emit(name, value, is_relative)
