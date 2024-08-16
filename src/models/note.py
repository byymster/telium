from ..utils import Printable


class Note(Printable):
    def __init__(self, note_id: int, content: str):
        self.id = note_id
        self.content = content
        self.tags = Note.extract_hashtags(content)

    def __str__(self):
        return f"#{self.id}, Content: {self.content}\n Tags: {', '.join(self.tags)}"

    @classmethod
    def extract_hashtags(cls, content: str):
        return [
            word.replace('#', '').lower()
            for word in content.split()
            if word.startswith('#')
        ]
