from unittest import TestCase

import urwid

from ugh import ugh


class TestWidgets(TestCase):
    def test_text(self):
        ''' Generate text widget '''
        xml = r'<ugh> <Text markup="Test"/> </ugh>'
        result = ugh(xml)[0]
        self.assertIsInstance(result, urwid.Text)
        self.assertEqual(result.text, 'Test')

    def test_attributes(self):
        ''' Attributes are created correctly '''
        xml = r'<ugh> <Text markup="Test" align="left" wrap="any"/></ugh>'
        result = ugh(xml)[0]
        self.assertIsInstance(result, urwid.Text)
        self.assertEqual(result.align, 'left')
        self.assertEqual(result.wrap, 'any')
        self.assertEqual(result.text, 'Test')

    def test_values(self):
        ''' Should convert attributes to python values '''
        xml = r'''
        <ugh>
            <Button label="text" on_press="func" user_data="True"/>
        </ugh>
        '''
        kwargs = {
            'text': 'Some Text',
            'func': lambda t: None
        }
        result = ugh(xml, **kwargs)[0]
        self.assertIsInstance(result, urwid.Button)
        self.assertEqual(result.label, 'Some Text')

    def test_complex(self):
        ''' Generates complex widgets '''
        xml = r'''
        <ugh>
            <Pile>
                <Button label="Button"/>
                <Text markup="Text"/>
                <Columns>
                    <Text markup="Column"/>
                </Columns>
            </Pile>
        </ugh>
        '''
        result = ugh(xml)[0]

        # button
        button = result.contents[0][0]
        self.assertIsInstance(button, urwid.Button)
        self.assertEqual(button.label, 'Button')

        # text
        text = result.contents[1][0]
        self.assertIsInstance(text, urwid.Text)
        self.assertEqual(text.text, 'Text')

        # columns
        cols = result.contents[2][0]
        self.assertIsInstance(cols, urwid.Columns)

        # columns-text
        text = cols.contents[0][0]
        self.assertIsInstance(text, urwid.Text)
        self.assertEqual(text.text, 'Column')

    def test_callback(self):
        ''' Correctly assigns callbacks '''
        def callback(): pass
        data = ['some', 'list']

        xml = r'''
        <ugh>
            <Button label="Test" on_press="callback" user_data='data'/>
        </ugh>
        '''
        result = ugh(xml, callback=callback, data=data)[0]
        self.assertIsInstance(result, urwid.Button)
        # god this part is ugly
        self.assertIs(result._urwid_signals['click'][0][1], callback)
        self.assertIs(result._urwid_signals['click'][0][2], data)
