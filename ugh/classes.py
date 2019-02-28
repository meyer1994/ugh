import inspect

import urwid

# Dict with all classes of urwid
CLASSES = dict(inspect.getmembers(urwid, inspect.isclass))


def get_class(class_name):
    '''
    Gets the respective class.

    Args:
        class_name: Name of class.

    Returns:
        Respective class from urwid.

    Raises:
        KeyError when class is not an uriwd class.
    '''
    if class_name not in CLASSES:
        error = 'Class %s is not an urwid class' % class_name
        raise KeyError(error)

    return CLASSES[class_name]
