

from typing import List, Dict, Optional

class HTMLNode:
    def __init__(self, tag: str = "", value: str = "", children: Optional[List["HTMLNode"]] = None, props: Optional[Dict[str, str]] = None):
        self.tag = tag
        self.value = value
        self.children = list(children) if children is not None else []  # Convert to list to handle any sequence
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError("Subclasses should implement this method")
    
    def props_to_html(self):
        if not self.props:
            return ""
        
        attributes = ""
        for key, val in self.props.items():
            attributes += f' {key}="{val}"'
        return attributes

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (self.tag == other.tag and
                self.value == other.value and
                self.children == other.children and
                self.props == other.props)

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str = "", props: Optional[Dict[str, str]] = None):
        if value is None:  # Only reject None, not empty strings
            raise ValueError("LeafNode value cannot be None")
        if not value and tag != "img":  # Allow empty strings for img tags only
            raise ValueError("LeafNode value cannot be empty except for img tags")
        super().__init__(tag, value, [], props)

    def to_html(self):
        if not self.tag:
            return self.value
        props_html = self.props_to_html()
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"
    
    def __eq__(self, other):
        return isinstance(other, LeafNode) and super().__eq__(other)

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: List["HTMLNode"], props: Optional[Dict[str, str]] = None):
        if not tag:
            raise ValueError("Invalid HTML: ParentNode must have a tag")
        if children is None or not children:
            raise ValueError("Invalid HTML: ParentNode must have at least one child")
        super().__init__(tag, "", children, props)

    def to_html(self):
        # recursively builds an HTML string fromt he node and its children
        # start with the opening tag of the parent
        html_string = f"<{self.tag}{self.props_to_html()}>"
        # recursively call to_html on each child and append to the string
        for child in self.children:
            html_string += child.to_html()
        # close the parent tag
        html_string += f"</{self.tag}>"
        return html_string
    
    def __eq__(self, other):
        return isinstance(other, ParentNode) and super().__eq__(other)
