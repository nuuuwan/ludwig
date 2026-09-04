# ludwig

Ludwig turns short text melodies into MIDI files that music players and
digital audio workstations can open. It is intended for anyone who wants to
experiment with composition without learning music software first.

```python
from ludwig import Instrument, Piece, Voice

twinkle_twinkle = Piece(
 Instrument('Violin'),
 Voice('C4-C-G4-G-A-A-G---F-F-E-E-D-D-C---'),
 Voice('E3-E-C4-E-E-F-E-C-G-G-G-C-C-B-C---'),
 Voice('C2-G2-E4-C-F-C-E-C-D-B-C-A-F-G-C---'),
)
twinkle_twinkle.to_midi('midi/twinkle_twinkle.mid')
```

Each token is one eighth note of time. Letters `A` through `G` begin a note,
`-` sustains it, and `.` adds silence. An octave number fixes a note's pitch, so
`C4` is middle C. Without a number, Ludwig chooses the pitch closest to the
previous note; the first unnumbered note starts in octave 4. Spaces are ignored,
so voices can be aligned for readability. Try changing the first `G` to an `E`,
run the example again, and compare the two melodies.

`Piece` recognizes each argument by its class, so instrument, key, time, tempo,
and voices can appear in any order. Omitted settings default to acoustic grand
piano, the key of C, 4/4 time, and 120 beats per minute.
