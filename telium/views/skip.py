from prompt_toolkit import HTML
from prompt_toolkit import print_formatted_text


def print_skip(error_message: str):
    print_formatted_text(HTML(f'<ansiyellow>{error_message}</ansiyellow>'))
