import os # access to os
import speech_recognition as sr #text to speech
import winsound # for sounds
import pyttsx3 #for speech synthesis
import time 
import spacy #for nlp , extract the file needed to be deleted


#  Functions
def say(text): #say stuff using speech engine
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def play_sound(sound_freq, duration): #play any sounds
    winsound.Beep(sound_freq, duration)


def listen(timeout= 30): # wait 10 seconds once called  
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=5)
        print("Bestie is listening ...")
        play_sound(600,300)
        try:
            audio = r.listen(source, timeout= timeout) # """get  user's command"""   
        except sr.WaitTimeoutError:
            handle_error("No command received. Please try again.")
            audio = None
    return audio

def take_command():
    audio = listen()  
    command = recognize_command(audio)
    if command is not None:
        return command
    else:
        print("Error: Unable to recognize the command. Please try again.")
        return None
    

def understand_words(audio):
    try:
        r = sr.Recognizer()
        query = r.recognize_google(audio, language='en-US')
        print(f"You said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        handle_error("I could not understand you. Please say it again.")
        return ''
    except sr.RequestError as e:
        handle_error("Gold, You are not connected to the internet.")
        return ''
    except Exception as e:
        handle_error(f"An unexpected error occurred: {e}")
        return ''



def check_intent_sent(command): #check the meaning of query given
    words = command.split()
    for word in words:
        if "delete" in words or "remove" in words:
            return "delete"
    
        elif "go to sleep" in words or "sleep" in words:
            return "go_to_sleep"
        elif "confirm" in words or  "yes" in words:
            return "confirm_deletion"
        else:
            return "unknown_intent"

def find_matching_files(file_name):
    current_directory = os.getcwd()
    matching_files = [file for file in os.listdir(current_directory) if file_name.lower() in file.lower()]
    return matching_files

def find_matching_folders(folder_name):
    current_directory = os.getcwd()
    matching_files = [folder for folder in os.path.isdir(current_directory) if folder_name.lower() in folder.lower()]

def delete_specific_file(file_path):
    try:
        os.remove(file_path)
        say(f"Your file '{file_path}' has been deleted successfully.")
    except FileNotFoundError:
        handle_error(f"File '{file_path}' not found.")
    except PermissionError:
        handle_error(f"I was denied Permission and I'm unable to delete the file.")
    except Exception as e:
        handle_error(f"An unexpected error occurred: {e}")
        say("Sorry Gold, an unexpected error occurred while deleting the file.")


def handle_error(error_message):
    say(f"Error: {error_message}")


def recognize_audio(r, audio):
    try:
        query = r.recognize_google(audio, language='en-US')
        print(f"User said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        handle_error("I could not understand you Gold. Please say it again")
        return ''
    except sr.RequestError as e:
        handle_error("I use the internet. Gold, you are not connected to the internet")
        return ''
    except Exception as e:
        handle_error(f"An unexpected error occurred: {e}")
        return ''


def delete_file(file_name):
    matching_files = find_matching_files(file_name.lower())
    if not matching_files:
        say("No file match found")
    else:
        say(f"{len(matching_files)} matches found")
        for index, file in enumerate(matching_files, start=1):
            say(f"{index}. {file}")

            try:
                selection = take_command().lower()
                index = int(selection)

                if 1 <= index <= len(matching_files):
                    file_to_delete = matching_files[index - 1]
                    if confirm_deletion(file_to_delete):
                        delete_specific_file(file_to_delete)
                        say("File deleted.")
                    else:
                        say("Deletion canceled.")
                else:
                    say("Invalid selection. Please select a file number I mentioned.")
            except ValueError:
                say("Invalid input. Please provide a valid file number.")
            except Exception as e:
                handle_error(f"An error occurred: {e}")
                say("Sorry, an unexpected error occurred.")



def check_for_audio(audio):
    r = sr.Recognizer()
    if not audio:
        handle_error("You have not said anything.")
        listen_for_commands(r)
    else:
        return audio


def take_confirmation_command():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=5)
        print("Listening for confirmation...")
        audio = r.listen(source)
    return audio    

#search for files matching filename gievn by user
def find_matching_files(file_name):
    current_directory = os.getcwd()
    matching_files = [file for file in os.listdir(current_directory)if file_name.lower() in file.lower() ]
    return matching_files

def


def delete_files_by_name(file_name):
    matching_files = find_matching_files(file_name.lower())
    if not matching_files:
        say("No file match found")
    else:
        say(f"{len(matching_files)} matches found")
        for index, file in enumerate(matching_files, start= 1):
            say(f"{index}. {file}")


            try:
                selection = take_command().lower()
                index = int(selection) 


                if 1 <= index <= len(matching_files):
                    file_to_delete = matching_files[index - 1]
                    if confirm_deletion(file_to_delete):
                        delete_specific_file(file_to_delete)
                        say("File deleted.")
                    else:
                        say("Deletion canceled.")
                else:
                    say("Invalid selection. Please select a file number I mentioned.")
            except Exception as e:
                say(f"Sorry, an error occurred.")

            except ValueError:
                say("Invalid input. Please provide a valid file number.")
            except Exception as e:
                handle_error(f"An error occurred: {e}")
                say("Sorry, an unexpected error occurred.")



def delete_specific_file(file_path):
    try:
        os.remove(file_path)
        say(f"Your file '{file_path}' has been deleted successfully.")
    except FileNotFoundError:
        handle_error(f"File '{file_path}' not found.")
    except PermissionError:
        handle_error(f"Permission denied. Unable to delete the file.")
    except Exception as e:
        handle_error(f"An unexpected error occurred: {e}")
        say("Sorry, an unexpected error occurred while deleting the file.")



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
    print(f"Query received: {query}")
    intent = parse_command(query)
    
    if intent == "delete_file":
        confirm_deletion(query)
        delete_files_by_name(query)
        return "delete_file"  # Reset intent after successful execution
        
    elif intent == "sleep" or intent == "sleep bestie":
        go_to_sleep()
        return "unknown_intent"  # Reset intent after successful execution

    elif intent == "list_files":
        list_files()
        return "list_files"  # Reset intent after successful execution

    else:
        return intent  # Return the original intent for further recognition attempts


# Add functionality to list files in directory
def list_files():
    files = os.listdir(os.getcwd())
    say("Here are the files in the current directory:")
    for file in files:
        say(file)


def confirm_deletion(file_to_delete, use_voice_confirmation=True):
    if use_voice_confirmation:
        say(f"Are you sure you want to delete the file {file_to_delete}? Say 'confirm' to proceed.")
        confirmation = take_confirmation_command()

        try:
            query = r.recognize_google(confirmation, language='en-US')
            if 'confirm' in query.lower() or 'yes' in query.lower():
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
    else:
        say(f"Are you sure you want to delete the file {file_to_delete}?")
        # Assuming the user has already given a command, wait for confirmation
        confirmation = take_confirmation_command()

        try:
            query = r.recognize_google(confirmation, language='en-US').lower()
            return 'confirm' in query or 'yes' in query
        except sr.UnknownValueError:
            handle_error("I could not understand your confirmation.")
        except sr.RequestError as e:
            handle_error("Error occurred during confirmation. Check your internet connection.")
        except Exception as e:
            handle_error(f"An unexpected error occurred during confirmation: {e}")

        return False


def main():
    while True:
        say("Gold, what do you want me to do for you?")
        time.sleep(1)
        query = take_command()

        if query:
            response = recognize_command(query)
            if response == "delete_file":
                time.sleep(1)
                say("Sure, let's proceed with deleting files.")
                delete_files_by_name(query)
            elif response == "unknown_intent":
                say("I'm sorry, I didn't understand that. Could you please rephrase?")
            elif response == "list_files":
                list_files()
            elif response == "go_to_sleep":
                say("Alright, deactivating. Have a great day!")
                go_to_sleep()
                break
            else:
                say("I'm not sure how to handle that. Can you please provide more details?")
        else:
            say("I didn't hear anything. Could you please repeat your command?")

if __name__ == "__main__":
    main()