import rv.api


class Command(object):
    args = ()

    processed = False

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


class ConnectModules(Command):
    args = 'engine', 'src', 'dest'


class Engine(Command):

    class Track(object):

        def __init__(self, engine, index):
            self.engine = engine
            self.index = index

        def __repr__(self):
            return '<Track {}>'.format(self.index)

        def __ror__(self, other):
            if isinstance(other, NoteOn):
                note = other.copy(engine=self.engine, track=self)
                return note

        def off(self):
            return NoteOff(self.engine, self)

    class Output(object):

        index = 0

        def __init__(self, engine):
            self.engine = engine

        def __repr__(self):
            return '<Output>'

        def __lshift__(self, other):
            return ConnectModules(self.engine, other.module, self)

        def __rshift__(self, other):
            return ConnectModules(self.engine, self, other.module)

    def __init__(self, *args, **kw):
        super(Engine, self).__init__(*args, **kw)
        self.output = self.Output(self)

    def new_module(self, obj, *args, **kw):
        if isinstance(obj, type) and issubclass(obj, rv.m.Module):
            obj = obj(*args, **kw)
        if isinstance(obj, rv.m.Module):
            return Module(self, obj)
        else:
            raise ValueError()

    def track(self, index):
        return self.Track(self, index)


class Generator(Command):
    args = 'fn', 'fn_args', 'fn_kw'

    generator = None

    def advance(self, cursor):
        if self.generator is not None:
            try:
                self.generator.send(cursor)
            except StopIteration:
                self.stop() | cursor

    @property
    def started(self):
        return self.generator is not None

    def start(self):
        if not self.started:
            self.generator = self.fn(*self.fn_args, **self.fn_kw)
            self.generator.send(None)

    def stop(self):
        return GeneratorStop(self)

    @classmethod
    def factory(cls, fn):
        def factory_fn(*args, **kw):
            return cls(fn, args, kw)
        return factory_fn


class GeneratorStop(Command):
    args = 'parent',


class Module(Command):
    args = 'engine', 'module'

    def __lshift__(self, other):
        return ConnectModules(self, other.module, self.module)

    def __rshift__(self, other):
        return ConnectModules(self, self.module, other.module)

    def on(self, note, vel=None):
        return NoteOn(note, vel, self.engine, self.module)


class NoteOff(Command):
    args = 'engine', 'track'


class NoteOn(Command):
    args = 'note', 'vel', 'engine', 'module', 'track'

    def off(self):
        return NoteOff(self.engine, self.track)
