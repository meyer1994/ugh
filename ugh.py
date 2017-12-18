import inspect
import json

from ast import literal_eval

import urwid


# will hold the dictionary containing all the classes of the urwid module
CLASSES = dict(inspect.getmembers(urwid, inspect.isclass))


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
        if is_class(obj) or isinstance(obj, list):
            lst.append(construct(obj))
        else:
            # or it will be some tuple, that is why we use the
            # literal_eval, or it will be some string
            try:
                lst.append(literal_eval(obj))
            except Exception:
                lst.append(obj)
    return lst


def handle_tuple(item):
    '''
    Handle tuples.

    Same as calling `tuple(handle_list(item))`.

    Args:
        item: Iterable of objects to be threated.

    Returns:
        Tuple of objects after all the threating was done.
    '''

    return tuple(handle_list(item))


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

        if key == 'class':
            continue

        # more classes to take care of
        if is_class(item):
            class_args[key] = construct(item)
            continue

        # threat lists
        if isinstance(item, list):
            class_args[key] = handle_list(item)
            continue

        # threat tuples
        try:
            obj = literal_eval(item)
            if isinstance(obj, tuple):
                class_args[key] = handle_tuple(obj)
            else:
                class_args[key] = obj

        # none of the above
        except Exception:
            class_args[key] = item







    bound_args = class_sig.bind(**class_args)
    bound_args.apply_defaults()

    return the_class(*bound_args.args, **bound_args.kwargs)
