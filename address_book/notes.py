from collections import UserList
from address_book.decorators import input_error
from address_book.utils import Printable


class Note(Printable):
    def __init__(self, note_id: int, content: str):
        self.id = note_id
        self.content = content
        self.tags = Note.extract_hashtags(content)

    def __str__(self):
        return f"#{self.id}, Content: {self.content}\n Tags: {', '.join(self.tags)}"

    @classmethod
    def extract_hashtags(cls, content: str):
        return [word.replace('#', '').lower() for word in content.split() if word.startswith("#")]


class Notes(UserList):
    def __init__(self, data=None):
        super().__init__(data or [])

    def add_note(self, content):
        note = Note(len(self.data) + 1, content)
        self.data.append(note)
        return f"Note '{content}' was added."

    @input_error()
    def find(self, needle: str = None):
        if not needle:
            return []
        if needle.startswith("#"):
            needle = needle[1:].lower()
            return [note for note in self.data if needle.lower() in note.tags]
        return [note for note in self.data if needle.lower() in note.content.lower()]

    @input_error({IndexError: "Note not found."})
    def delete(self, note_id: str):
        del self.data[int(note_id) - 1]
        return f"Note {note_id} was deleted."

    def all(self):
        return self.data

    def all_tags(self):
        tags = set()
        for note in self.data:
            tags.update(note.tags)
        return tags
