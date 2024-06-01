import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    nodes = [
        HTMLNode("p", "This is a paragraph"),
        HTMLNode("p", "This is a paragraph", None, []),
        HTMLNode("a", "a link", None, {
            "href": "google.com",
            "target": "_blank",
        }),
        HTMLNode("div", None, [
            HTMLNode("p", "First child"),
            HTMLNode("p", "Second child"),
        ], None)
    ]

    def test_to_html(self):
        with self.assertRaises(NotImplementedError):
            self.nodes[0].to_html()

    def test_props_to_html(self):
        self.assertEqual(
            "",
            self.nodes[0].props_to_html()
        )

        with self.assertRaises(ValueError):
            self.nodes[1].props_to_html()

        self.assertEqual(
            " href=\"google.com\" target=\"_blank\"",
            self.nodes[2].props_to_html()
        )

    def test_repr(self):
        self.assertEqual(
            "HTMLNode(p, This is a paragraph, None, None)",
            self.nodes[0].__repr__()
        )
        self.assertEqual(
            "HTMLNode(a, a link, None, {'href': 'google.com', 'target': '_blank'})",
            self.nodes[2].__repr__()
        )

        self.assertEqual(
            "HTMLNode(div, None, ["
            + "HTMLNode(p, First child, None, None), "
            + "HTMLNode(p, Second child, None, None)"
            + "], None)",
            self.nodes[3].__repr__()
        )
