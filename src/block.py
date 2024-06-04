from typing import List
from enum import Enum


class BlockType(Enum):
    Paragraph = 1
    Heading = 2
    Code = 3
    Quote = 4
    UnorderedList = 5
    OrderedList = 6


def markdown_to_blocks(text: str) -> List[str]:
    if type(text) is not str:
        raise ValueError("text must be a string")

    return list(
        filter(
            lambda block: len(block) > 0 and not block.isspace(),
            map(
                lambda block: block.strip(),
                text.split("\n\n")
            )
        )
    )


def block_to_block_type(text: str) -> BlockType:
    if type(text) is not str:
        raise ValueError("text must be a string")

    def is_heading():
        if len(text.split("\n")) > 1:
            return False
        for i in range(1, 7):
            line_beginning = "#" * i + " "
            remaining_text = text.replace(line_beginning, "", 1)
            if (
                text.startswith(line_beginning)
                and len(remaining_text) > 0
                and not remaining_text.isspace()
            ):
                return True
        return False

    def is_code():
        return text.startswith("```") and text.endswith("```")

    def is_quote():
        lines = text.split("\n")
        for line in lines:
            if not line.startswith("> "):
                return False
        return True

    def is_unordered_list():
        lines = text.split("\n")
        for line in lines:
            if not line.startswith("* ") and not line.startswith("- "):
                return False
        return True

    def is_ordered_list():
        lines = text.split("\n")
        for i in range(len(lines)):
            if not lines[i].startswith(f"{i + 1}. "):
                return False
        return True

    if is_heading():
        return BlockType.Heading
    elif is_code():
        return BlockType.Code
    elif is_quote():
        return BlockType.Quote
    elif is_unordered_list():
        return BlockType.UnorderedList
    elif is_ordered_list():
        return BlockType.OrderedList
    else:
        return BlockType.Paragraph
