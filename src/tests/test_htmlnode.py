from htmlnode import HTMLNode, LeafNode, ParentNode
import unittest

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        # test case with multiple properties
        node = HTMLNode(
            tag="a", 
            value = "Click me!",
            props={"href": "https://example.com", "target": "_blank"}
        )
        expected_props = ' href="https://example.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected_props)

    def test_props_to_html_single_prop(self):
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

    # --- LeafNode Tests ---
    
    def test_leafnode_to_html_p(self):
        """Test a simple paragraph LeafNode."""
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_leafnode_to_html_with_props(self):
        """Test a LeafNode with HTML attributes."""
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com", "target": "_blank"})
        expected_html = '<a href="https://www.google.com" target="_blank">Click me!</a>'
        self.assertEqual(node.to_html(), expected_html)

    def test_leafnode_to_html_no_tag(self):
        """Test a LeafNode without a tag, which should return raw text."""
        node = LeafNode("", "Just plain text.")
        self.assertEqual(node.to_html(), "Just plain text.")
        
    def test_leafnode_no_value_raises_error(self):
        """Test that LeafNode raises a ValueError if no value is provided."""
        with self.assertRaises(ValueError):
            # This should fail because a value is required.
            LeafNode("p", "")

    # --- ParentNode Tests ---
    
    def test_parentnode_to_html_with_leaf_children(self):
        """Test a ParentNode with several LeafNode children."""
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode("", " and normal text"),
                LeafNode("i", " and some italic text."),
            ],
        )
        expected_html = "<p><b>Bold text</b> and normal text<i> and some italic text.</i></p>"
        self.assertEqual(node.to_html(), expected_html)

    def test_parentnode_to_html_nested(self):
        """Test a ParentNode containing another ParentNode."""
        nested_node = ParentNode("b", [LeafNode("", "this is bold")])
        top_node = ParentNode(
            "div",
            [
                LeafNode("", "Here is a div with "),
                nested_node,
                LeafNode("", " inside."),
            ],
            {"class": "container"}
        )
        expected_html = '<div class="container">Here is a div with <b>this is bold</b> inside.</div>'
        self.assertEqual(top_node.to_html(), expected_html)
        
    def test_parentnode_deeply_nested(self):
        """Test multiple levels of nesting."""
        node = ParentNode("html", [
            ParentNode("body", [
                ParentNode("div", [
                    LeafNode("h1", "Website Title")
                ])
            ])
        ])
        expected_html = "<html><body><div><h1>Website Title</h1></div></body></html>"
        self.assertEqual(node.to_html(), expected_html)

    def test_parentnode_invalid_constructor(self):
        """Test that ParentNode raises ValueErrors for invalid initialization."""
        leaf = LeafNode("p", "hello")
        
        # Test missing tag
        with self.assertRaises(ValueError):
            ParentNode("", [leaf])
            
        # Test missing children (None)
        with self.assertRaises(ValueError):
            ParentNode("div", None)
            
        # Test missing children (empty list)
        with self.assertRaises(ValueError):
            ParentNode("div", [])


if __name__ == "__main__":
    unittest.main()