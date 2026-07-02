import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_dif_txt(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is another text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a link node", TextType.LINK, "www.test.com")
        node2 = TextNode("This is a link node", TextType.LINK, "www.test.com")
        self.assertEqual(node, node2)

    def test_dif_url(self):
        node = TextNode("This is a link node", TextType.LINK, "www.testing.com")
        node2 = TextNode("This is another link node", TextType.LINK, "www.test.com")
        self.assertNotEqual(node, node2)

        

if __name__ == "__main__":
    unittest.main()
