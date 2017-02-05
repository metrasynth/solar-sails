try:
    import mido
except ImportError:
    backend = None
else:
    backend = mido.Backend('mido.backends.rtmidi')
