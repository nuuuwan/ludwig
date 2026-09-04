# Comparable systems

This is a representative survey, not an exhaustive list. Music notation ranges
from compact melody formats to live-coding languages, synthesis languages, and
full score-interchange standards.

## [ABC notation](https://abcnotation.com/wiki/abc:standard:v2.1)

ABC is a human-readable format used especially for folk tunes. Note letters
carry optional accidentals, octave marks, and duration multipliers. Headers
define key, meter, unit length, and tempo.

```abc
X:1
T:C major fragment
M:4/4
L:1/8
K:C
C2 D2 E2 F2 |
```

A default unit duration keeps simple tunes short while multipliers allow
rhythmic variation. Its long history also shows how extensions and dialects can
weaken portability.

## [LilyPond](https://lilypond.org/doc/v2.24/Documentation/notation/)

LilyPond produces publication-quality sheet music. Its source describes notes
and score structure while an engraving engine decides visual layout. Pitches
can be absolute or relative to the previous pitch.

```lilypond
\relative c' {
c4 d e f
}
```

Semantic music input and visual layout remain separate. Relative pitch is
compact, but one edit can change the interpretation of later notes.

## [MusicXML](https://www.w3.org/2021/06/musicxml40/)

MusicXML exchanges scores between notation programs. Its XML tree records
measures, notes, durations, voices, notation marks, and layout details.

```xml
<note>
<pitch>
<step>C</step>
<octave>4</octave>
</pitch>
<duration>1</duration>
<type>quarter</type>
</note>
```

It is a strong interchange target, not a friendly authoring syntax. Ludwig can
stay small while exporting to richer formats when needed.

## [Humdrum `**kern`](https://www.humdrum.org/guide/ch02/)

Humdrum supports computational musicology and analysis. Time runs down rows and
simultaneous parts occupy tab-separated columns. Reciprocal numbers encode
durations, while null tokens preserve the grid when another voice moves.

```text
**kern
*M4/4
=1
4c
4d
4e
4f
*-
```

Explicit alignment makes polyphony easy to analyze. Ludwig's equal-length voice
strings provide a simpler version of the same idea.

## [music21 TinyNotation](https://www.music21.org/music21docs/usersGuide/usersGuide_16_tinyNotation.html)

TinyNotation belongs to music21, a Python toolkit whose name reflects its
origins as a project nurtured at MIT. It provides a deliberately small grammar
for entering short musical fragments without constructing Python note objects
one at a time.

```text
tinyNotation: 4/4 c4 d e f
```

The first duration is inherited by later notes. Letter case and repetition
select octaves, while suffixes express accidentals, rests, dots, and ties. Its
designers intentionally exclude complex notation and provide extension points
instead. This is close to Ludwig's goal and offers a useful warning: compact
syntax stays compact only when its boundary is explicit.

## [Alda](https://alda.io/tutorial/)

Alda writes playable scores in text. Notes follow instrument labels. Duration
suffixes become defaults for following notes; `/` forms chords, `r` forms rests,
and named markers synchronize parts.

```alda
piano: o4 c4 d e f
```

Stateful defaults make scores concise, but local meaning depends on preceding
tokens. Instrument sections and synchronization markers scale better than
positional arguments.

## [Sonic Pi](https://sonic-pi.net/tutorial.html)

Sonic Pi is designed for live coding and algorithmic performance. Ruby-like
commands generate music directly through notes, delays, loops, functions, and
concurrent `live_loop` blocks.

```ruby
play :c4
sleep 1
play :d4
sleep 1
play :e4
sleep 1
play :f4
```

General programming constructs unlock repetition and variation, but they make
a composition harder to inspect as static musical data. Deterministic randomness
is valuable for reproducibility.
