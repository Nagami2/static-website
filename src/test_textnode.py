import unittest

from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_different_text_types(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    #----- test text_node_to_html_node() -----
    def test_text_node_to_html_node_link(self):
        node = TextNode("This is some anchor text", TextType.LINK, url="https://example.com")
        expected_html_node = LeafNode("a", "This is some anchor text", {"href": "https://example.com"})
        self.assertEqual(node.text_node_to_html_node(), expected_html_node) 

    def test_text_node_to_html_node_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        expected_html_node = LeafNode("b", "This is bold text")
        self.assertEqual(node.text_node_to_html_node(), expected_html_node)

    def test_text_node_to_html_node_italic(self):
        node = TextNode("This is italic text", TextType.ITALIC)
        expected_html_node = LeafNode("i", "This is italic text")
        self.assertEqual(node.text_node_to_html_node(), expected_html_node)

    def test_text_node_to_html_node_code(self):
        node = TextNode("print('Hello, World!')", TextType.CODE)
        expected_html_node = LeafNode("code", "print('Hello, World!')")
        self.assertEqual(node.text_node_to_html_node(), expected_html_node)

    def test_text_node_to_html_node_image(self):
        node = TextNode("An image", TextType.IMAGE, url="https://example.com/image.png")
        expected_html_node = LeafNode("img", "", {"src": "https://example.com/image.png", "alt": "An image"})
        self.assertEqual(node.text_node_to_html_node(), expected_html_node)

    def test_text_node_to_html_node_plain_text(self):
        node = TextNode("Just some plain text", TextType.TEXT)
        expected_html_node = LeafNode("", "Just some plain text")
        self.assertEqual(node.text_node_to_html_node(), expected_html_node)



if __name__ == "__main__":
    unittest.main()