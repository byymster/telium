from collections import UserDict
from datetime import datetime
from datetime import timedelta

from .decorators import input_error
from .record import DATA_TYPES
from .record import Record


class AddressBook(UserDict):
    @input_error()
    def add_record(self, args):
        name, *phones = args
        record = self.find(name)
        if not isinstance(record, Record):
            record = Record(name)
            self.data[record.name.value] = record

        for phone in phones:
            record.add_phone(phone)

        return f'Contact {record.name.value} was added.'

    @input_error()
    def add_record_interactive(self, name):
        record = self.find(name)
        if not isinstance(record, Record):
            record = Record(name)
            self.data[record.name.value] = record
        should_exit = False

        while should_exit is False:
            birthday_data = yield
            if birthday_data:
                try:
                    record.add_birthday(birthday_data)
                    should_exit = yield True
                except ValueError as e:
                    yield e
                    continue

            else:
                should_exit = yield False

        for data_type, add_method in DATA_TYPES:
            while True:
                add_data = yield
                if add_data:
                    data = yield
                    try:
                        add_method(record, data)
                    except ValueError as e:
                        yield e
                        continue
                else:
                    break

        yield True
        return True

    def find(self, name):
        return self.data.get(name, 'Contact not found')

    def delete(self, name):
        del self.data[name]

    def get_upcoming_birthdays(self, days: int) -> list[dict[str, str]]:
        upcoming_birthdays = []
        today = datetime.now()
        for user in self.data.values():
            if user.birthday and user.birthday.value:
                birthday_this_year = datetime.strptime(
                    f'{user.birthday.value.day}.{user.birthday.value.month}.{today.year}',
                    '%d.%m.%Y',
                )
                difference = (birthday_this_year - today).days

                if 0 <= difference <= days:
                    if birthday_this_year.weekday() >= 5:
                        birthday_this_year += timedelta(
                            days=(7 - birthday_this_year.weekday())
                        )
                    upcoming_birthdays.append(
                        {
                            'name': user.name.value,
                            'congratulation_date': birthday_this_year.strftime(
                                '%d.%m.%Y'
                            ),
                        }
                    )
        return upcoming_birthdays

    @input_error()
    def change_record(self, args):
        name, old_phone, new_phone = args
        record = self.find(name)
        if isinstance(record, Record):
            record.edit_phone(old_phone, new_phone)
            return f'Phone number {old_phone} was changed to {new_phone} for contact {name}.'
        else:
            return record

    def all(self):
        return '\n'.join([str(data) for data in self.data.values()])

    @input_error()
    def add_birthday(self, args):
        name, birthday = args
        record = self.find(name)
        if not isinstance(record, Record):
            return record
        record.add_birthday(birthday)
        return f'Birthday {birthday} was added to contact {name}.'

    @input_error()
    def show_birthday(self, args):
        name = args[0]
        record = self.find(name)
        return record.birthday.value.strftime('%d.%m.%Y')

    @input_error()
    def birthdays(self, args):
        upcoming_birthdays = self.get_upcoming_birthdays(args)
        if not upcoming_birthdays:
            return 'No upcoming birthdays.'
        return '\n'.join(
            [
                f"{data['name']} - {data['congratulation_date']}"
                for data in upcoming_birthdays
            ]
        )

    @input_error()
    def add_email(self, args):
        name, email = args
        record = self.find(name)
        if not isinstance(record, Record):
            return record
        record.add_email(email)
        return f'Email {email} was added to contact {name}.'

    @input_error()
    def add_address(self, args):
        name = args[0]
        address = ' '.join(args[1:])
        record = self.find(name)
        if not isinstance(record, Record):
            return record

        record.add_address(address)
        return f"Address '{address}' was added to contact '{name}'."
