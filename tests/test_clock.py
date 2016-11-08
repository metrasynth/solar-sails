from collections import deque

from sails.clock import BasicClock


def test_clock_accuracy():
    c = BasicClock()
    ticks = deque()
    for x in range(10):
        c.advance()
        ticks.append(c.last_tick_frame)
    for x in range(9):
        diff = ticks[x + 1] - ticks[x]
        diff_bpm = round(c.freq * 60 / (diff * 24))
        assert diff_bpm == c.bpm
    c.bpm = 133
    c.advance()
    ticks.append(c.last_tick_frame)
    diff = ticks[-1] - ticks[-2]
    diff_bpm = round(c.freq * 60 / (diff * 24))
    assert diff_bpm == c.bpm
    c.bpm = 150
    c.advance()
    ticks.append(c.last_tick_frame)
    diff = ticks[-1] - ticks[-2]
    diff_bpm = round(c.freq * 60 / (diff * 24))
    assert diff_bpm == c.bpm
