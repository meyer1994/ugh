import urwid
import json

import ugh

'''
This example is a little bit more complex. It shows the use of multiple
attributes with multiple widgets.

Press 'q' to exit.
'''

def exit_q(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()

json_string = '''
{
    "class": "ListBox",
    "body": [
        {
            "class": "Text",
            "markup": [ "bg", "frst line" ]
        },
        {
            "class": "Button",
            "label": "Second line (button)"
        },
        {
            "class": "Columns",
            "widget_list": [
                {
                    "class": "Text",
                    "markup": [ "banner", "third line, part 1/3" ]
                },
                {
                    "class": "Text",
                    "markup": [ "streak", "third line, part 2/3" ]
                },
                {
                    "class": "Text",
                    "markup": [ "banner", "third line, part 3/3" ]
                }
            ]
        }
    ]
}
'''

palette = [
    ('banner', 'black', 'light gray'),
    ('streak', 'black', 'dark red'),
    ('bg', 'black', 'dark blue') ]

w_dict = json.loads(json_string)
t = ugh.construct(w_dict)
loop = urwid.MainLoop(t, palette, unhandled_input=exit_q)
loop.run()
