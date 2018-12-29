from unittest import TestCase

import urwid

from ugh.classes import get_class


class TestClasses(TestCase):
    def test_get_class(self):
        ''' Returns a class from string '''
        result = get_class('Button')
        expected = urwid.Button
        self.assertIs(result, expected)

    def test_get_class_raises(self):
        ''' Raises KeyError when non existent class is passed '''
        with self.assertRaises(KeyError):
            get_class('SomeClass')
