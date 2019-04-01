from ugh.parser import parse
from ugh.classes import by_id  # NOQA


def parse_file(filename, *args, **kwargs):
    ''' Simply reads file and parses string '''
    with open(filename, 'r') as file:
        return parse(file.read(), **kwargs)
