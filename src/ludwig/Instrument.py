class Instrument:
    PROGRAMS = {
        "Acoustic Grand Piano": 0,
        "Pipe Organ": 19,
        "Violin": 40,
    }

    def __init__(self, name):
        if name not in self.PROGRAMS:
            raise ValueError(f"Invalid instrument: {name}")
        self.name = name

    @property
    def midi_program(self):
        return self.PROGRAMS[self.name]
