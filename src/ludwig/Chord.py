import re
from collections import Counter

from ludwig.ChordQualities import ChordQualities
from ludwig.Note import Note


class Chord:
    def __init__(self, *notes):
        if not notes:
            raise ValueError("Chord requires one or more notes")
        if len(notes) == 1 and isinstance(notes[0], str):
            notes = self._parse(notes[0])
        self.notes = tuple(
            note if isinstance(note, Note) else Note(note) for note in notes
        )

    @staticmethod
    def _parse(notation):
        names = tuple(re.findall(r"[A-G]#?", notation))
        if not names or "".join(names) != notation:
            raise ValueError("Invalid chord notation")
        numbers = []
        for name in names:
            number = 60 + Note.NAMES.index(name)
            while numbers and number <= numbers[-1]:
                number += 12
            numbers.append(number)
        return tuple(numbers)

    @classmethod
    def named(cls, root, quality):
        if quality not in ChordQualities.INTERVALS:
            raise ValueError(f"Invalid chord quality: {quality}")
        return cls(
            *(
                root + interval
                for interval in ChordQualities.INTERVALS[quality]
            )
        )

    def __hash__(self):
        return hash(tuple(str(note) for note in self.notes))

    def edit_distance(self, other):
        if not isinstance(other, Chord):
            raise TypeError("Chord distance requires another Chord")
        left = Counter(note.number % 12 for note in self.notes)
        right = Counter(note.number % 12 for note in other.notes)
        return sum((left - right).values()) + sum((right - left).values())

    def __eq__(self, other):
        if not isinstance(other, Chord):
            return NotImplemented
        return tuple(map(str, self.notes)) == tuple(map(str, other.notes))
