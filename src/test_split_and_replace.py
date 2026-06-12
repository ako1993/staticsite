import unittest
from split_and_replace import split_and_replace

class TestSplitandReplace(unittest.TestCase):
    def test_replacement(self):
        text = "Keep it simple {{ Title }}"
        result = split_and_replace(text, "body", "title")
        self.assertEqual(result, "Keep it simple title")

    def test_replacement_with_content_and_title(self):
        text = "Keep it simple {{ Title }}. There's also some {{ Content }}"
        result = split_and_replace(text, "body", "title")
        self.assertEqual(result, "Keep it simple title. There's also some body")




    