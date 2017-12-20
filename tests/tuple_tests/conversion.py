import urwid

texts = [ urwid.Text('nice%2d' % i) for i in range(10) ]
texts = tuple(texts)

def exit_q(key):
    if key == 'q':
        raise urwid.ExitMainLoop()

pile = urwid.Pile(texts)

q = pile.contents
print(isinstance(q, list))

