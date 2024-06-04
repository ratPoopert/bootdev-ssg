import unittest

from block import markdown_to_blocks


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
