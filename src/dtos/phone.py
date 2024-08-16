from .base import Field
from .base import ValidationError


class Phone(Field):
    def __init__(self, value):
        if not self._validate(value):
            raise ValidationError('Phone number must contain 10 digits')
        super().__init__(value)

    @staticmethod
    def _validate(phone_number):
        return phone_number.isdigit() and len(phone_number) == 10
