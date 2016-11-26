from PyQt5.QtCore import QObject, pyqtSignal
from sails.lib import mido
from sails.ui import App
import sip


class MidiListener(QObject):
    """Listens for ``mido`` messages in a thread, routes to Qt signals"""

    message_received = pyqtSignal(str, 'PyQt_PyObject')

    def __init__(self, parent):
        super().__init__(parent)
        self.port_listeners = {
            # port_name: (port, listener),
        }

    def start_port_listener(self, port_name):
        available = mido.backend.get_input_names()
        if port_name not in self.port_listeners and port_name in available:
            def listener(message):
                self.message_received.emit(port_name, message)
            port = mido.backend.open_input(port_name, callback=listener)
            self.port_listeners[port_name] = (port, listener)

    def stop(self):
        for port_name, (port, _) in list(self.port_listeners.items()):
            port.close()
            del self.port_listeners[port_name]

    def update_ports(self):
        App.settings.beginGroup('midi')
        try:
            port_names = App.settings.value('in_devices') or []
        finally:
            App.settings.endGroup()
        for port_name, (port, _) in list(self.port_listeners.items()):
            if port_name not in port_names:
                port.close()
                del self.port_listeners[port_name]
        for port_name in port_names:
            if port_name not in self.port_listeners:
                self.start_port_listener(port_name)


midi_listener = MidiListener(None)
