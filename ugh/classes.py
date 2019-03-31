import inspect

import urwid


def handler(elem):
    '''
    Base handler for widgets creation.

    This function was created to
    '''
    if elem.tag in HANDLERS:
        cls = HANDLERS[elem.tag]
        return cls(elem)

    cls = getattr(urwid, elem.tag)
    if len(elem) == 0:
        return cls(**elem.attrib)

    children = [handler(e) for e in elem]
    return cls(children, **elem.attrib)


def filler_handler(elem):
    '''
    Handles `Filler` widget special case.

    Differently from most widgets, the `Filler` widget accepts a single widget
    as its first parameter. Not a list of widgets.
    '''
    child = handler(elem[0])
    return urwid.Filler(child, **elem.attrib)


HANDLERS = {
    'Filler': filler_handler
}
