from prompt_toolkit.completion import Completer
from prompt_toolkit.completion import Completion
from prompt_toolkit.key_binding import KeyBindings

from ..decorators import commands
from ..models import Note
from ..models import Record
from .address_book import CONTACTS_COMMAND_PREFIX
from .root import ROOT_COMMAND_PREFIX


def create_record_completion(completion, start_position):
    display_meta = ', '.join([
        str(completion.phones[0]) if completion.phones else '',
        str(completion.email[0]) if completion.email else '',
        str(completion.address[0]) if completion.address else ''
    ]).strip(', ')
    return Completion(str(completion.name), start_position=start_position, display_meta=display_meta)


def create_note_completion(completion, start_position):
    max_char_length = 15
    display_meta = completion.content[:max_char_length] + '...' if len(
        completion.content) > max_char_length else completion.content
    return Completion(
        str(completion.id),
        start_position=start_position,
        display_meta=display_meta,
        display=f'#{completion.id}'
    )


class CommandCompleter(Completer):
    def __init__(self, contacts, notes):
        self.contacts = contacts
        self.notes = notes

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
                    help_text = commands[ROOT_COMMAND_PREFIX][subcommand].func.__doc__ or ''
                    yield Completion(subcommand, start_position=-len(parts[0]), display_meta=help_text)
        elif parts[0] in commands and not parts[1] in commands[parts[0]].keys():
            for subcommand in commands[parts[0]].keys():
                if len(parts) == 1 or subcommand.startswith(parts[1]):
                    help_text = commands[parts[0]
                                         ][subcommand].func.__doc__ or ''
                    yield Completion(subcommand, display_meta=help_text, start_position=-len(parts[1]))
        elif parts[0] in commands and parts[1] in commands[parts[0]] and commands[parts[0]][
                parts[1]].completer is not None:

            search_term = (parts[2] if len(parts) > 2 else '').strip()
            completer = commands[parts[0]][parts[1]].completer(
                self.contacts if parts[0] == CONTACTS_COMMAND_PREFIX else self.notes, search_term)

            if len(completer) > 1 or (len(completer) == 1 and (
                    not isinstance(completer[0], Record) or len(parts) == 2 or str(completer[0].name) != parts[2])):
                for completion in completer:
                    start_position = -len(parts[2] if len(parts) > 2 else '')
                    if isinstance(completion, Record):
                        yield create_record_completion(completion, start_position)
                    elif isinstance(completion, Note):
                        yield create_note_completion(completion, start_position)
                    else:
                        yield Completion(str(completion), start_position=start_position)


def create_binding(fuzzy_completer, non_fuzzy_completer):
    bindings = KeyBindings()

    def should_enable_fuzzy(command: str) -> bool:
        restricted = [
            'note edit',
            'note delete',
        ]
        return command not in restricted

    @bindings.add(' ')
    def _(event):
        """
        When space is pressed, we check the word before the cursor, and
        autocorrect that.
        """
        b = event.app.current_buffer
        command = b.document.text_before_cursor
        w = command.split()[-1].strip() if len(command.split()) > 0 else ''
        if should_enable_fuzzy(command):
            b.completer = fuzzy_completer
        else:
            b.completer = non_fuzzy_completer

        completion_idx = b.complete_state.complete_index \
            if b.complete_state and b.complete_state.complete_index is not None \
            else 0
        if b.complete_state and b.complete_state.completions[completion_idx].text != w:
            b.complete_next()
        elif not b.complete_state:
            b.start_completion(select_first=False)
            b.insert_text(' ')
        else:
            b.insert_text(' ')

    return bindings
