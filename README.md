# UGH
Use JSON templates to create terminal UI with urwid

[![Build Status](https://travis-ci.org/meyer1994/ugh.svg?branch=master)](https://travis-ci.org/meyer1994/ugh)

PS: UGH does not mean anything. It is what I think when I need to use urwid (still better than curses). Ok. Maybe the 'U' means 'urwid'...


## Usage:
1. Define the `class` attribute with the name of the class you want to use;
2. Define the variables of the constructor as if you were coding it normally;
3. ????
4. Profit?

[text.py](examples/text.py)
```python
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

palette = [ ('streak', 'black', 'dark red') ]
w_dict = json.loads(json_string)
t = ugh.construct(w_dict)
loop = urwid.MainLoop(t, palette, unhandled_input=exit_q)
loop.run()

```

## TODO
- ~~Handle lists and tuples.~~
-- Better way to handle tuples.
- Handle callbacks (it breaks everything, for now).
