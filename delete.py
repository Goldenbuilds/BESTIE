import os
import speech_recognition as sr
import pyttsx3
import winsound
import time




def Delete_specific_file_in_documents(file_to_delete):
    document_path = r'C:\Users\GOLD\Documents'
    file_to_delete = file_to_delete.lower() #convert to lowercase 
    file_found = False

    try:
        for root, directories, files in os.walk(document_path):
            for file_name in files:
                if file_to_delete in file_name.lower(): 
                    file_path = os.path.join(root, file_name)
                    try:
                        os.remove(file_path)
                        say(f"Deleted: {file_path}")
                        print(f"Deleted: {file_path}")
                        file_found = True
                    except FileNotFoundError:
                        print(f"File not found: {file_path}")
                        say("File not found for deletion.")

                    except PermissionError:
                        print(f"No permission to delete: {file_path}")
                        say("Permission denied to delete the file.")

                    except Exception as e:
                        print(f"Error deleting {file_path}: {e}")
                        say(f"Error deleting {file_path}: {e}")
    except OSError as e:
        print(f"OS error occured while searching for files: {e}")
        say("An OS error occured while searching for file")
    except Exception as e:
        print(f"An error occurred while searching for files: {e}")
        say("An unexpected error occurred while processing the request.")

    if not file_found:
        print(f"No file found matching '{file_to_delete}' in the documents folder")

def take_command():  # hear what is being said
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Calibrating ambient noise... Please remain silent.")
        r.adjust_for_ambient_noise(source, duration=5)  # Adjust for 5 seconds of ambient noise
        Ready_sound1()  # Make a sound to know terminator is ready
        audio = r.listen(source)
        print("listening...") # Add this line
        say("Listening... ")
        audio = r.listen(source)
        query = ''
        try:
            print("Recognizing... ", end="")
            say("Recognizing...")
            Ready_sound2()
            time.sleep(1)  # Add a delay for user feedback
            query = r.recognize_google(audio, language='en-US')
            print(f"User said: {query}")
        except sr.UnknownValueError:
            print("Speech recognition could not understand audio.")
            say("Sorry, I could not understand.")
        except sr.RequestError as e:
            print(
                f"Could not request results from Google Speech Recognition service; {e}")
            # speak("Encountered an error in recognition.")
        except Exception as e:
            print(f"Exception occurred: {e}")
            # speak("An unexpected error occurred.")
    return query.lower()

def Ready_sound1():
    winsound.Beep(600, 300)


def Ready_sound2():
    winsound.Beep(500, 300)


def delete_upon_keyword(query):
    words = query.lower().split()
    if "delete" in words:
        try:
            file_to_delete = ' '.join(words[words.index("delete")+ 1:])
            Delete_specific_file_in_documents(file_to_delete.strip())
        except ValueError:
            print("File name not found in the command.")
            say("File name not found in the command.")
    else:
        say("Command not recognized or not applicable.")



engine = pyttsx3.init()


def say(text):
    engine.say(text)
    engine.runAndWait()


command = take_command()  # Get user command
delete_upon_keyword(command)  # Perform action based on the command