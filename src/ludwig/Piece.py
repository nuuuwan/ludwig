from pathlib import Path

from ludwig.Instrument import Instrument
from ludwig.Key import Key
from ludwig.MidiEncoder import MidiEncoder
from ludwig.Tempo import Tempo
from ludwig.Time import Time
from ludwig.Voice import Voice


class Piece:
    def __init__(self, *parameters):
        self._validate_parameters(parameters)
        self.voices = tuple(
            parameter
            for parameter in parameters
            if isinstance(parameter, Voice)
        )
        self.instrument = self._resolve(
            parameters,
            Instrument,
            Instrument("Acoustic Grand Piano"),
        )
        self.key = self._resolve(parameters, Key, Key("C"))
        self.time = self._resolve(parameters, Time, Time("4/4"))
        self.tempo = self._resolve(parameters, Tempo, Tempo(120))
        self._validate_voices(self.voices)
        self._validate_voice_lengths(self.voices)
        self.instruments = tuple(
            voice.instrument or self.instrument for voice in self.voices
        )

    @staticmethod
    def _validate_parameters(parameters):
        supported = (Instrument, Key, Time, Tempo, Voice)
        if not all(
            isinstance(parameter, supported) for parameter in parameters
        ):
            raise TypeError("Unsupported Piece parameter")

    @staticmethod
    def _resolve(parameters, parameter_type, default):
        matches = tuple(
            parameter
            for parameter in parameters
            if isinstance(parameter, parameter_type)
        )
        if len(matches) > 1:
            raise TypeError(f"Piece accepts one {parameter_type.__name__}")
        return matches[0] if matches else default

    @staticmethod
    def _validate_voices(voices):
        if not voices:
            raise TypeError("Piece requires one or more voices")
        if not all(isinstance(voice, Voice) for voice in voices):
            raise TypeError("Piece requires one or more voices")

    @staticmethod
    def _validate_voice_lengths(voices):
        lengths = {len(voice) for voice in voices}
        if len(lengths) != 1:
            raise ValueError("All voices must have the same length")

    def to_midi(self, path):
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(
            MidiEncoder.encode(
                self.instruments,
                self.key,
                self.time,
                self.tempo,
                self.voices,
            )
        )
        return output_path

    def transpose(self, semitones):
        voices = tuple(voice.transpose(semitones) for voice in self.voices)
        return Piece(
            self.instrument,
            self.key,
            self.time,
            self.tempo,
            *voices,
        )
