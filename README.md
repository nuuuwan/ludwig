# ludwig

Ludwig turns short text melodies into MIDI files that music players and
digital audio workstations can open. It is intended for anyone who wants to
experiment with composition without learning music software first.

```python
from ludwig import Instrument, Piece, Voice

twinkle_twinkle = Piece(
    Instrument('Violin'),
    Voice('C-C-G-G-A-A-G---F-F-E-E-D-D-C---'),
    Voice('C-G-E-C-F-C-E-C-D-B-D-A-F-G-C---'),
).to_midi('midi/twinkle_twinkle.mid')
```

Each character is one eighth note of time. Letters `A` through `G` begin a
note, `-` sustains it, and `.` adds silence. Try changing the first `G` to an
`E`, run the example again, and compare the two melodies.

`Piece` recognizes each argument by its class, so instrument, key, time, tempo,
and voices can appear in any order. Omitted settings default to acoustic grand
piano, the key of C, 4/4 time, and 120 beats per minute.
