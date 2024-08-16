from .base import Field
from .base import ValidationError


class Name(Field):
    def __init__(self, value):
        if self.validate_name(value):
            super().__init__(value)
        else:
            raise ValidationError('Name cannot be empty.')

    @staticmethod
    def validate_name(name):
        return bool(name and name.strip())
