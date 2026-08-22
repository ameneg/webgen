import unittest

from generate_page import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_strips_whitespace(self):
        self.assertEqual(extract_title("#    Padded title    "), "Padded title")

    def test_finds_title_among_other_lines(self):
        md = "some intro\n\n# The Real Title\n\nmore text"
        self.assertEqual(extract_title(md), "The Real Title")

    def test_ignores_lower_level_headings(self):
        md = "## Not this\n\n# This one\n\n### Nor this"
        self.assertEqual(extract_title(md), "This one")

    def test_no_h1_raises(self):
        with self.assertRaises(Exception):
            extract_title("## No h1 here\n\njust text")


if __name__ == "__main__":
    unittest.main()
