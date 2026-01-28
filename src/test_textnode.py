import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    
    def test_type_none(self):
        node = TextNode("This is a text node", None)
        self.assertEqual(node.url, None)


    def test_eq(self):

        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self):

        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.PLAIN)
        self.assertNotEqual(node, node2)



if __name__ == "__main__":
    unittest.main()
