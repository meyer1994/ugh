import xml.etree.ElementTree as ET
from xml.dom import NotFoundErr

from ugh.classes import get_class


def parser(xml):
    '''
    Parses the XML into urwid widgets.

    Args:
        xml: XML string to be parsed.
        callbacks: List of callback to be used in the template. It will be
            converted to a dict of names and functions.
    '''
    root = ET.fromstring(xml)
    if root.tag != 'ugh':
        raise NotFoundErr('Root tag must be <ugh>')

    return [create_widget(e) for e in root]


def create_widget(elem):
    cls = get_class(elem.tag)

    # no children
    if len(elem) == 0:
        return cls(**elem.attrib)

    children = [create_widget(e) for e in elem]
    return cls(children, **elem.attrib)
