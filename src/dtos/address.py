from .base import Field


class Address(Field):
    VALIDATION_ERROR_MESSAGE = 'Address cannot be empty.'

    @staticmethod
    def validate(address):
        return bool(address and address.strip())
