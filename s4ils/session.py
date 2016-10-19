from pyrsistent import pmap, pvector

from s4ils.commands import Command

TICKS_PER_BEAT = 24


def advanced_to(timeline, pos, default, inherit):
    if pos in timeline:
        return timeline
    if len(timeline) == 0 or not inherit:
        return timeline.set(pos, default())
    else:
        first = min(timeline)
        last = max(timeline)
        if pos < first:
            return timeline.set(pos, default())
        elif pos > last:
            return timeline.set(pos, timeline[last])
        else:
            prevpos = pos
            while prevpos not in timeline:
                cpos = ControlPosition(None, prevpos)
                prevpos = (cpos - 1).pos
            return timeline.set(pos, timeline[prevpos])


class Session(object):
    """Provides time travel through a session's timelines."""

    def __init__(self):
        self._with_position = None
        self._ctl_timelines = pmap()
        self._namespaces = pmap()

    def __getattr__(self, item):
        if item.startswith('_'):
            return super(Session, self).__getattr__(item)
        else:
            cpos = self._with_position
            if cpos:
                pos = cpos.pos
                timeline = advanced_to(self._namespaces, pos, pmap, True)
                return timeline[pos][item]
            else:
                raise RuntimeError('Must be within a "with" block')

    def __setattr__(self, key, value):
        if key.startswith('_'):
            return super(Session, self).__setattr__(key, value)
        else:
            cpos = self._with_position
            if cpos:
                pos = cpos.pos
                timeline = advanced_to(self._namespaces, pos, pmap, True)
                ns = timeline[pos].set(key, value)
                timeline = timeline.set(pos, ns)
                # Ensure that values are rolled forward through timeline.
                last = max(timeline)
                while pos < last:
                    cpos = ControlPosition(None, pos)
                    pos = (cpos + 1).pos
                    timeline = advanced_to(timeline, pos, pmap, True)
                    ns = timeline[pos]
                    if key not in ns:
                        ns = ns.set(key, value)
                        timeline = timeline.set(pos, ns)
                    else:
                        break
                self._namespaces = timeline
            else:
                raise RuntimeError('Must be within a "with" block')

    def __getitem__(self, pos):
        return ControlPosition(self, *pos)

    def __add__(self, other):
        return CommandCursor(self, 0, 0) + other

    def __sub__(self, other):
        return CommandCursor(self, 0, 0) - other

    def __ror__(self, other):
        return other | CommandCursor(self, 0, 0)

    @property
    def cmd_timeline(self):
        cpos = self._with_position
        if cpos:
            pos = cpos.pos
            timeline = self.ctl_timeline_advanced_to(pos)
            return timeline[pos]
        else:
            raise RuntimeError('Must be within a "with" block')

    @property
    def beat(self):
        cpos = self._with_position
        if cpos:
            return cpos.beat
        else:
            raise RuntimeError('Must be within a "with" block')

    @property
    def tick(self):
        cpos = self._with_position
        if cpos:
            return cpos.tick
        else:
            raise RuntimeError('Must be within a "with" block')

    @property
    def ticks(self):
        return self.beat * 24 + self.tick

    def ctl_timeline_advanced_to(self, position):
        return advanced_to(self._ctl_timelines, position, pmap, True)

    def cmd_timeline_append(self, position, command):
        timeline = self.ctl_timeline_advanced_to(self._with_position.pos)
        ctl_timeline = timeline[self._with_position.pos]
        ctl_timeline = advanced_to(ctl_timeline, position, pvector, False)
        commands = ctl_timeline[position].append(command)
        ctl_timeline = ctl_timeline.set(position, commands)
        timeline = timeline.set(self._with_position.pos, ctl_timeline)
        self._ctl_timelines = timeline


class CommandCursor(object):

    def __init__(self, session, beat, tick=None):
        self.s = session
        if tick is not None:
            self.beat = beat
            self.tick = tick
        elif isinstance(beat, tuple):
            self.beat, self.tick = beat
        else:
            self.beat = beat // TICKS_PER_BEAT
            self.tick = beat % TICKS_PER_BEAT

    def __add__(self, other):
        if isinstance(other, int):
            other = (0, other)
        if isinstance(other, tuple) and len(other) == 2:
            beats, ticks = other
            ticks += beats * TICKS_PER_BEAT
            return self.__class__(self.s, self.ticks + ticks)

    def __sub__(self, other):
        if isinstance(other, int):
            return self + -other
        elif isinstance(other, tuple) and len(other) == 2:
            beats, ticks = other
            ticks += beats * TICKS_PER_BEAT
            return self + -ticks

    def __ror__(self, other):
        cpos = self.s._with_position
        if cpos and isinstance(other, Command):
            cpos += (self.beat, self.tick)
            self.s.cmd_timeline_append(cpos.pos, other)
            return other
        else:
            raise ValueError()

    def __repr__(self):
        return '<CommandCursor ({},{})>'.format(self.beat, self.tick)

    @property
    def ticks(self):
        return self.tick + self.beat * TICKS_PER_BEAT


class ControlPosition(object):

    def __init__(self, session, beat, tick=None):
        self.session = session
        if tick is not None:
            self.beat = beat
            self.tick = tick
        elif isinstance(beat, tuple):
            self.beat, self.tick = beat
        else:
            self.beat = beat // TICKS_PER_BEAT
            self.tick = beat % TICKS_PER_BEAT

    def __add__(self, other):
        if isinstance(other, int):
            other = (0, other)
        if isinstance(other, tuple) and len(other) == 2:
            beats, ticks = other
            ticks += beats * TICKS_PER_BEAT
            return self.__class__(self.session, self.ticks + ticks)

    def __sub__(self, other):
        if isinstance(other, int):
            return self + -other
        elif isinstance(other, tuple) and len(other) == 2:
            beats, ticks = other
            ticks += beats * TICKS_PER_BEAT
            return self + -ticks

    def __enter__(self):
        self._old_with_position = self.session._with_position
        self.session._with_position = self
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session._with_position = self._old_with_position

    @property
    def commands(self):
        timeline = self.session.ctl_timeline_advanced_to(self.pos)
        return timeline[self.pos]

    @property
    def pos(self):
        return self.beat, self.tick

    @property
    def ticks(self):
        return self.tick + self.beat * TICKS_PER_BEAT
