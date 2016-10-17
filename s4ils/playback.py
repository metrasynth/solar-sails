import os
import time
from tempfile import mkstemp

import rv
import sunvox

from s4ils import c


class BasicPlayback(object):

    def __init__(self):
        self.engine_processes = {}
        self.engine_slots = {}
        self.default_velocity = 128

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
            self.engine_slots[command] = sunvox.Slot(process=process)
        elif isinstance(command, c.Module):
            fd, name = mkstemp('.sunsynth')
            os.write(fd, rv.Synth(command.module).read())
            os.close(fd)
            slot = self.engine_slots[command.engine]
            index = slot.load_module(name.encode('utf8'), x=0, y=0, z=0)
            os.unlink(name)
            command.module.index = index
        elif isinstance(command, c.NoteOff):
            slot = self.engine_slots[command.engine]
            slot.send_event(
                track_num=command.track.index,
                note=sunvox.NOTECMD.NOTE_OFF,
                vel=0,
                module=command.module,
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


def play(session):
    """
    :type session: s4ils.session.Session
    """
    playback = BasicPlayback()
    pos = (-1, 0)
    last_ctl_pos = max(session._ctl_timelines)
    with session[last_ctl_pos]:
        last_cmd_pos = max(session.cmd_timeline)
    while pos <= last_cmd_pos:
        with session[pos] as cpos:
            cmds = session.cmd_timeline.get(pos, [])
            for cmd in cmds:
                print('pos={!r} cmd={!r}'.format(pos, cmd))
                playback.process(cmd)
            else:
                if pos[0] >= 0:
                    print('pos={!r}'.format(pos), end='\r')
            pos = (cpos + 1).pos
            if pos[0] >= 0:
                time.sleep(60. / 120. / 24.)
