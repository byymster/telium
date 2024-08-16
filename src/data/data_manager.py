import pickle

from ..services import AddressBook
from ..services import Notes


class DataManager:
    def __init__(self, dump_file):
        self.dump_file = dump_file

    def load_data(self):
        try:
            with open(self.dump_file, 'rb') as file:
                data = pickle.load(file)
                address_book = AddressBook(data.get('address_book', {}))
                notes = Notes(data.get('notes', {}))
                return address_book, notes
        except FileNotFoundError:
            print(
                f'No data file found at {self.dump_file}. Creating a new data structure.'
            )
            return AddressBook({}), Notes({})
    #     For development - when change files structure or rename files
        except ModuleNotFoundError:
            return AddressBook({}), Notes({})

    def save_data(self, address_book_data, notes_data):
        data = {'address_book': address_book_data, 'notes': notes_data}
        with open(self.dump_file, 'wb') as file:
            pickle.dump(data, file)
