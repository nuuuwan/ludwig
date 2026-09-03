class Voice:
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
        invalid = set(notation) - set(self.PITCHES) - {"-", "."}
        if invalid:
            symbols = "".join(sorted(invalid))
            raise ValueError(f"Invalid voice symbols: {symbols}")
        if notation[0] == "-":
            raise ValueError("A voice cannot begin with a sustain")
        self.notation = notation

    def events(self):
        events = []
        start = 0
        pitch = None
        for position, symbol in enumerate(self.notation):
            if symbol == "-":
                continue
            if pitch is not None:
                events.append((start, position - start, pitch))
            start = position
            pitch = self.PITCHES.get(symbol)
        if pitch is not None:
            events.append((start, len(self.notation) - start, pitch))
        return events

    def __len__(self):
        return len(self.notation)

    def __add__(self, other):
        if not isinstance(other, Voice):
            return NotImplemented
        return Voice(self.notation + other.notation)
