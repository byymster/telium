from ..dtos.address import Address
from ..dtos.birthday import Birthday
from ..dtos.email import Email
from ..dtos.name import Name
from ..dtos.phone import Phone
from ..utils import Printable
from ..utils import RichPrintable


class Record(Printable, RichPrintable):
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = []
        self.address = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                break

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p.value

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                break

    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

    def add_email(self, email):
        self.email.append(Email(email))

    def add_address(self, address):
        self.address.append(Address(address))

    def change_name(self, new_name):
        self.name = new_name

    def change_phone(self, index, new_phone):
        if 0 <= index < len(self.phones):
            self.phones[index] = new_phone
        else:
            raise IndexError('Invalid phone index.')

    def change_email(self, index, new_email):
        if 0 <= index < len(self.email):
            self.email[index] = new_email
        else:
            raise IndexError('Invalid email index.')

    def change_address(self, index, new_address):
        if 0 <= index < len(self.address):
            self.address[index] = new_address
        else:
            raise IndexError('Invalid address index.')

    def __str__(self):
        birthday_data = f', birthday: {self.birthday}' if self.birthday else ''
        email_data = (
            f", email: {', '.join(p.value for p in self.email)}" if self.email else ''
        )
        address_data = (
            f", address: {', '.join(p.value for p in self.address)}"
            if self.address
            else ''
        )
        return (
            f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
            f'{birthday_data}{email_data}{address_data}'
        )

    def __rich__(self, table, bg_color=None):
        table.add_row(
            str(self.name),
            str(self.birthday) if self.birthday else '',
            ', '.join(str(phone)
                      for phone in self.phones) if self.phones else '',
            ', '.join(str(email)
                      for email in self.email) if self.email else '',
            ', '.join(str(address)
                      for address in self.address) if self.address else '',
            style=f'on {bg_color}' if bg_color else None
        )


DATA_TYPES = [
    ('phone', Record.add_phone),
    ('email', Record.add_email),
    ('address', Record.add_address)
]
