import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def test_props_to_html_returns_empty_string_when_props_are_None(self):
        node = HTMLNode("tag", "value", "children", None)
        result = node.props_to_html()
        self.assertEqual(result, "")

    def test_props_to_html_returns_empty_string_when_props_are_empty(self):
        node = HTMLNode("tag", "value", "children", "")
        result = node.props_to_html()
        self.assertEqual(result, "")

