import re
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

    return [create_widget(e, **kwargs) for e in root]


def create_widget(elem, **kwargs):
    '''
    Recursively creates widgets from the passed XML tree element.

    Args:
        elem: XML Element from python's api.
        kwargs: Arguments to be used when passing data to the widgets. The
        'py:' prefied attributes.

    Returns:
        The top element converted to the respective urwid object.
    '''
    cls = get_class(elem.tag)
    args = handle_attributes(elem.attrib, **kwargs)

    # no children
    if len(elem) == 0:
        return cls(**args)

    children = [create_widget(e, **kwargs) for e in elem]
    return cls(children, **args)


def handle_attributes(attrs, **kwargs):
    '''
    Checks the attributes for python keywords and values in the kwargs.

    It will search the text values of the attributes by checking for the
    existence of the 'py:' prefix. It uses regex to do so.

    Args:
        attrs: A dict with name of the attributes as key and strings as values.
        kwargs: Dict of kwargs from the call to `ugh.parse`.

    Returns:
        Dict with the attributes names as keys and the corresponding objects
        from kwargs placed in its respective place. Which means: if there is a
        `'key': [1, 2, 3]` in `kwargs` and a value of `py:key` in some of the
        `attrs` values. The list will be placed in the place of the string
        `py:key`.
    '''
    for key, val in attrs.items():
        # check for the value pattern in strings
        pyval = re.findall(r'^py:(.+)', val)
        if len(pyval) == 1:
            pyval = pyval[0]
            attrs[key] = kwargs[pyval]

    return attrs
