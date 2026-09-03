class MidiEncoder:
    TICKS_PER_BEAT = 480

    @classmethod
    def encode(cls, instrument, key, time, tempo, voices):
        tracks = [cls._metadata_track(key, time, tempo)]
        tracks.extend(
            cls._voice_track(instrument, voice, index)
            for index, voice in enumerate(voices)
        )
        header = b"MThd" + (6).to_bytes(4, "big")
        header += (1).to_bytes(2, "big")
        header += len(tracks).to_bytes(2, "big")
        header += cls.TICKS_PER_BEAT.to_bytes(2, "big")
        return header + b"".join(tracks)

    @classmethod
    def _metadata_track(cls, key, time, tempo):
        body = b"\x00\xff\x51\x03"
        body += tempo.microseconds_per_beat.to_bytes(3, "big")
        body += b"\x00\xff\x58\x04"
        body += bytes((time.numerator, time.midi_denominator, 24, 8))
        body += b"\x00\xff\x59\x02"
        body += key.midi_offset.to_bytes(1, "big", signed=True) + b"\x00"
        return cls._track(body + b"\x00\xff\x2f\x00")

    @classmethod
    def _voice_track(cls, instrument, voice, channel):
        if channel > 15:
            raise ValueError("MIDI supports at most 16 voices")
        body = bytes((0, 0xC0 | channel, instrument.midi_program))
        cursor = 0
        step = cls.TICKS_PER_BEAT // 2
        for start, duration, pitch in voice.events():
            body += cls._variable_length(start * step - cursor)
            body += bytes((0x90 | channel, pitch, 64))
            body += cls._variable_length(duration * step)
            body += bytes((0x80 | channel, pitch, 0))
            cursor = (start + duration) * step
        return cls._track(body + b"\x00\xff\x2f\x00")

    @classmethod
    def _track(cls, body):
        return b"MTrk" + len(body).to_bytes(4, "big") + body

    @classmethod
    def _variable_length(cls, value):
        encoded = [value & 0x7F]
        value >>= 7
        while value:
            encoded.append((value & 0x7F) | 0x80)
            value >>= 7
        return bytes(reversed(encoded))
