from ugh.parser import parse
from ugh.classes import by_id


def parse_file(filename, **kwargs):
    ''' Simply reads file and parses string '''
    with open(filename, 'r') as file:
        return parse(file.read(), **kwargs)
