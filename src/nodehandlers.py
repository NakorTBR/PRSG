from textnode import TextType, TextNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    retval = []
    # print(f"OLD: {old_nodes}")

    for node in old_nodes:
        if node.text_type != TextType.TEXT.value:
            retval.append(node)
            continue

        modified_nodes = []
        lines = node.text.split(delimiter)
        if len(lines) % 2 == 0:
            raise ValueError("Bad markdown!  Element was not closed.")
        
        for i in range(len(lines)):
            if lines[i] == "":
                continue
            if i % 2 == 0:
                modified_nodes.append(TextNode(text=lines[i], text_type=TextType.TEXT))
            else:
                modified_nodes.append(TextNode(text=lines[i], text_type=text_type))
        
        retval.extend(modified_nodes)
    return retval

def extract_markdown_images(text):
    """Takes a markdown string and returns a list of tuples with an image URL and alt text.

    Parameters
    ----------
    text : str
        A string containing one or more MD image tags.
    
    Returns
    -------
    list[tuple]
        A list of tuples.  Each tuple contains both a URL and the alt text for the image.
    """

    # images
    reg = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    img_tuples = re.findall(reg, text)
    return img_tuples

def extract_markdown_links(text):
    """Takes a markdown string and returns a list of tuples with a URL and alt text.

    Parameters
    ----------
    text : str
        A string containing one or more MD link tags.
    
    Returns
    -------
    list[tuple]
        A list of tuples.  Each tuple contains both a URL and the alt text for the link.
    """

    # regular links
    reg = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    link_tuples = re.findall(reg, text)
    return link_tuples

