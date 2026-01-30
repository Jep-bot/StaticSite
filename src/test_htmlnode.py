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

    def test_to_string(self):
        node = HTMLNode("p", "Hello, world!", props)
        self.assertEqual(node.__repr__(), "HTMLNode(p, Hello, world!, {'href': 'https://www.google.com', 'target': '_blank'}, None)")
    
class TestLeadNode(unittest.TestCase):

    def test_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_p_props(self):
        node = LeafNode("p", "Hello, world!", props)
        self.assertEqual(node.to_html(), "<p href=\"https://www.google.com\" target=\"_blank\">Hello, world!</p>")
    
    def test_none_value(self):
        with self.assertRaises(ValueError):
            node = LeafNode(None, None, props)
            node.to_html()

    def test_to_string(self):
        node = LeafNode("p", "Hello, world!", props)
        self.assertEqual(node.__repr__(), "LeafNode(p, Hello, world!, {'href': 'https://www.google.com', 'target': '_blank'})")
    

if __name__ == "__main__":
    unittest.main()  
