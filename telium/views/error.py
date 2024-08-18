from prompt_toolkit import HTML
from prompt_toolkit import print_formatted_text


def print_error(error_message: str):
    print_formatted_text(HTML(f'<ansired>{error_message}</ansired>'))
