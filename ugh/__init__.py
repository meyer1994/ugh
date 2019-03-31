from functools import wraps

from ugh.parser import parse
from ugh.classes import by_id


def parse_file(filename, **kwargs):
    ''' Simply reads file and parses string '''
    with open(filename, 'r') as file:
        return parse(file.read(), **kwargs)


def callback(func):
    ''' Wraps the callback functions to receive the data object '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        pass
