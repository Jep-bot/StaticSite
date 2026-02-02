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

def block_to_block_type(block):
    if re.findall(r"^#{1,6}\s",block):
        return BlockType.HEADING
    elif re.findall(r"^`{3}\n(\.*?)`{3}",block):
        return BlockType.CODE
    elif re.findall(r">\s?(\.*?)\n?",block):
        return BlockType.QUOTE
    elif re.findall(r"-\s(\.*?)\n?",block):
        return BlockType.UNORDERED_LIST
    elif re.findall(r"\d{1}\.\s(\.*?)\n?",block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
      
