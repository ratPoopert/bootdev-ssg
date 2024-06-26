import unittest

from inline import (
    text_to_textnodes,
    split_nodes_delimiter,
    split_nodes_images,
    split_nodes_links,
    extract_markdown_images,
    extract_markdown_links
)
from textnode import TextNode, TextNodeType


class TestTextToTextNodes(unittest.TestCase):

    def test_requires_string(self):
        with self.assertRaises(ValueError):
            text_to_textnodes([])

    def test_extracts_textnodes(self):
        self.assertListEqual(
            [
                TextNode("Just some text and some ", TextNodeType.TEXT),
                TextNode("bold", TextNodeType.BOLD),
                TextNode(" text and some ", TextNodeType.TEXT),
                TextNode("italic", TextNodeType.ITALIC),
                TextNode(" text and some ", TextNodeType.TEXT),
                TextNode("code", TextNodeType.CODE),
                TextNode(" and a ", TextNodeType.TEXT),
                TextNode("link", TextNodeType.LINK, "index.html"),
                TextNode(" and an ", TextNodeType.TEXT),
                TextNode("image", TextNodeType.IMAGE, "image.png"),
            ],
            text_to_textnodes(" ".join([
                "Just some text",
                "and some **bold** text",
                "and some *italic* text",
                "and some `code`",
                "and a [link](index.html)",
                "and an ![image](image.png)",
            ]))
        )


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


class TestSplitNodesImage(unittest.TestCase):

    def test_requires_list_of_textnodes(self):
        with self.assertRaises(ValueError):
            split_nodes_images(TextNode("alt text",
                                        TextNodeType.IMAGE,
                                        "image.png"))
        with self.assertRaises(ValueError):
            split_nodes_images(["Just a string"])

    def test_extracts_images(self):
        self.assertListEqual(
            [
                TextNode("alt text", TextNodeType.IMAGE, "image.png"),
                TextNode("alt text", TextNodeType.IMAGE, "image.png"),
                TextNode("", TextNodeType.IMAGE, "image.png"),
                TextNode("These images", TextNodeType.IMAGE, "image.png"),
                TextNode(" have plain text ", TextNodeType.TEXT),
                TextNode("between them", TextNodeType.IMAGE, "image.png"),
            ],
            split_nodes_images([
                TextNode("![alt text](image.png)", TextNodeType.TEXT),
                TextNode("![alt text](image.png)![](image.png)",
                         TextNodeType.TEXT),
                TextNode("![These images](image.png)"
                         + " have plain text "
                         + "![between them](image.png)", TextNodeType.TEXT)
            ])
        )


class TestSplitNodesLinks(unittest.TestCase):

    def test_requires_list_of_textnodes(self):
        with self.assertRaises(ValueError):
            split_nodes_links(
                TextNode("click here", TextNodeType.LINK, "index.html")
            )
        with self.assertRaises(ValueError):
            split_nodes_links(["just a string"])

    def test_extracts_links(self):
        nodes = [
            TextNode("Just plain text", TextNodeType.TEXT),
            TextNode("[click here](index.html)", TextNodeType.TEXT),
            TextNode("[this has](index.html)[multiple links](index.html)",
                     TextNodeType.TEXT),
            TextNode("Some plain text with [a link](index.html)",
                     TextNodeType.TEXT),
            TextNode("[A link](index.html) with plain text after",
                     TextNodeType.TEXT),
        ]
        self.assertListEqual(
            [
                TextNode("Just plain text", TextNodeType.TEXT),
                TextNode("click here", TextNodeType.LINK, "index.html"),
                TextNode("this has", TextNodeType.LINK, "index.html"),
                TextNode("multiple links", TextNodeType.LINK, "index.html"),
                TextNode("Some plain text with ", TextNodeType.TEXT),
                TextNode("a link", TextNodeType.LINK, "index.html"),
                TextNode("A link", TextNodeType.LINK, "index.html"),
                TextNode(" with plain text after", TextNodeType.TEXT),
            ],
            split_nodes_links(nodes)
        )


class TestExtractMarkdownImages(unittest.TestCase):
    image_text = "![alt text](image.png)"
    without_alttext = "![](image.png)"

    def test_requires_string(self):
        with self.assertRaises(ValueError):
            extract_markdown_images([])

    def test_returns_empty_list_if_no_images(self):
        self.assertListEqual(
            [],
            extract_markdown_images("Just a plain old string")
        )

    def test_gets_image_url(self):
        self.assertEqual(
            "image.png",
            extract_markdown_images(self.image_text)[0][1]
        )

    def test_gets_image_alt_text(self):
        self.assertEqual(
            "alt text",
            extract_markdown_images(self.image_text)[0][0]
        )

    def test_only_gets_image(self):
        self.assertListEqual(
            [("alt text", "image.png")],
            extract_markdown_images(f"Text before {self.image_text} and after")
        )

    def test_extracts_multiple(self):
        self.assertListEqual(
            [("alt text", "image.png"), ("", "image.png")],
            extract_markdown_images(
                self.image_text + self.without_alttext)
        )


class TestExtractMarkdownLinks(unittest.TestCase):
    link_text = "[click here](link.html)"
    without_text = "[](link.html)"
    without_url = "[click here]()"

    def test_requires_string(self):
        with self.assertRaises(ValueError):
            extract_markdown_links([])

    def test_returns_empty_list_if_no_links(self):
        self.assertListEqual(
            [],
            extract_markdown_links("Just some text")
        )

    def test_gets_link_text(self):
        self.assertEqual(
            "click here",
            extract_markdown_links(self.link_text)[0][0]
        )

    def test_gets_link_url(self):
        self.assertEqual(
            "link.html",
            extract_markdown_links(self.link_text)[0][1]
        )

    def test_gets_multiple(self):
        self.assertListEqual(
            [
                ("click here", "link.html"),
                ("", "link.html"),
                ("click here", "")
            ],
            extract_markdown_links(self.link_text
                                   + self.without_text
                                   + self.without_url)
        )
