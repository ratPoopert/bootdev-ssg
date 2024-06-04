from typing import List


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
