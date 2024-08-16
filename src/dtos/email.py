import re

from .base import Field
from .base import ValidationError


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
