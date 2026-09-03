class Time:
    def __init__(self, signature):
        try:
            numerator, denominator = map(int, signature.split("/"))
        except (AttributeError, TypeError, ValueError):
            raise ValueError(f"Invalid time signature: {signature}") from None
        if numerator < 1 or denominator not in (1, 2, 4, 8, 16, 32):
            raise ValueError(f"Invalid time signature: {signature}")
        self.numerator = numerator
        self.denominator = denominator

    @property
    def midi_denominator(self):
        return self.denominator.bit_length() - 1
