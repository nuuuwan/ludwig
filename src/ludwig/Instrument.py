from ludwig.MidiPrograms import MidiPrograms
from ludwig.Voice import Voice


class Instrument:
    PROGRAMS = MidiPrograms.PROGRAMS

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
