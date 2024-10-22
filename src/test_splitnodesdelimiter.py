import unittest
from nodehandlers import split_nodes_delimiter

from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_italic_delimiter(self):
        node = TextNode(text="Look, an *italic* word", text_type=TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode(text="Look, an ", text_type=TextType.TEXT),
                TextNode(text="italic", text_type=TextType.ITALIC),
                TextNode(text=" word", text_type=TextType.TEXT),
            ],
            new_nodes,
        )

    def test_bi_delimiter(self):
        node = TextNode(text="**Bold** and *Italic*", text_type=TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", text_type=TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", text_type=TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode(text="Bold", text_type=TextType.BOLD),
                TextNode(text=" and ", text_type=TextType.TEXT),
                TextNode(text="Italic", text_type=TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_code_block_delimiter(self):
        node = TextNode(text="I present to you, an amazing bit of code `GOTO 10` block.", text_type=TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode(text="I present to you, an amazing bit of code ", text_type=TextType.TEXT),
                TextNode(text="GOTO 10", text_type=TextType.CODE),
                TextNode(text=" block.", text_type=TextType.TEXT),
            ],
            new_nodes,
        )

    def test_bold_delimiter(self):
        node = TextNode(text="This is text with **bold words**, yo!", text_type=TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode(text="This is text with ", text_type=TextType.TEXT),
                TextNode(text="bold words", text_type=TextType.BOLD),
                TextNode(text=", yo!", text_type=TextType.TEXT),
            ],
            new_nodes,
        )

    def test_bold_delimiter_twice(self):
        node = TextNode(
            text="Here we have some **bold** words. Over here, we have more **bold AF words**", text_type=TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode(text="Here we have some ", text_type=TextType.TEXT),
                TextNode(text="bold", text_type=TextType.BOLD),
                TextNode(text=" words. Over here, we have more ", text_type=TextType.TEXT),
                TextNode(text="bold AF words", text_type=TextType.BOLD),
            ],
            new_nodes,
        )

    def test_bold_delimiter_twice_again(self):
        node = TextNode(
            text="Look, it is more text with **bold words** and **more here!**", text_type=TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode(text="Look, it is more text with ", text_type=TextType.TEXT),
                TextNode(text="bold words", text_type=TextType.BOLD),
                TextNode(text=" and ", text_type=TextType.TEXT),
                TextNode(text="more here!", text_type=TextType.BOLD),
            ],
            new_nodes,
        )

    


if __name__ == "__main__":
    unittest.main()
