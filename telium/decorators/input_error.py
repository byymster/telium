DEFAULT_ERRORS = {
    ValueError: "Give me correct values.\nType 'help' to see available commands.",
    IndexError: "Invalid number of arguments.\nType 'help' to see available commands.",
}


def handle_generator(gen, combined_errors):
    try:
        value = next(gen)
        while True:
            try:
                sent_value = yield value
                value = gen.send(sent_value)
            except StopIteration as e:
                return e.value
    except Exception as e:
        error_message = combined_errors.get(type(e), str(e))
        yield error_message


def input_error(errors=None):
    if errors is None:
        errors = {}
    combined_errors = {**DEFAULT_ERRORS, **errors}

    def decorator(func):
        def inner(*args, **kwargs):
            try:
                gen = func(*args, **kwargs)
                if hasattr(gen, '__iter__') and hasattr(gen, '__next__'):
                    return handle_generator(gen, combined_errors)
                else:
                    return gen
            except Exception as e:
                return combined_errors.get(type(e), str(e))
        return inner

    return decorator
