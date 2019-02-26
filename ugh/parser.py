import xml.etree.ElementTree as ET
from xml.dom import NotFoundErr

from ugh.classes import get_class


def parser(xml, **kwargs):
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
    cls = get_class(elem.tag)

    # no children
    if len(elem) == 0:
        args = check_attributes(elem.attrib, **kwargs)
        return cls(**args)

    children = [create_widget(e, **kwargs) for e in elem]
    return cls(children, **elem.attrib)


def check_attributes(attrs, **kwargs):
    ''' Checks the attributes for python keywords and values in the kwargs '''
    for key, val in attrs.items():
        if val in ('True', 'False', 'None'):
            attrs[key] = eval(val)

        if val in kwargs:
            attrs[key] = kwargs[val]

    return attrs
