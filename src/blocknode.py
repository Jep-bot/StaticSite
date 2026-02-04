from enum import Enum
import re
from htmlnode import HTMLNode, ParentNode
from helper import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    split = markdown.split("\n\n")
    split = list(map(lambda x: x.strip(),split))
    split = list(filter(None,split))
    return split

def checke_list(block,char,block_type):
    block_by_lines = block.split("\n")
    for line in block_by_lines:
        if not line.startswith(char):
            return BlockType.PARAGRAPH
    return block_type

def checke_ordered_list(block,block_type):
    block_by_lines = block.split("\n")
    i = 1
    char = "{}. ".format(i) 
    for line in block_by_lines:
        if not line.startswith(char):
            return BlockType.PARAGRAPH
        i += 1
        char = "{}. ".format(i) 
    return block_type

def block_to_block_type(block): 
    if re.findall(r"^#{1,6}\s",block):
        return BlockType.HEADING
    elif block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    elif re.findall(r"\>\s?(\.*?)",block):
        return checke_list(block,">", BlockType.QUOTE)
    elif re.findall(r"\-\s\.*?\n?",block):
        return checke_list(block,"- ", BlockType.UNORDERED_LIST)
    elif re.findall(r"\d{1}\.\s\.*?\n?",block):
        return checke_ordered_list(block, BlockType.ORDERED_LIST)
    else:
        return BlockType.PARAGRAPH
      
def text_to_children(text):
    textNodes = text_to_textnodes(text)     
    htmlNodes = []
    for node in textNodes:
        htmlNodes.append(text_node_to_html_node(node))
    return htmlNodes

def header_to_htmlNode(text):
    header_num = block.count("#")
    header = ""
    for i in range(1,num):
        header += "#"
    children = text_to_children(text.replace(header,''))
    return ParentNode("h{}".format(header_num), children)

def quote_to_htmlNode(text):
    htmlNodes = []
    lines = text.split("\n")
    for line in lines:
        line = line.replace(">",'').replace("> ",'')
        children = text_to_children(line)
        htmlNodes.append(ParentNode("blockquote", children))
    return htmlNodes

def list_to_htmlNode(text,tags,index):
    htmlNodes = []
    lines = text.split("\n")
    for line in lines:
        children = text_to_children(line[index:])
        htmlNodes.append(ParentNode(tags[1],children))
    return ParentNode(tags[0],htmlNodes)

def block_to_parentNode(block, block_type):
    match block_type:
        case BlockType.HEADING:
            return header_to_htmlNode(block)
        case BlockType.QUOTE:
            return quote_to_htmlNode(block)
        case BlockType.CODE:
            return ParentNode("pre",
                              [text_node_to_html_node(
                                TextNode(block.replace('```\n','').replace("```",'')
                                ,TextType.CODE))])
        case BlockType.UNORDERED_LIST:
            return list_to_htmlNode(block,("ul","li"),2)
        case BlockType.ORDERED_LIST:
            return list_to_htmlNode(block,("ol","li"),3)
        case BlockType.PARAGRAPH:
            return ParentNode("p",text_to_children(block))
        case _:
            raise ValueError("BlockType {} is not supported".format(block_type))

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    htmlNodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        htmlNode = block_to_parentNode(block, block_type)
        htmlNodes.append(htmlNode)
    parnetNode = ParentNode("div",htmlNodes) 
    #print(htmlNodes)
    return parnetNode
