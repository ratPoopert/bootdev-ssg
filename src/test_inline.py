import unittest

from inline import (
    split_nodes_delimiter,
)
from textnode import TextNode, TextNodeType


class TestSplitNodesDelimiter(unittest.TestCase):

    def test_requires_list_of_textnodes(self):
        node = TextNode("A *single* TextNode", TextNodeType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter(node, "*", TextNodeType.ITALIC)
        nodes = ["Just a string"]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, "*", TextNodeType.ITALIC)

    def test_skips_nontext(self):
        nodes = [TextNode("italic text", TextNodeType.ITALIC)]
        self.assertListEqual(
            nodes,
            split_nodes_delimiter(nodes, "*", TextNodeType.ITALIC)
        )

    def test_requires_matching_delimiter(self):
        nodes = [
            TextNode("Missing a matching *italic delimiter", TextNodeType.TEXT)
        ]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, "*", TextNodeType.ITALIC)

    def test_split_nodes_delimiter_bold(self):
        nodes = [
            TextNode("A string with **bold** text", TextNodeType.TEXT),
            TextNode("Just regular text", TextNodeType.TEXT),
            TextNode("**Multiple** bold **words**", TextNodeType.TEXT),
            TextNode("**bold** **bold**", TextNodeType.TEXT),
        ]
        self.assertListEqual(
            [
                TextNode("A string with ", TextNodeType.TEXT),
                TextNode("bold", TextNodeType.BOLD),
                TextNode(" text", TextNodeType.TEXT),
                TextNode("Just regular text", TextNodeType.TEXT),
                TextNode("Multiple", TextNodeType.BOLD),
                TextNode(" bold ", TextNodeType.TEXT),
                TextNode("words", TextNodeType.BOLD),
                TextNode("bold", TextNodeType.BOLD),
                TextNode(" ", TextNodeType.TEXT),
                TextNode("bold", TextNodeType.BOLD),
            ],
            split_nodes_delimiter(nodes, "**", TextNodeType.BOLD)
        )

    def test_split_nodes_delimiter_italic(self):
        nodes = [
            TextNode("A string with *italic* text", TextNodeType.TEXT),
            TextNode("Just regular text", TextNodeType.TEXT),
            TextNode("*Multiple* italic *words*", TextNodeType.TEXT),
            TextNode("*italic* *italic*", TextNodeType.TEXT),
        ]
        self.assertListEqual(
            [
                TextNode("A string with ", TextNodeType.TEXT),
                TextNode("italic", TextNodeType.ITALIC),
                TextNode(" text", TextNodeType.TEXT),
                TextNode("Just regular text", TextNodeType.TEXT),
                TextNode("Multiple", TextNodeType.ITALIC),
                TextNode(" italic ", TextNodeType.TEXT),
                TextNode("words", TextNodeType.ITALIC),
                TextNode("italic", TextNodeType.ITALIC),
                TextNode(" ", TextNodeType.TEXT),
                TextNode("italic", TextNodeType.ITALIC),
            ],
            split_nodes_delimiter(nodes, "*", TextNodeType.ITALIC)
        )

    def test_split_nodes_delimiter_code(self):
        nodes = [
            TextNode("A string with `code` text", TextNodeType.TEXT),
            TextNode("Just regular text", TextNodeType.TEXT),
            TextNode("`Multiple` code `words`", TextNodeType.TEXT),
            TextNode("`code` `code`", TextNodeType.TEXT),
        ]
        self.assertListEqual(
            [
                TextNode("A string with ", TextNodeType.TEXT),
                TextNode("code", TextNodeType.CODE),
                TextNode(" text", TextNodeType.TEXT),
                TextNode("Just regular text", TextNodeType.TEXT),
                TextNode("Multiple", TextNodeType.CODE),
                TextNode(" code ", TextNodeType.TEXT),
                TextNode("words", TextNodeType.CODE),
                TextNode("code", TextNodeType.CODE),
                TextNode(" ", TextNodeType.TEXT),
                TextNode("code", TextNodeType.CODE),
            ],
            split_nodes_delimiter(nodes, "`", TextNodeType.CODE)
        )
