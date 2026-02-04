import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_is_none(self):
        node = TextNode("This is a test node", TextType.PLAIN)
        self.assertEqual(node.url, None)

    def test_that_text_types_are_different(self):
        node1 = TextNode("This is a plain node", TextType.CODE)
        node2 = TextNode("This is a link node", TextType.LINK, "www.link.com")
        self.assertNotEqual(node1.text_type, node2.text_type)

    def test_that_link_urls_are_different(self):
        node1 = TextNode("This is link 1", TextType.LINK, "www.site1.com")
        node2 = TextNode("This is link 2", TextType.LINK, "www.site2.com")
        self.assertNotEqual(node1.url, node2.url)


if __name__ == "__main__":
    unittest.main()