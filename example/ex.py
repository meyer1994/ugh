import urwid
import json

import ugh

with open('test.json', 'r') as f:
    templ = json.load(f)

def exit_q(key):
    if key == 'q':
        raise urwid.ExitMainLoop()

palette = [
    ('banner', 'black', 'light gray'),
    ('streak', 'black', 'dark red'),
    ('bg', 'black', 'dark blue') ]

t = ugh.construct(templ)
loop = urwid.MainLoop(t, palette, unhandled_input=exit_q)
loop.run()
