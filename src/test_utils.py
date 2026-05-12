import unittest
from utils import split_nodes_delimiter
from textnode import TextType, TextNode

class TestDelimiter(unittest.TestCase):
    def test_bold(self):
        test_list = [TextNode("My name is earl", TextType.TEXT),
                     TextNode("This has **bold** text", TextType.TEXT)]
        result = split_nodes_delimiter(test_list, "**", TextType.BOLD)
        self.assertEqual(result, [TextNode("My name is earl", TextType.TEXT),
                                  TextNode("This has ", TextType.TEXT),
                                  TextNode("bold", TextType.BOLD),
                                  TextNode(" text", TextType.TEXT)])
        
    def test_hanging_delimiter(self):
        test_list = [TextNode("Here is some text with a _hanging delimiter", TextType.TEXT)]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(test_list, "_", TextType.ITALIC)

    def test_code(self):
        test_list = [TextNode("My name is earl", TextType.TEXT),
                     TextNode("This has `code` text", TextType.TEXT)]
        result = split_nodes_delimiter(test_list, "`", TextType.CODE)
        self.assertEqual(result, [TextNode("My name is earl", TextType.TEXT),
                                  TextNode("This has ", TextType.TEXT),
                                  TextNode("code", TextType.CODE),
                                  TextNode(" text", TextType.TEXT)])

    def test_two_delimiter_pairs(self):
        test_list = [TextNode("this sentence **has** two **bold** parts", TextType.TEXT)]
        result = split_nodes_delimiter(test_list, "**", TextType.BOLD)
        self.assertEqual(result, [TextNode("this sentence ", TextType.TEXT),
                                  TextNode("has", TextType.BOLD),
                                  TextNode(" two ", TextType.TEXT),
                                  TextNode("bold", TextType.BOLD),
                                  TextNode(" parts", TextType.TEXT)])
        
    def test_three_delimiter_pairs(self):
        test_list = [TextNode("Hello I _have a lot_ of different _parts that are_ markdown just _so you know_", TextType.TEXT)]
        result = split_nodes_delimiter(test_list, "_", TextType.ITALIC)
        self.assertEqual(result, [TextNode("Hello I ", TextType.TEXT),
                                  TextNode("have a lot", TextType.ITALIC),
                                  TextNode(" of different ", TextType.TEXT),
                                  TextNode("parts that are", TextType.ITALIC),
                                  TextNode(" markdown just ", TextType.TEXT),
                                  TextNode("so you know", TextType.ITALIC),
                                  TextNode("", TextType.TEXT)])
        

    def test_three_delimiter_pairs_with_hanging_delimiter(self):
        test_list = [TextNode("Hello I _have a lot of different _parts that are_ markdown just _so you know_", TextType.TEXT)]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(test_list, "_", TextType.ITALIC)

    def test_two_delimiters(self):
        test_list = [(TextNode("**bold** and _italic_", TextType.TEXT))]
        result = split_nodes_delimiter(test_list, "**", TextType.BOLD)
        result = split_nodes_delimiter(result, "_", TextType.ITALIC)
        self.assertEqual(result, [TextNode("", TextType.TEXT),
                                  TextNode("bold", TextType.BOLD),
                                  TextNode(" and ", TextType.TEXT),
                                  TextNode("italic", TextType.ITALIC),
                                  TextNode("", TextType.TEXT)])
