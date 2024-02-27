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
import speech_recognition as sr 
import winsound 
import pyttsx3
import difflib

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
        image = Image.open(r"icons/mic.jpg")  #  path to microphone icon
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
        self.gui.update_text("Listening for 'Hey Bestie' ...")
        print("Listening for 'Hey Bestie' ...")

        r = sr.Recognizer()
        microphone = sr.Microphone()

        while True:
            with microphone as source:
                try:
                    audio = r.listen(source, timeout=5)
                    detected_phrase = r.recognize_google(audio, language='en-NG').lower()
                    self.say(f"Detected: {detected_phrase}")
                    print(f"Detected: {detected_phrase}")
                    self.gui.update_text(f"{detected_phrase}") #show text in textbox
                    
                    if "hey bestie" in detected_phrase:
                        self.say("Hey there! How can i help you? ")
                        self.activate_deletion()
                    
                    if "go to sleep" in detected_phrase:
                        self.sleep()

                except sr.WaitTimeoutError:
                    print("Timeout. No speech detected.")
                    self.gui.update_text("Timeout. No speech detected")
                except sr.UnknownValueError:
                    pass  # Ignore if the speech couldn't be recognized
                except sr.RequestError:
                    print("Failed to request results from Google Speech Recognition service.")
                    self.gui.update_text("Now listening for command to delete a file.")
    
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
                    self.say(f"Detected: {detected_phrase}")

                    if "go to sleep" in detected_phrase or "sleep" in detected_phrase:
                        self.sleep()
                        break #exit the loop after activating sleep mode

                    else:
                        print("Waiting for  command")
                        self.say("waiting for command")
                except sr.UnknownValueError:
                    pass  # Ignore if the speech couldn't be recognized
                except sr.RequestError:
                    print("Failed to request results from Google Speech Recognition service.")
    
    
    def activate_deletion(self):
        print("Now listening for command to delete a file.")
        self.gui.update_text("Say 'delete a file for me' ")  
        self.play_sound(500,600)

        r = sr.Recognizer()
        microphone = sr.Microphone()


        while True:
            with microphone as source:
                try:
                    audio = r.listen(source, timeout=5)
                    detected_phrase = r.recognize_google(audio, language= 'en-NG').lower()
                    print(f"Detected: {detected_phrase}")
                    self.gui.update_text(f"Detected: {detected_phrase}")

                    if "delete a file" in detected_phrase or "delete" in detected_phrase or "remove a file" in detected_phrase or "remove" in detected_phrase:
                        self.say("Okay I'll help you with file deletion")
                        self.delete()
                        break #exit the loop after command is processed
                    
                    if "go to sleep" in detected_phrase:
                        self.sleep()

                    else:
                        print("waiting for deletion command")
                        self.say("You need to tell me to delete a file for you")
                        
                except sr.RequestError:
                    print("Failed to request results. Don't worry it is a problem with Google API")
                except sr.UnknownValueError:
                    pass #ignore if the speech couldn't be recognized

    def delete(self):
        self.say("What file would you like to delete?")
        r = sr.Recognizer()
        microphone = sr.Microphone()


        while True:
            with microphone as source:
                try:
                    audio = r.listen(source, timeout= 5)
                    detected_phrase = r.recognize_google(audio, language= "en-NG").lower()
                    print(f"FILENAME DETECTED: {detected_phrase}")
                    self.say("What file would you like to delete?")
                    self.gui.update_text("What file would you like to delete?")

                    #Remove the file extension from the detected phrase
                    detected_phrase_no_extn, _= os.path.splitext(detected_phrase)

                    #Remove spaces and special characters from the detected phrase
                    detected_phrase_cleaned = ''.join(char for char in detected_phrase_no_extn if char.isalnum())
                    

                    #use difflib to find similar filenames
                    close_matches = difflib.get_close_matches(detected_phrase_cleaned, self.file_system)
                    # There are close matches  
                    if close_matches:
                        self.say(f"Did you mean {close_matches[0]}?")
                        users_reply = self.listen().lower()
                        print(f"User's reply: {users_reply}")

                        #confirm if close match is what the user wants
                        if "yes" in users_reply or "okay" in users_reply:
                            filename = close_matches[0]
                            self.confirm_deletion(filename)
                            return filename

                    else:
                        #Exact match is found
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
                            for file in os.listdir():
                                file_no_extn, _ = os.path.splitext(file) #file with no extension
                                file_no_extn_cleaned = ''.join(char for char in file_no_extn if char.isalnum())
                                if file_no_extn_cleaned == detected_phrase_no_extn:
                                    self.confirm_deletion(file)
                                    filename_found = file
                                    break

                            if filename_found:
                                self.confirm_deletion(filename_found)
                                return filename_found

                    
                            else:
                                self.gui.update_text(f"{filename} does not exist.")  # Update text box in GUI
                                print(f"{filename} does not exist.")
                                self.say("Sorry but the file you want deleted does not exist.")
                                return None
                                            
                        else:
                            self.gui.update_text("Please provide a valid filename.")  # Update text box in GUI
                            print("Please provide a valid filename.")
                            self.say("Please provide a valid filename.")

                    # break # Exit the loop after processing the deletion
                except FileNotFoundError:
                    self.gui.update_text(f"{filename} not found")
                    print(f"{filename} not found")
                    self.say(f"{filename} not found")

                except PermissionError:
                    self.gui.update_text("Permission denied  to delete this file ")
                    print(f"Error: Permission denied to delete file")
                    self.say("I do not have the permission to delete this file")
                
                except OSError as e:
                    print(f"Error: {e}.")

            return None
            

    def confirm_deletion(self, filename):
        while True:
            self.say(f"Are you sure you want to delete {filename}?")
            self.gui.update_text(f"Are you sure you want to delete {filename}?")  # Update text box in GUI
            print(f"Are you sure you want to delete {filename}?")

            confirm = self.listen_for_confirmation()
            if confirm:
                try:
                    os.remove(filename)
                    print(f"{filename} has been deleted successfully")
                    self.say("Your file has been deleted successfully")
                    self.gui.update_text(f"{filename} has been deleted successfully")  # Update text box in GUI

                except OSError as e:
                    print(f"Failed to delete{filename}: {e}")
                    self.say(f"Failed to delete{filename}: {e}")
                    self.gui.update_text(f"Failed to delete{filename}: {e}")
            else:
                print("Deletion cancelled")
                self.gui.update_text("Deletion cancelled")  # Update text box in GUI
                self.say("Deletion cancelled")
                break # Exit the loop if deletion is cancelled

            # Ask if user wants to delete another file
            self.say("Do you want to delete another file?")
            self.gui.update_text("Do you want to delete another file?")
            print("Do you want to delete another file?")

            confirm_another = self.listen_for_confirmation()
            if confirm_another:
                try:
                    os.remove(filename)
                    print(f"{filename} has been deleted successfully")
                    self.say("Your file has been deleted successfully")
                    self.gui.update_text(f"{filename} has been deleted successfully")  # Update text box in GUI

                except OSError as e:
                    print(f"Failed to delete{filename}: {e}")
                    self.say(f"Failed to delete{filename}: {e}")
                    self.gui.update_text(f"Failed to delete{filename}: {e}")
            else:
                print("Deletion cancelled")
                self.gui.update_text("Deletion cancelled")  # Update text box in GUI
                self.say("Deletion cancelled")
                break # Exit the loop if deletion is cancelled
            
            if not confirm_another:
                break #EXit the loop if user does not want another file deleted
            
            break  # This break will exit the confirm_deletion function after completing the loop

                

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

                    if "yes" in detected_phrase:
                        return True
                    elif "no" in detected_phrase:
                        return False
                    else:
                        print("Please respond with yes or no")
                        self.say("Please respond with yes or no")
                        self.gui.update_text("Please respond with a yes or no")
                except sr.RequestError:
                    print("Failed to request results. It seems there is an issue with Google API")
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