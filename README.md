# UGH
-----
Use JSON templates to create terminal UI with urwid
PS: UGH does not mean anything. It is what I think when I need to use urwid (still better than curses).

## Example

templ.json
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
