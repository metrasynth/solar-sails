from PyQt5.QtCore import QObject, pyqtSlot

from sunvox.api import NOTECMD

from sails import midi


class NotePlayer(QObject):

    def __init__(self, slot, parent=None):
        super().__init__(parent)
        self.slot = slot
        self.active_playback_notes = 0
        midi.listener.message_received.connect(self.on_midi_listener_message_received)

    @pyqtSlot(str, 'PyQt_PyObject')
    def on_midi_listener_message_received(self, port_name, message):
        note_on = message.type == 'note_on'
        note_off = message.type == 'note_off'
        if note_on and message.velocity > 0:
            note = message.note + 1
            self.slot.send_event(0, note, message.velocity, 2, 0, 0)
            self.active_playback_notes += 1
        elif note_off or (note_on and message.velocity == 0):
            self.active_playback_notes -= 1
            self.active_playback_notes = max(self.active_playback_notes, 0)
            if self.active_playback_notes == 0:
                self.slot.send_event(0, NOTECMD.NOTE_OFF, 0, 0, 0, 0)
