from filedeletionassistant import listen, recognize_audio
from delete_logic import delete_files_by_name, go_to_sleep, recognize_command


def main():
    while True:
        query = listen()
        recognize_command(query)


if __name__ == "__main__":
    main()
