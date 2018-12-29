import xml.etree.ElementTree as ET
from xml.dom import NotFoundErr

import urwid


def parser(xml):
    ''' Parses the XML '''
    root = ET.fromstring(xml)
    if root.tag != 'ugh':
        raise NotFoundErr('Root tag must be <ugh>')

    return [urwid.Text(e.text.strip()) for e in root]
