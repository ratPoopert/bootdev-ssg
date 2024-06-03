from functools import reduce
from re import findall

from textnode import TextNode, TextNodeType


def text_to_textnodes(text):
    if type(text) is not str:
        raise ValueError("text must be a string")

    nodes = [TextNode(text, TextNodeType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextNodeType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextNodeType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextNodeType.CODE)
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_links(nodes)
    return nodes


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


def split_nodes_images(nodes):
    if (type(nodes) is not list
            or False in map(lambda node: type(node) is TextNode, nodes)):
        raise ValueError("")

    result = []

    for node in nodes:
        images = extract_markdown_images(node.text)
        if images:
            image_node = TextNode(images[0][0],
                                  TextNodeType.IMAGE,
                                  images[0][1])
            image_text = f"![{images[0][0]}]({images[0][1]})"
            remaining_text = node.text.replace(image_text, "", 1)

            if not node.text.startswith(image_text):
                plain_text = node.text.split(image_text)[0]
                result.append(TextNode(plain_text, TextNodeType.TEXT))
                remaining_text = remaining_text.replace(plain_text, "", 1)

            result.append(image_node)

            if remaining_text:
                result.extend(split_nodes_images(
                    [TextNode(remaining_text, TextNodeType.TEXT)]
                ))

        else:
            result.append(node)
    return result


def split_nodes_links(nodes):
    if (type(nodes) is not list
            or False in map(lambda node: type(node) is TextNode, nodes)):
        raise ValueError("nodes must be a list of TextNodes")

    result = []

    for node in nodes:
        links = extract_markdown_links(node.text)
        if links:
            link_text = f"[{links[0][0]}]({links[0][1]})"
            link_node = TextNode(links[0][0], TextNodeType.LINK, links[0][1])
            remaining_text = node.text.replace(link_text, "", 1)

            if not node.text.startswith(link_text):
                plain_text = node.text.split(link_text)[0]
                result.append(TextNode(plain_text, TextNodeType.TEXT))
                remaining_text = remaining_text.replace(plain_text, "", 1)
            result.append(link_node)
            if remaining_text:
                result.extend(split_nodes_links([
                    TextNode(remaining_text, TextNodeType.TEXT)
                ]))
        else:
            result.append(node)

    return result


def extract_markdown_images(text):
    if type(text) is not str:
        raise ValueError("text must be a string")
    regex = r"!\[(.*?)\]\((.*?)\)"
    return findall(regex, text)


def extract_markdown_links(text):
    if type(text) is not str:
        raise ValueError("text must be a string")
    regex = r"\[(.*?)\]\((.*?)\)"
    return findall(regex, text)
