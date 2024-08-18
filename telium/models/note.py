from rich.table import Table

from ..utils import Printable
from ..utils import RichPrintable


class Note(Printable, RichPrintable):
    def __init__(self, note_id: int, content: str):
        self.id = note_id
        self.content = content
        self.tags = Note.extract_hashtags(content)

    def __str__(self):
        tags_text = f"\n Tags: {', '.join(self.tags)}" if len(
            self.tags) > 0 else ''
        return f'#{self.id}, Content: {self.content}{tags_text}'

    def __rich__(self, table: Table, bg_color=None):
        table.add_row(
            str(self.id),
            str(self.content),
            ', '.join(str(tag) for tag in self.tags) if len(self.tags) else '',
            style=f'on {bg_color}' if bg_color else None
        )

    @classmethod
    def extract_hashtags(cls, content: str):
        return [
            word.replace('#', '').lower()
            for word in content.split()
            if word.startswith('#')
        ]
