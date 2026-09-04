import math
import unittest

from ludwig import Chord, Composer, Instrument, Tempo


class TestComposer(unittest.TestCase):
    @staticmethod
    def _continuous(voice):
        events = voice.events()
        adjacent = zip(events, events[1:])
        return (
            events[0][0] == 0
            and events[-1][0] + events[-1][1] == len(voice)
            and all(left[0] + left[1] == right[0] for left, right in adjacent)
        )

    def test_composes_seeded_piece_of_exact_duration(self):
        tonic = Chord(48, 52, 55)
        dominant = Chord(55, 59, 62)
        composer = Composer((tonic, dominant), seed=7)
        piece = composer.compose(
            120,
            [Instrument("Cello"), Instrument("Viola"), Instrument("Flute")],
            Tempo(60),
        )
        self.assertEqual([len(voice) for voice in piece.voices], [240] * 3)
        self.assertTrue(all(map(self._continuous, piece.voices)))
        self.assertTrue(
            all(
                start % 2 == duration % 2 == 0
                for voice in piece.voices
                for start, duration, _ in voice.events()
            )
        )
        held = Composer((Chord(60),)).compose(
            2, [Instrument("Cello")], Tempo(60)
        )
        self.assertEqual(held.voices[0].events(), [(0, 4, 60)])
        self.assertEqual(piece.voices[0].events()[0][2], 48)
        pitches = tuple(
            tuple(event[2] for event in voice.events())
            for voice in piece.voices
        )
        self.assertTrue(
            all(
                abs(pitch - voice[0]) <= 12
                for voice in pitches
                for pitch in voice
            )
        )
        self.assertLessEqual(
            max(
                abs(right - left)
                for voice in pitches
                for left, right in zip(voice, voice[1:])
            ),
            4,
        )

    def test_infers_transitions_from_chord_distance(self):
        tonic = Chord("CEG")
        near = Chord("CEGB")
        far = Chord("DFA#")
        composer = Composer((tonic, near, far))
        self.assertGreater(
            composer.transitions[tonic][near],
            composer.transitions[tonic][far],
        )
        self.assertTrue(
            math.isclose(sum(composer.transitions[tonic].values()), 1)
        )

    def test_rejects_invalid_chords(self):
        chord = Chord(60)
        with self.assertRaisesRegex(ValueError, "requires Chords"):
            Composer(())
        with self.assertRaisesRegex(ValueError, "distinct Chords"):
            Composer((chord, chord))
        with self.assertRaisesRegex(ValueError, "instrument voice"):
            Composer((Chord(60, 64),)).compose(1, [Instrument("Cello")])
