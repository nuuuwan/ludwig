import unittest

from ludwig import Chord


class TestChord(unittest.TestCase):
    @staticmethod
    def _numbers(chord):
        return [note.number for note in chord.notes]

    def test_builds_from_compact_notation(self):
        self.assertEqual(self._numbers(Chord("CEGB")), [60, 64, 67, 71])
        self.assertEqual(self._numbers(Chord("DFG#BE")), [62, 65, 68, 71, 76])
        with self.assertRaisesRegex(ValueError, "Invalid chord notation"):
            Chord("C?G")

    def test_builds_extended_qualities(self):
        self.assertEqual(
            self._numbers(Chord.named(48, "dominant thirteenth")),
            [48, 52, 58, 62, 69],
        )
        self.assertEqual(len(Chord.named(60, "dominant seventh").notes), 4)
        self.assertEqual(len(Chord.named(60, "major ninth").notes), 5)
        self.assertEqual(len(Chord.named(60, "diminished seventh").notes), 4)
        self.assertEqual(len(Chord.named(60, "augmented").notes), 3)
        with self.assertRaisesRegex(ValueError, "Invalid chord quality"):
            Chord.named(60, "mysterious")
