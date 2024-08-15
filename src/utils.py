from abc import ABC
from abc import abstractmethod
from typing import List

DUMP_FILE = 'telium_data.pkl'
HISTORY_FILE = '.history'


def parse_input(user_input):
    parts = user_input.strip().split()
    if not parts:
        raise ValueError('No command entered.')
    # Join the first two parts to form the command
    cmd = ' '.join(parts[:2]).lower()
    args = parts[2:]  # The rest are arguments
    return cmd, *args


class Printable(ABC):
    @abstractmethod
    def __str__(self):
        pass


def pretty_print(arr: List[Printable]):
    if len(arr) == 0:
        return print('Nothing found')
    return print('\n'.join(str(row) for row in arr))
