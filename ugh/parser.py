import xml.etree.ElementTree as ET
from xml.dom import NotFoundErr

from ugh.classes import get_class


def parser(xml):
    ''' Parses the XML '''
    root = ET.fromstring(xml)
    if root.tag != 'ugh':
        raise NotFoundErr('Root tag must be <ugh>')

    return [create_widget(e) for e in root]


def create_widget(elem):
    cls = get_class(elem.tag)

    # has children
    if len(elem) > 0:
        children = [create_widget(e) for e in elem]
        return cls(children, **elem.attrib)
    return cls(**elem.attrib)
