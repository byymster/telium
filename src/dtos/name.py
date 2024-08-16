from .base import Field


class Name(Field):
    VALIDATION_ERROR_MESSAGE = 'Name cannot be empty.'

    @staticmethod
    def validate(name):
        return bool(name and name.strip())
