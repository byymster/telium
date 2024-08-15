from src.decorators import create_command_register
from src.decorators import display_help

ROOT_COMMAND_PREFIX = 'root'
root_commands = create_command_register(ROOT_COMMAND_PREFIX)


@root_commands('help')
def help_command(*args):
    """- Display help information."""
    display_help()


@root_commands('exit')
@root_commands('close')
def exit_command(*args):
    """- Exit the application."""
    print('Good bye!')
    return False
