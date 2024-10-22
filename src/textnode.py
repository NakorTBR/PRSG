from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    HTML = "html"
    LEAF = "leaf"
    TEXT = "text"
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode():
    """A "TextNode" is an intermediate representation between Markdown and HTML, and is specific to inline markup.
    """
    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type.value
        self.url = url

    def __eq__(self, other):
        if self.text != other.text:
            return False
        if self.text_type != other.text_type:
            return False
        if self.url != other.url:
            return False
        
        return True
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT.value:
        return LeafNode(tag=None, value=text_node.text)
    if text_node.text_type == TextType.BOLD.value:
        return LeafNode(tag="b", value=text_node.text)
    if text_node.text_type == TextType.ITALIC.value:
        return LeafNode(tag="i", value=text_node.text)
    if text_node.text_type == TextType.CODE.value:
        return LeafNode(tag="code", value=text_node.text)
    if text_node.text_type == TextType.LINK.value:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    if text_node.text_type == TextType.IMAGE.value:
        return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
        
    raise ValueError(f"Invalid text type: {text_node.text_type}")
