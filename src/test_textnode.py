import unittest

from textnode import TextNode, TextType, text_node_to_html_node

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
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)
        
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_italic(self):
        node = TextNode("This is a italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic text node")


    def test_code(self):
        node = TextNode("text node == code", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "text node == code")


    def test_link(self):
        node = TextNode("This is a link anchor text node", TextType.LINK, "https://test.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link anchor text node")
        self.assertEqual(html_node.props, {'href': 'https://test.com'})

    def test_img(self):
        node = TextNode("This is a alt img text text node", TextType.IMAGES, "https://test.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {'src': 'https://test.com', 'alt': 'This is a alt img text text node' })

    def test_not_supported_type(self):
        node = TextNode("This is a text node", "something")
        with self.assertRaises(ValueError):
            html_node = text_node_to_html_node(node)

    def test_link_no_url(self):
        node = TextNode("This is a link anchor text node", TextType.LINK, None)
        with self.assertRaises(ValueError):
            html_node = text_node_to_html_node(node)





if __name__ == "__main__":
    unittest.main()
