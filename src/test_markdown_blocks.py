import unittest

from markdown_blocks import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
    markdown_to_html_node,
)


class TestMarkdownToBlocks(unittest.TestCase):
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

    def test_single_block(self):
        md = "Just one paragraph with no blank lines"
        self.assertEqual(
            markdown_to_blocks(md),
            ["Just one paragraph with no blank lines"],
        )

    def test_excessive_newlines(self):
        md = "First block\n\n\n\nSecond block\n\n\n\n\nThird block"
        self.assertEqual(
            markdown_to_blocks(md),
            ["First block", "Second block", "Third block"],
        )

    def test_leading_and_trailing_whitespace(self):
        md = "   \n\n   Padded block with spaces   \n\n   "
        self.assertEqual(
            markdown_to_blocks(md),
            ["Padded block with spaces"],
        )

    def test_empty_string(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_only_whitespace(self):
        self.assertEqual(markdown_to_blocks("\n\n   \n\n"), [])


class TestBlockToBlockType(unittest.TestCase):
    def test_heading_levels(self):
        for prefix in ["# ", "## ", "### ", "#### ", "##### ", "###### "]:
            self.assertEqual(
                block_to_block_type(f"{prefix}Heading"),
                BlockType.HEADING,
            )

    def test_heading_seven_hashes_is_paragraph(self):
        self.assertEqual(
            block_to_block_type("####### too many"),
            BlockType.PARAGRAPH,
        )

    def test_heading_no_space_is_paragraph(self):
        self.assertEqual(
            block_to_block_type("#nospace"),
            BlockType.PARAGRAPH,
        )

    def test_code_block(self):
        block = "```\ncode goes here\nmore code\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_single_backtick_line_is_paragraph(self):
        self.assertEqual(block_to_block_type("```"), BlockType.PARAGRAPH)

    def test_quote_block(self):
        block = "> line one\n> line two\n>line three"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_broken_is_paragraph(self):
        block = "> line one\nnot a quote line"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        block = "- item one\n- item two\n- item three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_no_space_is_paragraph(self):
        block = "-item one\n-item two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        block = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_wrong_start_is_paragraph(self):
        block = "2. first\n3. second"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_wrong_increment_is_paragraph(self):
        block = "1. first\n3. third"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph(self):
        block = "Just a normal paragraph with **bold** and _italic_ text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_multiline_paragraph(self):
        block = "First line of a paragraph\nsecond line of the same paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


class TestMarkdownToHTMLNode(unittest.TestCase):
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

    def test_headings(self):
        md = """
# Heading one

### Heading three with **bold**
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading one</h1><h3>Heading three with <b>bold</b></h3></div>",
        )

    def test_quote(self):
        md = """
> This is a quote
> spanning multiple lines
> with **bold** text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote spanning multiple lines with <b>bold</b> text</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- first item with _italic_
- second item
- third item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>first item with <i>italic</i></li><li>second item</li><li>third item</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. first item
2. second item with `code`
3. third item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>first item</li><li>second item with <code>code</code></li><li>third item</li></ol></div>",
        )

    def test_mixed_document(self):
        md = """
# Title

A paragraph with a [link](https://boot.dev).

- item one
- item two
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><h1>Title</h1><p>A paragraph with a <a href="https://boot.dev">link</a>.</p><ul><li>item one</li><li>item two</li></ul></div>',
        )


if __name__ == "__main__":
    unittest.main()
