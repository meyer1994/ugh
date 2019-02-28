from unittest import TestCase
from xml.dom import NotFoundErr

import ugh


class TestRoot(TestCase):
    def test_root(self):
        ''' Returns empty root '''
        xml = r'<ugh></ugh>'
        result = ugh.parse(xml)
        result = len(result)
        self.assertEqual(result, 0)

    def test_raises(self):
        ''' Raises error when root is not <ugh> '''
        with self.assertRaises(NotFoundErr):
            ugh.parse(r'<Button></Button>')
