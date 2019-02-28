import re
import ast
import xml.etree.ElementTree as ET

from xml.dom import NotFoundErr

from ugh.classes import get_class


def parse(xml, **kwargs):
    '''
    Parses the XML into urwid widgets.

    Args:
        xml: XML string to be parsed.
        callbacks: List of callbacks to be used in the template. It will be
            converted to a dict of names and functions.
    '''
    root = ET.fromstring(xml)
    if root.tag != 'ugh':
        raise NotFoundErr('Root tag must be <ugh>')

    return [create_widget(e, kwargs) for e in root]


def create_widget(elem, data={}):
    '''
    Recursively creates widgets from the passed XML tree element.

    Args:
        elem: XML Element from python's api.
        data: Dict of arguments to be used when passing data to the widgets.
        The 'py:' prefied attributes.

    Returns:
        The top element converted to the respective urwid object.
    '''
    cls = get_class(elem.tag)
    args = handle_attributes(elem.attrib, data)

    # no children
    if len(elem) == 0:
        return cls(**args)

    children = [create_widget(e, data) for e in elem]
    return cls(children, **args)


def handle_attributes(attrs, data):
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
    for key, val in attrs.items():
        # check for the value pattern in strings
        pyval = re.findall(r'^py:(.+)', val)
        if len(pyval) == 1:
            attrs[key] = handle_value(pyval[0], data)

    return attrs


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
