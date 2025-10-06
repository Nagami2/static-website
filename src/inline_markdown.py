from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    new_nodes = []
    for old_node in old_nodes:
        # if the node is not a plain text node, add it to the list and continue
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        #Split the text of the current node by the delimiter
        split_parts = old_node.text.split(delimiter)

        #Check for valid markdown: must have an even number of delimiters
        if len(split_parts) % 2 == 0:
            raise ValueError(f"Invalid Markdown: unclosed delimiter '{delimiter}'")
        
        # process the split parts
        for i, part in enumerate(split_parts):
            if not part:
                # don't create nodes for empty strings
                continue

            # parts at even indices are plain text
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                # parts at odd indices are of the specified text_type (bold, code etc.)
                new_nodes.append(TextNode(part, text_type))
    return new_nodes

import re

def extract_markdown_links(markdown_text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", markdown_text)
    return matches

def extract_markdown_images(markdown_text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", markdown_text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        original_text = node.text
        images = extract_markdown_images(original_text)

        if not images:
            new_nodes.append(node)
            continue

        text_to_process = original_text
        for image_tuple in images:
            alt_text, url = image_tuple
            sections = text_to_process.split(f"![{alt_text}]({url})", 1)

            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section is not closed")
            
            # add the text before the image, it it exists
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            # add the image node
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url=url))
            # update the text to process for the next iteration
            text_to_process = sections[1]

        # add any remaining text after the last image
        if text_to_process:
            new_nodes.append(TextNode(text_to_process, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        original_text = node.text
        links = extract_markdown_links(original_text)

        if not links:
            new_nodes.append(node)
            continue

        text_to_process = original_text
        for link_tuple in links:
            anchor_text, url = link_tuple
            sections = text_to_process.split(f"[{anchor_text}]({url})", 1)

            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section is not closed")
            
            # add the text before the link, it it exists
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            # add the link node
            new_nodes.append(TextNode(anchor_text, TextType.LINK, url=url))
            # update the text to process for the next iteration
            text_to_process = sections[1]

        # add any remaining text after the last link
        if text_to_process:
            new_nodes.append(TextNode(text_to_process, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    # 1. start with a single node containing athe full text
    nodes = [TextNode(text, TextType.TEXT)]

    # 2. split by images, then links
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    # 3. split by bold, italic and code delimiters
    # Process bold first (longer delimiter), then italic (both * and _), then code
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    return nodes
