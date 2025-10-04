from textnode import TextNode, TextType

def main():
    node1 = TextNode("This is some anchor text", TextType.LINK, url="https://example.com")
    print(node1)

if __name__ == "__main__":
    main()