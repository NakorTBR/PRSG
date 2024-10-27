from textnode import TextType, TextNode
import re
from htmlnode import LeafNode, ParentNode
from print_colours import debug_colours as dc


block_type_paragraph = "paragraph"
block_type_quote = "quote"
block_type_code = "code"
block_type_ulist = "unordered_list"
block_type_olist = "ordered_list"
block_type_heading = "heading"

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
    # dc.d_print(f"TEXT: {text}", combo=dc.Colour.COMBO_OB)
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

    for node in old_nodes:
        if node.text_type != TextType.TEXT.value:
            # print(f"{dc.fg.red}SKIPPING TEXT TYPE TEXTNODE{dc.reset}: {node}")
            retval.append(node)
            continue

        modified_nodes = []
        lines = node.text.split(delimiter)
        if len(lines) % 2 == 0:
            raise ValueError("Bad markdown!  Element was not closed.")
        
        for i in range(len(lines)):
            # print(f"Line: {dc.fg.lightcyan}{lines[i]}{dc.reset}")
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
            # print(f"SUS: {dc.fg.lightred}{node}{dc.reset}")
            retval.append(node)
            continue

        # Hold modified nodes when they are ready
        modified_nodes = []
        # After stripping a chunk off a string, store the remainder here.
        remainder = ""
        links_initial = extract_markdown_images(node.text)

        # If no links were found then we just have a text node that 
        # needs to be appended to the list.
        if len(links_initial) == 0:
            modified_nodes.append(node)
            
        
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
        # print(f"{dc.fg.orange}{retval}{dc.reset}")
    
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
        if isinstance(links_initial, str):
            dc.d_print("Link parsed into string?", dc.Colour.COMBO_LGrR)
            old_nodes = [old_nodes]

        # print(f"LINK COUNT: {len(links_initial)}")
        # if len(links_initial) > 20:
        #     print(f"Link sus: {links_initial}")

        # If no links were found then we just have a text node that 
        # needs to be appended to the list.
        if len(links_initial) == 0:
            modified_nodes.append(node)
        
        # dc.d_print(f"Links:\n{links_initial}", dc.Colour.COMBO_GB)

        for link in links_initial:
            # try:
            #     print(f"{link[0]=}{link[1]=}")
            # except:
            #     dc.d_print("Error: Link data bad", dc.Colour.COMBO_LGrR)
                
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
    if text_node.text_type == TextType.ULIST.value:
        return LeafNode(tag="li", value=text_node.text)
    if text_node.text_type == TextType.OLIST.value:
        return LeafNode(tag="li", value=text_node.text)
    if text_node.text_type == TextType.LITEM.value:
        return LeafNode(tag="li", value=text_node.text)
        
    raise ValueError(f"Invalid text type: {text_node.text_type=}")

def text_to_textnodes(text):
    """Takes a string and converts it to TextNode objects.

    Parameters
    ----------
    text : str
        A list of strings to be processed into relevant TextNode objects.
    split : bool
        If you are passing in a string that is a chunk of MD text that still needs 
        to be split, pass True for the split variable.
    
    Returns
    -------
    list[TextNode]
        A list of TextNode objects.  Each node is properly split to the correct type 
        based on the content of the string.

    Note
    ----
    If there is a problem with this function then it happened in one of the called functions.  
    That is really all this function does.
    """


    # dc.d_print(text, combo=dc.Colour.COMBO_GB)
    node_links_split = split_nodes_link([TextNode(text=text, text_type=TextType.TEXT)])
    # dc.d_print(node_links_split, combo=dc.Colour.COMBO_GB)
    node_images_split = split_nodes_image(node_links_split)
    node_bold_split = split_nodes_delimiter(node_images_split, "**", TextType.BOLD)
    node_italic_split = split_nodes_delimiter(node_bold_split, "*", TextType.ITALIC)
    node_code_block_final = split_nodes_delimiter(node_italic_split, "`", TextType.CODE)

    # for node in node_code_block_final:
    #     print(f"\n{node}")

    return node_code_block_final


def markdown_to_blocks(markdown: str):
    """Takes a string and returns a list of block strings.  Blocks are logical groupings 
    of MD formatted strings (paragraphs, lists, etc.).

    Parameters
    ----------
    markdown : str
        A MD formatted string to be processed into relevant block strings.
    
    Returns
    -------
    list[str]
        A list of TextNode objects.  Each node is properly split to the correct type 
        based on the content of the string.
    """
    split = markdown.split("\n\n")

    # split = [i for i in split if i]
    blocks = []
    # for item in split:
    #     item.replace("\n", "<br />")
    # for block in split:
    #     block = block.strip()
    #     if block == "":
    #         block = "<br />"
    #     blocks.append(block)
    for i in range(len(split)):
        block = split[i].strip()
        block = block.replace("\n", "<br />")
        if block == "":
            blocks[-1] += "<br />"
            # print("Adding BR")
        else:
            blocks.append(block + "<br />")
    # print(f"BLOCKS IN MTB:\n{blocks}\n")

    return blocks

def block_to_block_type(block:str) -> str:
    """Takes a block (string of MD formatted text representing a basic block) and 
    returns a properly typed block.

    Parameters
    ----------
    block : str
        A string of MD formatted text representing a block.
    
    Returns
    -------
    str
        A string representing the type of block that was found.
    """

    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return block_type_heading
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return block_type_code
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return block_type_paragraph
        return block_type_quote
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return block_type_paragraph
        return block_type_ulist
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return block_type_paragraph
        return block_type_ulist
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return block_type_paragraph
            i += 1
        return block_type_olist
    return block_type_paragraph

def __strip_ulist(block):
    """Takes a block string and breaks it down, stripping the MD UL formatting.
    """
    lmd = "* "
    # print(f"BLOCK TEST:\n {block}")
    blines = block.split("<br />")
    glines = []
    for l in blines:
        if l:
            glines.append(l.lstrip(lmd))
    # print(f"BLOCK TEST POST: {glines}")

    return glines

def __strip_olist(block):
    """Takes a block string and breaks it down, stripping the MD OL formatting.
    """
    lmd = "* "
    # print(f"BLOCK TEST:\n {block}")
    blines = block.split("<br />")
    glines = []
    for l in blines:
        pattern = r"^\d+\.\s+"
        stripped_out = re.sub(pattern=pattern, repl='', string=l,  count=1)
        # print(stripped_out)
        if stripped_out:
            glines.append(stripped_out)
    # print(f"BLOCK TEST POST: {glines}")

    return glines

def text_to_list_item_text_node(text):
    """Converts a text string to a TextNode with type LITEM.  Regardless of being submitted 
      as either ULIST or OLIST, it will return LITEM TextNodes.  Does not check text.
    """
    return TextNode(text=text, text_type=TextType.LITEM)


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown=markdown)
    # print(f"BLOCKS DISPLAY:\n{blocks}")
    nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)
        # dc.d_print(f"BLOCK({block_type}):\n{block}", combo=dc.Colour.COMBO_PiB)

        if block_type != block_type_olist and block_type != block_type_ulist:
            new_nodes = text_to_textnodes(block)
            new_html_nodes = []
            for item in new_nodes:
                new_html_nodes.append(text_node_to_html_node(item))
            # dc.d_print(f"Non-list items:\n{new_html_nodes}", dc.Colour.COMBO_OB)
            nodes.extend(new_html_nodes)
        elif block_type == block_type_ulist:
            # print(f"SPAM: {block}")
            ulist_lines =__strip_ulist(block)
            new_list_nodes = []
            for item in ulist_lines:
                new_node = text_to_list_item_text_node(item)
                # new_list_nodes.append(new_node)
                new_list_nodes.append(text_node_to_html_node(new_node))
            # dc.d_print(f"ULIST ITEMS: {new_list_nodes}", combo=dc.Colour.COMBO_NOTICEMESENPAI)

            # At this point TextNodes are LITEM and not ULIST.  Use ULIST enum to know how to parent.
            parent = ParentNode(children=new_list_nodes, tag=TextType.ULIST.value)
            html_parent = parent.to_html()
            # print(f"Parent is as follows:\n{html_parent}")
            nodes.append(html_parent)
        elif block_type == block_type_olist:
            olist_lines =__strip_olist(block)
            new_list_nodes = []
            for item in olist_lines:
                new_node = text_to_list_item_text_node(item)
                new_list_nodes.append(text_node_to_html_node(new_node))
            # dc.d_print(f"OLIST ITEMS: {new_list_nodes}", combo=dc.Colour.COMBO_NOTICEMESENPAI)

            # At this point TextNodes are LITEM and not OLIST.  Use OLIST enum to know how to parent.
            parent = ParentNode(children=new_list_nodes, tag=TextType.OLIST.value)
            html_parent = parent.to_html()
            # print(f"Parent is as follows:\n{html_parent}")
            nodes.append(html_parent)
    
    master_parent = ParentNode(children=nodes, tag=TextType.DIV.value)
    return master_parent.to_html()



    
    
        