from unittest import TestCase
from tempfile import NamedTemporaryFile
from xml.dom import NotFoundErr

import ugh


class TestRoot(TestCase):
    def test_root(self):
        ''' Returns empty root '''
        xml = r'<ugh></ugh>'
        result = ugh.parse(xml)
        self.assertEqual(len(result), 0)

    def test_file(self):
        ''' Parses from file '''
        xml = r'<ugh></ugh>'
        with NamedTemporaryFile(mode='w') as file:
            file.write(xml)
            file.flush()
            result = ugh.parse_file(file.name)

        self.assertEqual(len(result), 0)

    def test_raises(self):
        ''' Raises error when root is not <ugh> '''
        with self.assertRaises(NotFoundErr):
            ugh.parse(r'<Button></Button>')
