import urwid
import json

import ugh

'''
Simple example used to show a centered Text widget written 'nice' with red
background.

Press 'q' to exit.
'''


def exit_q(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()


json_string = '''
{
    "class": "Filler",
    "body": {
        "class": "AttrMap",
        "w": {
            "class": "Text",
            "markup": "nice",
            "align": "center"
        },
        "attr_map": "streak"
    }
}
'''

palette = [('streak', 'black', 'dark red')]
w_dict = json.loads(json_string)
t = ugh.construct(w_dict)
loop = urwid.MainLoop(t, palette, unhandled_input=exit_q)
loop.run()
