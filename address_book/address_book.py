from collections import UserDict
from .record import Record
from .decorators import input_error
from .utils import DUMP_FILE
import pickle
from datetime import datetime, timedelta

class AddressBook(UserDict):
    @input_error
    def add_record(self, args):
        record = Record(args[0])
        record.add_phone(args[1])
        self.data[record.name.value] = record
        return f"Contact {record.name.value} was added."

    def find(self, name):
        return self.data.get(name, "Contact not found")

    def delete(self, name):
        del self.data[name]

    def get_upcoming_birthdays(self) -> list[dict[str, str]]:
        upcoming_birthdays = []
        today = datetime.now()
        for user in self.data.values():
            birthday_this_year = datetime.strptime(
                f'{today.year}.{user.birthday.value.month}.{user.birthday.value.day}', "%Y.%m.%d")
            difference = (birthday_this_year - today).days

            if 0 <= difference <= 7:
                if birthday_this_year.weekday() >= 5:
                    birthday_this_year += timedelta(days=(7 - birthday_this_year.weekday()))
                upcoming_birthdays.append({
                    'name': user.name.value,
                    'congratulation_date': birthday_this_year.strftime('%Y.%m.%d')
                })

        return upcoming_birthdays

    @input_error
    def change_record(self, args):
        name, old_phone, new_phone = args
        record = self.find(name)
        if isinstance(record, Record):
            record.edit_phone(old_phone, new_phone)
            return f"Phone number {old_phone} was changed to {new_phone} for contact {name}."
        else:
            return record

    def all(self):
        return "\n".join([str(data) for data in self.data.values()])

    @input_error
    def add_birthday(self, args):
        name, birthday = args
        record = self.find(name)
        if not isinstance(record, Record):
            return record
        record.add_birthday(birthday)
        return f"Birthday {birthday} was added to contact {name}."

    @input_error
    def show_birthday(self, args):
        name = args[0]
        record = self.find(name)
        return record.birthday

    @input_error
    def birthdays(self):
        upcoming_birthdays = self.get_upcoming_birthdays()
        if not upcoming_birthdays:
            return "No upcoming birthdays."
        return "\n".join([f"{data['name']} - {data['congratulation_date']}" for data in upcoming_birthdays])

    @input_error
    def add_email(self, args):
        name, email = args
        record = self.find(name)
        if not isinstance(record, Record):
            return record
        record.add_email(email)
        return f"Email {email} was added to contact {name}."

    def load(self):
        try:
            with open(DUMP_FILE, "rb") as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            print("No data file found. Creating a new data structure.")

    def save(self):
        with open(DUMP_FILE, "wb") as file:
            pickle.dump(self.data, file)