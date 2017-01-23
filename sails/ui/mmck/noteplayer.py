from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtCore import pyqtSignal

from sails import midi


class NotePlayer(QObject):

    noteOn = pyqtSignal(int, int, int)  # track, note, velocity
    noteOff = pyqtSignal(int)  # track

    def __init__(self, parent=None):
        super().__init__(parent)
        self.polyphony = 16
        self.tracks_active = [False] * 16
        midi.listener.message_received.connect(self.on_midi_listener_message_received)

    @property
    def polyphony(self):
        return self._polyphony

    @polyphony.setter
    def polyphony(self, value):
        self._polyphony = value
        self.reset()

    def flush_old_if_full(self):
        if len(self.note_tracks) == self.polyphony:
            _, track = self.note_tracks.pop(0)
            self.tracks_active[track] = False
            self.noteOff.emit(track)

    def reset(self):
        for track in range(16):
            self.noteOff.emit(track)
        self.note_tracks = []  # (note, track)
        self.tracks_active = [False] * 16

    @pyqtSlot(str, 'PyQt_PyObject')
    def on_midi_listener_message_received(self, port_name, message):
        note_on = message.type == 'note_on'
        note_off = message.type == 'note_off'
        if note_on and message.velocity > 0:
            self.flush_old_if_full()
            track = self.tracks_active.index(False)
            self.tracks_active[track] = True
            note = message.note
            velocity = message.velocity
            self.note_tracks.append((note, track))
            self.noteOn.emit(track, note, velocity)
        elif note_off or (note_on and message.velocity == 0):
            for i, (note, track) in enumerate(self.note_tracks):
                if note == message.note:
                    self.tracks_active[track] = False
                    del self.note_tracks[i]
                    self.noteOff.emit(track)
                    break
