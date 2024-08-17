class ValidationError(Exception):
    pass


class Field:
    VALIDATION_ERROR_MESSAGE = 'Validation error.'

    def __init__(self, value):
        if self.validate(value):
            self._value = value
        else:
            raise ValidationError(self.VALIDATION_ERROR_MESSAGE)

    def __str__(self):
        return str(self._value)

    @staticmethod
    def validate(value):
        return True

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if self.validate(new_value):
            self._value = new_value
        else:
            raise ValidationError(self.VALIDATION_ERROR_MESSAGE)
