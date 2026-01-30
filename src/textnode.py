from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGES = "images"

class TextNode:

    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
        self.text == other.text and
        self.text_type == other.text_type and
        self.url == other.url
        )
    def __repr__(self):
        return "TextNode({}, {}, {})".format(self.text, self.text_type, self.url)

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text, None )
        case TextType.BOLD:
            return LeafNode("b", text_node.text, None )
        case TextType.ITALIC:
            return LeafNode("i", text_node.text, None )
        case TextType.CODE:
            return LeafNode("code", text_node.text, None )
        case TextType.LINK:
            if text_node.url == None:
                raise ValueError("No url provided")
            return LeafNode("a", text_node.text, {"href":text_node.url} )
        case TextType.IMAGES:
            if text_node.url == None:
                raise ValueError("No url provided")           
            return LeafNode("img", "", {"src":text_node.url,"alt":text_node.text} )
        case _:
            raise ValueError("TextType not supported:"+ text_node.text_type)
