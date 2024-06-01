import unittest

from textnode import TextNode, TextNodeType
from leafnode import LeafNode


class TestTextNode(unittest.TestCase):

    textnodes = [
        TextNode("This is a text node", TextNodeType.TEXT),
        TextNode("This is a link", TextNodeType.LINK, "google.com"),
        TextNode("This is a text node", TextNodeType.TEXT),
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
            "TextNode(This is a text node, TextNodeType.TEXT, None)",
            self.textnodes[0].__repr__()
        )
        self.assertEqual(
            "TextNode(This is a link, TextNodeType.LINK, google.com)",
            self.textnodes[1].__repr__()
        )

    def test_to_htmlnode_invalid(self):
        invalid = TextNode("Invalid text_type", "invalid")
        with self.assertRaises(ValueError):
            invalid.to_htmlnode()

    def test_to_htmlnode_text(self):
        self.assertEqual(
            LeafNode(None, "A text node"),
            TextNode("A text node", TextNodeType.TEXT).to_htmlnode()
        )

    def test_to_htmlnode_bold(self):
        self.assertEqual(
            LeafNode("b", "A bold node"),
            TextNode("A bold node", TextNodeType.BOLD).to_htmlnode()
        )

    def test_to_htmlnode_italic(self):
        self.assertEqual(
            LeafNode("i", "An italic node"),
            TextNode("An italic node", TextNodeType.ITALIC).to_htmlnode()
        )

    def test_to_htmlnode_code(self):
        self.assertEqual(
            LeafNode("code", "A code node"),
            TextNode("A code node", TextNodeType.CODE).to_htmlnode()
        )

    def test_to_htmlnode_link(self):
        self.assertEqual(
            LeafNode("a", "A link node", {'href': 'google.com'}),
            TextNode("A link node", TextNodeType.LINK,
                     "google.com").to_htmlnode()
        )

    def test_to_htmlnode_image(self):
        self.assertEqual(
            LeafNode("img", "", {
                     'src': 'image.png', 'alt': "An image node"}),
            TextNode("An image node", TextNodeType.IMAGE,
                     'image.png').to_htmlnode()
        )


if __name__ == "__main__":
    unittest.main()
