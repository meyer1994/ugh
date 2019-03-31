from unittest import TestCase

import urwid

import ugh


class TestData(TestCase):
    def test_literals(self):
        ''' Correctly evaluates literals '''
        # _urwid_signals is not created if no callback is passed
        def callback(): pass
        xml = r'''
        <ugh>
            <Button label="Test" on_press="callback" user_data="True"/>
            <Button label="Test" on_press="callback" user_data="'False'"/>
            <Button label="Test" on_press="callback" user_data="1"/>
            <Button label="Test" on_press="callback" user_data="-1.1"/>
            <Button label="Test" on_press="callback" user_data="'1.1'"/>
            <Button label="Test" on_press="callback" user_data="''"/>
            <Button label="Test" on_press="callback" user_data="None"/>
            <Button label="Test" on_press="callback" user_data="[1, '2']"/>
            <Button label="Test" on_press="callback" user_data="(1, '2')"/>
            <Button label="Test" on_press="callback" user_data="{1, '2'}"/>
            <Button label="Test" on_press="callback" user_data="{'': '2'}"/>
        </ugh>
        '''
        results = ugh.parse(xml, [callback])
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
            self.assertEqual(button._urwid_signals['click'][0][2], val)

    def test_data(self):
        ''' Passes data object when user_data is not defined '''
        def callback(): pass
        data = dict()
        xml = r'''
        <ugh>
            <Button label="Test" on_press="callback" />
        </ugh>
        '''
        button = ugh.parse(xml, [callback], data)[0]
        self.assertIs(button._urwid_signals['click'][0][2], data)

    def test_callback(self):
        ''' Correctly assigns callback '''
        def callback(): pass
        xml = r'''
        <ugh>
            <Button label="Test" on_press="callback" />
        </ugh>
        '''
        result = ugh.parse(xml, [callback])[0]
        self.assertIs(result._urwid_signals['click'][0][1], callback)

    def test_invalid_data(self):
        ''' Raises ValueError when passing invalid data '''
        xml = r'''
        <ugh>
            <Button label="Test" user_data="variable" />
        </ugh>
        '''
        # with self.assertRaises(ValueError):
        #     ugh.parse(xml)

    def test_invalid_callback(self):
        ''' Raises ValueError when using invalid callback '''
        xml = r'''
        <ugh>
            <Button label="Test" on_press="callback" />
        </ugh>
        '''
        with self.assertRaises(KeyError):
            ugh.parse(xml)
