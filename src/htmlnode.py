from functools import reduce


class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None:
            return ""
        if type(self.props) is not dict:
            raise ValueError("HTML properties must be a dictionary")
        return reduce(
            lambda acc, i: f'{acc} {i[0]}="{i[1]}"',
            self.props.items(),
            ''
        )

    def __eq__(self, htmlnode):
        return (
            self.tag == htmlnode.tag
            and self.value == htmlnode.value
            and self.children == htmlnode.children
            and self.props == htmlnode.props
        )

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
