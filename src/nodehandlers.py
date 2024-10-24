from textnode import TextType, TextNode
import re

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

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """Splits strings into sections by the delimiter.  Sets the TextType for the sections 
    based on their section / the passed text_type.

    Parameters
    ----------
    old_nodes : list[str]
        A list of strings containing old nodes of text that need to be processed.
    delimiter: str
        The delimiter is the string to split the nodes on.
    text_type: TextType
        The text type to set the split node type to.  Normal text will be set as TextType.TEXT, 
        but the node being sliced off with the delimiter will be set to this type.
    
    Returns
    -------
    list[tuple]
        A list of tuples.  Each tuple contains both a URL and the alt text for the link.
    """
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

def split_nodes_image(old_nodes):
    """Takes a list of MD formatted strings and returns TextNode objects (images) populated with the string elements.

    Parameters
    ----------
    old_nodes : list[str]
        A list containing one or more MD formatted strings.
    
    Returns
    -------
    list[TextNode]
        A list of TextNode objects.  Each node is either an image link or a basic text node.
    """

    retval = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT.value:
            retval.append(node)
            continue

        # Hold modified nodes when they are ready
        modified_nodes = []
        # After stripping a chunk off a string, store the remainder here.
        remainder = ""
        links_initial = extract_markdown_images(node.text)
        for link in links_initial:
            image_alt = link[0]
            image_link = link[1]
            lines = ""
            if remainder == "":
                lines = node.text.split(f"![{image_alt}]({image_link})", 1)
            else:
                lines = remainder.split(f"![{image_alt}]({image_link})", 1)
            if len(lines) > 1:
                remainder = lines[1]
            modified_nodes.append(TextNode(text=lines[0], text_type=TextType.TEXT))
            modified_nodes.append(TextNode(text=link[0], text_type=TextType.IMAGE, url=link[1]))
        
        if remainder != "":
            modified_nodes.append(TextNode(text=remainder, text_type=TextType.TEXT))
        
        retval.extend(modified_nodes)
    
    return retval
        


def split_nodes_link(old_nodes):
    """Takes a list of MD formatted strings and returns TextNode objects (links) populated with the string elements.

    Parameters
    ----------
    old_nodes : list[str]
        A list containing one or more MD formatted strings.
    
    Returns
    -------
    list[TextNode]
        A list of TextNode objects.  Each node is either a link or a basic text node.
    """

    retval = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT.value:
            retval.append(node)
            continue

        # Hold modified nodes when they are ready
        modified_nodes = []
        # After stripping a chunk off a string, store the remainder here.
        remainder = ""
        links_initial = extract_markdown_links(node.text)
        for link in links_initial:
            found_alt = link[0]
            found_link = link[1]
            lines = ""
            if remainder == "":
                lines = node.text.split(f"[{found_alt}]({found_link})", 1)
            else:
                lines = remainder.split(f"[{found_alt}]({found_link})", 1)
            if len(lines) > 1:
                remainder = lines[1]
            modified_nodes.append(TextNode(text=lines[0], text_type=TextType.TEXT))
            modified_nodes.append(TextNode(text=link[0], text_type=TextType.LINK, url=link[1]))
        
        if remainder != "":
            modified_nodes.append(TextNode(text=remainder, text_type=TextType.TEXT))
        
        retval.extend(modified_nodes)
    
    return retval

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

# Adding a line and this comment so that I may do a test commit (testing formatting).


