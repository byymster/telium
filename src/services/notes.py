from collections import UserDict

from ..decorators import input_error
from ..models import Note

NOTE_NOT_FOUND_MESSAGE = 'Note not found.'


class Notes(UserDict):
    def __init__(self, data=None):
        super().__init__(data or [])

    def add_note(self, content):
        new_index = len(self.data.keys()) + 1
        note = Note(new_index, content)
        self.data[new_index] = note
        return f"Note '{content}' was added."

    @input_error()
    def find(self, needle: str = ''):
        if needle.startswith('#'):
            needle = needle[1:].lower()
            return [note for note in self.data.values() if needle.lower() in note.tags]
        return [note for note in self.data.values() if needle.lower() in note.content.lower()]

    @input_error({KeyError: NOTE_NOT_FOUND_MESSAGE})
    def delete(self, *args):
        note_id = args[0]
        del self.data[int(note_id)]
        return f'Note {note_id} was deleted.'

    def all(self):
        return self.data.values()

    def all_tags(self):
        tags = set()
        for note in self.data.values():
            tags.update(note.tags)
        return tags

    def sort_by_tags(self, direction='asc'):
        reverse = direction == 'desc'
        return sorted(
            self.data.values(),
            key=lambda note: sorted(note.tags, reverse=reverse)[
                0] if note.tags else '',
            reverse=reverse,
        )

    @input_error({KeyError: NOTE_NOT_FOUND_MESSAGE, ValueError: NOTE_NOT_FOUND_MESSAGE})
    def change_note(self, args):
        note_id = int(args[0])
        note = self.data[note_id]
        current_content = note.content
        new_content = yield current_content
        if not new_content:
            yield f'Note {note_id} was not updated.'
            return
        note.content = new_content
        note.tags = Note.extract_hashtags(new_content)
        yield f'Note {note_id} was updated.'
