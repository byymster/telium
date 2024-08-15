from src.decorators import create_command_register
from src.record import DATA_TYPES

CONTACTS_COMMAND_PREFIX = 'contact'
address_book_commands = create_command_register(CONTACTS_COMMAND_PREFIX)


@address_book_commands('add')
def add(contacts, *args):
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
        if isinstance(prompt, ValueError):
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
                    if isinstance(prompt, ValueError):
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


@address_book_commands('edit')
def edit(contacts, *args):
    """<username> <phone> - Change an existing contact."""
    print(contacts.change_record(*args))


@address_book_commands('phone')
def phone(contacts, *args):
    """<username> - Get phone number of a contact."""
    print(contacts.get(*args))


@address_book_commands('all')
def all(contacts, *args):
    """- List all contacts."""
    print(contacts.list_all())


@address_book_commands('search')
def search(contacts, args):
    """<needle> - Find contacts containing a substring."""
    print(contacts.search(args))

# Birthday Blok


@address_book_commands('add-birthday')
def add_birthday(contacts, *args):
    """<username> <birthday> - Set birthday to a contact."""
    print(contacts.add_birthday(args))


@address_book_commands('show-birthday')
def show_birthday(contacts, *args):
    """<username> - Show birthday of a contact."""
    print(contacts.show_birthday(args))


@address_book_commands('birthdays')
def birthdays(contacts, *args):
    """<days> - Show upcoming birthdays. Default 7 days."""
    days = int(args[0]) if args else 7
    print(contacts.get_upcoming_birthdays(days))

# Email Blok


@address_book_commands('add-email')
def add_email(contacts, args):
    """<username> <email> - Add email to a contact."""
    print(contacts.add_email(args))


@address_book_commands('add-address')
def add_address(contacts, args):
    """<username> <address> - Add address to a contact."""
    print(contacts.add_address(args))
