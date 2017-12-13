# UGH
Use JSON templates to create terminal UI with urwid

PS: UGH does not mean anything. It is what I think when I need to use urwid (still better than curses). Ok. Maybe the 'U' means 'urwid'...


## Usage:
1. Define the `class` attribute with the name of the class you want to use;
2. Define the variables of the constructor as if you were coding it normally;
3. ????
4. Profit?

[ex.py](https://github.com/meyer1994/ugh/blob/master/example/ex.py)
```python
import urwid
import json

import ugh

with open('templ.json', 'r') as f:
    templ = json.load(f)

t = ugh.construct(templ)
loop = urwid.MainLoop(t)
loop.run()

```

## Example:
[templ.json](https://github.com/meyer1994/ugh/blob/master/example/templ.json)
```json
{
    "class": "Filler",
    "body":
    {
        "class": "AttrMap",
        "w": {
            "class": "Text",
            "markup": "nice",
            "align": "center"
        },
        "attr_map": "bob"
    }
}
```


## TODO
- ~~Handle lists and tuples.~~
- Handle callbacks.
