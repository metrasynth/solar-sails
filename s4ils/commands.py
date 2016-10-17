class Command(object):
    args = ()

    def __init__(self, *args, **kw):
        self._apply_args(*args, **kw)

    def __repr__(self):
        attrs = ' '.join(
            '{}={!r}'.format(
                arg,
                getattr(self, arg),
            )
            for arg in self.args
            if hasattr(self, arg)
        )

        return '<{}{}>'.format(
            self.__class__.__name__,
            ' ' + attrs if attrs else '',
        )

    def _apply_args(self, *args, **kw):
        for key, value in zip(self.args, args):
            setattr(self, key, value)
        for key, value in kw.items():
            if key in self.args:
                setattr(self, key, value)

    def copy(self, *args, **kw):
        c2 = self.__class__()
        for key in self.args:
            try:
                value = getattr(self, key)
            except AttributeError:
                pass
            else:
                setattr(c2, key, value)
        c2._apply_args(*args, **kw)
        return c2


class Engine(Command):

    class Track(object):

        def __init__(self, engine, index):
            self.engine = engine
            self.index = index

        def __ror__(self, other):
            if isinstance(other, NoteOn):
                note = other.copy(engine=self.engine, track=self)
                return note

    def track(self, index):
        return self.Track(self, index)


class NoteOn(Command):
    args = 'note', 'vel', 'engine', 'track'

    def off(self):
        return NoteOff(self.engine, self.track)


class NoteOff(Command):
    args = 'engine', 'track'
