class Note:
    NAMES = (
        "C",
        "C#",
        "D",
        "D#",
        "E",
        "F",
        "F#",
        "G",
        "G#",
        "A",
        "A#",
        "B",
    )

    def __init__(self, number):
        if not isinstance(number, int):
            raise TypeError("Note number must be an integer")
        if not 0 <= number <= 127:
            raise ValueError("Note number outside supported range")
        self.number = number
        octave, name_index = divmod(number, len(self.NAMES))
        self.name = self.NAMES[name_index]
        self.octave = octave - 1

    def __str__(self):
        return f"{self.name}{self.octave}"
