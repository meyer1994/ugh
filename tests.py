import unittest
import json

import urwid

import ugh


class UghTest(unittest.TestCase):

    def test_simple_widgets(self):
        '''
        Simple test that verifies the creation of simple widgets.

        Simple widgets are widgets that do not need other widgets for it to be
        created. For example: Text and Button widgets. A Filler, List etc.
        widgets need some widget to be passed in the cosntructor for it to be
        created.
        '''

        with open('tests/test_simple_widgets.json') as f:
            widgets_dict = json.load(f)

        for key, item in widgets_dict.items():
            widgets_dict[key] = ugh.construct(item)

        # easier reading
        t1 = widgets_dict['text1']
        t2 = widgets_dict['text2']
        b1 = widgets_dict['button1']
        b2 = widgets_dict['button2']

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

        with open('tests/test_text_attr.json') as f:
            text_dict = json.load(f)

        text = ugh.construct(text_dict)

        # type
        self.assertTrue(isinstance(text, urwid.Text))

        # properties
        self.assertEqual(text.text, 'nice')
        # get_text() returns the the text and a tuple with the attribute and
        # size of the string
        attrs = [ ('reversed', 4) ]
        txt = 'nice'
        self.assertEqual(text.get_text(), (txt, attrs))

    def test_composite_widgets(self):
        '''
        Test the creation of composite widgets.

        Composite widgets are widgets that receive some other widget in it's
        constructor. For example: Filler, WdigetPlaceholder etc.
        '''

        with open('tests/test_composite_widgets.json') as f:
            widgets_dict = json.load(f)

        filler = ugh.construct(widgets_dict['filler'])
        filler_text = filler.original_widget.original_widget
        padding = ugh.construct(widgets_dict['padding'])
        padding_text = padding.original_widget.original_widget
        placeholder = ugh.construct(widgets_dict['placeholder'])

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

        with open('tests/test_list_widgets.json') as f:
            widgets_dict = json.load(f)

        pile = ugh.construct(widgets_dict)

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

        with open('tests/test_composite_list_widgets.json') as f:
            widgets_dict = json.load(f)

        pile = ugh.construct(widgets_dict)

        cols = pile.contents[0][0]
        self.assertTrue(isinstance(cols, urwid.Columns))

        text = cols.contents[0][0]
        self.assertTrue(isinstance(text, urwid.Text))
        txt = 'text0text1text2'
        self.assertEqual(text.text, txt)
        text_attrs = (txt, [ ("attr0", 5), (None, 5), ("attr2", 5) ])
        self.assertEqual(text.get_text(), text_attrs)

        button = cols.contents[1][0]
        self.assertTrue(isinstance(button, urwid.Button))
        self.assertEqual(button.label, 'button')

        cols = cols.contents[2][0]
        self.assertTrue(isinstance(cols, urwid.Columns))
        for i, t in enumerate(cols.contents):
            self.assertEqual(t[0].text, f'text{i}')

    def test_multiple_text_attrs(self):

        with open('tests/test_multiple_text_attrs.json') as f:
            widgets_dict = json.load(f)

        widget = ugh.construct(widgets_dict)

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


if __name__ == '__main__':
    unittest.main()
