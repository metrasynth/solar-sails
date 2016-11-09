import logging
import os
import threading
from collections import OrderedDict
from tempfile import mkstemp
from time import sleep, time
from uuid import uuid4

import rv.api
import sunvox
from pythonosc import osc_server, udp_client
from pythonosc.osc_message_builder import OscMessageBuilder
from sails.api import c
from sunvosc.dispatcher import PeerDispatcher


class OscPlayback(object):

    def __init__(self, interface='localhost', port=9001,
                 sunvosc_host='localhost', sunvosc_port=9000):
        self.interface = interface
        self.port = port
        self.sunvosc_host = sunvosc_host
        self.sunvosc_port = sunvosc_port
        self.client = udp_client.UDPClient(sunvosc_host, sunvosc_port)
        self.dispatcher = PeerDispatcher()
        server = osc_server.ThreadingOSCUDPServer(
            (interface, port), self.dispatcher)
        logging.info('Peer serving on %s:%s', *server.server_address)
        self.server_thread = threading.Thread(target=server.serve_forever)
        self.server_thread.start()
        self.engine = None
        self.generators = OrderedDict()
        self.default_velocity = 128
        b = OscMessageBuilder('/slot0/inform/start')
        b.add_arg(interface, 's')
        b.add_arg(port, 'i')
        msg = b.build()
        self.client.send(msg)

    def advance_generators(self, session, pos):
        with session[pos]:
            for gen, last_pos in self.generators.items():
                if gen.started and last_pos < pos:
                    with session[pos]:
                        gen.advance(session.cursor())
                    self.generators[gen] = pos
                    yield gen

    def process(self, pos, command):
        if isinstance(command, c.ConnectModules):
            module_numbers = self.dispatcher.module_numbers[0]
            src = command.src
            if hasattr(src, 'index'):
                while src.index is None and src.tag not in module_numbers:
                    sleep(0)
                if src.index is None:
                    src.index = module_numbers[src.tag]
                src = src.index
            dest = command.dest
            if hasattr(dest, 'index'):
                while (
                    dest.index is None
                    and dest.tag not in self.dispatcher.module_numbers[0]
                ):
                    sleep(0)
                if dest.index is None:
                    dest.index = module_numbers[dest.tag]
                dest = dest.index
            b = OscMessageBuilder('/slot0/connect')
            b.add_arg(src, 'i')
            b.add_arg(dest, 'i')
            msg = b.build()
            self.client.send(msg)
        elif isinstance(command, c.Engine):
            if self.engine is not None:
                logging.warning(
                    'Only one engine is supported for OSC playback')
            else:
                self.engine = command
                b = OscMessageBuilder('/slot0/init')
                b.add_arg(1, 'i')
                b.add_arg(128, 'i')
                msg = b.build()
                self.client.send(msg)
        elif isinstance(command, c.Generator):
            self.generators[command] = (-1, 0)
            command.start()
        elif isinstance(command, c.GeneratorStop):
            del self.generators[command.parent]
            command.parent.generator = None
        elif isinstance(command, c.Module):
            data = rv.Synth(command.module).read()
            command.module.tag = uuid4().hex
            b = OscMessageBuilder('/slot0/load_module')
            b.add_arg(command.module.tag, 's')
            fd, name = mkstemp('.sunsynth')
            os.write(fd, data)
            os.close(fd)
            b.add_arg(name, 's')
            # TODO: delete later after we know it's loaded
            msg = b.build()
            self.client.send(msg)
        elif isinstance(command, c.NoteOff):
            beat, tick = pos
            row = beat * 24 + tick
            b = OscMessageBuilder('/slot0/queue')
            b.add_arg(row, 'i')
            b.add_arg(0, 'i')
            b.add_arg(command.track.index, 'i')
            b.add_arg(sunvox.NOTECMD.NOTE_OFF, 'i'),
            b.add_arg(False, 'F')
            b.add_arg(False, 'F')
            b.add_arg(False, 'F')
            b.add_arg(False, 'F')
            b.add_arg(False, 'F')
            msg = b.build()
            self.client.send(msg)
        elif isinstance(command, c.NoteOn):
            beat, tick = pos
            row = beat * 24 + tick
            vel = getattr(command, 'vel', None)
            vel = self.default_velocity if vel is None else vel
            b = OscMessageBuilder('/slot0/queue')
            b.add_arg(row, 'i')
            b.add_arg(0, 'i')
            b.add_arg(command.track.index, 'i')
            b.add_arg(command.note, 'i'),
            b.add_arg(vel, 'i')
            b.add_arg(getattr(command.module, 'index', command.module), 'i')
            b.add_arg(False, 'F')
            b.add_arg(False, 'F')
            b.add_arg(False, 'F')
            msg = b.build()
            self.client.send(msg)
        command.processed = True


def play_sunvosc(session, bpm=125, forever=False, writeahead=12):
    """
    :type session: sails.session.Session
    :type forever: bool
    """
    playback = OscPlayback()
    pos = (-1, 0)
    last_ctl_pos = max(session._ctl_timelines)
    with session[last_ctl_pos]:
        last_cmd_pos = max(session.cmd_timeline)
    start_time = None
    while forever or pos <= last_cmd_pos:
        with session[pos] as cpos:
            processed = 0
            last_played = playback.dispatcher.last_played[0]
            if last_played is not None:
                last_played, frames = last_played
            while cpos.ticks >= (last_played or 0) + writeahead:
                if start_time is None:
                    start_time = time()
                    b = OscMessageBuilder('/slot0/start')
                    msg = b.build()
                    playback.client.send(msg)
                else:
                    sleep(0.1)
                last_played = playback.dispatcher.last_played[0]
                if last_played is not None:
                    last_played, frames = last_played
            keep_processing = True
            while keep_processing:
                cmds = session.cmd_timeline.get(pos, [])
                processed = 0
                for cmd in cmds:
                    if not cmd.processed:
                        print('pos={!r} cmd={!r}'.format(pos, cmd))
                        playback.process(pos, cmd)
                        processed += 1
                advanced = list(playback.advance_generators(session, pos))
                keep_processing = len(advanced) > 0
            cmds = session.cmd_timeline.get(pos, [])
            for cmd in cmds:
                if not cmd.processed:
                    print('pos={!r} cmd={!r}'.format(pos, cmd))
                    playback.process(pos, cmd)
                    processed += 1
            if pos[0] >= 0 and processed == 0:
                print('pos={!r}'.format(pos), end='\r')
            pos = (cpos + 1).pos
