from unittest import TestCase

import ugh


class TestID(TestCase):
    def test_get_by_id(self):
        ''' Stores the elements by ID '''
        xml = r'''
            <ugh>
                <Filler id="filler">
                    <Pile id="pile">
                        <Text id="text" markup="Test" />
                    </Pile>
                </Filler>
            </ugh>'''

        result = ugh.parse(xml)[0]
        self.assertIs(result, ugh.by_id('filler'))

        result = result.body
        self.assertIs(result, ugh.by_id('pile'))

        result = result.contents[0][0]
        self.assertIs(result, ugh.by_id('text'))

    def test_double_id(self):
        ''' Raises KeyError when creating 2 elements with same id '''
        xml = r'''
            <ugh>
                <Text id="text" markup="Test"/>
                <Text id="text" markup="Test"/>
            </ugh>'''
        with self.assertRaises(KeyError):
            ugh.parse(xml)
