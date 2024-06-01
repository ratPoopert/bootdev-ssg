from enum import Enum

from leafnode import LeafNode


class TextNodeType(Enum):
    TEXT = 1
    BOLD = 2
    ITALIC = 3
    CODE = 4
    LINK = 5
    IMAGE = 6


class TextNode:

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, textnode):
        return (
            self.text == textnode.text
            and
            self.text_type == textnode.text_type
            and
            self.url == textnode.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

    def to_htmlnode(self):
        if self.text_type == TextNodeType.TEXT:
            return LeafNode(None, self.text)
        elif self.text_type == TextNodeType.BOLD:
            return LeafNode("b", self.text)
        elif self.text_type == TextNodeType.ITALIC:
            return LeafNode("i", self.text)
        elif self.text_type == TextNodeType.CODE:
            return LeafNode("code", self.text)
        elif self.text_type == TextNodeType.LINK:
            return LeafNode("a", self.text, {'href': self.url})
        elif self.text_type == TextNodeType.IMAGE:
            return LeafNode("img", "", {'src': self.url, 'alt': self.text})
        else:
            raise ValueError(f"Invalid text_type: {self.text_type}")
