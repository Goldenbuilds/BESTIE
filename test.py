import pyaudio
import pyttsx3
import speech_recognition 
import speech_recognition as sr
import time
import struct  # helps deal with large data files
import winsound

USER = "Ma"

# ********************* Function to listen to microphone and convert spoken words to text

def take_command(r, source):  # hear what is being said
    Ready_sound1()  # Make a sound to know terminator is ready
    print("listening...")
    speak("Listening... ")
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)  # Adjust for 5 seconds of ambient noise
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
        print(
            f"Could not request results from Google Speech Recognition service; {e}")
        # speak("Encountered an error in recognition.")
    except Exception as e:
        print(f"Exception occurred: {e}")
        # speak("An unexpected error occurred.")
    return query.lower()

# Terminator's sound
def Ready_sound1():
    winsound.Beep(600, 300)


def Ready_sound2():
    winsound.Beep(500, 300)

# ******************* Function to speak any text passed to it.**********************    

def speak(text):  # speak back to me
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    print("T.E.R.M.I.N.A.T.O.R.: " + text + "\n")
    engine.say(text)
    engine.runAndWait()


# ************************* Function to make conversation with terminator more fun
# def ConversationFlow():
#     user_word = take_command()
#     while True:
#         if "hello" in user_word:
#             speak("hello")
#             break
#         if "bye" in user_word:
#             speak("goodbye")
#             break
#         if "how are you" in user_word:
#             speak("I'm doing well")
#         if "are you ready to delete some files for me" in user_word:
#             speak("Of course! That is my job. I am the terminator")
#         if "stop" in user_word:
#             speak("Stopping sir")
#             break
#         if "exit" in user_word:
#             speak("ending program")
#         if "that's it for today" in user_word:
#             speak("Okay,I'll end the program now.")
#             break
#         if "delete" in user_word:
#             speak("Okay let's do this!")

#         time.sleep(2)


def main():
#wake bestie with a word
    r = sr.Recognizer()
    microphone = sr.Microphone()
    with microphone as source:
        # r.adjust_for_ambient_noise(source)
        print("Listening for 'Hey Bestie' ...")
        # speak(" Say 'Hey Bestie' to activate me and 'go to sleep' to deactivate")
    
    
        # continuously listen for speech
        while True:
            audio = r.listen(source)
            try:
                detected_phrase = r.recognize_google(audio, language = 'en-US')
                print(f"Detected: {detected_phrase}")

                if "bestie" in detected_phrase.lower():
                    speak("Hotword detected! Activating assistant")
                    query = take_command(r, source)

                    if "go to sleep" in query:
                        speak("Deactivating assistant")
                        break  # Exit the loop to stop listening
            except sr.UnknownValueError:
                speak("I could not detect an hot word")
                pass  # Ignore if the speech couldn't be recognized
            except sr.RequestError:
                print("Failed to request results from Google Speech Recognition service.")



if __name__ == "__main__":
    main()