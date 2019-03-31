import urwid

import ugh

xml = r'''
<ugh>
    <Filler>
        <Pile>
            <Text id="counter" markup="0" align="center" />
            <Button label="+1" on_press="count_up"/>
        </Pile>
    </Filler>
</ugh>
'''


def count_up(button, data):
    data['value'] += 1
    val = str(data['value'])
    text = ugh.by_id('counter')
    text.set_text(val)


data = {'value': 0}

root = ugh.parse(xml, [count_up], data)[0]
loop = urwid.MainLoop(root)
loop.run()
