import unittest
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    #----- test split_nodes_delimiter() -----
    def test_split_code(self):
        """Test splitting a simple code block."""
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_bold(self):
        """Test splitting a bold phrase."""
        node = TextNode("Here is **bold text** and more text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("Here is ", TextType.TEXT),
                TextNode("bold text", TextType.BOLD),
                TextNode(" and more text", TextType.TEXT),
            ],
        )

    def test_double_bold(self):
        """Test splitting two bold phrases in one node."""
        node = TextNode("One **bold** and another **bold** phrase", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("One ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and another ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" phrase", TextType.TEXT),
            ],
        )

    def test_no_change_for_non_text_node(self):
        """Test that non-TEXT nodes are not split."""
        node = TextNode("This is already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(new_nodes, [node])
    
    def test_unclosed_delimiter_raises_error(self):
        """Test that an unclosed delimiter raises a ValueError."""
        node = TextNode("This has an `unclosed code block", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_starts_with_delimiter(self):
        """Test a node that starts with a delimiter."""
        node = TextNode("**Starts bold** and then text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("Starts bold", TextType.BOLD),
                TextNode(" and then text", TextType.TEXT),
            ],
        )
    
    
    
    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [
                ("link", "https://www.example.com"),
                ("another", "https://www.example.com/another"),
            ],
            matches
        )   

    def test_extract_markdown_images(self):
        text = "This is an image ![alt text](https://www.example.com/image.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [
                ("alt text", "https://www.example.com/image.png"),
            ],
            matches
        )

    def test_no_links_or_images(self):
        text = "This is plain text with no links or images."
        self.assertListEqual([], extract_markdown_links(text))
        self.assertListEqual([], extract_markdown_images(text))

    
    # --- Image Tests ---
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_image_starts_and_ends(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    # --- Link Tests ---
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_no_links_or_images(self):
        node = TextNode("This is plain text with no special markdown.", TextType.TEXT)
        image_nodes = split_nodes_image([node])
        link_nodes = split_nodes_link([node])
        self.assertListEqual([node], image_nodes)
        self.assertListEqual([node], link_nodes)

    #--- text_to_textnodes Tests ---
    def test_full_conversion(self):
        """
        Tests the conversion of a full markdown string into a list of TextNodes.
        """
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        
        nodes = text_to_textnodes(text)
        
        self.assertListEqual(
            [
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
            ],
            nodes
        )

    def test_another_example(self):
        """
        Tests another example to ensure robustness.
        """
        text = "`code` that is _italic_ and **bold**"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("code", TextType.CODE),
                TextNode(" that is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" and ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
            ],
            nodes
        )


if __name__ == "__main__":
    unittest.main()
