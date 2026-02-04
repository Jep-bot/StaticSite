import unittest
from blocknode import BlockType, markdown_to_blocks, block_to_block_type, markdown_to_html_node

class TestMarkdownToBlock(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_multi_empty(self):
        md = """


This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class TestBlockToBlocksTypeHeadings(unittest.TestCase):

    def test_block_to_block_type_paragraph(self):
        block = "This is **bolded** paragraph"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type, BlockType.PARAGRAPH
        )

    def test_block_to_block_type_headings(self):
        block = "# This is header"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type, BlockType.HEADING
        )

    def test_block_to_block_type_headings6(self):
        block = "###### This is header"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type, BlockType.HEADING
        )

    def test_block_to_block_type_headings7_not(self):
        block = "#######This is header"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type, BlockType.PARAGRAPH
        )


    def test_block_to_block_type_headings_no_wspace(self):
        block = "######This is header"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type, BlockType.PARAGRAPH
        )
    def test_block_to_block_type_headings_not_on_start(self):
        block = "Incorrect ######This is header"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type, BlockType.PARAGRAPH
        )


class TestBlockToBlocksTypeCode(unittest.TestCase):

    def test_block_to_block_type_code(self):
        block = """```
        code block
        ```"""
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type, BlockType.CODE
        )

    def test_block_to_block_type_code_big(self):
        block = """```
        code block
        code block
        code block
        code block
        code block
        code block
        ```"""
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type, BlockType.CODE
        )

    def test_block_to_block_type_code_doesnt_start(self):
        block = """wrong```
        code block
        code block
        code block
        code block
        code block
        code block
        ```"""
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type, BlockType.PARAGRAPH
        )

    def test_block_to_block_type_code_doesnt_end(self):
        block = """```
        code block
        code block
        code block
        code block
        code block
        code block
        ```wrong"""
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type, BlockType.PARAGRAPH
        )


    def test_block_to_block_type_code_no_newline(self):
        block = """```code block
        code block
        code block
        code block
        code block
        code block
        ```"""
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type, BlockType.PARAGRAPH
        )

class TestBlockToBlocksTypeQuote(unittest.TestCase):

    def test_block_to_block_type_code_quote(self):
        block = """>teest\n>sdfsdf\n> dfjasf\n>jdflsk\n> dlfjls"""
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type, BlockType.QUOTE
        )

    def test_block_to_block_type_code_quote_not_start(self):
        block = """>teest\n>sdfsdf\nsdk> dfjasf\n>jdflsk\n> dlfjls"""
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type, BlockType.PARAGRAPH
        )

class TestBlockToBlocksTypeUnorderedList(unittest.TestCase):

    def test_block_to_block_type_code_unordered_list(self):
        block = "- teest\n- sdfsdf\n- dfjasf\n- jdflsk\n- dlfjls"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type, BlockType.UNORDERED_LIST
        )

    def test_block_to_block_type_code_unordered_list_no_splace(self):
        block = "- teest\n- sdfsdf\n-dfjasf\n- jdflsk\n- dlfjls"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type, BlockType.PARAGRAPH
        )

    def test_block_to_block_type_code_unordered_list_not_start(self):
        block = "- teest\n- sdfsdf\nsdsaf- dfjasf\n- jdflsk\n- dlfjls"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type, BlockType.PARAGRAPH
        )

class TestBlockToBlocksTypeUnorderedList(unittest.TestCase):

    def test_block_to_block_type_code_ordered_list(self):
        block = "1. teest\n2. sdfsdf\n3. dfjasf\n4. jdflsk\n5. dlfjls"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type, BlockType.ORDERED_LIST
        )

    def test_block_to_block_type_code_ordered_list_no_splace(self):
        block = "1.teest\n2.sdfsdf\n3.dfjasf\n4.jdflsk\n5. dlfjls"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type, BlockType.PARAGRAPH
        )

    def test_block_to_block_type_code_ordered_list_not_start(self):
        block = "1. teest\ndf2. sdfsdf\n3. dfjasf\n4. jdflsk\n5. dlfjls"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type, BlockType.PARAGRAPH
        )

    def test_block_to_block_type_code_ordered_list_not_ordered(self):
        block = "1. teest\ndf6. sdfsdf\n3. dfjasf\n4. jdflsk\n5. dlfjls"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type, BlockType.PARAGRAPH
        )

class TestMarkdownToHtmlNode(unittest.TestCase):

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

if __name__ == "__main__":
    unittest.main()
