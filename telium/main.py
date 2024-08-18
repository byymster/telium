from os import makedirs
from pathlib import PurePath

from cryptography.fernet import InvalidToken
from platformdirs import user_data_dir
from prompt_toolkit import prompt
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import FuzzyCompleter
from prompt_toolkit.history import FileHistory

from telium.commands import CommandCompleter
from telium.commands import create_binding
from telium.commands import handle_command
from telium.data.data_manager import DataManager
from telium.utils import DUMP_FILE
from telium.utils import HISTORY_FILE
from telium.utils import logo
from telium.utils import parse_input

APP_NAME = 'Telium'


def main():
    # import pydevd_pycharm
    # pydevd_pycharm.settrace('localhost', port=8888, stdoutToServer=True, stderrToServer=True)

    print(logo)
    print('Welcome to the assistant bot!')
    user_data_directory = user_data_dir(APP_NAME, APP_NAME)
    makedirs(user_data_directory, exist_ok=True)
    file_path = PurePath(user_data_directory).joinpath(DUMP_FILE)
    decrypted = False
    while not decrypted:
        try:
            passphrase = prompt(
                'Please enter a passphrase: ', is_password=True)
            data_manager = DataManager(file_path, passphrase)
            contacts, notes = data_manager.load_data()
            decrypted = True
        except InvalidToken:
            print('Invalid passphrase. Please try again')
        except KeyboardInterrupt:
            print('\nGood bye!')
            return

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
        except EOFError:
            print('Good bye!')
            break

    data_manager.save_data(contacts.data, notes.data)


if __name__ == '__main__':
    main()
