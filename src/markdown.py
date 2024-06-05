from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode
from block import markdown_to_blocks, block_to_block_type, BlockType
from inline import text_to_textnodes


def markdown_to_html_node(text: str) -> HTMLNode:
    if type(text) is not str:
        raise ValueError("text must be a string")
    node = ParentNode("div", [], None)
    blocks = markdown_to_blocks(text)
    for block in blocks:
        block_type = block_to_block_type(block)
        child_node = get_child_node(block, block_type)
        node.children.append(child_node)
    return node


def get_child_node(block, block_type):
    if block_type == BlockType.Paragraph:
        return get_paragraph_node(block)
    if block_type == BlockType.Heading:
        return get_heading_node(block)
    if block_type == BlockType.Code:
        return get_code_node(block)
    if block_type == BlockType.Quote:
        return get_quote_node(block)
    if block_type == BlockType.UnorderedList:
        return get_unordered_list_node(block)
    if block_type == BlockType.OrderedList:
        return get_ordered_list_node(block)
    raise NotImplementedError(f"Not implemented for type {block_type}")


def get_paragraph_node(text):
    node = ParentNode("p", None)
    node.children = list(map(lambda t: t.to_htmlnode(),
                             text_to_textnodes(text)))
    return node


def get_heading_node(text):
    prefix, content = text.split(" ", maxsplit=1)
    return ParentNode(
        f"h{prefix.count("#")}",
        list(map(
            lambda textnode: textnode.to_htmlnode(),
            text_to_textnodes(content)
        )),
        None
    )


def get_code_node(text):
    content = text.strip("```").strip("\n")
    return ParentNode(
        "pre",
        [
            LeafNode("code", content),
        ],
    )


def get_quote_node(text):
    content = "\n".join(list(
        map(lambda ln: ln.lstrip("> "), text.split("\n"))
    ))
    return ParentNode(
        "blockquote",
        list(map(
            lambda textnode: textnode.to_htmlnode(),
            text_to_textnodes(content)
        ))
    )


def get_unordered_list_node(text):
    return ParentNode("ul", list(map(
        lambda line: ParentNode("li", list(map(
            lambda node: node.to_htmlnode(),
            text_to_textnodes(line)
        ))),
        map(
            lambda line: line.removeprefix("* ").removeprefix("- "),
            text.split("\n")
        )
    )))


def get_ordered_list_node(text):
    ol = ParentNode("ol", [])
    lines = text.split("\n")
    for i in range(len(lines)):
        li = ParentNode("li", [])
        line = lines[i].removeprefix(f"{i + 1}. ")
        nodes = text_to_textnodes(line)
        for node in nodes:
            li.children.append(node.to_htmlnode())
        ol.children.append(li)
    return ol
