import unittest

from parentnode import ParentNode
from htmlnode import HTMLNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):

    def test_is_htmlnode(self):
        node = ParentNode("div", [LeafNode("p", "paragraph")])
        self.assertIsInstance(node, HTMLNode)

    def test_requires_tag(self):
        node = ParentNode(None, [LeafNode("p", "paragraph")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_requires_children(self):
        nodes = [
            ParentNode("div", None),
            ParentNode("div", "This isn't a list"),
            ParentNode("div", []),
        ]
        for node in nodes:
            with self.assertRaises(ValueError):
                node.to_html()

    def test_to_html(self):
        node = ParentNode(
            "div",
            [
                LeafNode("p", "A paragraph"),
                LeafNode("a", "A link", {'href': 'google.com'}),
                ParentNode("div", [
                    LeafNode("p", "A nested paragraph"),
                ], {'class': 'wrapper'})
            ]
        )
        self.assertEqual(
            (
                '<div>'
                + '<p>A paragraph</p>'
                + '<a href="google.com">A link</a>'
                + '<div class="wrapper"><p>A nested paragraph</p></div>'
                + '</div>'
            ),
            node.to_html()
        )
