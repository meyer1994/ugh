import unittest
import json

import urwid

import ugh


class CallbackTest(unittest.TestCase):

    def test_simple_callback(self):
        '''
        Tests if a simple callback, with only the button itself, works.
        '''
        json_string = '''
        {
            "class": "Filler",
            "body": {
                "class": "Button",
                "id": "btn",
                "label": "my callback button",
                "on_press": "my_callback"
            }
        }
        '''

        call = {'my_callback': lambda btn: btn.set_label('nice')}
        w_dict = json.loads(json_string)
        widget = ugh.construct(w_dict, call)
        self.assertEqual(ugh.ids['btn'].label, 'nice')
