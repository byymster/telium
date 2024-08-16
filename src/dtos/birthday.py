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
