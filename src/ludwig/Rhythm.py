class Rhythm:
    NOTE_DURATION = 2

    @classmethod
    def spans(cls, tokens):
        if tokens % cls.NOTE_DURATION:
            raise ValueError("Duration must align with a beat")
        return (cls.NOTE_DURATION,) * (tokens // cls.NOTE_DURATION)

    @staticmethod
    def notation(arrangements, voice_index, spans):
        notation = ""
        previous = None
        for notes, width in zip(arrangements, spans):
            note = notes[voice_index]
            repeated = previous and note.number == previous.number
            notation += (
                "-" * width if repeated else str(note) + "-" * (width - 1)
            )
            previous = note
        return notation
