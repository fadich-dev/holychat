import socket
import pyaudio
from time import time
from settings import HOST, PORT, CHUNK


FORMAT = pyaudio.paInt16
CHANNELS = 1
# By default... RATE = 44100
RATE_IN = 80100
RATE_OUT = 82100
WIDTH = 2

CLIENT_ID = time()

try:
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect((HOST, PORT))
except ConnectionRefusedError as e:
    print('Connection refused by <{}:{}>'.format(HOST, PORT))
    exit()


audio_in = pyaudio.PyAudio()
audio_out = pyaudio.PyAudio()

format_out = audio_out.get_format_from_width(WIDTH)

stream_in = audio_in.open(format=FORMAT, channels=CHANNELS, rate=RATE_IN, input=True, frames_per_buffer=CHUNK)
stream_out = audio_out.open(format=format_out, channels=CHANNELS, rate=RATE_OUT, output=True, frames_per_buffer=CHUNK)


try:
    while True:
        soc.sendall(stream_in.read(CHUNK))
        stream_out.write(soc.recv(CHUNK * 10))
except ConnectionResetError as e:
    print('Disconnected...')
except KeyboardInterrupt as e:
    print('Stopping app...')
finally:
    soc.close()
    stream_in.stop_stream()
    stream_in.close()
    stream_out.stop_stream()
    stream_out.close()

    audio_in.terminate()
    audio_out.terminate()
