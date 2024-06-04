import unittest

from block import markdown_to_blocks, BlockType, block_to_block_type


class TestMarkdownToBlocks(unittest.TestCase):

    example_text = (
        "This is a **bolded** paragraph\n"
        + "\n"
        + "This is another paragraph with *italic* text and `code` here\n"
        + "This is the same paragraph on a new line\n"
        + "\n"
        + "\n"
        + "\n"
        + "* This is a list\n"
        + "* with items"
    )

    def test_requires_string_as_input(self):
        with self.assertRaises(ValueError):
            markdown_to_blocks([])

    def test_returns_list_of_strings(self):
        result = markdown_to_blocks(self.example_text)
        self.assertIsInstance(result, list)
        for r in result:
            self.assertIsInstance(r, str)

    def test_returns_correct_number_of_blocks(self):
        result = markdown_to_blocks(self.example_text)
        self.assertEqual(3, len(result))

    def test_returns_correct_output(self):
        self.assertListEqual(
            ["This is a **bolded** paragraph",

             "This is another paragraph with *italic* text and `code` here\n"
             + "This is the same paragraph on a new line",

             "* This is a list\n* with items"],
            markdown_to_blocks(self.example_text)
        )


class TestBlockTypes(unittest.TestCase):
    def test_block_types_exist(self):
        for block_type in [
            'Paragraph',
            'Heading',
            'Code',
            'Quote',
            'UnorderedList',
            'OrderedList',
        ]:
            self.assertTrue(block_type in BlockType._member_names_)


class TestBlockToBlockType(unittest.TestCase):

    def test_requires_string_as_input(self):
        with self.assertRaises(ValueError):
            block_to_block_type([])

    def test_parses_paragraphs(self):
        for block in [
            "Just a simple paragraph",
            "This paragraph\nis a multiline paragraph",
        ]:
            self.assertEqual(
                BlockType.Paragraph,
                block_to_block_type(block)
            )

    def test_parses_headings(self):
        self.assertListEqual(
            [
                BlockType.Heading,
                BlockType.Heading,
                BlockType.Heading,
                BlockType.Heading,
                BlockType.Heading,
                BlockType.Heading,
                BlockType.Paragraph,
                BlockType.Paragraph,
                BlockType.Paragraph,
            ],
            list(map(block_to_block_type, [
                "# Level 1 Heading",
                "## Level 2 Heading",
                "### Level 3 Heading",
                "#### Level 4 Heading",
                "##### Level 5 Heading",
                "###### Level 6 Heading",
                "####### Invalid Heading Level",
                "#Missing space after #",
                "### "  # No text after marker
            ])))

    def test_parses_code(self):
        self.assertListEqual(
            [
                BlockType.Code,
                BlockType.Code,
                BlockType.Paragraph,
                BlockType.Paragraph,
                BlockType.Paragraph,
            ],
            list(map(block_to_block_type, [
                "```\nThis is a code block\n```",
                "```\nThis is a multiline\nCode block```",
                "``Only two backticks``",
                "```Missing ending backticks",
                "Missing starting backticks```"
            ]))
        )

    def test_parses_quotes(self):
        self.assertListEqual(
            [
                BlockType.Quote,
                BlockType.Quote,
                BlockType.Paragraph,
                BlockType.Paragraph,
                BlockType.Paragraph,
            ],
            list(map(block_to_block_type, [
                "> This is a quote block",
                "> This is a multiline\n> Quote block",
                ">Missing space",
                ">\nNewline instead of space",
                ">\tTab instead of space",
            ]))
        )

    def test_parses_unordered_lists(self):
        self.assertListEqual(
            [
                BlockType.UnorderedList,
                BlockType.UnorderedList,
                BlockType.Paragraph,
                BlockType.Paragraph,
            ],
            list(map(block_to_block_type, [
                "* Unordered item 1\n* Unordered item 2",
                "- Slash list 1\n- Slash list 2",
                "* Missing second\nasterisk",
                "Missing first\n- slash",
            ]))
        )

    def test_parses_ordered_lists(self):
        self.assertListEqual(
            [
                BlockType.OrderedList,
                BlockType.Paragraph,
                BlockType.Paragraph,
            ],
            list(map(block_to_block_type, [
                "1. Ordered item 1\n2. Ordered item 2\n3. Ordered item 3",
                "1. Ordered item\nMissing prefix",
                "1. Ordered item\n3. Skipped sequence",
            ]))
        )
