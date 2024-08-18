from typing import List

from ..models import Note
from ..utils import rich_print


def print_notes_table(notes: List[Note]):
    rich_print(notes, [
        {'header': 'id', 'style': 'bold'},
        {'header': 'Content', 'style': 'bold'},
        {'header': 'Tags', 'style': 'bold'},
    ])
