from rich.console import Console
from rich.table import Table

from ..decorators import create_command_register
from ..dtos.base import ValidationError
from ..models import DATA_TYPES
from ..services import AddressBook
from ..views.contact_table import print_contact_table
from ..views.error import print_error
from ..views.skip import print_skip
from ..views.success import print_success

CONTACTS_COMMAND_PREFIX = 'contact'
address_book_commands = create_command_register(CONTACTS_COMMAND_PREFIX)


@address_book_commands('all')
def all(contacts: AddressBook, *args):
    """- List all contacts."""
    print_contact_table(contacts.all())


@address_book_commands('search')
def search(contacts: AddressBook, *args):
    """<needle> - Find contacts containing a substring."""
    print_contact_table(contacts.search(*args))


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
            print_error(f'Error adding birthday: {str(prompt)}')
            add_gen.send(False)
            continue
        elif prompt:
            print_success(f'Added birthday {user_input} to {name}.')
            add_gen.send(True)
            break
        else:
            print_skip(f'Birthday is skipped for {name}.')
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
                        print_error(
                            f'Error adding {data_type}: {str(prompt)}')
                        add_gen.send(True)
                        continue
                    else:
                        print_success(
                            f'Added {data_type} {user_input} to {name}.')
                else:
                    break
            except StopIteration as e:
                if e.value:
                    print_success(f'Contact {name} was added.')
                break

    if prompt:
        print_success(f'Contact {name} was added.')


@address_book_commands('edit', completer=AddressBook.search)
def edit(contacts: AddressBook, *args):
    """<username> - Change a name of an existing contact."""
    edit_gen = contacts.edit_name(*args)
    if not next(edit_gen):
        print_error('Contact not found')
        return
    new_name = input('Enter new name: ')
    result = edit_gen.send(new_name)
    if result:
        print_success(
            f"Contact name changed from '{args[0]}' to '{new_name}'.")
    else:
        print_skip('Contact name change was cancelled.')


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
        print_error('Contact not found')
        return
    elif isinstance(items, str):
        return print(items)

    if len(items) == 0:
        return print_skip(f'Contact has no {item_type}.')
    print(f'{item_type.capitalize()}:')
    print('\n'.join(f'#{i} {item}' for i, item in enumerate(items, start=1)))
    option = input(f'Which {item_type} you want to edit? (enter number): ')
    if option.isdigit() is False or int(option) > len(items) or int(option) < 0:
        return print_error('Invalid option. Please try again.')
    promt = edit_gen.send(int(option) - 1)
    if promt is True:
        new_phone = input(f'Enter new {item_type}: ')
        promt = edit_gen.send(new_phone)
        if promt is True:
            print_success(
                f"{item_type.capitalize()} #{option} was changed to '{new_phone}'.")
            return
        return print_error(f'{promt}. Please try again.')

    return print_error(f'{promt}. Please try again.')


@address_book_commands('delete', completer=AddressBook.search)
def delete(contacts: AddressBook, *args):
    """<username> - Delete a contact."""
    print(contacts.delete(*args))


@address_book_commands('phone', completer=AddressBook.search)
def phone(contacts: AddressBook, *args):
    """<username> - Get phone number of a contact."""
    contact = contacts.get(*args)
    if contact is None:
        print_error('Contact not found.')
        return
    phones = 'phones:\n' + '\n'.join(f'#{idx} {str(contact)}'
                                     for idx, contact in enumerate(contact.phones, start=1)) if len(contact.phones) \
        else 'no phones.'
    print(f'Contact {contact.name}, has {phones}')


@address_book_commands('add-phone', completer=AddressBook.search)
def add_phone(contacts: AddressBook, *args):
    """<username> <phone> - Add phone to a contact."""
    result = contacts.add_phone_to_contact(*args)
    if result is True:
        print_success(F'Phone {args[1]} was added to {args[0]}.')
    elif result is False:
        print_error('Contact not found.')
    else:
        print_error(result)


@address_book_commands('add-birthday', completer=AddressBook.search)
def add_birthday(contacts: AddressBook, *args):
    """<username> <birthday> - Set birthday to a contact."""
    print_success(contacts.add_birthday(args))


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
        table = Table(show_header=True, header_style='bold green')
        table.add_column('Name', style='bold')
        table.add_column('Congratulation day', style='bold')
        for bd in bds:
            table.add_row((bd['name']), bd['congratulation_date'])
        console = Console()
        return console.print(table)


@address_book_commands('add-email', completer=AddressBook.search)
def add_email(contacts: AddressBook, *args):
    """<username> <email> - Add email to a contact."""
    print(contacts.add_email(*args))


@address_book_commands('add-address', completer=AddressBook.search)
def add_address(contacts: AddressBook, *args):
    """<username> <address> - Add address to a contact."""
    print(contacts.add_address(args))
