import os
import time
from collections import OrderedDict
from tempfile import mkstemp

import rv.api
import sunvox.api
from sails.api import c
from sails.clock import BasicClock


class BasicPlayback(object):

    def __init__(self):
        self.engine_processes = {}
        self.engine_slots = {}
        self.generators = OrderedDict()
        self.default_velocity = 128

    def advance_generators(self, session, pos):
        with session[pos]:
            for gen, last_pos in self.generators.items():
                if gen.started and last_pos < pos:
                    with session[pos]:
                        gen.advance(session.cursor())
                    self.generators[gen] = pos
                    yield gen

    def process(self, command):
        if isinstance(command, c.ConnectModules):
            slot = self.engine_slots[command.engine]
            src = command.src
            src = src if isinstance(src, int) else src.index
            dest = command.dest
            dest = dest if isinstance(dest, int) else dest.index
            slot.connect_module(src, dest)
        elif isinstance(command, c.Engine):
            process = sunvox
            process.init(None, 44100, 2, 0)
            self.engine_processes[command] = process
            self.engine_slots[command] = sunvox.api.Slot(process=process)
        elif isinstance(command, c.Generator):
            self.generators[command] = (-1, 0)
            command.start()
        elif isinstance(command, c.GeneratorStop):
            del self.generators[command.parent]
            command.parent.generator = None
        elif isinstance(command, c.Module):
            fd, name = mkstemp('.sunsynth')
            os.write(fd, rv.api.Synth(command.module).read())
            os.close(fd)
            slot = self.engine_slots[command.engine]
            index = slot.load_module(name.encode('utf8'), x=0, y=0, z=0)
            os.unlink(name)
            command.module.index = index
        elif isinstance(command, c.NoteOff):
            slot = self.engine_slots[command.engine]
            slot.send_event(
                track_num=command.track.index,
                note=sunvox.api.NOTECMD.NOTE_OFF,
                vel=0,
                module=0,
                ctl=0,
                ctl_val=0,
            )
        elif isinstance(command, c.NoteOn):
            slot = self.engine_slots[command.engine]
            vel = getattr(command, 'vel', None)
            vel = self.default_velocity if vel is None else vel
            slot.send_event(
                track_num=command.track.index,
                note=command.note,
                vel=vel,
                module=command.module,
                ctl=0,
                ctl_val=0,
            )
        command.processed = True


def play(session, bpm=125, shuffle=0.0, forever=False):
    """
    :type session: sails.session.Session
    :type forever: bool
    """
    playback = BasicPlayback()
    clock = BasicClock(bpm=bpm, shuffle=shuffle)
    pos = (-1, 0)
    last_ctl_pos = max(session._ctl_timelines)
    with session[last_ctl_pos]:
        last_cmd_pos = max(session.cmd_timeline)
    start_time = None
    while forever or pos <= last_cmd_pos:
        with session[pos] as cpos:
            if pos == (0, 0):
                start_time = time.time()
            if pos >= (0, 0):
                clock.advance()
                wait_until = start_time + clock.last_tick_frame / clock.freq
                first_wait = max(0, (wait_until - time.time()) * 0.75)
                time.sleep(first_wait)
                while time.time() < wait_until:
                    time.sleep(0)
            keep_processing = True
            while keep_processing:
                cmds = session.cmd_timeline.get(pos, [])
                processed = 0
                for cmd in cmds:
                    if not cmd.processed:
                        print('pos={!r} cmd={!r}'.format(pos, cmd))
                        playback.process(cmd)
                        processed += 1
                advanced = list(playback.advance_generators(session, pos))
                keep_processing = len(advanced) > 0
            cmds = session.cmd_timeline.get(pos, [])
            for cmd in cmds:
                if not cmd.processed:
                    print('pos={!r} cmd={!r}'.format(pos, cmd))
                    playback.process(cmd)
                    processed += 1
            if pos[0] >= 0 and processed == 0:
                print('pos={!r}'.format(pos), end='\r')
            pos = (cpos + 1).pos
    clock.stop()
