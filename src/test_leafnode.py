import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):

    def test_to_html(self):
        node = LeafNode(None, None)
        with self.assertRaises(ValueError):
            node.to_html()
        node.value = "A simple paragraph"
        self.assertEqual(
            "A simple paragraph",
            node.to_html()
        )
        node.tag = "p"
        self.assertEqual(
            "<p>A simple paragraph</p>",
            node.to_html()
        )
