

class HTMLNode:
    def __init__(self, tag: str = "", value: str = "", children = [], props: dict = {}):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Subclasses should implement this method")
    
    def props_to_html(self):
        if not self.props:
            return ""
        
        attributes = ""
        for key, val in self.props.items():
            attributes += f' {key}="{val}"'
        return attributes
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    