import urwid

import ugh

xml = r'''
<ugh>
    <ListBox>
        <SimpleFocusListWalker>
            <SelectableIcon text="Item 1" />
            <SelectableIcon text="Item 2" />
            <SelectableIcon text="Item 3" />
            <SelectableIcon text="Item 4" />
            <SelectableIcon text="Item 5" />
        </SimpleFocusListWalker>
    </ListBox>
</ugh>
'''

root = ugh.parse(xml)[0]
for i, wid in enumerate(root.body):
    root.body[i] = urwid.AttrMap(wid, None, focus_map='reversed')

reverse = ('reversed', 'standout', '')

loop = urwid.MainLoop(root, palette=[reverse])
loop.run()
