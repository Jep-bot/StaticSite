import unittest

from helper import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNodeSpliter(unittest.TestCase):
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

class TestTextNodeSpliterImages(unittest.TestCase):

    def test_split_image(self):
        input = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another"
        node = TextNode(
                input,
                TextType.TEXT,
                )
        new_nodes = split_nodes_image([node])
        self.assertListEqual([
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another", TextType.TEXT),
        ],
        new_nodes)

    def test_split_images(self):
            input = "This is text with an ![image](https://i.imgur.com/zjjcjkz.png) and another ![second image](https://i.imgur.com/3elnhqu.png)"
            node = TextNode(
                    input,
                    TextType.TEXT,
                    )
            new_nodes = split_nodes_image([node])
            self.assertListEqual([
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcjkz.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elnhqu.png"),
            ],
            new_nodes)

    def test_split_image_some_links(self):
            input = "This is text with an ![image](https://i.imgur.com/zjjcjkz.png) and [to youtube](https://www.youtube.com/@bootdotdev)"
            node = TextNode(
                    input,
                    TextType.TEXT,
                    )
            new_nodes = split_nodes_image([node])
            self.assertListEqual([
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcjkz.png"),
                TextNode(" and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT),
            ],
            new_nodes)


    def test_split_image_only_links(self):
            input = "This is text with an [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
            node = TextNode(
                    input,
                    TextType.TEXT,
                    )
            new_nodes = split_nodes_image([node])
            self.assertListEqual([
                TextNode("This is text with an [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT),
            ],
            new_nodes)

class TestTextNodeSpliterLInks(unittest.TestCase):

    def test_split_link(self):
        input = "This is text with an [to boot dev](https://www.boot.dev) and another"
        node = TextNode(
                input,
                TextType.TEXT,
                )
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and another", TextType.TEXT),
        ],
        new_nodes)

    def test_split_links(self):
            input = "This is text with an [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
            node = TextNode(
                    input,
                    TextType.TEXT,
                    )
            new_nodes = split_nodes_link([node])
            self.assertListEqual([
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes)

    def test_split_link_some_images(self):
            input = "This is text with an [to boot dev](https://www.boot.dev) and ![image](https://i.imgur.com/zjjcjkz.png)"
            node = TextNode(
                    input,
                    TextType.TEXT,
                    )
            new_nodes = split_nodes_link([node])
            self.assertListEqual([
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ![image](https://i.imgur.com/zjjcjkz.png)", TextType.TEXT),
            ],
            new_nodes)


    def test_split_links_only_images(self):
            input = "This is text with an ![image](https://i.imgur.com/zjjcjkz.png) and another ![second image](https://i.imgur.com/3elnhqu.png)"
            node = TextNode(
                    input,
                    TextType.TEXT,
                    )
            new_nodes = split_nodes_link([node])
            self.assertListEqual([
                TextNode("This is text with an ![image](https://i.imgur.com/zjjcjkz.png) and another ![second image](https://i.imgur.com/3elnhqu.png)", TextType.TEXT),
            ],
            new_nodes)


class TestTextNodeExtractor(unittest.TestCase):

    def test_extract_markdown_image(self):
        input = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        matches = extract_markdown_images(input)
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images(self):
        input = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(input)
        self.assertListEqual([
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
            ], matches)

    def test_extract_markdown_images_only_links(self):
        input = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_images(input)
        self.assertListEqual([
            ], matches)

    def test_extract_markdown_images_some_links(self):
        input = "This is text with a link [to boot dev](https://www.boot.dev) and image ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(input)
        self.assertListEqual([
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ], matches)

    def test_extract_markdown_image_no_text(self):
        input = "This is text with an (https://i.imgur.com/zjjcJKZ.png)"
        matches = extract_markdown_images(input)
        self.assertListEqual([
            ], matches)

    def test_extract_markdown_image_no_url(self):
        input = "This is text with an ![image]"
        matches = extract_markdown_images(input)
        self.assertListEqual([
            ], matches)

    def test_extract_markdown_links(self):
        input = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(input)
        self.assertListEqual([
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ], matches)

    def test_extract_markdown_links_only_images(self):
        input = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_links(input)
        self.assertListEqual([], matches)

    def test_extract_markdown_links_some_images(self):
        input = "This is text with a link [to boot dev](https://www.boot.dev) and image ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_links(input)
        self.assertListEqual([
            ("to boot dev", "https://www.boot.dev"),
        ], matches)

    def test_extract_markdown_link_no_text(self):
        input = "This is text with a link (https://www.boot.dev)"
        matches = extract_markdown_links(input)
        self.assertListEqual([
            ], matches)

    def test_extract_markdown_link_no_url(self):
        input = "This is text with a link [to boot dev]"
        matches = extract_markdown_links(input)
        self.assertListEqual([
            ], matches)

class TestTextToTextNode(unittest.TestCase):

    def test_text_to_text_node_all(self):
        input = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        matches = text_to_textnodes(input)
        self.assertListEqual([
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ], matches)


if __name__ == "__main__":
    unittest.main()
