import unittest
import json

import urwid

import ugh


class CallbackTest(unittest.TestCase):

    def test_callback(self):
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

    def test_multiple_callbacks(self):
        '''
        Tests if multiple callbacks are correctly assigned.
        '''

        json_string = '''
        {
            "class": "Filler",
            "body": {
                "class": "Pile",
                "widget_list": [
                    {
                        "class": "Button",
                        "label": "my callback button",
                        "on_press": "my_callback"
                    }, {
                        "class": "Button",
                        "label": "my callback button",
                        "on_press": "my_callback"
                    }, {
                        "class": "Button",
                        "label": "my callback button",
                        "on_press": "my_callback"
                    }
                ]
            }
        }
        '''

        call = {'my_callback': lambda btn: btn.set_label('nice')}
        w_dict = json.loads(json_string)
        widget = ugh.construct(w_dict, call)

    def test_user_data(self):
        '''
        Tests if the user_data problem raises an exception
        '''

        json_string = '''
        {
            "class": "Button",
            "label": "my callback button",
            "on_press": "my_callback",
            "user_data": [12312312, "any data", {"lol": "what?"}]

        }
        '''

        call = {'my_callback': lambda btn: btn.set_label('nice')}
        w_dict = json.loads(json_string)
        with self.assertRaises(ValueError):
            ugh.construct(w_dict, call)
