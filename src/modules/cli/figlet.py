import pyfiglet

HEADER_TEXT = "Magic OMR"
HEADER_FONT = 'slant'


# def get_header():
#     return HEADER_FIGLET


def print_header():
    pyfiglet.print_figlet(HEADER_TEXT, HEADER_FONT)
