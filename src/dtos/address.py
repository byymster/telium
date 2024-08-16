from .base import Field
from .base import ValidationError


class Address(Field):
    def __init__(self, value):
        if self.validate_address(value):
            super().__init__(value)
        else:
            raise ValidationError('Address cannot be empty.')

    @staticmethod
    def validate_address(address):
        return bool(address and address.strip())
