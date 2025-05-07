import wave
import numpy as np


def embed_lsb(audio_in, audio_out, message):
    message += chr(0)
    bits = ''.join(f'{ord(c):08b}' for c in message)


    audio = wave.open(audio_in, mode='rb')
    frames = bytearray(list(audio.readframes(audio.getnframes())))
    audio.close()


    for i in range(len(bits)):
        frames[i] = (frames[i] & 254) | int(bits[i])


    stego = wave.open(audio_out, 'wb')
    stego.setparams(audio.getparams())
    stego.writeframes(frames)
    stego.close()


def extract_lsb(audio_file):
    audio = wave.open(audio_file, mode='rb')
    frames = bytearray(list(audio.readframes(audio.getnframes())))
    audio.close()


    bits = ''.join([str(f & 1) for f in frames])


    chars = [chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8)]


    message = ''
    for c in chars:
        if c == chr(0):
            break
        message += c

    return message


def generate_wav(file_name):

    framerate = 44100
    duration = 5
    t = np.linspace(0, duration, int(framerate * duration), endpoint=False)
    signal = 32767 * np.sin(2 * np.pi * 440 * t)


    signal = signal.astype(np.int16)
    with wave.open(file_name, 'wb') as file:
        file.setnchannels(1)
        file.setsampwidth(2)
        file.setframerate(framerate)
        file.writeframes(signal.tobytes())


if __name__ == "__main__":

    generate_wav('ornek.wav')


    embed_lsb('ornek.wav', 'stego.wav', 'Bu bir gizli test mesajıdır.')


    gizli_mesaj = extract_lsb('stego.wav')
    print("Çözülen mesaj:", gizli_mesaj)
