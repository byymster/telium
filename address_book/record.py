from .fields import Name, Phone, Birthday, Email

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = []

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

    def __str__(self):
        birthday_data = f", birthday: {self.birthday}" if self.birthday else ""
        email_data = f", email: {', '.join(p.value for p in self.email)}" if self.email else ""
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}{birthday_data}{email_data}"