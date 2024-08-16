from src.commands.address_book import CONTACTS_COMMAND_PREFIX
from src.commands.notes import NOTES_COMMAND_PREFIX
from src.commands.root import ROOT_COMMAND_PREFIX
from src.decorators import commands


def handle_command(command, contacts, notes, *args):
    parts = command.split()
    if len(parts) == 2 and parts[0] in commands and parts[1] in commands[parts[0]]:
        if parts[0] == CONTACTS_COMMAND_PREFIX:
            commands[parts[0]][parts[1]](contacts, *args)
        elif parts[0] == NOTES_COMMAND_PREFIX:
            commands[parts[0]][parts[1]](notes, *args)
    elif parts[0] in commands[
            ROOT_COMMAND_PREFIX]:
        return commands[ROOT_COMMAND_PREFIX][parts[0]](*args)
    else:
        print('Invalid command.')
    return True
