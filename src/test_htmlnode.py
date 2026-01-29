import unittest

from htmlnode import HTMLNode,LeafNode

props = {
    "href": "https://www.google.com",
    "target": "_blank",
}
class TestHTMLNode(unittest.TestCase):
    
    def test_type_none(self):
        node = HTMLNode("a", "This is a text node", None, props)
        self.assertEqual(node.props_to_html(),  " href=\"https://www.google.com\" target=\"_blank\"")


    def test_eq(self):
        node = HTMLNode("a", "This is a text node", None, props)
        node2 = HTMLNode("a", "This is a text node", None, props)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = HTMLNode("a", "This is a text node", None, props)
        node2 = HTMLNode("b", "This is a text node", None, props)
        self.assertNotEqual(node, node2)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_p_props(self):
        node = LeafNode("p", "Hello, world!",None, props)
        self.assertEqual(node.to_html(), "<p href=\"https://www.google.com\" target=\"_blank\">Hello, world!</p>")


if __name__ == "__main__":
    unittest.main()
