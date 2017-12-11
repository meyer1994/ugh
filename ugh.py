import inspect
import json

import urwid


# will hold the dictionary containing all the classes of the urwid module
CLASSES = dict(inspect.getmembers(urwid, inspect.isclass))

# get file
with open('test.json', 'r') as f:
    json_dict = json.load(f)


def construct(items_dict):

    the_class = items_dict['class']
    the_class = CLASSES[the_class]

    class_sig = inspect.signature(the_class)
    class_set = set(dir(the_class))

    class_args = {}

    for key, item in items_dict.items():

        if key in class_sig.parameters:
            # there is more classes to take care of
            if isinstance(item, dict):
                class_args[key] = construct(item)
            else:
                class_args[key] = item

    bound_args = class_sig.bind(**class_args)
    bound_args.apply_defaults()

    return the_class(*bound_args.args, **bound_args.kwargs)

t = construct(json_dict)
