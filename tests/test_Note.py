import unittest

from ludwig import Note


class TestNote(unittest.TestCase):
    def test_converts_midi_number_to_notation(self):
        self.assertEqual(
            [str(Note(number)) for number in (0, 1, 60, 127)],
            ["C-1", "C#-1", "C4", "G9"],
        )

    def test_rejects_invalid_number(self):
        with self.assertRaises(TypeError):
            Note(1.5)
        with self.assertRaises(ValueError):
            Note(128)
