from functools import reduce

from htmlnode import HTMLNode


class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError(f'ParentNode {self} requires a tag')
        if (
            not self.children
            or type(self.children) is not list
            or not len(self.children)
        ):
            raise ValueError(
                f'ParentNode {self} requires a list of child nodes')
        return (f'<{self.tag}{self.props_to_html()}>'
                + self.__children_to_html()
                + f'</{self.tag}>')

    def __children_to_html(self):
        return reduce(
            lambda acc, child: acc + child.to_html(),
            self.children,
            ''
        )
