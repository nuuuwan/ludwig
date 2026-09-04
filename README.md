# ludwig

Ludwig turns short text melodies into MIDI files that music players and
digital audio workstations can open. It is intended for anyone who wants to
experiment with composition without learning music software first.

```python
from ludwig import Instrument, Piece

twinkle_twinkle = Piece(
 Instrument('Violin')['C4-C-G4-G-A-A-G---F-F-E-E-D-D-C---'],
 Instrument('Violin')['E3---C4-E-C-F-C---B-D-C-A---G-E---'],
 Instrument('Viola')['G2-C---G-F---C-E-G-----C---B-G---'],
 Instrument('Cello')['C2-G2-E3-C-F-C-E-C-D-B-C-A-F-G-C---'],
)
twinkle_twinkle.transpose(-4).to_midi('midi/twinkle_twinkle.mid')
```

Each token is one eighth note of time. Letters `A` through `G` begin a note,
`-` sustains it, and `.` adds silence. An octave number fixes a note's pitch, so
`C4` is middle C. Without a number, Ludwig chooses the pitch closest to the
previous note; the first unnumbered note starts in octave 4. Spaces are ignored,
so voices can be aligned for readability. Try changing the first `G` to an `E`,
run the example again, and compare the two melodies.

Indexing an `Instrument` with notation creates a voice played by that
instrument. `Piece` recognizes key, time, tempo, and voices in any order.
Omitted settings default to the key of C, 4/4 time, and 120 beats per minute.
