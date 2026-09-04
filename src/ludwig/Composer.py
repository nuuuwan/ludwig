import random

from ludwig.Chord import Chord
from ludwig.Instrument import Instrument
from ludwig.Piece import Piece
from ludwig.Rhythm import Rhythm
from ludwig.Tempo import Tempo
from ludwig.VoiceLeading import VoiceLeading


class Composer:
    def __init__(self, chords, seed=None):
        self.chords = tuple(chords)
        self._validate_chords(self.chords)
        self.transitions = self._infer_transitions(self.chords)
        self.random = random.Random(seed)

    @staticmethod
    def _validate_chords(chords):
        if not chords or not all(
            isinstance(chord, Chord) for chord in chords
        ):
            raise ValueError("Composer requires Chords")
        if len(set(chords)) != len(chords):
            raise ValueError("Composer requires distinct Chords")

    @staticmethod
    def _infer_transitions(chords):
        if len(chords) == 1:
            return {chords[0]: {chords[0]: 1.0}}
        transitions = {}
        for chord in chords:
            destinations = tuple(other for other in chords if other != chord)
            weights = tuple(
                1 / (1 + chord.edit_distance(other)) for other in destinations
            )
            total = sum(weights)
            transitions[chord] = {
                other: weight / total
                for other, weight in zip(destinations, weights)
            }
        return transitions

    def _chords(self, count):
        chord = next(iter(self.transitions))
        chords = []
        for _ in range(count):
            chords.append(chord)
            destinations = self.transitions[chord]
            chord = self.random.choices(
                tuple(destinations),
                weights=tuple(destinations.values()),
            )[0]
        return chords

    def compose(self, duration, voices, tempo=Tempo(60)):
        if not isinstance(duration, (int, float)) or duration <= 0:
            raise ValueError("Duration must be greater than zero")
        if not voices or not all(
            isinstance(voice, Instrument) for voice in voices
        ):
            raise TypeError("Voices must be Instruments")
        if max(map(len, (chord.notes for chord in self.chords))) > len(
            voices
        ):
            raise ValueError("Every chord requires an instrument voice")
        tokens = duration * tempo.beats_per_minute / 30
        if not tokens.is_integer():
            raise ValueError("Duration must align with an eighth note")
        spans = Rhythm.spans(int(tokens))
        chords = self._chords(len(spans))
        arrangements = VoiceLeading.arrange(chords, len(voices))
        rendered = (
            voice[Rhythm.notation(arrangements, index, spans)]
            for index, voice in enumerate(voices)
        )
        return Piece(tempo, *rendered)
