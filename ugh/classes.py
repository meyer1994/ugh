import inspect

from functools import wraps

import urwid


IDS = {}

def by_id(id_):
    ''' Gets the element stored in IDS '''
    return IDS[id_]



def store_id(func):
    ''' Wraps the handlers to store the id into the dictionary '''
    @wraps(func)
    def wrapper(elem):
        '''
        Stores the element into the IDS dict and removes attribute from elem.

        Raises:
            KeyError when the ID already exists.
        '''
        # If no id, do nothing
        if 'id' not in elem.attrib:
            return func(elem)

        # If ID exists already, raises error
        if elem.attrib['id'] in IDS:
            rep = str(by_id(elem.attrib['id']))
            raise KeyError('ID already in use by %s' % rep)

        # Stores and removes from the attributes dict
        the_id = elem.attrib.pop('id')
        result = func(elem)
        IDS[the_id] = result
        return result

    return wrapper



@store_id
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

@store_id
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
