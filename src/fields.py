import re
from datetime import datetime


class ValidationError(Exception):
    pass


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Birthday(Field):
    def __init__(self, value):
        try:
            date = datetime.strptime(value, '%d.%m.%Y').date()
            super().__init__(date)
        except ValueError:
            raise ValidationError('Invalid date format. Use DD.MM.YYYY')


class Phone(Field):
    def __init__(self, value):
        if not self._validate(value):
            raise ValidationError('Phone number must contain 10 digits')
        super().__init__(value)

    @staticmethod
    def _validate(phone_number):
        return phone_number.isdigit() and len(phone_number) == 10


class Email(Field):
    def __init__(self, value):
        if self.validate_email(value):
            super().__init__(value)
        else:
            raise ValidationError(
                'Invalid email format. Please use a correct email address.'
            )

    @staticmethod
    def validate_email(email):
        email_regex = r'(^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$)'
        return re.match(email_regex, email) is not None


class Address(Field):
    def __init__(self, value):
        if self.validate_address(value):
            super().__init__(value)
        else:
            raise ValidationError('Address cannot be empty.')

    @staticmethod
    def validate_address(address):
        return bool(address and address.strip())
