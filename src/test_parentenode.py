import unittest

from htmlnode import HTMLNode,LeafNode,ParentNode

props = {
    "href": "https://www.google.com",
    "target": "_blank",
}
class TestParentNode(unittest.TestCase):
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multi_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        grandchild_node2 = LeafNode("b", "grandchild2")
        grandchild_node3 = LeafNode("i", "grandchild3")
        grandchild_node4 = LeafNode("i", "grandchild4")
        child_node = ParentNode("span", [grandchild_node, grandchild_node2, grandchild_node3, grandchild_node4])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b><b>grandchild2</b><i>grandchild3</i><i>grandchild4</i></span></div>",
        )
    def test_none_value(self):
        with self.assertRaises(ValueError):
            node = ParentNode(None, None, props)
            node.to_html()

    def test_none_tag(self):
        with self.assertRaises(ValueError):
            node = ParentNode(None, None, props)
            node.to_html()


    def test_to_string(self):
        child_node = LeafNode("span", "child")
        node = ParentNode("p", child_node, props)
        self.assertEqual(node.__repr__(), "ParentNode(p, LeafNode(span, child, None), {'href': 'https://www.google.com', 'target': '_blank'})")
    

if __name__ == "__main__":
    unittest.main()
