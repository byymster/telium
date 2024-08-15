from pathlib import PurePath

from platformdirs import user_data_dir

from address_book.data_manager import DataManager
from address_book.notes import NOT_FOUND_MESSAGE as NOTE_NOT_FOUND_MESSAGE
from address_book.utils import DUMP_FILE
from address_book.utils import parse_input
from address_book.utils import pretty_print


def main():
    user_data_directory = user_data_dir('Telium', 'Telium')
    file_path = PurePath(user_data_directory).joinpath(DUMP_FILE)
    data_manager = DataManager(file_path)
    contacts, notes = data_manager.load_data()
    print('Welcome to the assistant bot!')
    while True:
        try:
            user_input = input('Enter a command: ')
            command, *args = parse_input(user_input)
            match command:
                case 'close' | 'exit':
                    print('Good bye!')
                    break
                case 'hello':
                    print('How can I help you?')
                case 'add':
                    print(contacts.add_record(args))
                case 'change':
                    print(contacts.change_record(*args))
                case 'phone':
                    print(contacts.find(args[0]))
                case 'all':
                    print(contacts.all())
                case 'add-birthday':
                    print(contacts.add_birthday(args))
                case 'show-birthday':
                    print(contacts.show_birthday(args))
                case 'birthdays':
                    days = int(args[0]) if args else 7
                    print(contacts.birthdays(days))
                case 'add-email':
                    print(contacts.add_email(args))
                case 'add-address':
                    print(contacts.add_address(args))
                case 'add-note':
                    content = ''
                    while content == '':
                        content = input('Enter note content: ')
                    print(notes.add_note(content))
                case 'find-note':
                    pretty_print(notes.find(*args))
                case 'delete-note':
                    print(notes.delete(*args))
                case 'all-notes':
                    pretty_print(notes.all())
                case 'all-notes-tags':
                    pretty_print(notes.all_tags())
                case 'sort-notes':
                    direction = args[0] if args else 'asc'
                    pretty_print(notes.sort_by_tags(direction))
                case 'change-note':
                    change_gen = notes.change_note(args)
                    current_content = next(change_gen)
                    if current_content != NOTE_NOT_FOUND_MESSAGE:
                        print(f'Current content: {current_content}')
                        new_content = input('Enter new content: ')
                        print(change_gen.send(new_content))
                    else:
                        print(current_content)
                case 'help':
                    print(
                        """
                    Available commands:
                        hello - Greet the bot.
                        add <username> [phone] - Add a new contact. you can add more than one phone
                        change <username> <phone> - Change an existing contact.
                        phone <username> - Get phone number of a contact.
                        all - List all contacts.
                        add-birthday <username> <birthday> - Add birthday to a contact.
                        add-email <username> <email> - Add email to a contact.
                        add-address <username> <your address with spaces> - Add address to a contact.
                        show-birthday <username> - Show birthday of a contact.
                        birthdays <days> - Show upcoming birthdays. Default 7 days.
                        add-note - Add a new note.
                        find-note <needle> - Find notes containing a substring.
                        delete-note <id> - Delete a note by title.
                        all-notes - List all notes.
                        all-notes-tags - List all unique tags.
                        sort-notes <direction> - Sort notes by tags in ascending or descending order.
                    """
                    )
                case _:
                    print('Invalid command.')
        except ValueError as e:
            print(e)
        except KeyboardInterrupt:
            print('\nGood bye!')
            break
    data_manager.save_data(contacts.data, notes.data)


if __name__ == '__main__':
    main()
