'''
Test created to see the patterns used when passing callbacks for the button
widget.

The callback receives the button pressed as it's first argument. user_data
comes later.
'''

import urwid


def exit_q(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()


def btn_press(btn, w_txt):
    w_txt.set_text('clicked!')


txt = urwid.Text('nothing here')
btn = urwid.Button('click me', on_press=btn_press, user_data=txt)
pile = urwid.Pile(widget_list=[btn, txt])
fill = urwid.Filler(pile)

loop = urwid.MainLoop(fill, unhandled_input=exit_q)
loop.run()
