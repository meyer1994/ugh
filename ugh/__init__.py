import inspect
import re

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


def is_callback(param_name):
    '''
    Checks if the item is an callback.

    Luckily for us, urwid team has a pattern of always putting the callbacks
    parameters in the constructors as 'on_press' or 'on_state_changed',
    'on_something'. Then, we just need to check if in the beginning of the
    string is the pattern 'on_'. When it has, we have a callback.

    Args:
        param_name: String containing the name of the parameter.

    Returns:
        True if there is 'on_' in the beginning of the string. False otherwise.
    '''

    return bool(re.match(r'(^on_)', param_name))


def handle_list(item, callbacks):
    '''
    Handles json objects that are lists.

    In urwid we have lists of things. Fortunately, urwid does not care too much
    about the type of list. We can use tuples for (mostly) everything. That is
    why this function threats all the lists and returns them all as tuples.
    There is no need to worry, urwid converts them back to lists when we insert
    them into some widget (see the acceptance.py in the tests folder).

    Args:
        item: Iterable of objects to be threated.
        callbacks: dict of callbacks. As our list may have other widgets that
            uses callbacks, we need to pass them as well.

    Returns:
        Tuple containing all the threated tuples. Note that this may have many
        levels of tuples of tuples in it. It depends of your application.
    '''

    lst = []
    for obj in item:
        # add widget
        if is_class(obj):
            lst.append(construct(obj, callbacks))
        # add list
        elif isinstance(obj, list):
            lst.append(handle_list(obj, callbacks))
        # add something else
        else:
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
            # if there is any tuple inside, it means that it should be a list
            # of markups
            if isinstance(i, tuple):
                return list(markup)

    return markup


def construct(items_dict, callbacks={}):
    '''
    Constructs the classes described in the dict.

    It will create all the classes described in the dictionary, normally
    obtained from a json. It does it in a recursive way. Which means,
    every time it finds a new dict in the items, with the 'class' key, it will
    call itself again with this, just found, dict as it's parameter.

    Note:
        The attributes used to set different markups for the widgets, specially
        the Text widget, are supposed to be already defined in a 'palette' that
        is passed to the main loop. If it is not defined, the program WILL NOT
        fail, it will simply execute without the attributes. This is an urwid
        strategy.
        We do not accept 'user_data' to be used in the json descriptions
        because it's treatment would be of bigger complexity than the project
        itself. So, if you want to use some more fancy callbacks with many
        parameters etc.  you should use urwid.connect_signal for that.

    Args:
        items_dict: dict of items to be created.
        callbacks: dict of callbacks. The keys are the names of the callbacks.

    Returns:
        The top widget described in items_dict with it's inner widgets all
        created and included in itself.

    Raises:
        ValuerError: When 'user_data' parameters have been set.
        KeyError: When there is repeated IDs.
    '''

    the_class = items_dict['class']
    the_class = CLASSES[the_class]
    class_sig = inspect.signature(the_class)
    # will store all the arguments to be used in the constructor
    class_args = {}

    for key, item in items_dict.items():

        # same implementation as android's setOnClickListener
        if key == 'user_data':
            raise ValueError('user_data not implemented. If you need to use '
                             'some more sophisticated callback, please, use '
                             'urwid.connect_signal')

        # class is threated before this loop
        # id is threated after this loop
        if key in ('class', 'id'):
            continue

        # more classes to take care of
        if is_class(item):
            class_args[key] = construct(item, callbacks)
            continue

        # callbacks
        if is_callback(key):
            class_args[key] = callbacks[item]
            continue

        # threat lists
        if isinstance(item, list):
            class_args[key] = handle_list(item, callbacks)
            continue

        class_args[key] = item

    # markup edge-case testing
    if 'markup' in class_args:
        markup = class_args['markup']
        class_args['markup'] = handle_markup(markup)

    # create constructor function
    bound_args = class_sig.bind(**class_args)
    bound_args.apply_defaults()
    constructed_class = the_class(*bound_args.args, **bound_args.kwargs)

    # save into ids dict
    if 'id' in items_dict:
        i = items_dict['id']
        # no repeated ids
        if i in ids:
            raise KeyError(f'Defined ID ({i}) already in use by {ids[i]}')
        ids[i] = constructed_class

    return constructed_class
