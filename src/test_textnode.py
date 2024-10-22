import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        print("Testing TextNode...")
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        node3 = TextNode("I wrote a test", TextType.ITALIC)
        node4 = TextNode("I wrote a test", TextType.ITALIC)
        self.assertEqual(node3, node4)
        node5 = TextNode("z", TextType.NORMAL)
        node6 = TextNode("z", TextType.NORMAL)
        self.assertEqual(node5, node6)

        edge1 = TextNode("A website", TextType.LINKS, None)
        edge2 = TextNode("A website", TextType.LINKS, None)
        self.assertEqual(edge1, edge2)
        edge3 = TextNode("Is it different?", TextType.LINKS, None)
        edge4 = TextNode("Is it different?", TextType.CODE, None)
        self.assertNotEqual(edge3, edge4)
        edge5 = TextNode("I sit different?", TextType.TEXT)
        edge6 = TextNode("Is it different?", TextType.TEXT)
        self.assertNotEqual(edge5, edge6)
        
        #wrench = TextNode("What?", TextType.TEXT, "http://www.eh.com")
        #gear = TextNode("Are you deaf?", TextType.IMAGES, "What is a link?")
        #self.assertEqual(wrench, gear, "Good, these should not actually assert OK")


if __name__ == "__main__":
    unittest.main()
