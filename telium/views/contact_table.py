from typing import List

from ..models import Record
from ..utils import rich_print


def print_contact_table(contacts: List[Record]):
    rich_print(contacts, [
        {'header': 'Name', 'style': 'bold'},
        {'header': 'Birthday', 'style': 'bold'},
        {'header': 'Phones', 'style': 'bold'},
        {'header': 'Emails', 'style': 'bold'},
        {'header': 'Addresses', 'style': 'bold'},
    ])
