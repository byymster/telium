class Command:
    def __init__(self, func, completer=None):
        self.func = func
        self.completer = completer


commands: dict[str, dict[str, Command]] = {}


def create_command_register(prefix):
    if prefix not in commands:
        commands[prefix] = {}

    def register_command(name, completer=None):
        def decorator(func):
            commands[prefix][name] = Command(func, completer)
            return func

        return decorator

    return register_command


def display_help():
    print('Available commands:')
    for name, subcommands in commands.items():
        if isinstance(subcommands, dict):
            for subname, cmd in subcommands.items():
                print(
                    f"{name+' ' if name != 'root' else ''}{subname} {cmd.func.__doc__}")
        else:
            print(f'{name}{subcommands.__doc__}')
