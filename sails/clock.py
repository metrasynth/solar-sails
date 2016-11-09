class BasicClock(object):

    def __init__(self, bpm=125, shuffle=0.0, shuffle_range=50, freq=44100):
        self.bpm = bpm
        self.shuffle = shuffle
        self.shuffle_range = shuffle_range
        self.tick = -1
        self.last_tick_frame = None
        self.freq = freq

    def advance(self):
        if self.last_tick_frame is None:
            self.last_tick_frame = 0
        else:
            self.last_tick_frame += self.predicted_next_tick()
        self.tick += 1

    def predicted_next_tick(self):
        return self.freq * 60. // self.tick_bpm(self.tick) // 24

    def tick_bpm(self, tick):
        sixteenth = tick // 6
        shuffle_amount = round(self.shuffle * self.shuffle_range)
        if sixteenth % 2 == 0:
            shuffle_amount = -shuffle_amount
        return self.bpm + shuffle_amount

    def stop(self):
        pass
