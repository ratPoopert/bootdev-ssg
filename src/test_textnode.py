import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):

    textnodes = [
        TextNode("This is a text node", "text"),
        TextNode("This is a link", "link", "google.com"),
        TextNode("This is a text node", "text"),
    ]

    def test_url(self):
        self.assertEqual(None, self.textnodes[0].url)

        self.assertEqual("google.com", self.textnodes[1].url)

    def test_eq(self):
        self.assertEqual(self.textnodes[0], self.textnodes[2])

    def test_neq(self):
        self.assertNotEqual(self.textnodes[0], self.textnodes[1])

    def test_repr(self):
        self.assertEqual(
            "TextNode(This is a text node, text, None)",
            self.textnodes[0].__repr__()
        )
        self.assertEqual(
            "TextNode(This is a link, link, google.com)",
            self.textnodes[1].__repr__()
        )


if __name__ == "__main__":
    unittest.main()
