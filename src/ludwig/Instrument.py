from ludwig.Voice import Voice


class Instrument:
    PROGRAMS = {
        "Acoustic Grand Piano": 0,
        "Cello": 42,
        "Pipe Organ": 19,
        "Viola": 41,
        "Violin": 40,
    }

    def __init__(self, name):
        if name not in self.PROGRAMS:
            raise ValueError(f"Invalid instrument: {name}")
        self.name = name

    @property
    def midi_program(self):
        return self.PROGRAMS[self.name]

    def __getitem__(self, notation):
        voice = Voice(notation)
        voice.instrument = self
        return voice
