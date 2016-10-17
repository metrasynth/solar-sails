from collections import deque

import rv

import sunvox.buffered


class Clock(object):
    """
    High-resolution tick clock.
    """

    def __init__(self, bpm=125, shuffle=0.0, shuffle_range=24,
                 freq=44100, size=128):
        self.bpm = bpm
        self.shuffle = shuffle
        self.shuffle_range = shuffle_range
        self.tick = 0
        self.tick_frames = deque()
        self.last_tick_frame = -size
        self.frame = 0
        self.freq = freq
        self.size = size
        project = rv.Project()
        project.initial_bpm = self.bpm
        project.initial_tpl = 1
        self.module = project.new_module(
            rv.m.Generator,
            volume=128,
            waveform='square',
            attack=0,
            release=1,
            polyphony_ch=1,
            sustain=False,
        )
        project.output << self.module
        tick_pattern = rv.Pattern(tracks=1, lines=6)
        for line in range(6):
            cmd = tick_pattern.data[line][0]
            cmd.note = rv.NOTE.C5
            cmd.module = self.module.index + 1
        project.attach_pattern(tick_pattern)
        self.process = sunvox.buffered.BufferedProcess(
            freq=freq, channels=1, size=size)
        self.slot = sunvox.Slot(project, process=self.process)
        self.started = False

    def advance(self):
        self.set_tempo()
        if not self.started:
            self.slot.play_from_beginning()
            self.started = True
        next_tick_frame = int((self.last_tick_frame or 0) + self.predicted_tick_frames())
        blocks_to_advance = (next_tick_frame // self.size) - (self.frame // self.size) + 1
        for x in range(blocks_to_advance):
            buf = self.read_block()
            relative_pos = self.tick_pos_in_buffer(buf)
            if relative_pos is not None:
                pos = self.frame + relative_pos
                if self.last_tick_frame is None or pos > self.last_tick_frame + 1:
                    self.last_tick_frame = pos
                    self.tick_frames.append(pos)
            self.frame += self.size

    def read_block(self):
        buf = self.process.fill_buffer()
        return buf

    def set_tempo(self):
        self.slot.send_event(0, sunvox.NOTECMD.EMPTY, 0, 0, 0x001f,
                             self.tick_bpm(self.tick))

    def tick_bpm(self, tick):
        sixteenth = tick // 6
        shuffle_amount = round(self.shuffle * self.shuffle_range)
        if sixteenth % 2 == 0:
            shuffle_amount = -shuffle_amount
        return self.bpm + shuffle_amount

    def tick_pos_in_buffer(self, buf):
        ticks, = (buf.transpose()[0] < 0).nonzero()
        if ticks.any():
            return ticks[0]

    def predicted_tick_frames(self):
        return self.freq * 60. // self.bpm // 24

    def stop(self):
        self.process.kill()
