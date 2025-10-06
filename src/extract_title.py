import unittest

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

# --- Unit Tests ---
class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        md = """
# This is the Title

Some other content.
"""
        self.assertEqual(extract_title(md), "This is the Title")

    def test_no_title_raises_exception(self):
        md = "Just some text without a title."
        with self.assertRaises(Exception):
            extract_title(md)

    def test_not_h1_raises_exception(self):
        md = "## This is not an H1"
        with self.assertRaises(Exception):
            extract_title(md)