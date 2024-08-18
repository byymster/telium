from ..decorators import create_command_register
from ..services import NOTE_NOT_FOUND_MESSAGE
from ..services import Notes
from ..utils import pretty_print

NOTES_COMMAND_PREFIX = 'note'

notes_commands = create_command_register(NOTES_COMMAND_PREFIX)


@notes_commands('add')
def add(notes: Notes, *args):
    """- Add a new note."""
    content = ''
    while content == '':
        content = input('Enter note content: ')
    print(notes.add_note(content))


@notes_commands('edit', completer=Notes.find)
def edit(notes: Notes, *args):
    """<note_id> - Change a note by ID."""
    try:
        change_gen = notes.change_note(args)
        current_content = next(change_gen)
        if current_content != NOTE_NOT_FOUND_MESSAGE:
            print(f'Current content: {current_content}')
            new_content = input('Enter new content: ')
            print(change_gen.send(new_content))
        else:
            print(current_content)
    except StopIteration:
        print('Opps, something went wrong.')


@notes_commands('search')
def search(notes: Notes, *args):
    """<needle> - Find notes containing a substring. Use #text to find by tag"""
    pretty_print(notes.find(*args))


@notes_commands('delete', completer=Notes.find)
def delete(notes: Notes, *args):
    """<note_id> - Delete a note by ID."""
    print(notes.delete(*args))


@notes_commands('all')
def all_notes(notes: Notes, *args):
    """- List all notes."""
    pretty_print(notes.all())


@notes_commands('tags')
def all_tags(notes: Notes, *args):
    """- List all tags."""
    pretty_print(notes.all_tags())


@notes_commands('sort', completer=lambda notes, _: ['asc', 'desc'])
def sort(notes: Notes, *args):
    """<asc|desc> - Sort notes by tags."""
    direction = args[0] if args else 'asc'
    pretty_print(notes.sort_by_tags(direction))
