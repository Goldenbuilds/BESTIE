import pyttsx3
import speech_recognition as sr
import winsound
import time

# Function to listen to microphone and convert spoken words to text
def take_command(r,source):
    print("Listening...")
    speak("Listening... ")
    r.adjust_for_ambient_noise(source, duration=5)  # Adjust for 5 seconds of ambient noise
    Ready_sound1()  # Make a sound to know terminator is ready
    audio = r.listen(source)
    query = ''
    try:
        print("Recognizing... ", end="")
        speak("Recognizing...")
        Ready_sound2()
        time.sleep(1)  # Add a delay for user feedback
        query = r.recognize_google(audio, language='en-US')
        print(f"User said: {query}")
    except sr.UnknownValueError:
        print("Speech recognition could not understand audio.")
        speak("Sorry, I could not understand.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    except Exception as e:
        print(f"Exception occurred: {e}")
    return query.lower()

# Terminator's sound
def Ready_sound1():
    winsound.Beep(600, 300)

def Ready_sound2():
    winsound.Beep(500, 300)

# Function to speak any text passed to it
def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    print("T.E.R.M.I.N.A.T.O.R.: " + text + "\n")
    engine.say(text)
    engine.runAndWait()

def Detect_wake_word():
    r = sr.Recognizer()
    microphone = sr.Microphone()
    with microphone as source:
        print("Listening for 'Hey Bestie' ...")
        speak("Say 'Hey Bestie' to activate me and 'go to sleep' to deactivate")
        r.adjust_for_ambient_noise(source, duration=5)  # Adjust for 5 seconds of ambient noise
        Ready_sound1()  # Make a sound to know terminator is ready
        audio = r.listen(source)
        query = ''
        try:
            time.sleep(1)  # Add a delay for user feedback
            query = r.recognize_google(audio, language='en-US')
            print(f"User said: {query}")

            # Continuously listen for speech
            while True:
                audio = r.listen(source, timeout= None)
                try:
                    detected_phrase = r.recognize_google(audio, language='en-US')
                    print(f"Detected: {detected_phrase}")
                    if "hey bestie" in detected_phrase.lower():
                        speak("Hotword detected! Activating assistant")
                        query = take_command(r, source)
                    if "go to sleep" in detected_phrase:
                        speak("Deactivating assistant")
                        break  # Exit the loop to stop listening
                except sr.UnknownValueError:
                    speak("I could not detect a hot word")
                    pass  # Ignore if the speech couldn't be recognized
                except sr.RequestError:
                    print("Failed to request results from Google Speech Recognition service.")
        except sr.UnknownValueError:
            print("Speech recognition could not understand audio.")
            speak("Sorry, I could not understand.")
        except sr.RequestError as e:
            print(
                f"Could not request results from Google Speech Recognition service; {e}")
            # speak("Encountered an error in recognition.")
        except Exception as e:
            print(f"Exception occurred: {e}")
            # speak("An unexpected error occurred.")
    return query.lower()

    

Hotword = Detect_wake_word()
