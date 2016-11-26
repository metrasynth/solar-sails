from threading import Thread

from sails.lib import mido

from .listener import midi_listener as listener


def load():
    mido.backend.get_input_names()


__all__ = [
    'listener',
    'load',
]
