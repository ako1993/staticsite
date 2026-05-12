import unittest
from utils import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
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
        
class TestRegexForLinks(unittest.TestCase):
    def test_regex_function_images(self):
        test_text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(test_text)
        self.assertEqual(result, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_regex_function_links(self):
        test_text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown_links(test_text)
        self.assertEqual(result, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_link_and_image(self):
        test_text = "Here is a ![image](https://example.com/img.png) and a [link](https://example.com)"
        result = extract_markdown_images(test_text)
        result.extend(extract_markdown_links(test_text))
        self.assertEqual(result, [("image", "https://example.com/img.png"),("link", "https://example.com")])


