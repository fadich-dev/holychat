import pyaudio


FORMAT = pyaudio.paInt16
WIDTH = 2
CHANNELS = 1
RATE_IN = 40000
RATE_OUT = 60000
CHUNK_IN = 32
CHUNK_OUT = int(RATE_OUT / RATE_IN * CHUNK_IN)
# By default... RATE = 44100

print(RATE_IN, RATE_OUT)
print(CHUNK_IN, CHUNK_OUT)

audio_in = pyaudio.PyAudio()
audio_out = pyaudio.PyAudio()

format_out = audio_out.get_format_from_width(WIDTH)

stream_in = audio_in.open(format=FORMAT, channels=CHANNELS, rate=RATE_IN, input=True, frames_per_buffer=CHUNK_IN)
stream_out = audio_out.open(format=format_out, channels=CHANNELS, rate=RATE_OUT, output=True, frames_per_buffer=CHUNK_OUT)


try:
    while True:
        print('Speak...')
        rec = stream_in.read(2 ** 17)
        stream_out.write(rec)
except ConnectionResetError as e:
    print('Disconnected...')
except KeyboardInterrupt as e:
    print('Stopping app...')
finally:
    stream_in.stop_stream()
    stream_in.close()
    stream_out.stop_stream()
    stream_out.close()

    audio_in.terminate()
    audio_out.terminate()
