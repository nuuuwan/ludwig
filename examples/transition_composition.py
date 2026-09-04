from pathlib import Path

from ludwig import Chord, Composer, Instrument, Tempo

chords = tuple(
    Chord(notation)
    for notation in (
        "CEG",
        "GBD",
        "FAC",
        "ACE",
        "DFA",
    )
)

instrument = Instrument("Synth Voice")
piece = Composer(chords, seed=7).compose(
    duration=60,
    voices=(
        instrument,
        instrument,
        instrument,
    ),
    tempo=Tempo(60),
)
piece.to_midi(Path(__file__).with_suffix(".mid"))
