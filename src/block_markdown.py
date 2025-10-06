def markdown_to_blocks(markdown_text):
    """
    splits a markdown string into a list of blocks
    """
    blocks = markdown_text.split("\n\n")
    cleaned_blocks = []
    for block in blocks:
        if block == "":
            continue
        cleaned_blocks.append(block.strip())
    return cleaned_blocks

from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


import re

def block_to_block_type(block):
    block = block.strip()  # Remove leading/trailing whitespace from the whole block
    
    # check for heading
    if re.match(r"^#{1,6}\s+", block):
        return BlockType.HEADING
    
    # check for code block (triple backticks)
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    lines = [line.strip() for line in block.split("\n") if line.strip()]

    # check for quote (lines starting with >)
    if lines and all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    
    # check for unordered list (lines starting with * or -)
    if lines and all(line.startswith(("* ", "- ")) for line in lines):
        return BlockType.UNORDERED_LIST
    
    # check for ordered list (lines starting with 1., 2., etc.)
    if lines and all(re.match(r"^\d+\.\s+", line) for line in lines):
        return BlockType.ORDERED_LIST
    
    # default to paragraph
    return BlockType.PARAGRAPH