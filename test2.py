import os
import speech_recognition as sr
from delete import Ready_sound1, Ready_sound2, say
import time

 #Functions for command recognition
def calibrate_noise(r, source):
    print("Calibrating ambient noise... Please remain silent.")
    r.adjust_for_ambient_noise(source, duration=5)
    Ready_sound1()

def listen_command(r):
    with sr.Microphone() as source:
        calibrate_noise(r, source)
        print("Listening...")
        say("Listening... ")
        audio = r.listen(source)
        wait = r.pause(source)
    return audio

def recognize_audio(r, audio):
    print("Recognizing... ", end="")
    say("Recognizing...")
    Ready_sound2()
    time.sleep(1)
    try:
        query = r.recognize_google(audio, language='en-US')
        print(f"User said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        print("Speech recognition could not understand audio.")
        say("I could not recognise your words. Please say it again")
        return ''
    except sr.RequestError as e:
        say("I am unable to work offline. Check your network.")
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ''
    except Exception as e:
        print(f"Exception occurred: {e}")
        return ''

def take_command():
    r = sr.Recognizer()
    audio = listen_command(r)
    return recognize_audio(r, audio)

def parse_command(command):
    if "delete" in command and "file" in command:
        return "delete_file"
    elif any(word in command for word in ["go to sleep", "bestie sleep", "sleep"]):
        return "go to sleep"
    else:
        return "unknown_intent"

#search for files matching filename gievn by user
def find_matching_files(file_name):
    current_directory = os.getcwd()
    matching_files = [file for file in os.listdir(current_directory)if file_name.lower() in file.lower() ]
    return matching_files



#delete files by name (with user selection)
def delete_files_by_name(file_name):
    matching_files = find_matching_files(file_name)

    if not matching_files:
        say("No file match found")

    else:
        say(f"{len(matching_files)} matches found")
        for index, file in enumerate(matching_files, start= 1):
            say(f"{index}.{file}")

        try:
            selection = take_command().lower()
            # Match spoken input directly with filenames for deletion
            for file_index, file in enumerate(matching_files, start=1):
                if str(file_index) in selection:
                    file_to_delete = matching_files[file_index - 1]
                    say(f"Are you sure you want to delete {file_to_delete}? (yes/no)")
                    confirmation = take_command().lower()
                    
                    if confirmation == "yes":
                        delete_specific_file(file_to_delete)
                        say("File deleted.")
                    else:
                        say("Deletion canceled.")
                    break  # Exit loop after handling file deletion
                    
            else:
                say("Invalid selection. Please select a file number I mentioned.")
        except Exception as e:
            say("Sorry, an error occurred.")
def delete_specific_file(file_path):
    try:
        os.remove(file_path)
        print(f"Your file has been deleted successfully.")
    except FileNotFoundError:
        print("File not found.")
    except PermissionError:
        print("Permission denied. Unable to delete the file.")
    except Exception as e:
        print(f"An error occurred: {e}")


def delete_upon_keyword(query):
    words = query.lower().split()
    if "delete" in words:
        try:
            file_to_delete = ' '.join(words[words.index("delete")+ 1:])
            delete_specific_file(file_to_delete.strip())
        except ValueError:
            print("File name not found in the command.")
            say("File name not found in the command.")
    else:
        say("Command not recognized or not applicable.")



def go_to_sleep():
    print("Deactivating bestie...")
    say("I am going to sleep...")
    exit()  # Exiting the script or performing necessary cleanup actions

   

def recognize_command(query):
    intent = parse_command(query)
    
    if intent == "delete_file":
        delete_files_by_name(query)
        
    elif intent == "go to sleep" or intent == "sleep bestie":
        go_to_sleep()
    else:
        say("Command not recognized or not applicable.")


def main():
    print("Listening for commands...")
    while True:
        query = take_command()
        recognize_command(query)

if __name__ == "__main__":
    main()