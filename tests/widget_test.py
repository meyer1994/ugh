import unittest
import json

import urwid

import ugh


class WidgetTest(unittest.TestCase):

    def test_simple_widgets(self):
        '''
        Simple test that verifies the creation of simple widgets.

        Simple widgets are widgets that do not need other widgets for it to be
        created. For example: Text and Button widgets. A Filler, List etc.
        widgets need some widget to be passed in the cosntructor for it to be
        created.
        '''

        json_string = '''
        {
            "text1": {
                "class": "Text",
                "markup": "nice",
                "align": "center"
            },
            "text2": {
                "class": "Text",
                "markup": "not nice",
                "align": "left"
            },
            "button1": {
                "class": "Button",
                "label": "this button"
            },
            "button2": {
                "class": "Button",
                "label": "other button"
            }
        }
        '''
        w_dict = json.loads(json_string)

        for key, item in w_dict.items():
            w_dict[key] = ugh.construct(item)

        # easier reading
        t1 = w_dict['text1']
        t2 = w_dict['text2']
        b1 = w_dict['button1']
        b2 = w_dict['button2']

        # types
        self.assertTrue(isinstance(t1, urwid.Text))
        self.assertTrue(isinstance(t2, urwid.Text))
        self.assertTrue(isinstance(b1, urwid.Button))
        self.assertTrue(isinstance(b2, urwid.Button))

        # properties
        self.assertEqual(t1.text, 'nice')
        self.assertEqual(t1.align, 'center')
        self.assertEqual(t2.text, 'not nice')
        self.assertEqual(t2.align, 'left')
        self.assertEqual(b1.label, 'this button')
        self.assertEqual(b2.label, 'other button')

    def test_text_attr(self):
        '''
        Test if attributes passed are properly loaded.
        '''

        json_string = '''
        {
            "class": "Text",
            "markup": [ "reversed", "nice" ]
        }
        '''

        w_dict = json.loads(json_string)
        text = ugh.construct(w_dict)

        # type
        self.assertTrue(isinstance(text, urwid.Text))

        # properties
        self.assertEqual(text.text, 'nice')
        # get_text() returns the the text and a tuple with the attribute and
        # size of the string
        attrs = [('reversed', 4)]
        txt = 'nice'
        self.assertEqual(text.get_text(), (txt, attrs))

    def test_composite_widgets(self):
        '''
        Test the creation of composite widgets.

        Composite widgets are widgets that receive some other widget in it's
        constructor. For example: Filler, WdigetPlaceholder etc.
        '''
        json_string = '''
        {
            "filler": {
                "class": "Filler",
                "body":
                {
                    "class": "AttrMap",
                    "w": {
                        "class": "Text",
                        "markup": "nice",
                        "align": "center"
                    },
                    "attr_map": "reversed"
                }
            },
            "padding": {
                "class": "Padding",
                "w":
                {
                    "class": "AttrMap",
                    "w": {
                        "class": "Text",
                        "markup": "nice",
                        "align": "center"
                    },
                    "attr_map": "reversed"
                }
            },
            "placeholder": {
                "class": "WidgetPlaceholder",
                "original_widget": {
                    "class": "Button",
                    "label": "nice"
                }
            }
        }
        '''
        w_dict = json.loads(json_string)

        filler = ugh.construct(w_dict['filler'])
        filler_text = filler.original_widget.original_widget
        padding = ugh.construct(w_dict['padding'])
        padding_text = padding.original_widget.original_widget
        placeholder = ugh.construct(w_dict['placeholder'])

        # types
        self.assertTrue(isinstance(filler, urwid.Filler))
        self.assertTrue(isinstance(filler.original_widget, urwid.AttrMap))
        self.assertTrue(isinstance(filler_text, urwid.Text))

        self.assertTrue(isinstance(padding, urwid.Padding))
        self.assertTrue(isinstance(padding.original_widget, urwid.AttrMap))
        self.assertTrue(isinstance(padding_text, urwid.Text))

        self.assertTrue(isinstance(placeholder, urwid.WidgetPlaceholder))
        self.assertTrue(isinstance(placeholder.original_widget, urwid.Button))

        # properties
        self.assertEqual(filler_text.text, 'nice')
        self.assertEqual(padding_text.text, 'nice')
        self.assertEqual(placeholder.original_widget.label, 'nice')

    def test_list_widgets(self):
        '''
        Tests the creation of widgets that receive lists of widgets in it's
        constructor.

        For example, the Pile widget. It receives a list of widgets, or tuples,
        with options for each widget.
        '''

        json_string = '''
        {
            "class": "Pile",
            "widget_list": [
                { "class": "Text", "markup": "nice0" },
                { "class": "Text", "markup": "nice1" },
                { "class": "Text", "markup": "nice2" },
                { "class": "Text", "markup": "nice3" }
            ]
        }
        '''

        w_dict = json.loads(json_string)
        pile = ugh.construct(w_dict)

        # types
        for w, _ in pile.contents:
            self.assertTrue(isinstance(w, urwid.Text))

        # properties
        i = 0
        for w, _ in pile.contents:
            self.assertEqual(w.text, f'nice{i}')
            i += 1

    def test_composite_list_widgets(self):
        '''
        Tests widgets that have widgets with lists of widgets in it.

        A multi-level test_list_widgets, basically.
        '''

        json_string = '''
        {
            "class": "Pile",
            "widget_list": [
                {
                    "class": "Columns",
                    "widget_list": [
                        {
                            "class": "Text",
                            "markup": [
                                ["attr0", "text0"],
                                "text1",
                                ["attr2", "text2"]
                            ]
                        },
                        {
                            "class": "Button",
                            "label": "button"
                        },
                        {
                            "class": "Columns",
                            "widget_list": [
                                { "class": "Text", "markup": "text0"},
                                { "class": "Text", "markup": "text1"},
                                { "class": "Text", "markup": "text2"},
                                { "class": "Text", "markup": "text3"}
                            ]
                        }
                    ]
                }
            ]
        }
        '''

        w_dict = json.loads(json_string)
        pile = ugh.construct(w_dict)

        cols = pile.contents[0][0]
        self.assertTrue(isinstance(cols, urwid.Columns))

        text = cols.contents[0][0]
        self.assertTrue(isinstance(text, urwid.Text))
        txt = 'text0text1text2'
        self.assertEqual(text.text, txt)
        text_attrs = (txt, [("attr0", 5), (None, 5), ("attr2", 5)])
        self.assertEqual(text.get_text(), text_attrs)

        button = cols.contents[1][0]
        self.assertTrue(isinstance(button, urwid.Button))
        self.assertEqual(button.label, 'button')

        cols = cols.contents[2][0]
        self.assertTrue(isinstance(cols, urwid.Columns))
        for i, t in enumerate(cols.contents):
            self.assertEqual(t[0].text, f'text{i}')

    def test_multiple_text_attrs(self):
        '''
        Tests the widget Text when using multiple markup attributes to it's
        constructor.
        '''

        json_string = '''
        {
            "class": "Text",
            "markup": [
                [ "some_attr", "nice0 " ],
                "nice1 ",
                [ "other_attr", "nice2" ]
            ]
        }
        '''

        w_dict = json.loads(json_string)
        widget = ugh.construct(w_dict)

        text = widget.text
        correct_text = 'nice0 nice1 nice2'
        self.assertEqual(text, correct_text)

        attrs = widget.get_text()
        correct_attrs = (
            'nice0 nice1 nice2',
            [
                ('some_attr', 6),
                (None, 6),
                ('other_attr', 5)
            ]
        )
        self.assertEqual(attrs, correct_attrs)
