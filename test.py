#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
#
# Created:  2015-02-14
#

import checker

import unittest

class TestHtmlTagIterator(unittest.TestCase):

    def test_parse_simple_html(self):
        document = '<a href="test">doc</a>'
        ite = checker.HtmlTagIterator(document)
        self.assertEqual(ite.next().value, '<a href="test">')
        self.assertEqual(ite.next().value, '</a>')

        self.assertRaises(StopIteration, ite.next)


class TestHtmlTag(unittest.TestCase):

    def test_open_tag(self):
        self.assertTrue(checker.HtmlTag('<a>').open_tag)
        self.assertTrue(checker.HtmlTag('<a href="#">').open_tag)
        self.assertTrue(checker.HtmlTag('< a href="#">').open_tag)
        self.assertTrue(checker.HtmlTag('<div>').open_tag)

    def test_close_tag(self):
        self.assertTrue(checker.HtmlTag('</a>').close_tag)
        self.assertTrue(checker.HtmlTag('</ a>').close_tag)
        self.assertTrue(checker.HtmlTag('< / a>').close_tag)
        self.assertTrue(checker.HtmlTag('< / a >').close_tag)
        self.assertTrue(checker.HtmlTag('</div>').close_tag)

    def test_kind_close_tag(self):
        self.assertEqual(checker.HtmlTag('</div>').kind, 'div')
        self.assertEqual(checker.HtmlTag('< / div>').kind, 'div')
        self.assertEqual(checker.HtmlTag('< /div>').kind, 'div')
        self.assertEqual(checker.HtmlTag('< /a >').kind, 'a')
        self.assertEqual(checker.HtmlTag('</div>').kind, 'div')
        self.assertEqual(checker.HtmlTag('< / div >').kind, 'div')

    def test_kind_open_tag(self):
        self.assertEqual(checker.HtmlTag('<div>').kind, 'div')
        self.assertEqual(checker.HtmlTag('<div>').kind, 'div')
        self.assertEqual(checker.HtmlTag('<div class="clazz">').kind, 'div')

    def test_match(self):
        self.assertTrue(checker.HtmlTag('<div>').match(checker.HtmlTag('</div>')))
        self.assertTrue(checker.HtmlTag('</div>').match(checker.HtmlTag('<div>')))
        self.assertTrue(checker.HtmlTag('<div class="fuga">').match(checker.HtmlTag('</div>')))
        self.assertTrue(checker.HtmlTag('<a href="#">').match(checker.HtmlTag('</a>')))


    def test_match_fail_not_match_tag(self):
        self.assertFalse(checker.HtmlTag('<div>').match(checker.HtmlTag('</p>')))
        self.assertFalse(checker.HtmlTag('</div>').match(checker.HtmlTag('<p>')))

    def test_match_fail_both_close(self):
        self.assertFalse(checker.HtmlTag('</div>').match(checker.HtmlTag('</div>')))

    def test_match_fail_both_open(self):
        self.assertFalse(checker.HtmlTag('<div>').match(checker.HtmlTag('<div>')))
    

if __name__ == '__main__':
    unittest.main()
