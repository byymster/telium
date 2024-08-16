from prompt_toolkit.completion import Completer
from prompt_toolkit.completion import Completion

from .root import ROOT_COMMAND_PREFIX
from src.decorators import commands


class CommandCompleter(Completer):
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        parts = text.split()
        while len(parts) < 2:
            parts.append('')
        if not parts[0] in commands.keys():
            for command in commands.keys():
                if command.startswith(parts[0]) and command != ROOT_COMMAND_PREFIX:
                    yield Completion(command, start_position=-len(parts[0]))

            for subcommand in commands[ROOT_COMMAND_PREFIX].keys():
                if subcommand.startswith(parts[0]):
                    help_text = commands[ROOT_COMMAND_PREFIX][subcommand].__doc__ or ''
                    yield Completion(subcommand, start_position=-len(parts[0]), display_meta=help_text)
        elif parts[0] in commands and not parts[1] in commands[parts[0]].keys():
            for subcommand in commands[parts[0]].keys():
                if len(parts) == 1 or subcommand.startswith(parts[1]):
                    help_text = commands[parts[0]][subcommand].__doc__ or ''
                    yield Completion(subcommand, display_meta=help_text, start_position=-len(parts[1]))
