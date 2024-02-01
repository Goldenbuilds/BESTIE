import os #gives access to user's os
import speech_recognition as sr 
import winsound 
import pyttsx3 
import time 


def welcome(): #greet
    say("Hello, I am bestie!")

def get_user_name(): 
    say("What is your name?")
    audio = listen()
    username = recognize(audio)

    if username: # if username is not empty or none
        say(f"Welcome, {username}!")
        print("Welcome {username}")
        return username

    else: 
        say("Sorry, I didn't quite get that")
        return ""

    
def listen():  
    recognizer = sr.Recognizer() 
    with sr.Microphone() as source: #capture audio from mic
        recognizer.adjust_for_ambient_noise(source)
        play_sound(300,500)
        audio = recognizer.listen(source, timeout=5) #listens to the audio input from the mic and stores it in the audio variable

    return audio 
    
def recognize(audio):
    recognizer = sr.Recognizer()

    try:
        text = recognizer.recognize_google(audio)
        return text
    
    except sr.UnknownValueError:
        return ""

def say(text): #allows bestie speak to user
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def play_sound(sound_freq, duration): 
    winsound.Beep(sound_freq, duration)

def get_files_in_directory(directory):
    files = []
    for root, _, filenames in os.walk(directory): #get file name with paths
        files.extend([os.path.join(root, filename) for filename in filenames])
    return files


def find_file(file_system, category, filename):
    # Check if the given filename is associated with the specified category in the file_system
    file_names = file_system.get(category, [])
    return filename in [os.path.basename(path) for path in file_names]

def get_category_from_filename(filename, file_system):
    _, extension = os.path.splitext(filename)
    category = extension[1:] if extension else None

    if category and category in file_system:
        return category
    else:
        return None


def get_files_to_delete(file_system):
    say("Please specify the name of the file:")
    audio_filename = listen()
    filename = recognize(audio_filename)

    category = get_category_from_filename(filename, file_system)

    if category and filename and find_file(file_system, category, filename):
        return os.path.join(category, filename)
    else:
        print("File not found or category not recognized.")
        return ""

def delete(file_name):
    try:
        os.remove(file_name)
        say(f"{file_name} has been deleted successfully.")
    except FileNotFoundError:
        handle_error(f"File '{file_name}' not found.")
    except PermissionError:
        handle_error(f"I was denied Permission and I'm unable to delete the file.")
    except Exception as e:
        handle_error(f"An unexpected error occurred: {e}")
        say("An unexpected error occurred while deleting the file.")


def handle_error(error_message):
    say(f"Error: {error_message}")


def go_to_sleep():
    say("Deactivating bestie. I am going to sleep.")
    exit()  # Exiting the script or performing necessary cleanup actions


def confirm_deletion(file_name):
    say(f"Are you sure you want to delete the file {file_name}? Say 'confirm' to proceed.")
    audio_confirmation = listen()
    confirmation = recognize(audio_confirmation)
    return confirmation

    try:
        if 'confirm' in confirmation.lower() or 'yes' in confirmation.lower():
            say("Okay, proceeding with the deletion.")
            return True
        else:
            say("Deletion canceled.")
            return False
    except sr.UnknownValueError:
        handle_error("I could not understand your confirmation. Deletion canceled.")
        return False
    except sr.RequestError as e:
        handle_error("I use the internet. Gold, you are not connected to the internet.")
        return False
    except Exception as e:
        handle_error("Sorry, an error occurred during confirmation. Deletion canceled.")
        return False

def main():
    file_system = {} #initialize an empty file system
    welcome()
    username = get_user_name()

    if not username:
        return
    say(f"Hello, {username}! How can I assist you today?")

    while True:
        say("What do you want me to do for you?")
        time.sleep(1)
        query = listen()

        if query:
            try:
                response = recognize(query)
                if response == "delete_file":
                    say("Sure , let;s proceed with deleting ")
                    file_to_delete = get_files_to_delete(file_system)
                    if file_to_delete and confirm_deletion(file_to_delete):
                        delete(file_to_delete)
                elif response == "unknown_intent":
                    say("I'm sorry, I didn't understand that. Could you please rephrase?")
                elif response == "go_to_sleep":
                    say("Alright, deactivating. Have a great day!")
                    go_to_sleep()
                    break
                else:
                    say("I'm not sure how to handle that. Can you please provide more details?")
            except Exception as e:
                handle_error(f"An unexpected error occurred: {e}")
                say("Sorry, an unexpected error occurred. Exiting.")
                break
        else:
            say("I didn't hear anything. Could you please repeat your command?")

    

if __name__ == "__main__":
    main()