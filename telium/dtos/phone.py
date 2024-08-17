from .base import Field


class Phone(Field):
    VALIDATION_ERROR_MESSAGE = 'Phone number must be a 10-digit number.'

    @staticmethod
    def validate(phone_number):
        return phone_number.isdigit() and len(phone_number) == 10
