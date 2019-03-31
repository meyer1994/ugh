import urwid

import ugh

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
