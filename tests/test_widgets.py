from unittest import TestCase

import urwid

from ugh import ugh


class TestWidgets(TestCase):
    def test_text(self):
        ''' Generate text widget '''
        xml = r'<ugh> <Text> Test </Text> </ugh>'
        result = ugh(xml)[0]
        self.assertIsInstance(result, urwid.Text)
        self.assertEqual(result.text, 'Test')

    def test_aatributes(self):
        xml = r'<ugh> <Text align="left" wrap="any"> Test </Text> </ugh>'
        result = ugh(xml)[0]
        self.assertIsInstance(result, urwid.Text)
        self.assertEqual(result.align, 'left')
        self.assertEqual(result.wrap, 'any')
        self.assertEqual(result.text, 'Test')
