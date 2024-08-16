from ..decorators import create_command_register
from ..dtos.base import ValidationError
from ..models import DATA_TYPES
from ..services import AddressBook
from ..utils import pretty_print

CONTACTS_COMMAND_PREFIX = 'contact'
address_book_commands = create_command_register(CONTACTS_COMMAND_PREFIX)


@address_book_commands('add')
def add(contacts: AddressBook, *args):
    """<username> - Add a new contact. you can add more than one phone"""
    if not args or len(args) != 1:
        raise ValueError(
            'Invalid argument, should be contact name.')
    name = args[0]
    add_gen = contacts.add_record_interactive(name)
    next(add_gen)
    prompt = False

    while True:
        user_input = input(
            f'Enter day of birth for {name} (dd.mm.yyyy): ')
        prompt = add_gen.send(user_input)
        if isinstance(prompt, ValidationError):
            print(f'Error adding birthday: {str(prompt)}')
            add_gen.send(False)
            continue
        elif prompt:
            print(f'Added birthday {user_input} to {name}.')
            add_gen.send(True)
            break
        else:
            print(f'Birthday is skipped for {name}.')
            add_gen.send(True)
            break

    for data_type, _ in DATA_TYPES:
        while True:
            user_input = input(
                f'Would you like to add a {data_type} for {name}? (y/N): ').lower() == 'y'
            try:
                prompt = add_gen.send(user_input)
                if user_input:
                    user_input = input(f'Enter {data_type}: ')
                    prompt = add_gen.send(user_input)
                    if isinstance(prompt, ValidationError):
                        print(
                            f'Error adding {data_type}: {str(prompt)}')
                        add_gen.send(True)
                        continue
                    else:
                        print(
                            f'Added {data_type} {user_input} to {name}.')
                else:
                    break
            except StopIteration as e:
                if e.value:
                    print(f'Contact {name} was added.')
                break

    if prompt:
        print(f'Contact {name} was added.')


@address_book_commands('edit', completer=AddressBook.search)
def edit(contacts: AddressBook, *args):
    """<username> - Change a name of an existing contact."""
    edit_gen = contacts.edit_name(*args)
    if not next(edit_gen):
        print('Contact not found')
        return
    new_name = input('Enter new name: ')
    result = edit_gen.send(new_name)
    if result:
        print(f"Contact name changed from '{args[0]}' to '{new_name}'.")
    else:
        print('Contact name change was cancelled.')


@address_book_commands('edit-phone')
def interactive_edit_phone(self, contact_name):
    record = self.find(contact_name)
    if not record:
        print(f"Contact '{contact_name}' not found.")
        return

    while True:
        self.list_items(record.phone, 'phone')
        index = yield from self.get_user_choice(len(record.phone))
        new_phone = yield 'Enter new phone: '
        try:
            record.edit_phone(index, new_phone)
            print(f'Phone #{index + 1} was changed to {new_phone}.')
            break
        except IndexError:
            print('Invalid index. Please try again.')


@address_book_commands('edit-email')
def interactive_edit_email(self, contact_name):
    record = self.find(contact_name)
    if not record:
        print(f"Contact '{contact_name}' not found.")
        return

    while True:
        self.list_items(record.email, 'email')
        index = yield from self.get_user_choice(len(record.email))
        new_email = yield 'Enter new email: '
        try:
            record.edit_email(index, new_email)
            print(f'Email #{index + 1} was changed to {new_email}.')
            break
        except IndexError:
            print('Invalid index. Please try again.')


@address_book_commands('edit-address')
def interactive_edit_address(self, contact_name):
    record = self.find(contact_name)
    if not record:
        print(f"Contact '{contact_name}' not found.")
        return

    while True:
        self.list_items(record.addresі, 'addresі')
        index = yield from self.get_user_choice(len(record.addresі))
        new_address = yield 'Enter new address: '
        try:
            record.edit_address(index, new_address)
            print(f'Address #{index + 1} was changed to {new_address}.')
            break
        except IndexError:
            print('Invalid index. Please try again.')


def list_items(self, items, item_type):
    if not items:
        print(f'No {item_type} available.')
        return
    print(f'You have {len(items)} {item_type}:')
    for i, item in enumerate(items, start=1):
        print(f'#{i} {item}')


def get_user_choice(self, max_choice):
    while True:
        try:
            choice = int((yield 'Choose an item: ')) - 1
            if 0 <= choice < max_choice:
                yield choice
                return
            else:
                print(f'Please enter a number between 1 and {max_choice}.')
        except ValueError:
            print('Please enter a valid number.')


def run_interactive(generator):
    try:
        prompt = next(generator)
        while True:
            user_input = input(prompt)
            prompt = generator.send(user_input)
    except StopIteration:
        pass


@address_book_commands('delete', completer=AddressBook.search)
def delete(contacts: AddressBook, *args):
    """<username> - Delete a contact."""
    print(contacts.delete(*args))


@address_book_commands('phone', completer=AddressBook.search)
def phone(contacts: AddressBook, *args):
    """<username> - Get phone number of a contact."""
    print(contacts.get(*args))


@address_book_commands('all')
def all(contacts: AddressBook):
    """- List all contacts."""
    pretty_print(contacts.all())


@address_book_commands('search')
def search(contacts: AddressBook, args):
    """<needle> - Find contacts containing a substring."""
    pretty_print(contacts.search(args))


@address_book_commands('add-phone', completer=AddressBook.search)
def add_phone(contacts: AddressBook, *args):
    """<username> <phone> - Add phone to a contact."""
    result = contacts.add_phone_to_contact(*args)
    if result is True:
        print(F'Phone {args[1]} was added to {args[0]}.')
    elif result is False:
        print('Contact not found.')
    else:
        print(result)

# Birthday Blok


@address_book_commands('add-birthday', completer=AddressBook.search)
def add_birthday(contacts: AddressBook, *args):
    """<username> <birthday> - Set birthday to a contact."""
    print(contacts.add_birthday(args))


@address_book_commands('show-birthday', completer=AddressBook.search)
def show_birthday(contacts: AddressBook, *args):
    """<username> - Show birthday of a contact."""
    print(contacts.show_birthday(args))


@address_book_commands('birthdays')
def birthdays(contacts: AddressBook, *args):
    """<days> - Show upcoming birthdays. Default 7 days."""
    days = int(args[0]) if args else 7
    bds = contacts.get_upcoming_birthdays(days)
    if len(bds) == 0:
        print('No upcoming birthdays.')
    else:
        print(
            '\n'.join(f"{bd['name']} - {bd['congratulation_date']}" for bd in bds))

# Email Blok


@address_book_commands('add-email', completer=AddressBook.search)
def add_email(contacts: AddressBook, *args):
    """<username> <email> - Add email to a contact."""
    print(contacts.add_email(*args))


@address_book_commands('add-address', completer=AddressBook.search)
def add_address(contacts: AddressBook, *args):
    """<username> <address> - Add address to a contact."""
    print(contacts.add_address(args))
