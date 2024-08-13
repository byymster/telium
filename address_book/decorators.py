def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me correct values.\nType 'help' to see available commands."
        except IndexError:
            return "Invalid number of arguments.\nType 'help' to see available commands."

    return inner