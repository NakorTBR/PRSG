import unittest

from nodehandlers import (
    markdown_to_blocks,
    block_to_block_type,
    block_type_heading,
    block_type_code,
    block_type_paragraph,
    block_type_quote,
    block_type_olist,
    block_type_ulist,
)

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines2(self):
        md = """
This is **bolded** paragraph




RAND OM  T  E XT         

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "RAND OM  T  E XT",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

class TestMarkdownBlockTypes(unittest.TestCase):
    def test_block_to_block_types(self):
        block = "# Awesome header"
        self.assertEqual(block_to_block_type(block), block_type_heading)
        block = "```\nint main()\n```"
        self.assertEqual(block_to_block_type(block), block_type_code)
        block = "> Something quotable\n> continued here"
        self.assertEqual(block_to_block_type(block), block_type_quote)
        block = "* A list\n* With multiple\n* List items"
        self.assertEqual(block_to_block_type(block), block_type_ulist)
        block = "1. Ordered\n2. List"
        self.assertEqual(block_to_block_type(block), block_type_olist)
        block = "Wow.  An entire paragraph?  Not even special.  Just the default case."
        self.assertEqual(block_to_block_type(block), block_type_paragraph)



if __name__ == "__main__":
    unittest.main()