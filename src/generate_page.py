from block_to_html_node import markdown_to_html_node

def extract_title(markdown):
    """
    Extracts the H1 title from a markdown string.

    Args:
        markdown (str): The markdown content.

    Returns:
        str: The text of the H1 heading.

    Raises:
        Exception: If no H1 heading is found.
    """
    for line in markdown.split('\n'):
        if line.startswith("# "):
            return line[2:].strip() # Slice to remove '# '
    raise Exception("Validation Error: All pages need a single h1 header.")



import os
# Assuming markdown_to_html_node is in another file, e.g., 'block_markdown'
# from block_markdown import markdown_to_html_node

def generate_page(from_path, template_path, dest_path, base_path="/"):
    """
    Generates a static HTML page from a markdown file and a template.
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # 1. Read the markdown and template files
    with open(from_path, 'r') as f:
        markdown_content = f.read()

    with open(template_path, 'r') as f:
        template_content = f.read()

    # 2. Convert markdown to HTML and extract the title
    html_content = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)

    # 3. Replace placeholders in the template
    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)

    # replace relative paths with the provided base_path
    final_html = final_html.replace('href="/', f'href="{base_path}')
    final_html = final_html.replace('src="/', f'src="{base_path}')

    # 4. Write the new HTML to the destination path
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    with open(dest_path, 'w') as f:
        f.write(final_html)

def generate_pages_recursive(content_dir_path, template_path, dest_dir_path, base_path="/"):
    """
    Recursively generates HTML pages from markdown files in a content directory.
    """
    for item in os.listdir(content_dir_path):
        source_path = os.path.join(content_dir_path, item)
        dest_path = os.path.join(dest_dir_path, item)

        # If the item is a directory, make a recursive call
        if os.path.isdir(source_path):
            # Create the corresponding directory in the destination
            os.makedirs(dest_path, exist_ok=True)
            generate_pages_recursive(source_path, template_path, dest_path, base_path)  
        
        # If the item is a markdown file, generate a page for it
        elif source_path.endswith(".md"):
            # Change the extension from .md to .html for the destination
            html_dest_path = os.path.splitext(dest_path)[0] + ".html"
            
            # Call the function from the previous lesson
            generate_page(source_path, template_path, html_dest_path, base_path)
