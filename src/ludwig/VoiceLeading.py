import itertools

from ludwig.Note import Note


class VoiceLeading:
    REGISTER_RANGE = 12

    @classmethod
    def arrange(cls, chords, voice_count):
        arrangements = [cls._expand(chords[0].notes, voice_count)]
        anchors = arrangements[0]
        for chord in chords[1:]:
            notes = cls._expand(chord.notes, voice_count)
            arrangements.append(cls._closest(notes, arrangements[-1], anchors))
        return tuple(arrangements)

    @classmethod
    def _expand(cls, notes, voice_count):
        numbers = {note.number for note in notes}
        candidates = {
            number for note in notes for number in cls._octaves(note)
        }
        nearby = sorted(
            candidates - numbers,
            key=lambda number: (
                min(abs(number - note.number) for note in notes),
                number,
            ),
        )
        numbers.update(nearby[: voice_count - len(numbers)])
        return tuple(Note(number) for number in sorted(numbers))

    @classmethod
    def _closest(cls, notes, previous, anchors):
        candidates = []
        for permutation in itertools.permutations(notes):
            firsts = cls._choices(permutation[0], anchors[0])
            for first in firsts:
                numbers = cls._ascending(permutation, previous, anchors, first)
                if numbers:
                    movement = sum(
                        abs(number - prior.number)
                        for number, prior in zip(numbers, previous)
                    )
                    register = sum(
                        abs(number - anchor.number)
                        for number, anchor in zip(numbers, anchors)
                    )
                    candidates.append((movement, register, numbers))
        return tuple(Note(number) for number in min(candidates)[2])

    @classmethod
    def _ascending(cls, notes, previous, anchors, first):
        numbers = [first]
        for index, note in enumerate(notes[1:], 1):
            choices = tuple(
                number
                for number in cls._choices(note, anchors[index])
                if number > numbers[-1]
            )
            if not choices:
                return None
            target = previous[min(index, len(previous) - 1)].number
            numbers.append(
                min(choices, key=lambda number: abs(number - target))
            )
        return tuple(numbers)

    @classmethod
    def _choices(cls, note, anchor):
        return tuple(
            number
            for number in cls._octaves(note)
            if abs(number - anchor.number) <= cls.REGISTER_RANGE
        )

    @staticmethod
    def _octaves(note):
        pitch_class = note.number % 12
        return tuple(range(pitch_class, 128, 12))
