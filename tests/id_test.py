import unittest
import json

import urwid

import ugh


class IdTest(object):

    def test_ids(self):
        '''
        Tests the id management implementation of ugh.

        Every widget with an id key in it's json should be included in the ids
        dictionary.
        '''

        json_string = '''
        {
            "class": "Pile",
            "widget_list": [
                {
                    "class": "Columns",
                    "id": 1,
                    "widget_list": [
                        { "class": "Button", "label": "btn0" },
                        { "class": "Button", "label": "btn1" },
                        { "class": "Button", "label": "btn2" },
                        { "class": "Button", "label": "btn3" },
                        {
                            "class": "Columns",
                            "id": 2,
                            "widget_list": [
                                { "class": "Button", "label": "btn0" },
                                { "class": "Button", "label": "btn1" },
                                { "class": "Button", "label": "btn2" },
                                { "class": "Button", "label": "btn3" }
                            ]
                        }
                    ]
                }
            ]
        }
        '''

        w_dict = json.loads(json_string)
        widget = ugh.construct(w_dict)
        print(ugh.ids)
        self.assertTrue(1 in ugh.ids)
        self.assertTrue(2 in ugh.ids)

        i = 0
        for w, _ in ugh.ids[1].contents:
            if not isinstance(w, urwid.Columns):
                self.assertEqual(w.label, f'btn{i}')
                i += 1

        i = 0
        for w, _ in ugh.ids[2].contents:
            self.assertEqual(w.label, f'btn{i}')
            i += 1
