import unittest

from nodehandlers import (
    markdown_to_blocks,
    markdown_to_html_node,
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
TMTB This is a **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "TMTB This is a **bolded** paragraph<br />",
                "This is another paragraph with *italic* text and `code` here<br />This is the same paragraph on a new line<br />",
                "* This is a list<br />* with items<br />",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
TMTBN This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "TMTBN This is **bolded** paragraph<br /><br />",
                "This is another paragraph with *italic* text and `code` here<br />This is the same paragraph on a new line<br />",
                "* This is a list<br />* with items<br />",
            ],
        )

    def test_markdown_to_blocks_newlines2(self):
        md = """
TMTBN2 This is **bolded** paragraph




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
                "TMTBN2 This is **bolded** paragraph<br /><br />",
                "RAND OM  T  E XT<br />",
                "This is another paragraph with *italic* text and `code` here<br />This is the same paragraph on a new line<br />",
                "* This is a list<br />* with items<br />",
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

class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_HTML(self):
        md = """
TMTHTML This is a **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items

1. Different lists,
2. Might be ordered.
3. This one is.
"""
        result = markdown_to_html_node(md)
        # print(f"FINAL RESULT:\n{result}")
        self.assertEqual(
            result, 
            "<div>TMTHTML This is a <b>bolded</b> paragraph<br />This is another paragraph with "
            "<i>italic</i> text and <code>code</code> here<br />This is the same paragraph on a "
            "new line<br /><ul><li>This is a list</li><li>with items</li></ul><ol><li>Different "
            "lists,</li><li>Might be ordered.</li><li>This one is.</li></ol></div>")
        
        

if __name__ == "__main__":
    unittest.main()