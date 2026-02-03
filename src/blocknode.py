from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    split = markdown.split("\n\n")
    split = list(map(lambda x: x.strip("\n"),split))
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
      
