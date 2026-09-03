import unittest
from pathlib import Path

from ludwig import Instrument, Key, Piece, Tempo, Time, Voice


class TestLudwig(unittest.TestCase):
    def test_voice_converts_timeline_to_events(self):
        voice = Voice("C-D---.E-")

        self.assertEqual(
            voice.events(),
            [(0, 2, 60), (2, 4, 62), (7, 2, 64)],
        )

    def test_voices_add_sequentially(self):
        first = Voice("C-")
        second = Voice("D---")

        combined = first + second

        self.assertEqual(combined.notation, "C-D---")
        self.assertEqual(len(combined), 6)
        self.assertEqual(combined.events(), [(0, 2, 60), (2, 4, 62)])
        self.assertEqual(first.notation, "C-")
        self.assertEqual(second.notation, "D---")

    def test_voice_rejects_adding_other_types(self):
        with self.assertRaises(TypeError):
            Voice("C-") + "D-"

    def test_piece_writes_midi(self):
        path = Path(__file__).parent.parent / "midi" / "twinkle_twinkle.mid"
        result = Piece(
            Instrument("Violin"),
            Voice("C-C-G-G-A-A-G---F-F-E-E-D-D-C---"),
            Voice("C-G-E-C-F-C-E-C-D-B-D-A-F-G-C---"),
        ).to_midi(path)
        data = path.read_bytes()

        self.assertEqual(result, path)
        self.assertEqual(data[:4], b"MThd")
        self.assertEqual(int.from_bytes(data[10:12], "big"), 3)
        self.assertEqual(data.count(b"MTrk"), 3)
        self.assertIn(b"\x00\xff\x51\x03\x07\xa1\x20", data)
        self.assertEqual(data.count(b"\x00\xc0\x28"), 1)
        self.assertEqual(data.count(b"\x00\xc1\x28"), 1)

    def test_piece_infers_parameters_in_any_order(self):
        piece = Piece(
            Voice("C-"),
            Tempo(90),
            Key("G"),
            Time("3/4"),
        )

        self.assertEqual(piece.key.name, "G")
        self.assertEqual(piece.time.numerator, 3)
        self.assertEqual(piece.time.denominator, 4)
        self.assertEqual(piece.tempo.beats_per_minute, 90)
        self.assertEqual(piece.instrument.name, "Acoustic Grand Piano")

    def test_piece_uses_configuration_defaults(self):
        piece = Piece(Voice("C-"))

        self.assertEqual(piece.key.name, "C")
        self.assertEqual(piece.time.numerator, 4)
        self.assertEqual(piece.time.denominator, 4)
        self.assertEqual(piece.tempo.beats_per_minute, 120)

    def test_piece_rejects_duplicate_configuration(self):
        with self.assertRaisesRegex(TypeError, "one Key"):
            Piece(Voice("C-"), Key("C"), Key("G"))

    def test_piece_rejects_unequal_voices(self):
        with self.assertRaisesRegex(ValueError, "same length"):
            Piece(
                Key("C"),
                Time("2/4"),
                Tempo(120),
                Voice("C-"),
                Voice("C---"),
            )

    def test_voice_rejects_invalid_notation(self):
        with self.assertRaisesRegex(ValueError, "Invalid voice symbols"):
            Voice("C-X")

    def test_values_reject_invalid_inputs(self):
        with self.assertRaises(ValueError):
            Key("H")
        with self.assertRaises(ValueError):
            Time("3/3")
        with self.assertRaises(ValueError):
            Tempo(0)
