import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import threading
import speech_recognition as sr 
import winsound 
import pyttsx3
import os
import re

class VoiceAssistantGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simple Voice Assistant")
        self.root.configure(bg="#292929")  # Set darker background color
        
        self.assistant = VoiceAssistant(self)  # Pass a reference to the GUI class to the VoiceAssistant

        self.create_widgets()

    def create_widgets(self):
        bg_color = "#292929"
        text_color = "white"
        button_color = "#4CAF50"
        button_hover_color = "#45a049"

        # Text box for displaying recognized text
        self.text_box = tk.Text(self.root, height=10, width=50, font=("Arial", 12), bd=2, relief=tk.SOLID, fg=text_color, bg=bg_color)
        self.text_box.pack(padx=10, pady=10)

        # Start Listening Button
        self.start_button = tk.Button(self.root, text="Start Listening", command=self.start_listening,
                                      bg=button_color, fg="white", padx=10, pady=5,
                                      activebackground=button_hover_color)
        self.start_button.pack(pady=5)

        # Exit Button
        self.exit_button = tk.Button(self.root, text="Exit", command=self.root.destroy,
                                     bg="red", fg="white", padx=10, pady=5,
                                     activebackground="#d32f2f")
        self.exit_button.pack(pady=5)

    def start_listening(self):
        self.start_button.config(state=tk.DISABLED)
        threading.Thread(target=self.assistant.activate_assistant).start()  # Start listening in a separate thread

    def update_text(self, text): #display text on textbox
        self.text_box.insert(tk.END, text + '\n')
        self.text_box.see(tk.END)

    def run(self):#start gui
        self.root.mainloop()

class VoiceAssistant:
    def __init__(self, gui):
        self.file_system = []
        self.gui = gui  # Reference to the GUI class

    def activate_assistant(self):
        self.gui.update_text("Listening for 'Hey Bestie' ...")  # Update text box in GUI
        print("Listening for 'Hey Bestie' ...")

        r = sr.Recognizer()
        microphone = sr.Microphone()

        with microphone as source:
            try:
                while True:
                    audio = r.listen(source, timeout=5)
                    detected_phrase = r.recognize_google(audio, language='en-US').lower()
                    self.gui.update_text(f"Detected: {detected_phrase}")  # Update text box in GUI
                    print(f"Detected: {detected_phrase}")

                    if "hey bestie" in detected_phrase:
                        self.say("Hey there! How can I help you?")
                        self.activate_deletion()

                    if "go to sleep" in detected_phrase:
                        self.sleep()
            except sr.WaitTimeoutError:
                self.gui.update_text("Timeout. No speech detected.")
                print("Timeout. No speech detected.")

    def activate_deletion(self):
        self.say("Now listening for command to delete a file.")
        self.gui.update_text("Now listening for command to delete a file.")
        print("Now listening for command to delete a file.")

        r = sr.Recognizer()
        microphone = sr.Microphone()

        with microphone as source:
            try:
                while True:
                    audio = r.listen(source, timeout=5)
                    detected_phrase = r.recognize_google(audio, language='en-NG').lower()
                    self.gui.update_text(f"Detected: {detected_phrase}")  # Update text box in GUI
                    print(f"Detected: {detected_phrase}")

                    if any(keyword in detected_phrase for keyword in ["delete a file", "delete", "remove a file", "remove"]):
                        self.say("Okay, I'll help you with file deletion")
                        self.delete()
                        break

                    if "go to sleep" in detected_phrase:
                        self.sleep()
            except sr.WaitTimeoutError:
                self.gui.update_text("Timeout. No speech detected.")
                print("Timeout. No speech detected.")

    def delete(self):
        self.say("What file would you like to delete?")
        self.gui.update_text("What file would you like to delete?")
        print("What file would you like to delete?")

        r = sr.Recognizer()
        microphone = sr.Microphone()

        with microphone as source:
            try:
                while True:
                    audio = r.listen(source, timeout=5)
                    detected_phrase = r.recognize_google(audio, language="en-US").lower()
                    self.gui.update_text(f"Detected: {detected_phrase}")  # Update text box in GUI
                    print(f"Detected: {detected_phrase}")

                    match = re.search(r'delete\s*(\w+\s*\w*)', detected_phrase)

                    if match:
                        filename = match.group(1).strip()
                        self.gui.update_text(f"Filename: {filename}")  # Update text box in GUI
                        print(f"Filename: {filename}")

                        if os.path.exists(filename):
                            self.confirm_deletion(filename)
                        else:
                            self.gui.update_text(f"{filename} does not exist.")  # Update text box in GUI
                            print(f"{filename} does not exist.")
                            self.say(f"Sorry, but the file {filename} does not exist.")
                        break
                    else:
                        self.gui.update_text("Please provide a valid filename.")  # Update text box in GUI
                        print("Please provide a valid filename.")
            except sr.WaitTimeoutError:
                self.gui.update_text("Timeout. No speech detected.")
                print("Timeout. No speech detected.")

    def confirm_deletion(self, filename):
        self.say(f"Are you sure you want to delete {filename}?")
        self.gui.update_text(f"Are you sure you want to delete {filename}?")  # Update text box in GUI
        print(f"Are you sure you want to delete {filename}?")

        r = sr.Recognizer()
        microphone = sr.Microphone()

        with microphone as source:
            try:
                while True:
                    audio = r.listen(source, timeout=5)
                    detected_phrase = r.recognize_google(audio, language='en-US').lower()
                    self.gui.update_text(f"Detected: {detected_phrase}")  # Update text box in GUI
                    print(f"Detected: {detected_phrase}")

                    if "yes" in detected_phrase:
                        try:
                            os.remove(filename)
                            self.gui.update_text(f"{filename} has been deleted successfully")  # Update text box in GUI
                            print(f"{filename} has been deleted successfully")
                            self.say(f"Your file {filename} has been deleted successfully")
                        except OSError as e:
                            print(f"Error: {e}.")
                            self.gui.update_text("An error occurred while deleting the file.")  # Update text box in GUI
                            self.say("An error occurred while deleting the file.")
                        break
                    elif "no" in detected_phrase:
                        self.gui.update_text("Deletion cancelled")  # Update text box in GUI
                        print("Deletion cancelled")
                        self.say("Deletion cancelled")
                        break
                    else:
                        self.gui.update_text("Please respond with yes or no")  # Update text box in GUI
                        print("Please respond with yes or no")
            except sr.WaitTimeoutError:
                self.gui.update_text("Timeout. No speech detected.")
                print("Timeout. No speech detected.")

    def say(self, text): 
        engine = pyttsx3.init(driverName='sapi5')
        engine.say(text)
        engine.runAndWait()

    def sleep(self):
        self.gui.update_text("Bestie is deactivating...")  # Update text box in GUI
        print("Bestie is deactivating...")
        self.say("Deactivating bestie. Call me once you need me")
        exit(0)

if __name__ == "__main__":
    app = VoiceAssistantGUI()
    app.run()
