import pyaudio
import pyttsx3
import speech_recognition as sr
import time
import struct #helps deal with large data files
import winsound


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        Ready_sound1()
        print("Listening... ", end="")
        audio = r.listen(source)
        query = ''
        try:
            print("Recognizing... ", end="")
            query = r.recognize_google(audio, language='en-US')
            print(f"user said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            print("Sorry, I could not understand")
        except sr.RequestError as e:
            print(f"Encountered a {e}")

    return query.lower()

#Terminator's sound 
def Ready_sound1():
    winsound.Beep(600,300)
