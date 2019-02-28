from unittest import TestCase

import urwid

import ugh


class TestWidgets(TestCase):
    def test_text(self):
        ''' Generate text widget '''
        xml = r'<ugh> <Text markup="Test"/> </ugh>'
        result = ugh.parse(xml)[0]
        self.assertIsInstance(result, urwid.Text)
        self.assertEqual(result.text, 'Test')

    def test_attributes(self):
        ''' Attributes are created correctly '''
        xml = r'<ugh> <Text markup="Test" align="left" wrap="any"/> </ugh>'
        result = ugh.parse(xml)[0]
        self.assertIsInstance(result, urwid.Text)
        self.assertEqual(result.align, 'left')
        self.assertEqual(result.wrap, 'any')
        self.assertEqual(result.text, 'Test')

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
        result = ugh.parse(xml)[0]

        # pile
        self.assertIsInstance(result, urwid.Pile)
        self.assertEqual(len(result.contents), 3)

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
        self.assertEqual(len(cols.contents), 1)

        # columns-text
        text = cols.contents[0][0]
        self.assertIsInstance(text, urwid.Text)
        self.assertEqual(text.text, 'Column')
