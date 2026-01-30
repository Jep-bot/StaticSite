import unittest

from helper import split_nodes_delimiter
from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expeted_list = [
                        TextNode("This is text with a ", TextType.TEXT),
                        TextNode("code block", TextType.CODE),
                        TextNode(" word", TextType.TEXT)
                        ]
        self.assertEqual(new_nodes, expeted_list)

    def test_bold(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expeted_list = [
                        TextNode("This is text with a ", TextType.TEXT),
                        TextNode("bolded phrase", TextType.BOLD),
                        TextNode(" in the middle", TextType.TEXT)
                        ]
        self.assertEqual(new_nodes, expeted_list)

    def test_italic(self):
        node = TextNode("This is text with a _italic phrase_ in the middle", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expeted_list = [
                        TextNode("This is text with a ", TextType.TEXT),
                        TextNode("italic phrase", TextType.ITALIC),
                        TextNode(" in the middle", TextType.TEXT)
                        ]
        self.assertEqual(new_nodes, expeted_list)

    
    def test_italic_ends(self):
        node = TextNode("This is text with a _italic phrase_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expeted_list = [
                        TextNode("This is text with a ", TextType.TEXT),
                        TextNode("italic phrase", TextType.ITALIC)
                        ]
        self.assertEqual(new_nodes, expeted_list)

    def test_italic_starts(self):
        node = TextNode("_italic phrase_ this is text with", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expeted_list = [
                        TextNode("italic phrase", TextType.ITALIC),
                        TextNode(" this is text with", TextType.TEXT)
                        ]
        self.assertEqual(new_nodes, expeted_list)
    
    def test_multi_diff_nodes(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("site link", TextType.LINK,"/to/link/")
        node3 = TextNode("image text ", TextType.LINK,"/to/image/")
        node4 = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node,node2,node3,node4], "`", TextType.CODE)
        expeted_list = [
                        TextNode("This is text with a ", TextType.TEXT),
                        TextNode("code block", TextType.CODE),
                        TextNode(" word", TextType.TEXT),
                        TextNode("site link", TextType.LINK,"/to/link/"),
                        TextNode("image text ", TextType.LINK,"/to/image/"),
                        TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
                        ]
        self.assertEqual(new_nodes, expeted_list)
    
    def test_multi_same_nodes(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This is text with a `code block2`", TextType.TEXT)
        node3 = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node,node2,node3], "`", TextType.CODE)
        expeted_list = [
                        TextNode("This is text with a ", TextType.TEXT),
                        TextNode("code block", TextType.CODE),
                        TextNode(" word", TextType.TEXT),
                        TextNode("This is text with a ", TextType.TEXT),
                        TextNode("code block2", TextType.CODE),
                        TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
                        ]
        self.assertEqual(new_nodes, expeted_list)



    def test_italic_invalid(self):
        node = TextNode("This is text with a italic phrase_", TextType.TEXT)
        with self.assertRaises(ValueError):
            new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)

    def test_italic_invalid_multi(self):
        node = TextNode("This is text _with a _italic phrase_", TextType.TEXT)
        with self.assertRaises(ValueError):
            new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)

    def test_italic_invalid_none(self):
        node = TextNode("This is text with a italic phrase", TextType.TEXT)
        with self.assertRaises(ValueError):
            new_nodes = split_nodes_delimiter([node], "", TextType.ITALIC)


if __name__ == "__main__":
    unittest.main()
