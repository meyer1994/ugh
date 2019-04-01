# UGH
Use XML templates to create terminal UI with urwid

[![Build Status](https://travis-ci.org/meyer1994/ugh.svg?branch=master)](https://travis-ci.org/meyer1994/ugh)
[![Code Coverage](https://codecov.io/gh/meyer1994/ugh/branch/master/graph/badge.svg)](https://codecov.io/gh/meyer1994/ugh)


## Usage:
1. Create an XML where the tags are names of urwid classes;
2. Define attributes to the tags based on the constructor parameters;
3. ?
4. Profit!

---

## Getting started

```python
import urwid

import ugh

# Same as
# Filler(Text('Hello world!', align='center'))
xml = r'''
<ugh>
    <Filler>
        <Text markup="Hello world!" align="center" />
    </Filler>
</ugh>
'''

root = ugh.parse(xml)[0]
loop = urwid.MainLoop(root)
loop.run()
```

## How it works

It is very simple actually. I just use the [ElementTree](https://docs.python.org/3/library/xml.etree.elementtree.html?highlight=element%20tree) library to do all the heavy work. The attributes of each element generated from the XML are passed to the respective Widget constructor as `args` and `kwargs`. This can be later improved. I've coded so it could be easily customized and adapted later.

For widgets with callbacks and `user_data` there is some things more. The data used in `user_data` is passed through `literal_eval`. If no data is passed in the `user_data`, or there is an evaluation error, the data dictionary passed into the `parse` function is assigned to it. This means that the widgets use a shared state.

The ID system that I use is simply a dictionary that is rebuild every time the `parse` function is called. The `by_id` method is a wrapper for `ids_store[id]`.

## TODO

- Implement handlers for all Widgets.
