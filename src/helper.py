from textnode import TextNode, TextType

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
        else:
            if delimiter not in node.text:
                new_nodes.append(node)
            else:
                new_nodes.extend(split_node(node, delimiter, text_type))
    return new_nodes
                    
