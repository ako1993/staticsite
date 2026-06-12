import unittest
from extract_title import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        md = "# Hello"
        result = extract_title(md)
        self.assertEqual(result, "Hello")

    def test_extract_title_multiline(self):
        md = """
            Here is a markdown
            with multiple lines
            # But the title is at the bottom!
        

            """
        result = extract_title(md)
        self.assertEqual(result, "But the title is at the bottom!")
