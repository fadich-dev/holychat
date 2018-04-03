import pyaudio


RECORD_FORMAT_IN = pyaudio.paInt16
RECORD_WIDTH = 2
RECORD_FORMAT_OUT = pyaudio.PyAudio().get_format_from_width(RECORD_WIDTH)
RECORD_CHANNELS = 1
RECORD_RATE_IN = 32000
RECORD_CHUNK = 96


def create_stream_in(
        format=RECORD_FORMAT_IN,
        channels=RECORD_CHANNELS,
        rate=RECORD_RATE_IN,
        frames_per_buffer=RECORD_CHUNK):

    return pyaudio.PyAudio().open(
        format=format,
        channels=channels,
        rate=rate,
        input=True,
        frames_per_buffer=frames_per_buffer
    )


def create_stream_out(
        format=RECORD_FORMAT_OUT,
        channels=RECORD_CHANNELS,
        rate=RECORD_RATE_IN,
        frames_per_buffer=RECORD_CHUNK):

    return pyaudio.PyAudio().open(
        format=format,
        channels=channels,
        rate=rate,
        output=True,
        frames_per_buffer=frames_per_buffer
    )
