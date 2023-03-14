import wave
import pyaudio
import speech_recognition as sr
from flask import Flask, render_template, redirect, url_for, request
from flask import jsonify, Request
import subprocess


app = Flask(__name__)


@app.route('/')
def index():

   # subprocess.run(['python', 'voicetomorse.py'])
    # import voicetomorse

    return render_template('body.html')


@app.route('/run_program', methods=['GET'])
def run_program():
    FRAMES_PER_BUFFER = 3200
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000

    p = pyaudio.PyAudio()

    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=FRAMES_PER_BUFFER
    )

    print("start recording")

    seconds = 5
    frames = []
    for i in range(0, int(RATE/FRAMES_PER_BUFFER*seconds)):
        data = stream.read(FRAMES_PER_BUFFER)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    obj = wave.open("output.wav", "wb")
    obj.setnchannels(CHANNELS)
    obj.setsampwidth(p.get_sample_size(FORMAT))
    obj.setframerate(RATE)
    obj.writeframes(b"".join(frames))
    obj.close()

    filename = "output.wav"
    r = sr.Recognizer()

    with sr.AudioFile(filename) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data)

    # print(text)

    MORSE_CODE_DICT = {'A': '.-', 'B': '-...',
                       'C': '-.-.', 'D': '-..', 'E': '.',
                       'F': '..-.', 'G': '--.', 'H': '....',
                       'I': '..', 'J': '.---', 'K': '-.-',
                       'L': '.-..', 'M': '--', 'N': '-.',
                       'O': '---', 'P': '.--.', 'Q': '--.-',
                       'R': '.-.', 'S': '...', 'T': '-',
                       'U': '..-', 'V': '...-', 'W': '.--',
                       'X': '-..-', 'Y': '-.--', 'Z': '--..',
                       '1': '.----', '2': '..---', '3': '...--',
                       '4': '....-', '5': '.....', '6': '-....',
                       '7': '--...', '8': '---..', '9': '----.',
                       '0': '-----', ', ': '--..--', '.': '.-.-.-',
                       '?': '..--..', '/': '-..-.', '-': '-....-',
                       '(': '-.--.', ')': '-.--.-'}

    def encrypt(message):
        cipher = ''
        for letter in message:
            if letter != ' ':

                cipher += MORSE_CODE_DICT[letter] + ' '
            else:
                cipher += ' '
        return cipher

    print('Input Voice:'+'\t'+text)
    message = text
    result = encrypt(message.upper())
    print('Morse Code:'+'\t'+result)

    return render_template('body.html', text=message, morse=result)


if __name__ == '__main__':
    app.run(debug=True)
