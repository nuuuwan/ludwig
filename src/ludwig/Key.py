class Key:
    OFFSETS = {
        "Cb": -7,
        "Gb": -6,
        "Db": -5,
        "Ab": -4,
        "Eb": -3,
        "Bb": -2,
        "F": -1,
        "C": 0,
        "G": 1,
        "D": 2,
        "A": 3,
        "E": 4,
        "B": 5,
        "F#": 6,
        "C#": 7,
    }

    def __init__(self, name):
        if name not in self.OFFSETS:
            raise ValueError(f"Invalid major key: {name}")
        self.name = name

    @property
    def midi_offset(self):
        return self.OFFSETS[self.name]
