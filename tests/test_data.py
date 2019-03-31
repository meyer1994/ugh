from unittest import TestCase

import urwid

import ugh


class TestData(TestCase):
    def test_callback(self):
        ''' Correctly assigns callbacks and data '''
        def callback(): pass
        xml = r'''
        <ugh>
            <Button label="B" on_press="py:callback" user_data="py:True"/>
            <Button label="B" on_press="py:callback" user_data="py:'False'"/>
            <Button label="B" on_press="py:callback" user_data="py:1"/>
            <Button label="B" on_press="py:callback" user_data="py:-1.1"/>
            <Button label="B" on_press="py:callback" user_data="py:'1.1'"/>
            <Button label="B" on_press="py:callback" user_data="py:''"/>
            <Button label="B" on_press="py:callback" user_data="py:None"/>
            <Button label="B" on_press="py:callback" user_data="py:[1, '2']"/>
            <Button label="B" on_press="py:callback" user_data="py:(1, '2')"/>
            <Button label="B" on_press="py:callback" user_data="py:{1, '2'}"/>
            <Button label="B" on_press="py:callback" user_data="py:{'': '2'}"/>
        </ugh>
        '''
        data = {
            'callback': callback
        }
        results = ugh.parse(xml, data)
        expected = [
            True,
            'False',
            1,
            -1.1,
            '1.1',
            '',
            None,
            [1, '2'],
            (1, '2'),
            {1, '2'},
            {'': '2'}
        ]

        for button, val in zip(results, expected):
            self.assertIsInstance(button, urwid.Button)
            self.assertIs(button._urwid_signals['click'][0][1], callback)
            self.assertEqual(button._urwid_signals['click'][0][2], val)

    def test_invalid_data(self):
        ''' Raises ValueError when passing invalid data '''
        def callback(): pass
        xml = r'''
        <ugh>
            <Button label="B" on_press="py:callback" user_data="py:variable"/>
        </ugh>
        '''

        with self.assertRaises(ValueError):
            ugh.parse(xml)
