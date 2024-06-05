import unittest

from markdown import (
    markdown_to_html_node,
    get_paragraph_node,
    get_heading_node,
    get_code_node,
    get_quote_node,
    get_unordered_list_node,
    get_ordered_list_node,
)
from htmlnode import HTMLNode


class TestMarkdownToHTMLNode(unittest.TestCase):

    def test_requires_string(self):
        with self.assertRaises(ValueError):
            markdown_to_html_node([])

    def test_multiparagraph_markdown(self):
        example_markdown = """
# Level 1 Heading

This is a paragraph.

```
This is a code block
```

> This is a quote block
> This is another line in a quote block

* This is a list item
* This is another list item

1. This is a numbered item
2. This is also a numbered item
"""
        self.assertEqual(
            HTMLNode("div", None, [
                HTMLNode("h1", None, [HTMLNode(None, "Level 1 Heading")]),
                HTMLNode("p", None, [HTMLNode(None, "This is a paragraph.")]),
                HTMLNode("pre", None, [
                    HTMLNode("code", "This is a code block")
                ]),
                HTMLNode("blockquote", None, [
                    HTMLNode(None,
                             "This is a quote block"
                             + "\n"
                             + "This is another line in a quote block")
                ]),
                HTMLNode("ul", None, [
                    HTMLNode("li", None, [
                        HTMLNode(None, "This is a list item")]),
                    HTMLNode("li", None, [
                        HTMLNode(None, "This is another list item")]),
                ]),
                HTMLNode("ol", None, [
                    HTMLNode("li", None, [
                        HTMLNode(None, "This is a numbered item")]),
                    HTMLNode("li", None, [
                        HTMLNode(None, "This is also a numbered item")]),
                ]),
            ]),
            markdown_to_html_node(example_markdown)
        )

    def test_markdown_to_p(self):
        md = (
            "This is plain text"
            + "\n*This is italic text*"
            + "\n**This is bold text**"
            + "\n`This is code`"
            + "\n![This is an image](image.png)"
            + "\n[This is a link](google.com)"
        )
        self.assertEqual(
            HTMLNode("p", None, [
                HTMLNode(None, "This is plain text\n"),
                HTMLNode("i", "This is italic text"),
                HTMLNode(None, "\n"),
                HTMLNode("b", "This is bold text"),
                HTMLNode(None, "\n"),
                HTMLNode("code", "This is code"),
                HTMLNode(None, "\n"),
                HTMLNode("img", "", None,
                         {'src': 'image.png', 'alt': 'This is an image'}),
                HTMLNode(None, "\n"),
                HTMLNode("a", "This is a link", None,
                         {'href': 'google.com'}),
            ]),
            get_paragraph_node(md)
        )

    def test_markdown_to_h(self):
        headings = [
            "# Level 1 Heading",
            "## Level 2 Heading",
            "### Level 3 Heading",
            "#### Level 4 Heading",
            "##### Level 5 Heading",
            "###### Level 6 Heading",
        ]
        self.assertListEqual([
            HTMLNode("h1", None, [HTMLNode(None, "Level 1 Heading")]),
            HTMLNode("h2", None, [HTMLNode(None, "Level 2 Heading")]),
            HTMLNode("h3", None, [HTMLNode(None, "Level 3 Heading")]),
            HTMLNode("h4", None, [HTMLNode(None, "Level 4 Heading")]),
            HTMLNode("h5", None, [HTMLNode(None, "Level 5 Heading")]),
            HTMLNode("h6", None, [HTMLNode(None, "Level 6 Heading")]),
        ], list(map(get_heading_node, headings)))

    def test_markdown_to_code(self):
        md = "```\nSome code\nAnother line\n```"
        self.assertEqual(
            HTMLNode("pre", None, [
                HTMLNode("code", "Some code\nAnother line"),
            ]),
            get_code_node(md)
        )

    def test_markdown_to_quote(self):
        md = (
            "> Quote line 1"
            + "\n> Quote with *italic* text"
            + "\n> Quote with **bold** text"
            + "\n> Quote with `some code`"
            + "\n> Quote with [a link](google.com)"
            + "\n> Quote with ![an image](image.png)"
        )
        self.assertEqual(
            HTMLNode("blockquote", None, [
                HTMLNode(None, "Quote line 1\nQuote with "),
                HTMLNode("i", "italic"),
                HTMLNode(None, " text\nQuote with "),
                HTMLNode("b", "bold"),
                HTMLNode(None, " text\nQuote with "),
                HTMLNode("code", "some code"),
                HTMLNode(None, "\nQuote with "),
                HTMLNode("a", "a link", None, {"href": "google.com"}),
                HTMLNode(None, "\nQuote with "),
                HTMLNode("img", "", None, {
                         "src": "image.png", "alt": "an image"})
            ]),
            get_quote_node(md)
        )

    def test_markdown_to_ul(self):
        self.assertEqual(
            HTMLNode("ul", None, [
                HTMLNode("li", None, [HTMLNode(None, "List item 1")]),
                HTMLNode("li", None, [HTMLNode(None, "List item 2")]),
                HTMLNode("li", None, [HTMLNode("i", "List item 3")]),
                HTMLNode("li", None, [HTMLNode("b", "List item 4")]),
                HTMLNode("li", None, [HTMLNode("code", "List item 5")]),
                HTMLNode("li", None, [HTMLNode("a", "List item 6", None, {
                    'href': 'google.com'
                })]),
                HTMLNode("li", None, [HTMLNode("img", "", None, {
                    'src': 'image.png', 'alt': 'List item 7'
                })]),
            ]),
            get_unordered_list_node((
                "* List item 1"
                + "\n- List item 2"
                + "\n* *List item 3*"
                + "\n- **List item 4**"
                + "\n* `List item 5`"
                + "\n- [List item 6](google.com)"
                + "\n* ![List item 7](image.png)"
            ))
        )

    def test_markdown_to_ol(self):
        self.assertEqual(
            HTMLNode("ol", None, [
                HTMLNode("li", None, [HTMLNode(None, "List item 1")]),
                HTMLNode("li", None, [HTMLNode("i", "List item 2")]),
                HTMLNode("li", None, [HTMLNode("b", "List item 3")]),
                HTMLNode("li", None, [HTMLNode("code", "List item 4")]),
                HTMLNode("li", None, [HTMLNode("a", "List item 5", None, {
                    'href': 'google.com'
                })]),
                HTMLNode("li", None, [HTMLNode("img", "", None, {
                    'src': 'image.png', 'alt': 'List item 6'
                })]),
            ]),
            get_ordered_list_node((
                "1. List item 1"
                + "\n2. *List item 2*"
                + "\n3. **List item 3**"
                + "\n4. `List item 4`"
                + "\n5. [List item 5](google.com)"
                + "\n6. ![List item 6](image.png)"
            ))
        )
