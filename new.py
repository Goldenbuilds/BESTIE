import os
import speech_recognition as sr
import winsound
import pyttsx3
import time

class VoiceAssistant:
    def __init__(self):
        self.file_system = {}
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()

        # Define intent keywords for recognition
        self.intent_keywords = {
    "name_of_user": ["my name is", "I am", "call me", "people call me", "they call me", "I go by", "you can call me"],
    "delete_file": ["delete", "remove", "get rid of"],
    "unknown_intent": ["unknown", "not understood", "confused"],
    "go_to_sleep": ["sleep", "deactivate", "exit"],
}


    def welcome(self):
        self.say("Hello, I am Bestie!")

    def get_user_name(self):
        self.say("What is your name?")
        audio = self.listen()
        username = self.recognize(audio)

        if username:
            self.say(f"Welcome, {username}!")
            print(f"Welcome {username}")
            return username
        else:
            self.say("Sorry, I didn't quite get that")
            return ""

    def listen(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            self.play_sound(300, 500)
            audio = self.recognizer.listen(source, timeout=5)
        return audio

    def recognize(self, audio):
        try:
            text = self.recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return ""

    def say(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def play_sound(self, sound_freq, duration):
        winsound.Beep(sound_freq, duration)

    def delete(self, file_name):
        try:
            os.remove(file_name)
            self.say(f"{file_name} has been deleted successfully.")
        except FileNotFoundError:
            self.handle_error(f"File '{file_name}' not found.")
        except PermissionError:
            self.handle_error(f"Permission denied. Unable to delete the file.")
        except Exception as e:
            self.handle_error(f"An unexpected error occurred: {e}")
            self.say("An unexpected error occurred while deleting the file.")

    def handle_error(self, error_message):
        self.say(f"Error: {error_message}")

    def confirm_deletion(self, file_name):
        self.say(f"Are you sure you want to delete the file {file_name}? Say 'confirm' to proceed.")
        audio_confirmation = self.listen()
        confirmation = self.recognize(audio_confirmation)

        if 'confirm' in confirmation.lower() or 'yes' in confirmation.lower():
            self.say("Okay, proceeding with the deletion.")
            return True
        else:
            self.say("Deletion canceled.")
            return False

    def get_files_to_delete(self):
        self.say("Please specify the name of the file:")
        audio_filename = self.listen()
        filename = self.recognize(audio_filename)

        category = self.get_category_from_filename(filename)

        if category and filename and self.find_file(category, filename):
            return os.path.join(category, filename)
        else:
            print("File not found or category not recognized.")
            return ""

    def get_category_from_filename(self, filename):
        _, extension = os.path.splitext(filename)
        category = extension[1:] if extension else None

        if category and category in self.file_system:
            return category
        else:
            return None

    def find_file(self, category, filename):
        file_names = self.file_system.get(category, [])
        return filename in [os.path.basename(path) for path in file_names]

    def recognize_intent(self, query):
        query = query.lower()
        for intent, keywords in self.intent_keywords.items():
            if any(keyword in query for keyword in keywords):
                return intent
        return "unknown_intent"

    def main(self):
        self.welcome()
        username = self.get_user_name()

        if not username:
            return

        self.say(f"Hello, {username}! How can I assist you today?")

        while True:
            self.say("What do you want me to do for you?")
            time.sleep(1)
            query = self.listen()

            if query:
                try:
                    response = self.recognize(query)
                    intent = self.recognize_intent(response)

                    if intent == "delete_file":
                        self.say("Sure, let's proceed with deleting.")
                        file_to_delete = self.get_files_to_delete()
                        if file_to_delete and self.confirm_deletion(file_to_delete):
                            self.delete(file_to_delete)
                    elif intent == "unknown_intent":
                        self.say("I'm sorry, I didn't understand that. Could you please rephrase?")
                    elif intent == "go_to_sleep":
                        self.say("Alright, deactivating. Have a great day!")
                        break
                    else:
                        self.say("I'm not sure how to handle that. Can you please provide more details?")
                except Exception as e:
                    self.handle_error(f"An unexpected error occurred: {e}")
                    self.say("Sorry, an unexpected error occurred. Exiting.")
                    break
            else:
                self.say("I didn't hear anything. Could you please repeat your command?")


if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.main()