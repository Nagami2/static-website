from block_markdown import markdown_to_blocks, block_to_block_type, BlockType

import unittest

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        * This is a list
        * with items
        """
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
            blocks,
        )

    def test_markdown_to_blocks_with_extra_newlines(self):
        md = """

        This is a paragraph


        * list item 1
        * list item 2


        Another paragraph

        """
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            [
                "This is a paragraph",
                "* list item 1\n* list item 2",
                "Another paragraph",
            ],
            blocks,
        )
    #--- block_to_block_type Tests ---
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        self.assertNotEqual(block_to_block_type("####### Not a Heading"), BlockType.HEADING)

    def test_code(self):
        self.assertEqual(block_to_block_type("```\ncode block\n```"), BlockType.CODE)

    def test_quote(self):
        self.assertEqual(block_to_block_type("> quote\n> another line"), BlockType.QUOTE)

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("* item 1\n* item 2"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("- item 1\n- item 2"), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. first\n2. second\n3. third"), BlockType.ORDERED_LIST)
        self.assertNotEqual(block_to_block_type("1. first\n3. third"), BlockType.ORDERED_LIST)

    def test_paragraph(self):
        self.assertEqual(block_to_block_type("This is a plain paragraph."), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()