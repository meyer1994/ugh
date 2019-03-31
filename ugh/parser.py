import xml.etree.ElementTree as ET

from ast import literal_eval
from xml.dom import NotFoundErr

from ugh.classes import handler, ids_store


def parse(xml, callbacks=[], data={}):
    '''
    Parses the XML into urwid widgets.

    Args:
        xml: XML string to be parsed.
    '''
    root = ET.fromstring(xml)
    if root.tag != 'ugh':
        raise NotFoundErr('Root tag must be <ugh>')

    # Resets ID store
    ids_store.clear()

    # Transform into a dict of callbacks wheere the keys are the names of
    # passed functions
    callbacks = {f.__name__: f for f in callbacks}
    handle_attributes(root, callbacks, data)

    return [handler(e) for e in root]


def handle_attributes(root, callbacks, data):
    '''
    Apply the callbacks to the XML structure.

    It simply checks for the attributes that start with 'on_'. Thankfully,
    urwid's devs always use the 'on_' prefix when dealing with callbacks.

    As for the data, if there is a callback, it will check for the 'user_data'
    attribute. If it exists, it will `literal_eval` the string. If it does not
    exists, it will pass the data dict as the value.

    Args:
        root: Root object of the XML document.
        callbacks: Dict of callbacks to use.
        data: Dict of data to use.

    Returns:
        Root object, modified. The modification will happen in place.

    Raises:
        KeyError when the callback was not passed in the dict.
    '''
    for child in root:
        for attr in list(child.attrib.keys()):

            # Handle callbacks
            if attr.startswith('on_'):
                callback_name = child.get(attr)
                child.attrib[attr] = callbacks[callback_name]

                # Handle data
                if 'user_data' in child.attrib:
                    # Evaluates
                    value = child.get('user_data')
                    child.attrib['user_data'] = literal_eval(value)
                else:
                    child.attrib['user_data'] = data

        handle_attributes(child, callbacks, data)
    return root
