def input_error(errors=None):
    if errors is None:
        errors = dict()

    def decorator(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValueError:
                return "Give me correct values.\nType 'help' to see available commands." \
                    if errors.get(ValueError) is None else errors[ValueError]
            except IndexError:
                return "Invalid number of arguments.\nType 'help' to see available commands." \
                    if errors.get(IndexError) is None else errors[IndexError]

        return inner

    return decorator
