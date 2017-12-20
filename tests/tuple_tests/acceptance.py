'''
Test created to check if the widgets that should accept lists can also accept
tuples in it's constructors.

Yes, they can.
But, for the markup in the urwid.Text widget, it won't work. The tuple of
tuples needs to be converted into a list
'''

import urwid

def exit_q(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()

t = [ urwid.Text(str(i) * 3) for i in range(5) ]
ts = [ ('weight', .5, i) for i in t ]
ts = tuple(ts)

print(ts)

cols = urwid.Columns(ts)

filler = urwid.Filler(cols)

loop = urwid.MainLoop(filler, unhandled_input=exit_q)
loop.run()
