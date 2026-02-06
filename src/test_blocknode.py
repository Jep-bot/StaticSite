import unittest
from blocknode import BlockType, markdown_to_blocks, block_to_block_type, markdown_to_html_node, extract_title

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

    def test_unorderedlist(self):
        md = """
- `Item 1`
- Item 2
- Item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li><code>Item 1</code></li><li>Item 2</li><li>Item 3</li></ul></div>",
        )

    def test_orderedlist(self):
        md = """
1. Item 1
2. _Item_ 2
3. Item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Item 1</li><li><i>Item</i> 2</li><li>Item 3</li></ol></div>",
        )

    def test_quote(self):
        md = """
> This is a quote.
>This **is bold** a quote.
> This is a quote.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote. This <b>is bold</b> a quote. This is a quote.</blockquote></div>",
        )

    def test_header(self):
        md = """
# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6></div>",
        )


    def test_all(self):
        md = """"
# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6

This is **bolded** paragraph
text in a p
tag here

> This is a quote.
>This **is bold** a quote.
> This is a quote.

This is another paragraph with _italic_ text and `code` here

1. Item 1
2. _Item_ 2
3. Item 3

- `Item 1`
- Item 2
- Item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.maxDiff = None
        html_expected = [
            "<div>",
            "<h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6>",
            "<p>This is <b>bolded</b> paragraph text in a p tag here</p>",
            "<blockquote>This is a quote. This <b>is bold</b> a quote. This is a quote.</blockquote>",
            "<p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p>",
            "<ol><li>Item 1</li><li><i>Item</i> 2</li><li>Item 3</li></ol>",
            "<ul><li><code>Item 1</code></li><li>Item 2</li><li>Item 3</li></ul>",
            "</div>"
        ]
        self.assertEqual(
            html, "".join(html_expected),
        )

    def test_extract_title(self):
        md = "# hello"
        header = extract_title(md)        
        self.assertEqual(
            header, "hello",
        )



if __name__ == "__main__":
    unittest.main()
