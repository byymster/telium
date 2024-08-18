from datetime import datetime

from .base import Field
from .base import ValidationError


class Birthday(Field):
    def __init__(self, value):
        try:
            date = datetime.strptime(value, '%d.%m.%Y').date()
            super().__init__(date)
        except ValueError:
            raise ValidationError('Invalid date format. Use DD.MM.YYYY')

    @staticmethod
    def validate(date):
        try:
            if (date - datetime.now().date()).days > 0:
                raise ValidationError('Birthday cannot be from future.')
            if (datetime.now().date() - date).days > 365 * 100:
                raise ValidationError(
                    'Birthday cannot be more than 100 years ago.')
            return True
        except ValueError:
            return False

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        try:
            date = datetime.strptime(new_value, '%d.%m.%Y').date()
            super().value = date
        except ValueError:
            raise ValidationError('Invalid date format. Use DD.MM.YYYY')
