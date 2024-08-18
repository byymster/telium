from abc import ABC
from abc import abstractmethod
from typing import List
from typing import Optional
from typing import TypedDict
from typing import Union

from rich.console import Console
from rich.style import Style
from rich.table import Table
from rich.text import Text


def parse_input(user_input):
    parts = user_input.strip().split()
    if not parts:
        raise ValueError('No command entered.')
    cmd = ' '.join(parts[:2]).lower()
    args = parts[2:]
    return cmd, *args


class Printable(ABC):
    @abstractmethod
    def __str__(self):
        pass


class RichPrintable():
    @abstractmethod
    def __rich__(self, table: Table, bg_color: str | None):
        pass


def pretty_print(arr: List[Printable]):
    if len(arr) == 0:
        return print('Nothing found')
    return print('\n'.join(str(row) for row in arr))


class ColumnConfig(TypedDict, total=False):
    header: Union[str, 'Text']
    footer: Union[str, 'Text']
    header_style: Optional[Union[str, 'Style']]
    footer_style: Optional[Union[str, 'Style']]
    style: Optional[Union[str, 'Style']]
    justify: Optional[str]
    vertical: Optional[str]
    overflow: Optional[str]
    width: Optional[int]
    min_width: Optional[int]
    max_width: Optional[int]
    ratio: Optional[int]
    no_wrap: Optional[bool]


def rich_print(arr: List[RichPrintable], columns: List[ColumnConfig]):
    table = Table(show_header=True, header_style='bold magenta')
    for column in columns:
        table.add_column(**column)
    if len(arr) == 0:
        return print('Nothing found')
    for row_index, row in enumerate(arr):
        row.__rich__(table, bg_color='grey37' if row_index % 2 == 1 else None)
    console = Console()
    return console.print(table)
