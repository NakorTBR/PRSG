import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        print("Testing HTML Node...")
        t1 = HTMLNode()
        t2 = HTMLNode()
        self.assertEqual(t1, t2)
        t3 = HTMLNode("slot", "Test data / text")
        t4 = HTMLNode("slot", "Test data / text")
        self.assertEqual(t3, t4)
        t5 = HTMLNode("start", "Cu vi parolas?", ["one", "two", "three"])
        t6 = HTMLNode("start", "Cu vi parolas?", ["one", "two", "three"])
        self.assertEqual(t5, t6)

        n1 = HTMLNode("start", "Cu vi parolas?")
        n2 = HTMLNode("end", "Cu vi parolas?")
        self.assertNotEqual(n1, n2)
        n3 = HTMLNode("Start", "Hello")
        n4 = HTMLNode("Start", "hello")
        self.assertNotEqual(n3, n4)
        n5 = HTMLNode("end", "bye", ["boring", "test", "trial", "data"], {"monkey":"fun"})
        n6 = HTMLNode("end", "bye", ["boring", "test", "trill", "data"], {"monkey":"fun"})
        self.assertNotEqual(n5, n6)

        print(n5.props_to_html())
        print(n5)

        leaf1 = HTMLNode.LeafNode("just text").to_html()
        print(leaf1)
        self.assertEqual("just text", leaf1)
        leaf2 = HTMLNode.LeafNode("Paragraph text", "p").to_html()
        print(leaf2)
        self.assertEqual("<p>Paragraph text</p>", leaf2)
        leaf3 = HTMLNode.LeafNode("This is a link", "a", {"href":"https://boot.dev"}).to_html()
        print(leaf3)
        self.assertEqual('<a href="https://boot.dev">This is a link</a>', leaf3)
        leaf4 = HTMLNode.LeafNode("Another...link...", "a", 
                                  {"href":"whomstistesting.com?user=farkleton", "deer":"droppings"}).to_html()
        print(leaf4)
        self.assertEqual("<a href=\"whomstistesting.com?user=farkleton\">Another...link...</a>", leaf4)


        print("\n\n\n")


if __name__ == "__main__":
    unittest.main()
