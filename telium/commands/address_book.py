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


@address_book_commands('edit-phone', completer=AddressBook.search)
def interactive_edit_phone(contacts: AddressBook, *args):
    """<username> - Change a phone number of an existing contact."""
    return interactive_edit_list_data(contacts, args, 'phones')


@address_book_commands('edit-email', completer=AddressBook.search)
def interactive_edit_email(contacts: AddressBook, *args):
    """<username> - Change an email number of an existing contact."""
    return interactive_edit_list_data(contacts, args, 'email')


@address_book_commands('edit-address', completer=AddressBook.search)
def interactive_edit_address(contacts: AddressBook, *args):
    """<username> - Change an address number of an existing contact."""
    return interactive_edit_list_data(contacts, args, 'address')


def interactive_edit_list_data(contacts: AddressBook, args, item_type):
    edit_gen = contacts.edit_list_data(args, item_type)
    items = next(edit_gen)
    if items is False:
        print('Contact not found')
        return
    elif isinstance(items, str):
        return print(items)

    print(f'{item_type.capitalize()}:')
    print('\n'.join(f'#{i} {phone}' for i, phone in enumerate(items, start=1)))
    option = input(f'Which {item_type} you want to edit? (enter number): ')
    promt = edit_gen.send(int(option) - 1)
    if promt is True:
        new_phone = input(f'Enter new {item_type}: ')
        promt = edit_gen.send(new_phone)
        if promt is True:
            print(f"{item_type.capitalize()} #{option} was changed to '{new_phone}'.")
            return
        return print(f'{promt}. Please try again.')

    return print(f'{promt}. Please try again.')


@address_book_commands('delete', completer=AddressBook.search)
def delete(contacts: AddressBook, *args):
    """<username> - Delete a contact."""
    print(contacts.delete(*args))


@address_book_commands('phone', completer=AddressBook.search)
def phone(contacts: AddressBook, *args):
    """<username> - Get phone number of a contact."""
    print(contacts.get(*args))


@address_book_commands('all')
def all(contacts: AddressBook, *args):
    """- List all contacts."""
    pretty_print(contacts.all())


@address_book_commands('search')
def search(contacts: AddressBook, *args):
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


@address_book_commands('add-email', completer=AddressBook.search)
def add_email(contacts: AddressBook, *args):
    """<username> <email> - Add email to a contact."""
    print(contacts.add_email(*args))


@address_book_commands('add-address', completer=AddressBook.search)
def add_address(contacts: AddressBook, *args):
    """<username> <address> - Add address to a contact."""
    print(contacts.add_address(args))
