import base64
import os
import pickle

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from ..services import AddressBook
from ..services import Notes


class DataManager:
    def __init__(self, dump_file, passphrase):
        self.dump_file = dump_file
        self.passphrase = passphrase
        self.salt = os.urandom(16)
        self.key = self.derive_key_from_passphrase(passphrase, self.salt)

    @staticmethod
    def derive_key_from_passphrase(passphrase: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return base64.urlsafe_b64encode(kdf.derive(passphrase.encode()))

    def load_data(self):
        try:
            with open(self.dump_file, 'rb') as file:
                data = file.read()
            salt = data[:16]
            encrypted_data = data[16:]
            key = self.derive_key_from_passphrase(self.passphrase, salt)
            decrypted_data = Fernet(key).decrypt(encrypted_data)
            data = pickle.loads(decrypted_data)
            address_book = AddressBook(data.get('address_book', {}))
            notes = Notes(data.get('notes', {}))
            return address_book, notes
        except FileNotFoundError:
            print(
                f'No data file found at {self.dump_file}. Creating a new data structure.'
            )
            return AddressBook({}), Notes({})
        except ModuleNotFoundError:
            return AddressBook({}), Notes({})

    def save_data(self, address_book_data, notes_data):
        data = {'address_book': address_book_data, 'notes': notes_data}
        pickled_data = pickle.dumps(data)
        encrypted_data = Fernet(self.key).encrypt(pickled_data)
        with open(self.dump_file, 'wb') as file:
            file.write(self.salt + encrypted_data)
