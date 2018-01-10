'''
Test created to see if a tuple inserted in the place of a list would be
converted to list after it is passed to the constructor.

Yes, it will.
That is a good behavior, at least I think.
'''

import urwid

texts = [urwid.Text('nice%2d' % i) for i in range(10)]
texts = tuple(texts)


def exit_q(key):
    if key == 'q':
        raise urwid.ExitMainLoop()


pile = urwid.Pile(texts)

q = pile.contents
print(isinstance(q, list))
