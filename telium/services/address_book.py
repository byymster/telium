from collections import UserDict
from datetime import datetime
from datetime import timedelta
from typing import List

from ..decorators import input_error
from ..dtos.base import ValidationError
from ..models import DATA_TYPES
from ..models import Record

NOT_FOUND_MESSAGE = 'Contact not found.'


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
    def add_phone_to_contact(self, *args):
        name, phone = args
        record = self.find(name)
        if not isinstance(record, Record):
            return False
        record.add_phone(phone)
        return True

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
                except ValidationError as e:
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
                    except ValidationError as e:
                        yield e
                        continue
                else:
                    break

        yield True
        return True

    @input_error()
    def edit_name(self, *args):
        old_name, = args
        result = self.find(old_name)
        if result is None:
            yield False
            return False
        else:
            new_name = yield True
        if not new_name:
            yield False
        else:
            record = self.data.pop(old_name)
            record.name.value = new_name
            self.data[new_name] = record
            yield True
            return True

    @input_error({IndexError: 'No such  index'})
    def edit_list_data(self, args, item_type):
        username, = args
        record = self.find(username)
        if record is None:
            yield False
            return False
        items = getattr(record, item_type)

        option = yield items
        if items[option]:
            new_value = yield True
            items[option].value = new_value
            yield True
            return True

    @input_error({KeyError: NOT_FOUND_MESSAGE})
    def delete(self, *args):
        contact_name = args[0]
        del self.data[contact_name]
        return f'Note {contact_name} was deleted.'

    def find(self, name) -> Record | None:
        return self.data.get(name)

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
                if difference < 0:
                    birthday_this_year = datetime.strptime(
                        f'{user.birthday.value.day}.{user.birthday.value.month}.{today.year + 1}',
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

    def all(self) -> list[Record]:
        return list(self.data.values())

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
    def add_email(self, *args):
        name, email = args
        record = self.find(name)
        if not isinstance(record, Record):
            return record
        record.add_email(email)
        return f'Email {email} was added to contact {name}.'

    @input_error()
    def search(self, search_term) -> List[Record]:
        search_term = ' '.join(search_term) if isinstance(
            search_term, list) else search_term

        search_results = []
        search_lowered = search_term.lower().strip()

        for record in self.data.values():
            name = str(record.name.value).lower().strip()
            phones = ' '.join(str(phone).lower().strip()
                              for phone in record.phones)
            email = ' '.join(str(email).lower().strip()
                             for email in record.email)

            combined_fields = f'{name}{phones}{email}'

            if search_lowered in combined_fields:
                search_results.append(record)

        return search_results

    @input_error()
    def add_address(self, args):
        name = args[0]
        address = ' '.join(args[1:])
        record = self.find(name)
        if not isinstance(record, Record):
            return record

        record.add_address(address)
        return f"Address '{address}' was added to contact '{name}'."
