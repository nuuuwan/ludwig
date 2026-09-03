class Tempo:
    def __init__(self, beats_per_minute):
        if not isinstance(beats_per_minute, (int, float)):
            raise TypeError("Tempo must be a number")
        if beats_per_minute <= 0:
            raise ValueError("Tempo must be greater than zero")
        self.beats_per_minute = beats_per_minute

    @property
    def microseconds_per_beat(self):
        return round(60_000_000 / self.beats_per_minute)
