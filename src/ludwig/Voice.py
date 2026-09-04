import re


class Voice:
    TOKEN_PATTERN = r"[A-G][0-9]?|[-.]"
    PITCHES = {
        "C": 60,
        "D": 62,
        "E": 64,
        "F": 65,
        "G": 67,
        "A": 69,
        "B": 71,
    }

    def __init__(self, notation):
        if not isinstance(notation, str) or not notation:
            raise ValueError("Voice notation must be a non-empty string")
        compact = notation.replace(" ", "")
        self._tokens = tuple(re.findall(self.TOKEN_PATTERN, compact))
        invalid = re.sub(self.TOKEN_PATTERN, "", compact)
        if invalid:
            symbols = "".join(sorted(set(invalid)))
            raise ValueError(f"Invalid voice symbols: {symbols}")
        if not self._tokens:
            raise ValueError("Voice notation must contain a note or rest")
        if self._tokens[0] == "-":
            raise ValueError("A voice cannot begin with a sustain")
        self._validate_pitches()
        self.notation = notation
        self._semitones = 0

    def _validate_pitches(self):
        for token in self._tokens:
            if len(token) == 2:
                self._explicit_pitch(token)

    @classmethod
    def _explicit_pitch(cls, token):
        pitch = cls.PITCHES[token[0]] + 12 * (int(token[1]) - 4)
        if not 0 <= pitch <= 127:
            raise ValueError(f"Pitch outside MIDI range: {token}")
        return pitch

    @classmethod
    def _resolve_pitch(cls, token, previous):
        if len(token) == 2:
            return cls._explicit_pitch(token)
        if previous is None:
            return cls.PITCHES[token]
        pitch_class = cls.PITCHES[token] % 12
        lower = previous - (previous - pitch_class) % 12
        candidates = (lower, lower + 12)
        valid = (pitch for pitch in candidates if 0 <= pitch <= 127)
        return min(valid, key=lambda pitch: abs(pitch - previous))

    @staticmethod
    def _append_event(events, start, end, pitch):
        if pitch is not None:
            events.append((start, end - start, pitch))

    def events(self):
        events = []
        start = 0
        pitch = None
        previous = None
        for position, symbol in enumerate(self._tokens):
            if symbol == "-":
                continue
            self._append_event(events, start, position, pitch)
            start = position
            if symbol == ".":
                pitch = None
            else:
                previous = self._resolve_pitch(symbol, previous)
                pitch = previous + self._semitones
        self._append_event(events, start, len(self._tokens), pitch)
        return events

    def transpose(self, semitones):
        if not isinstance(semitones, int):
            raise TypeError("Semitones must be an integer")
        if any(
            not 0 <= pitch + semitones <= 127 for _, _, pitch in self.events()
        ):
            raise ValueError("Transposed pitch outside MIDI range")
        voice = Voice(self.notation)
        voice._semitones = self._semitones + semitones
        return voice

    def __len__(self):
        return len(self._tokens)

    def __add__(self, other):
        if not isinstance(other, Voice):
            return NotImplemented
        return Voice(self.notation + other.notation)
