import inspect
import json

from ast import literal_eval

import urwid


# will hold the dictionary containing all the classes of the urwid module
CLASSES = dict(inspect.getmembers(urwid, inspect.isclass))

ids = {}


def is_class(item):
    '''
    Checks if the item is a dict representation of a class.

    A class, for this project, is a dict with some key 'class'.

    Args:
        item: Object to see if it is a class.

    Returns:
        True if it is a class, False otherwise.
    '''

    return isinstance(item, dict) and 'class' in item


def handle_list(item):
    '''
    Handles json objects that are lists.

    JSON objects are quite simple. They are lists, or they are dicts. Simply.
    For this project, there is also the need to threat tuples, which is done by
    using literal_eval function.
    Each object in a list is a dict, a list, or something else. So we need to
    threat the list and dict ones and the literal_eval function takes care of
    the rest (almost).

    Args:
        item: Iterable of objects to be threated.

    Returns:
        List of items after all the threating was done.
    '''

    lst = []
    for obj in item:

        if is_class(obj):
            lst.append(construct(obj))
            continue

        if isinstance(obj, list):
            lst.append(handle_list(obj))
            continue

        lst.append(obj)

    return tuple(lst)


def handle_markup(markup):
    '''
    Handle markups edge-case.

    There is this special case for when we are trying to add a list of tuples
    to an urwid.Text.

    Example:
    >>> import urwid
    >>> l = [ ('attr1', 'text1'), 'text2', ('attr2', 'text3') ]
    >>> t = urwid.Text(l)
    >>> t.get_text()
    ('text1text2text3', [('attr1', 4), (None, 5), ('attr2', 5)])

    In this case, as our program threats all lists as tuples, we need to
    convert the tuple, here, to a list.

    Args:
        markup: The markup to threat. It may be a list of tuples and strings,
        list of tuples, a list of strings or a single string.

    Returns:
        The markup itself if it detects that it is not a list of tuples. A list
        of tuples and/or strings otherwise.
    '''

    # detect json list (tuple)
    if isinstance(markup, tuple):
        for i in markup:
            # if there is any tuple inside, it meanst it should be a list of
            # markups
            if isinstance(i, tuple):
                return list(markup)

    return markup


def construct(items_dict):
    '''
    Constructs the classes described in the dict.

    It will create all the classes described in the dictionary, normally
    obtained from a .json. It does it in a recursive way. Which means,
    everytime it finds a new dict in the items, with the 'class' key, it will
    call itself again with this, just found, dict as it's parameter.

    Note:
        The attributes used to set different markups for the widgets, specially
        the Text widget, are supposed to be already defined in a 'pallete' that
        is passed to the main loop. If it is not defined, the program WILL NOT
        fail, it will simply execute without the attributes. This is an urwid
        strategy.

    Args:
        items_dict: dict of items to be created.

    Returns:
        The top widget described in items_dict with it's inner widgets all
        created and included in itself.
    '''

    the_class = items_dict['class']
    the_class = CLASSES[the_class]
    class_sig = inspect.signature(the_class)
    # will store all the arguments to be used in the constructor
    class_args = {}

    for key, item in items_dict.items():

        if key in ('class', 'id'):
            continue

        # more classes to take care of
        if is_class(item):
            class_args[key] = construct(item)
            continue

        # threat lists
        if isinstance(item, list):
            class_args[key] = handle_list(item)
            continue

        class_args[key] = item

    # markup edge-case testing
    if 'markup' in class_args:
        markup = class_args['markup']
        class_args['markup'] = handle_markup(markup)


    bound_args = class_sig.bind(**class_args)
    bound_args.apply_defaults()

    constructed_class = the_class(*bound_args.args, **bound_args.kwargs)

    if 'id' in items_dict:
        i = items_dict['id']
        ids[i] = constructed_class

    return constructed_class
