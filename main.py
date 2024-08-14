from address_book.address_book import AddressBook
from address_book.utils import parse_input

def main():
    contacts = AddressBook()
    contacts.load()
    print("Welcome to the assistant bot!")
    while True:
        try:
            user_input = input("Enter a command: ")
            command, *args = parse_input(user_input)
            match command:
                case "close" | "exit":
                    print("Good bye!")
                    break
                case "hello":
                    print("How can I help you?")
                case "add":
                    print(contacts.add_record(args))
                case "change":
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
                    print(contacts.birthdays())
                case 'help':
                    print("""
                    Available commands:
                        hello - Greet the bot.
                        add <username> [phone] - Add a new contact. you can add more than one phone
                        change <username> <phone> - Change an existing contact.
                        phone <username> - Get phone number of a contact.
                        all - List all contacts.
                        add-birthday <username> <birthday> - Add birthday to a contact.
                        show-birthday <username> - Show birthday of a contact.
                        birthdays - Show upcoming birthdays.
                    """)
                case _:
                    print("Invalid command.")
        except ValueError as e:
            print(e)
    contacts.save()

if __name__ == "__main__":
    main()