commands = {}


# Decorator to register commands
def create_command_register(prefix):
    if prefix not in commands:
        commands[prefix] = {}

    def register_command(name):
        def decorator(func):
            commands[prefix][name] = func
            return func

        return decorator

    return register_command


# Function to display help information
def display_help():
    print('Available commands:')
    for name, subcommands in commands.items():
        if isinstance(subcommands, dict):
            for subname, func in subcommands.items():
                print(
                    f"{name+' ' if name != 'root' else ''}{subname} {func.__doc__}")
        else:
            print(f'{name}{subcommands.__doc__}')
