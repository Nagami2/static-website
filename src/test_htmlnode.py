from htmlnode import HTMLNode
import unittest

class TestHTMLNode(unittest.TestCase):
    def text_props_to_html(self):
        # test case with multiple properties
        node = HTMLNode(
            tag="a", 
            value = "Click me!",
            props={"href": "https://example.com", "target": "_blank"}
        )
        expected_props = ' href="https://example.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected_props)

    def text_props_to_html_single_prop(self):
        # test case with a single property
        node = HTMLNode(
            tag="img", 
            props={"src": "image.png"}
        )
        expected_props = ' src="image.png"'
        self.assertEqual(node.props_to_html(), expected_props)

    def test_props_to_html_no_props(self):
        # test case with no properties
        node = HTMLNode(tag="div")
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        node = HTMLNode(
            tag="p", 
            value="Hello, World!", 
            children=[HTMLNode(tag="b", value="Bold Text")], 
            props={"class": "intro"}
        )
        expected_repr = ("HTMLNode(tag=p, value=Hello, World!, "
                         "children=[HTMLNode(tag=b, value=Bold Text, children=[], props={})], "
                         "props={'class': 'intro'})")
        self.assertEqual(repr(node), expected_repr)

if __name__ == "__main__":
    unittest.main()