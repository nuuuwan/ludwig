import math
from pathlib import Path

from ludwig import Instrument, Note, Piece, Tempo

instruments = []
for i in range(1, 7):
    note_num = int(round(12 * math.log2(10 * i), 0))
    instrument = Instrument("Pad 1 (new age)")[
        ".." * (2 * i) + f"{Note(note_num)}" + "-" * 31 + ".." * (16 - 2 * i)
    ]
    instruments.append(instrument)
instruments.reverse()

yoga = Piece(Tempo(20), *instruments)
yoga.to_midi(Path(__file__).with_suffix(".mid"))
