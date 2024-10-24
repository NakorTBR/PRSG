import unittest
from nodehandlers import split_nodes_delimiter, split_nodes_image, split_nodes_link

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


class TestSplitNodes(unittest.TestCase):
    def test_split_nodes_images(self):
        node = TextNode(
        "This is text with an image ![a can in a bucket](url/of/image.jpg) and ![neither image is real](url/of/image.jpg)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode(text="This is text with an image ", text_type=TextType.TEXT),
                TextNode(text="a can in a bucket", text_type=TextType.IMAGE, url="url/of/image.jpg"),
                TextNode(text=" and ", text_type=TextType.TEXT),
                TextNode(text="neither image is real", text_type=TextType.IMAGE, url="url/of/image.jpg"),
            ],
            new_nodes,
        )

    def test_split_nodes_images_three(self):
        node = TextNode(
        "We are going to have ![a picture](url/of/image.jpg) three ![no image is real](url/of/image.jpg)"
         " images here ![cool pic](http://www.atotallyrealwebsite.com)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode(text="We are going to have ", text_type=TextType.TEXT),
                TextNode(text="a picture", text_type=TextType.IMAGE, url="url/of/image.jpg"),
                TextNode(text=" three ", text_type=TextType.TEXT),
                TextNode(text="no image is real", text_type=TextType.IMAGE, url="url/of/image.jpg"),
                TextNode(text=" images here ", text_type=TextType.TEXT),
                TextNode(text="cool pic", text_type=TextType.IMAGE, url="http://www.atotallyrealwebsite.com"),
            ],
            new_nodes,
        )

    def test_split_nodes_images_three_with_post_text(self):
        node = TextNode(
        "We are going to have ![a picture](url/of/image.jpg) three ![no image is real](url/of/image.jpg)"
         " images here ![cool pic](http://www.atotallyrealwebsite.com) and this text comes after.",
        TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode(text="We are going to have ", text_type=TextType.TEXT),
                TextNode(text="a picture", text_type=TextType.IMAGE, url="url/of/image.jpg"),
                TextNode(text=" three ", text_type=TextType.TEXT),
                TextNode(text="no image is real", text_type=TextType.IMAGE, url="url/of/image.jpg"),
                TextNode(text=" images here ", text_type=TextType.TEXT),
                TextNode(text="cool pic", text_type=TextType.IMAGE, url="http://www.atotallyrealwebsite.com"),
                TextNode(text=" and this text comes after.", text_type=TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_images_three_with_post_text_confusion_check(self):
        node = TextNode(
        "We are going to have ![a picture](url/of/image.jpg) three ![no image is real](url/of/image.jpg)"
         " images here ![cool pic](http://www.atotallyrealwebsite.com) and this text comes after! [Be "
         "careful with links] because they are important! (but whatever).",
        TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode(text="We are going to have ", text_type=TextType.TEXT),
                TextNode(text="a picture", text_type=TextType.IMAGE, url="url/of/image.jpg"),
                TextNode(text=" three ", text_type=TextType.TEXT),
                TextNode(text="no image is real", text_type=TextType.IMAGE, url="url/of/image.jpg"),
                TextNode(text=" images here ", text_type=TextType.TEXT),
                TextNode(text="cool pic", text_type=TextType.IMAGE, url="http://www.atotallyrealwebsite.com"),
                TextNode(text=" and this text comes after! [Be careful with links] because they are important! "
                         "(but whatever).", text_type=TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_links(self):
        node = TextNode(
        "This is text with a link [I am a link](https://www.boot.dev) and [Google](http://www.google.com)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode(text="This is text with a link ", text_type=TextType.TEXT),
                TextNode(text="I am a link", text_type=TextType.LINK, url="https://www.boot.dev"),
                TextNode(text=" and ", text_type=TextType.TEXT),
                TextNode(text="Google", text_type=TextType.LINK, url="http://www.google.com"),
            ],
            new_nodes,
        )

    def test_split_nodes_links_complex(self):
        node = TextNode(
        "This is text with a link [I am a link & $t00p1D stuff](https://www.boot.dev?user=FarkleDarkle|doy=duhdoy) "
        "and [Google](http://www.google.com?h4x=d0g&prox=vangard) with text at the end.",
        TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode(text="This is text with a link ", text_type=TextType.TEXT),
                TextNode(text="I am a link & $t00p1D stuff", text_type=TextType.LINK, 
                         url="https://www.boot.dev?user=FarkleDarkle|doy=duhdoy"),
                TextNode(text=" and ", text_type=TextType.TEXT),
                TextNode(text="Google", text_type=TextType.LINK, 
                         url="http://www.google.com?h4x=d0g&prox=vangard"),
                TextNode(text=" with text at the end.", text_type=TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_links_confusion_check(self):
        node = TextNode(
        "This is text with a link [I am a link & $t00p1D stuff](https://www.boot.dev?user=FarkleDarkle|doy=duhdoy) "
        "and [Google](http://www.google.com?h4x=d0g&prox=vangard) with text at the end.  I am an idiot and like [to "
        "put things in] boxes to confuse [the code]  (but not in a mean way).",
        TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode(text="This is text with a link ", text_type=TextType.TEXT),
                TextNode(text="I am a link & $t00p1D stuff", text_type=TextType.LINK, 
                         url="https://www.boot.dev?user=FarkleDarkle|doy=duhdoy"),
                TextNode(text=" and ", text_type=TextType.TEXT),
                TextNode(text="Google", text_type=TextType.LINK, url="http://www.google.com?h4x=d0g&prox=vangard"),
                TextNode(text=" with text at the end.  I am an idiot and like [to put things in] boxes to confuse "
                         "[the code]  (but not in a mean way).", text_type=TextType.TEXT),
            ],
            new_nodes,
        )

        
if __name__ == "__main__":
    unittest.main()
