from functools import reduce

from textnode import TextNode, TextNodeType


def split_nodes_delimiter(nodes, delimiter, text_type):

    if not (
        type(nodes) is list
        and reduce(lambda result, node: type(node) is TextNode, nodes, True)
    ):
        raise ValueError("nodes must be a list of TextNodes")

    result = []

    for node in nodes:
        if (node.text_type is not TextNodeType.TEXT
           or delimiter not in node.text):
            result.append(node)
        elif node.text.count(delimiter) % 2 != 0:
            raise ValueError(
                f"Missing matching delimiter '{delimiter}' in {node}"
            )
        else:
            (formatted_text,
             plain_text,
             remaining_text) = None, None, None
            if node.text.startswith(delimiter):
                formatted_text = node.text.split(delimiter)[1]
                remaining_text = node.text.replace(
                    f"{delimiter}{formatted_text}{delimiter}", "", 1)
            else:
                plain_text = node.text.split(delimiter)[0]
                remaining_text = node.text.replace(plain_text, "", 1)

            result.append(
                TextNode(formatted_text, text_type) if formatted_text
                else TextNode(plain_text, TextNodeType.TEXT)
            )

            if remaining_text:
                result.extend(split_nodes_delimiter(
                    [TextNode(remaining_text, TextNodeType.TEXT)],
                    delimiter,
                    text_type
                ))

    return result
