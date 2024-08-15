from os import makedirs
from pathlib import PurePath

from platformdirs import user_data_dir
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import FuzzyCompleter
from prompt_toolkit.history import FileHistory

from src.commands import address_book
from src.commands import notes
from src.commands import root
from src.commands.completer import CommandCompleter
from src.commands.handle import handle_command
from src.data_manager import DataManager
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

    session = PromptSession(
        completer=FuzzyCompleter(CommandCompleter()),
        history=FileHistory(
            PurePath(user_data_directory).joinpath(HISTORY_FILE))
    )
    while True:
        try:
            user_input = session.prompt('Enter a command: ')
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

# Fix for Flake8 F401 unused import
c = {address_book, notes, root}
