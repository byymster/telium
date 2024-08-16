import re

from .base import Field


class Email(Field):
    VALIDATION_ERROR_MESSAGE = 'Invalid email format. Please use a correct email address.'

    @staticmethod
    def validate(email):
        email_regex = r'(^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$)'
        return re.match(email_regex, email) is not None
