from s4ils.clock import Clock


def test_clock_accuracy():
    c = Clock()
    for x in range(10):
        c.advance()
    ticks = c.tick_frames
    for x in range(9):
        diff = ticks[x + 1] - ticks[x]
        diff_bpm = round(c.freq * 60 / (diff * 24))
        assert diff_bpm == c.bpm
    c.bpm = 133
    c.advance()
    diff = ticks[-1] - ticks[-2]
    diff_bpm = round(c.freq * 60 / (diff * 24))
    assert diff_bpm == c.bpm
    c.bpm = 150
    c.advance()
    diff = ticks[-1] - ticks[-2]
    diff_bpm = round(c.freq * 60 / (diff * 24))
    assert diff_bpm == c.bpm
