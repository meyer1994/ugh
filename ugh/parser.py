import xml.etree.ElementTree as ET
from xml.dom import NotFoundErr

import urwid


def parser(xml):
    ''' Parses the XML '''
    root = ET.fromstring(xml)
    if root.tag != 'ugh':
        raise NotFoundErr('Root tag must be <ugh>')

    results = []
    for elem in root:
        text = elem.text.strip()
        item = urwid.Text(text, **elem.attrib)
        results.append(item)
    return results
