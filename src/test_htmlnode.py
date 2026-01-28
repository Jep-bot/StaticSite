import unittest

from htmlnode import HTMLNode

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



if __name__ == "__main__":
    unittest.main()
