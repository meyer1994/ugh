# UGH
Use XML templates to create terminal UI with urwid

[![Build Status](https://travis-ci.org/meyer1994/ugh.svg?branch=master)](https://travis-ci.org/meyer1994/ugh)


PS: UGH does not mean anything. It is what I think when I need to use urwid (still better than curses).


## Usage:
1. Create an XML where the tags are names of urwid classes;
2. Define attributes to the tags based on the constructor parameters;
3. ?
4. Profit!

---

## Hello world

```python
import urwid

import ugh


def exit_q(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()


text = urwid.Text(markup="Hello")

xml = r'''
<ugh>
    <Filler body="py:text">
</ugh>
'''

root = ugh.parse(xml, text=text)[0]
loop = urwid.MainLoop(root, unhandled_input=exit_q)
loop.run()
```

## TODO
- ~~Handle lists and tuples.~~

   - ~~Better way to handle tuples.~~

- ~~Handle callbacks (it breaks everything, for now).~~
