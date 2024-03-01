import sys
import os
import re
import threading
import tkinter as ttk
import tkinter as tk
from PIL import Image, ImageTk
import speech_recognition as sr
import requests
import os
import winsound 
import pyttsx3
import difflib
import shutil

# # https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
# def resource_path(relative_path):
#     """ Get absolute path to resource, works for dev and for PyInstaller """
#     try:
#         # PyInstaller creates a temp folder and stores path in _MEIPASS
#         base_path = sys._MEIPASS2
#     except Exception:
#         base_path = os.path.abspath(".")

#     return os.path.join(base_path, relative_path)

# Logo = resource_path("Logo.png")


# GUI CODE FOR BESTIE
class VoiceAssistantGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("B. E. S. T. I. E.")
        self.root.configure(bg="#f0f0f0") #background colour for root GUI WINDOW
        
        self.assistant = VoiceAssistant(self) #instance of voice assistant
        self.create_widgets() 

    def create_widgets(self): #ATTRIBUTES OF THE TEXTBOX LAYER, INCLUDING LISTENING AND EXIT SYMBOLS
        # Configure color scheme
        bg_color = "#f0f0f0"
        text_color = "#292929"
        button_color = "#007EA7"
        button_hover_color = "#00A8E8"

        # Header label
        header_label = ttk.Label(self.root, text="B. E. S. T. I. E.", font=("Helvetica", 24), background=bg_color, foreground=button_color)
        header_label.pack(pady=20)
        # Text box for displaying recognized text
        self.text_box = tk.Text(self.root, height=10, width=50, font=("Arial", 12), bd=2, relief=tk.SOLID, bg=bg_color)
        self.text_box.pack(padx=10, pady=10)

        # Feedback label
        self.feedback_label = tk.Label(self.root, text="", font=("Arial", 12), bg=bg_color, fg=text_color)
        self.feedback_label.pack(pady=5)

        # Instructions label
        instructions_text = "Instructions:\n1. Click 'Start Listening' to begin.\n2. Speak clearly into the microphone and activate with 'hey bestie' or deactivate with 'go to sleep'.\n3. Wait for recognition results."
        self.instructions_label = tk.Label(self.root, text=instructions_text, font=("Arial", 10), bg=bg_color, fg=text_color)
        self.instructions_label.pack(pady=5)

        # Frame for holding the microphone icon and button
        button_frame = tk.Frame(self.root, bg=bg_color)
        button_frame.pack(pady=5)

        # Microphone icon
        image = Image.open(r"icon.ico")  #  path to microphone icon
        image = image.resize((50, 50), Image.LANCZOS)
        microphone_icon = ImageTk.PhotoImage(image)
        self.microphone_label = tk.Label(button_frame, image=microphone_icon, bg=bg_color)
        self.microphone_label.image = microphone_icon
        self.microphone_label.pack(side=tk.LEFT, padx=5)

        # Button to start listening
        self.start_button = tk.Button(button_frame, text="Start Listening", command=self.start_listening,
                                    bg=button_color, fg="white", padx=10, pady=5,
                                    activebackground=button_hover_color)
        self.start_button.pack(pady=5)

        # Button to exit the application
        self.exit_button = tk.Button(self.root, text="Exit", command=self.root.destroy,
                                    bg="red", fg="white", padx=10, pady=5,
                                    activebackground="#d32f2f")
        self.exit_button.pack(pady=5)


    def start_listening(self):
        self.start_button.config(state=tk.DISABLED)
        threading.Thread(target=self.assistant.activate_assistant).start() #Start listening in a seperate thread
        #Reset the state of the Start Listening button
        self.start_button.config(state=tk.NORMAL) # Make the button clickable again    
   
    def run(self): #keeps GUI application running
        self.root.mainloop()

    def update_text(self, text):
        self.text_box.insert(tk.END, text + "\n")
        self.text_box.see(tk.END)

 

class VoiceAssistant:
    def __init__(self, gui):
        self.file_system = [] #keeps track of filenames present in  cwd
        self.gui = gui
    
    def listen(self):  
        recognizer = sr.Recognizer() 
        with sr.Microphone() as source: #captures audio from mic
            recognizer.adjust_for_ambient_noise(source, duration= 1)
            self.play_sound(300,500)
            audio = recognizer.listen(source) #listens to the audio input from the mic and stores it in the audio variable

        return audio 

    def recognize(self, audio):
        recognizer = sr.Recognizer()

        try:
            text = recognizer.recognize_google(audio)
            print("Recognized Text:", text)  # Added this line for debugging
            return text
            
        except sr.UnknownValueError:
            return ""
        
    
    def say(self,text): 
        engine = pyttsx3.init(driverName='sapi5')
        engine.say(text)
        engine.runAndWait()

    def play_sound(self,sound_freq, duration): 
        winsound.Beep(sound_freq, duration)

    def activate_assistant(self):
        self.play_sound(500,600)
        self.gui.update_text("Listening for 'Hey Bestie' ...")

        print("Listening for 'Hey Bestie' ...")

        r = sr.Recognizer()
        microphone = sr.Microphone()

        while True:
            with microphone as source:
                try:
                    audio = r.listen(source, timeout=5) # listen to commands

                    detected_phrase = r.recognize_google(audio, language='en-NG').lower() #words extracted from user

                    #feedback mechanisms
                    self.say(f"Detected: {detected_phrase}")
                    self.gui.update_text(f"Detected: {detected_phrase}")
                    print(f"Detected: {detected_phrase}")


                    #activation mechanisms for various cases/scenarious
                    if "hey bestie" in detected_phrase: #user say hey bestie
                        self.say("Hey there! I am Bestie your file deletion buddy ")
                        self.activate_deletion()
                    
                    if "go to sleep" in detected_phrase: #user wants to end task 
                        self.sleep()

                    if "delete" in detected_phrase: #user needs to delete a file
                        self.activate_deletion()

                    else:
                        self.say("You need to give me a command. So that i can do my job")
                        self.gui.update_text(f"Wake command not recognized")


                # Exceptions for programs not to run with feedback to user 
                except sr.WaitTimeoutError: # for no speech detection
                    print("Timeout. No speech detected.")
                    self.say("Say something")
                    self.gui.update_text("Timeout. No speech detected")

                except sr.UnknownValueError:
                    pass  # Ignore if no speech recognized

                except sr.RequestError:
                    print("Failed to request results from Google Speech Recognition service.")
                    self.gui.update_text("Failed to request results from Google Speech Recognition service. Check your internet connection")
    
    def activate_sleepmode(self):
        self.gui.update_text("Sleep mode activated ...")
        self.say("sleep mode activated")
        print("Sleep mode activated ...")

        r = sr.Recognizer()
        microphone = sr.Microphone()

        while True:
            with microphone as source:
                try:
                    audio = r.listen(source, timeout=5)
                    detected_phrase = r.recognize_google(audio, language='en-NG').lower()
                    print(f"Detected: {detected_phrase}")
                    self.gui.update_text(f"Detected: {detected_phrase}")
                    self.say(f"Detected: {detected_phrase}")

                    if "go to sleep" in detected_phrase or "sleep" in detected_phrase:
                        self.sleep()
                        break # exit loop 
                    else: 
                        print("Waiting for  command")
                        self.say("waiting for command")
                except sr.UnknownValueError:
                    pass  # Ignore if the speech couldn't be recognized
                except sr.RequestError:
                    print("Failed to request results from Google Speech Recognition service.")
    

    def activate_deletion(self):
        self.gui.update_text("Deletion mode activated")  
        self.play_sound(500,600)
        self.delete_file()

       

    def delete_file(self):
        r = sr.Recognizer()
        microphone = sr.Microphone()
        self.say("What file would you like to delete?")
        self.gui.update_text("What file would you like to delete?")


        while True:
            with microphone as source:
                try:
                    audio = r.listen(source, timeout= 5)
                    detected_phrase = r.recognize_google(audio, language= "en-NG").lower()
                    print(f"FILENAME DETECTED: {detected_phrase}")
                    self.gui.update_text(f"FILENAME DETECTED: {detected_phrase}")
                    
                    #Remove  file extension from  detected phrase
                    detected_phrase_no_extn, _= os.path.splitext(detected_phrase)

                    #Remove space and special characters from the detected phrase
                    detected_phrase_cleaned = ''.join(char for char in detected_phrase_no_extn if char.isalnum())
                
                    #use difflib to find files with similar names with detected phrase
                    close_matches = difflib.get_close_matches(detected_phrase_cleaned, self.file_system)

                    # if there are close matches  
                    if close_matches:
                        self.say(f"Did you mean {close_matches[0]}?") #ask if user means to delete the close match
                        users_reply = self.listen().lower() #store user's reply
                        self.gui.update_text(f" You replied: {users_reply}")

                        #confirm if close match is what the user wants
                        if "yes" in users_reply or "okay" in users_reply or "yh " in users_reply:
                            filename = close_matches[0] #filename is now the match chosen by user
                            self.confirm_file_deletion(filename) #confirm deletion of the file
                            return filename

                    else:
                        # if Exact match is found
                        match = re.search(r'delete\s*(.*)', detected_phrase)
                        
                        if match:
                            filename = match.group(1).strip() #filename gotten from match
                            print(f"{filename}")

                            # Remove spaces and special characters from the file
                            filename_cleaned = ''.join(char for char in filename if char.isalnum())
                            #Remove the file extension from the filename
                            detected_phrase_no_extn, _= os.path.splitext(filename_cleaned)

                            filename_found = None

                            #search for matches without considering the extension
                            for root, _, files in os.walk(os.getcwd()):  # using current working directory
                                for file in files:
                                    file_no_extn, _ = os.path.splitext(file)  # file with no extension
                                    file_no_extn_cleaned = ''.join(char for char in file_no_extn if char.isalnum())
                                    if file_no_extn_cleaned == detected_phrase_no_extn:
                                        file_path = os.path.join(root, file)
                                        self.confirm_file_deletion(file_path)
                                        filename_found = file
                                        break

                            if filename_found:
                                self.confirm_file_deletion(filename_found)
                                return filename_found

                    
                            else:                                
                                self.gui.update_text(f"{filename} does not exist.")  # Update text box in GUI
                                print(f"{filename} does not exist.")
                                self.say("Sorry but the file you want deleted does not exist.")
                                self.play_sound(500,600)
                                continue # go back to asking user what file they want to delete
                                

                        else:
                            self.gui.update_text("Please provide a valid filename.")  # Update text box in GUI
                            print("Please provide a valid filename.")
                            self.say("Please provide a valid filename.")
                            self.play_sound(500,600)
                            continue # Continue the loop to re-ask for file deletion

                    break # Exit the loop after processing the deletion
                except FileNotFoundError:
                    self.gui.update_text(f"{filename} not found")
                    print(f"{filename} not found")
                    self.say(f"{filename} not found")
                    self.play_sound(500,600)
                    continue # Continue the loop to re-ask for file deletion

                except PermissionError:
                    self.gui.update_text("Permission denied  to delete this file ")
                    print(f"Error: Permission denied to delete file")
                    self.say("Permission denied to delete this file. Run this program as an Administrator.")
                    self.play_sound(500,600)
                    continue # Continue the loop to re-ask for file deletion

                except OSError as e:
                    self.gui.update_text(f"Error: {e}")
                    print(f"Error: {e}.")
                    continue # Continue the loop to re-ask for file deletion
                
        return None
            


    def confirm_file_deletion(self, filename):
        while True:
            filename_only = os.path.basename(filename) #extract filename from the path
            self.say(f"Are you sure you want to delete the file?{filename_only}")
            self.gui.update_text(f"Are you sure you want to delete {filename_only}?")  # Update text box in GUI
            print(f"Are you sure you want to delete {filename_only}?")

            confirm = self.listen_for_confirmation()
            if confirm:
                try:
                    os.remove(filename)
                    print(f"{filename_only} has been deleted successfully")
                    self.say(f"{filename_only} has been deleted successfully")
                    self.gui.update_text(f"{filename_only} has been deleted successfully")  # Update text box in GUI

                except OSError as e:
                    print(f"Failed to delete{filename_only}: {e}")
                    self.say(f"Failed to delete{filename_only}: {e}")
                    self.gui.update_text(f"Failed to delete{filename_only}: {e}")
                    self.delete_file()
            else:
                print("Deletion cancelled")
                self.gui.update_text("Deletion cancelled")  # Update text box in GUI
                self.say("Deletion cancelled")
                break # Exit the loop if deletion is cancelled

            # Ask if user wants to delete another file
            self.say("Do you want to delete another file?")
            self.gui.update_text("Do you want to delete another file?")
            print("Do you want to delete another file?")

            user_reply2 = self.listen_for_confirmation()
            if user_reply2:
                self.say("Okay sure")
                self.delete_file()

            else:
                self.say("If there is nothing more for me to do for you i'll be going off now")
                self.sleep()
                break



            
        # Exit the confirm_deletion function after completing the loop
        return
                

    def listen_for_confirmation(self):
        r = sr.Recognizer()
        microphone = sr.Microphone()

        while True:
            with microphone as source:
                try:
                    audio = r.listen(source, timeout=5)
                    detected_phrase = r.recognize_google(audio, language='en-NG').lower()
                    print(f"Detected: {detected_phrase}")
                    self.gui.update_text(f"Detected: {detected_phrase}")  # Update text box in GUI

                    # Check for exact match of "yes" or "no"
                    if "yes" in detected_phrase:
                        return True
                    if "no" in detected_phrase:
                        print("no works")
                        return False
                    else:
                        # Check for similar-sounding words to "no"
                        similar_words = ["know", "now", "neon", "kno", "nope"]
                        for word in similar_words:
                            if word in detected_phrase:
                                return False

                        print("Please respond with yes or no")
                        self.say("Please respond with yes or no")
                        self.gui.update_text("Please respond with yes or no")

                except sr.RequestError:
                    print("Failed to request results. It seems there is an issue with Google API")
                    self.gui.update_text("Failed to request results. It seems there is an issue with Google API")

                except sr.UnknownValueError:
                    print("Sorry, I couldn't understand your response. Please try again.")
                    self.say("Sorry, I couldn't understand your response. Please try again.")
                    self.gui.update_text("Sorry, I couldn't understand your response. Please try again.")

                except sr.WaitTimeoutError:
                    print("Timeout. No response detected.")
                    self.say("No response detected. Please try again.")
                    self.gui.update_text("No response detected. Please try again.")


    def sleep(self):
        self.gui.update_text("Bestie is deactivating...")  # Update text box in GUI

        print("Bestie is deactivating...")
        self.say("Deactivating bestie. Call me once you need me")
        sys.exit(0)

        
    def task_to_be_done(self):
        self.say("What can I do for you today?")
        self.gui.update_text("What can I do for you today")

    
    def main(self):
        while True:
            self.activate_assistant()

# if __name__ == "__main__":
#     assistant = VoiceAssistant()
#     assistant.main()




    
    
if __name__ == "__main__":
    app = VoiceAssistantGUI()
    app.run()