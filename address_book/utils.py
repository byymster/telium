from abc import ABC
from abc import abstractmethod
from typing import List

DUMP_FILE = 'telium_data.pkl'


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


class Printable(ABC):
    @abstractmethod
    def __str__(self):
        pass


def pretty_print(arr: List[Printable]):
    if len(arr) == 0:
        return print('Nothing found')
    return print('\n'.join(str(row) for row in arr))
