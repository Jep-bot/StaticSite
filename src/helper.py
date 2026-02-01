from textnode import TextNode, TextType
import re 

def split_node(old_node, delimiter, text_type):
    if old_node.text.count(delimiter) % 2 != 0:
        raise ValueError("invalid Markdown syntax:"+delimiter+"closing delimter not found")
        
    texts = list(filter(None,old_node.text.split(delimiter)))
    new_nodes = []
    if len(texts) == 3:
        new_nodes = [
            TextNode(texts[0],TextType.TEXT), 
            TextNode(texts[1],text_type), 
            TextNode(texts[2],TextType.TEXT)
            ]
    elif len(texts) == 2:
        if old_node.text.startswith(delimiter):
            new_nodes = [
                TextNode(texts[0],text_type), 
                TextNode(texts[1],TextType.TEXT), 
                ]   
        else:
             new_nodes = [
                TextNode(texts[0],TextType.TEXT), 
                TextNode(texts[1],text_type) 
                ]
    return new_nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if delimiter not in node.text:
            new_nodes.append(node)
        else:
            new_nodes.extend(split_node(node, delimiter, text_type))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)",text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)",text)

def split_text_image_link(text, delimiter, text_type, extractor):
    matches = extractor(text)
    if len(matches) == 0:
        return [TextNode(text,TextType.TEXT)]
    new_nodes = []
    i = 0
    for matche in matches:
        text = text.replace(delimiter.format(matche[0],matche[1]),"{}{}{}".format(delimiter,i,delimiter))
        i+=1
    split_texts = filter(None,text.split(delimiter))
    for split_text in split_texts:
        if split_text.isdigit():
            image_link = matches[int(split_text)]
            new_nodes.append(TextNode(image_link[0], text_type, image_link[1]))
        else:
            new_nodes.append(TextNode(split_text,TextType.TEXT))
    return new_nodes

def split_nodes_image(old_nodes):
    delimiter = "![{}]({})"
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        new_nodes.extend(split_text_image_link(node.text,delimiter,TextType.IMAGE, extract_markdown_images))
    return new_nodes

def split_nodes_link(old_nodes):
    delimiter = "[{}]({})"
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        new_nodes.extend(split_text_image_link(node.text,delimiter,TextType.LINK, extract_markdown_links))
    return new_nodes

def text_to_textnodes(text):
    old_node = TextNode(text,TextType.TEXT)
    new_nodes = [old_node]
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    new_nodes = split_nodes_delimiter(new_nodes,"**",TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes,"_",TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes,"`",TextType.CODE)
    return new_nodes
