import inspect
import json

import urwid


# will hold the dictionary containing all the classes of the urwid module
CLASSES = dict(inspect.getmembers(urwid, inspect.isclass))


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

    Raises:
        KeyError: if one of the args it's not part of the defined class'
        constructor.

    TODO:
        - Handle lists of widgets ('_list' in etc...)
        - Handle tuple (style, widget)
        - Handle callbacks (inspect + search for functions in some file)

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
        if isinstance(item, dict) and 'class' in item:
            class_args[key] = construct(item)
        else:
            try:
                class_args[key] = eval(item)
            except Exception as e:
                class_args[key] = eval("'%s'" % item)


    bound_args = class_sig.bind(**class_args)
    bound_args.apply_defaults()

    return the_class(*bound_args.args, **bound_args.kwargs)
