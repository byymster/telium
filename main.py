from os import makedirs
from pathlib import PurePath

from platformdirs import user_data_dir
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import FuzzyCompleter
from prompt_toolkit.history import FileHistory

from src.commands import CommandCompleter
from src.commands import create_binding
from src.commands import handle_command
from src.data.data_manager import DataManager
from src.utils import DUMP_FILE
from src.utils import HISTORY_FILE
from src.utils import parse_input

APP_NAME = 'Telium'


def main():
    user_data_directory = user_data_dir(APP_NAME, APP_NAME)
    makedirs(user_data_directory, exist_ok=True)
    file_path = PurePath(user_data_directory).joinpath(DUMP_FILE)
    data_manager = DataManager(file_path)
    contacts, notes = data_manager.load_data()
    print('Welcome to the assistant bot!')

    command_completer = CommandCompleter(contacts, notes)
    fuzzy_completer = FuzzyCompleter(command_completer, enable_fuzzy=True)
    non_fuzzy_completer = FuzzyCompleter(command_completer, enable_fuzzy=False)
    session = PromptSession(
        completer=fuzzy_completer,
        history=FileHistory(
            PurePath(user_data_directory).joinpath(HISTORY_FILE))
    )

    while True:
        try:
            user_input = session.prompt('Enter a command: ',
                                        key_bindings=create_binding(fuzzy_completer, non_fuzzy_completer))
            command, *args = parse_input(user_input)

            if not handle_command(command, contacts, notes, *args):
                break
        except ValueError as e:
            print(e)
        except KeyboardInterrupt:
            print('\nGood bye!')
            break

    data_manager.save_data(contacts.data, notes.data)


if __name__ == '__main__':
    main()
