import unittest
from utils import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
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


class TestLinkandImageExtraction(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_partial_image(self):
        node = TextNode("This one has an ![almost image](www.fake.com hopefully this passes", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [TextNode("This one has an ![almost image](www.fake.com hopefully this passes", TextType.TEXT)])


    def test_partial_link(self):
        node = TextNode("This one has an [almost link](www.fake.com hopefully this passes", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [TextNode("This one has an [almost link](www.fake.com hopefully this passes", TextType.TEXT)])

    def test_non_texttype(self):
        node = TextNode("This one is **bold**", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [TextNode("This one is **bold**", TextType.BOLD)])

class TestTexttoTextNode(unittest.TestCase):
    def test_multiple_types(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        self.assertEqual(result, [
    TextNode("This is ", TextType.TEXT),
    TextNode("text", TextType.BOLD),
    TextNode(" with an ", TextType.TEXT),
    TextNode("italic", TextType.ITALIC),
    TextNode(" word and a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" and an ", TextType.TEXT),
    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
    TextNode(" and a ", TextType.TEXT),
    TextNode("link", TextType.LINK, "https://boot.dev"),
        ])
    def test_bold_and_italic(self):
        text = "Here is a string with **bold text** and _italic text_"
        result = text_to_textnodes(text)
        self.assertEqual(result, [TextNode("Here is a string with ", TextType.TEXT),
                                  TextNode("bold text", TextType.BOLD),
                                  TextNode(" and ", TextType.TEXT),
                                  TextNode("italic text", TextType.ITALIC)])