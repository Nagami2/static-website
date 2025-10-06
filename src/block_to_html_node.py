from htmlnode import HTMLNode, LeafNode, ParentNode
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType
from inline_markdown import text_to_textnodes

from typing import List
import re

def text_to_children(text) -> List[HTMLNode]:
    "Converts raw text with inline markdown to a list of HTMLNode children."
    text_nodes = text_to_textnodes(text)
    children: List[HTMLNode] = []
    for text_node in text_nodes:
        children.append(text_node.text_node_to_html_node())
    return children


def paragraph_to_html_node(block):
    # Clean up whitespace and join lines with spaces
    text = ' '.join(line.strip() for line in block.split('\n') if line.strip())
    if not text.strip():
        return None  # Skip empty paragraphs
    children = text_to_children(text)
    if not children and text.strip():
        # If no children but we have text, create a text node
        children = [LeafNode("", text)]
    elif not children:
        return None
    return ParentNode("p", list(children))

def heading_to_html_node(block):
    # count the "#" to determine heading level
    level = 0
    while block[level] == "#":
        level += 1

    if level < 1 or level > 6:
        raise ValueError(f"Invalid heading level: {level}")
    
    # remove the leading "#" and space
    text = block[level+1:].strip()
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    # code blocks are special: no inline markdown processing
    # Remove the backticks but preserve internal whitespace
    lines = block.split('\n')
    
    # Find and remove the opening ``` line
    start_index = 0
    for i, line in enumerate(lines):
        if line.strip() == '```':
            start_index = i + 1
            break
    
    # Find and remove the closing ``` line
    end_index = len(lines)
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].strip() == '```':
            end_index = i
            break
    
    # Extract the code content and remove common leading whitespace
    code_lines = lines[start_index:end_index]
    
    # Find the minimum indentation (excluding empty lines)
    min_indent = float('inf')
    for line in code_lines:
        if line.strip():  # Skip empty lines
            indent = len(line) - len(line.lstrip())
            min_indent = min(min_indent, indent)
    
    if min_indent == float('inf'):
        min_indent = 0
    
    # Remove the common leading whitespace
    text = '\n'.join(line[min_indent:].rstrip() if line.strip() else line.rstrip() for line in code_lines)
    
    code_child = LeafNode("code", text)
    return ParentNode("pre", [code_child])

def quote_to_html_node(block):
    lines = block.split("\n")
    # remove the leading "> " from each line and join them
    new_lines = []
    for line in lines:
        new_lines.append(line.lstrip("> ").strip())
    text = " ".join(new_lines)
    children = text_to_children(text)
    return ParentNode("blockquote", children)

def ulist_to_html_node(block):
    list_items = []
    lines = block.split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Remove the leading "* " or "- " 
        if line.startswith("* "):
            item_text = line[2:]
        elif line.startswith("- "):
            item_text = line[2:]
        else:
            continue
        item_children = text_to_children(item_text)
        if not item_children:
            # Create a text node if no children
            item_children = [LeafNode("", item_text)]
        list_items.append(ParentNode("li", list(item_children)))

    return ParentNode("ul", list_items)

def olist_to_html_node(block):
    list_items = []
    lines = block.split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Remove the leading "1. ", "2. ", etc.
        match = re.match(r"^\d+\.\s+(.*)$", line)
        if match:
            item_text = match.group(1)
            item_children = text_to_children(item_text)
            if not item_children:
                # Create a text node if no children
                item_children = [LeafNode("", item_text)]
            list_items.append(ParentNode("li", list(item_children)))
    return ParentNode("ol", list_items)

def markdown_to_html_node(markdown_text):
    blocks = markdown_to_blocks(markdown_text)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)
        node = None
        if block_type == BlockType.PARAGRAPH:
            node = paragraph_to_html_node(block)
        elif block_type == BlockType.HEADING:
            node = heading_to_html_node(block)
        elif block_type == BlockType.CODE:
            node = code_to_html_node(block)
        elif block_type == BlockType.QUOTE:
            node = quote_to_html_node(block)
        elif block_type == BlockType.UNORDERED_LIST:
            node = ulist_to_html_node(block)
        elif block_type == BlockType.ORDERED_LIST:
            node = olist_to_html_node(block)
        
        if node is not None:
            children.append(node)
    
    # wrap all the block nodes in a single "div"
    return ParentNode("div", children)