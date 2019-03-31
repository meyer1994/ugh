import re
import ast
import xml.etree.ElementTree as ET

from xml.dom import NotFoundErr

from ugh.classes import handler


def parse(xml, data={}):
    '''
    Parses the XML into urwid widgets.

    Args:
        xml: XML string to be parsed.
        callbacks: a dict containing the data and callbacks to be used in the
        template.
    '''
    root = ET.fromstring(xml)
    if root.tag != 'ugh':
        raise NotFoundErr('Root tag must be <ugh>')

    handle_attributes(root, data)
    return [handler(e) for e in root]


def handle_attributes(root, data):
    '''
    Checks `attrs` for python keywords and values in `data`.

    It will search the text values of the attributes by checking for the
    existence of the 'py:' prefix. It uses regex to do so. It will convert
    everything after the 'py:' to some value using `handle_values`.

    Args:
        attrs: A dict with name of the attributes as key and strings as values.
        data: Dict of kwargs from the call to `ugh.parse`.

    Returns:
        Dict with the attributes names as keys and the corresponding objects
        from kwargs placed in its respective place. Which means: if there is a
        `'key': [1, 2, 3]` in `data` and a value of `py:key` in some of the
        `attrs` values. The list will be placed in the place of the string
        `py:key`.
    '''
    for key, val in root.attrib.items():
        # check for the value pattern in strings
        pyval = re.findall(r'^py:(.+)', val)
        if len(pyval) == 1:
            root.attrib[key] = handle_value(pyval[0], data)

    # recursively apply to all children
    for i, _ in enumerate(root):
        handle_attributes(root[i], data)

    return root


def handle_value(val, data):
    '''
    Tries to convert the value.

    It will first try to convert `val` as a literal using `ast.literal_eval`.
    If it fails, it will use `val` as key on `data`.

    Args:
        val: Value to convert, as string.
        data: Dict of items to use if `literal_eval` fails.

    Returns:
        Converted value.

    Raises:
        ValueError if `val` could not be converted to literal and it was not
        present in `data`.
    '''
    try:
        return ast.literal_eval(val)
    except ValueError:
        pass

    if val in data:
        return data[val]

    raise ValueError('Could not convert the value "%s" passed' % val)
