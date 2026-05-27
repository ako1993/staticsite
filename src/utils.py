from textnode import TextType, TextNode
import re


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter:str, text_type:TextType)->list:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            splits = node.text.split(delimiter)
            if len(splits)% 2 == 0:
                raise ValueError("Invalid Markdown")
            for i in range(len(splits)):
                if i % 2 != 0:
                    new_node = TextNode(splits[i], text_type)
                    new_nodes.append(new_node)
                else:
                    new_node = TextNode(splits[i], TextType.TEXT)
                    new_nodes.append(new_node)
    return new_nodes

def extract_markdown_images(text: str)->list[tuple]:
    result = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return result

def extract_markdown_links(text: str)->list[tuple]:
    result = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return result

def split_nodes_image(old_nodes:list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        result = re.split(r'(!\[[^\]]*\]\([^)]+\))', node.text)
        for part in result:
            match = re.match(r'(!\[[^\]]*\]\([^)]+\))', part)
            if part == "":
                continue
            elif match:
                image_parts = extract_markdown_images(part)
                for part in image_parts:
                    new_node = TextNode(part[0], TextType.IMAGE, part[1])
            else:
                new_node = TextNode(part, TextType.TEXT)
            new_nodes.append(new_node)
    return new_nodes
   

def split_nodes_link(old_nodes:list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        result = re.split(r'(\[[^\]]*\]\([^)]+\))', node.text)
        for part in result:
            match = re.match(r'(\[[^\]]*\]\([^)]+\))', part)
            if part == "":
                continue
            elif match:
                link_parts = extract_markdown_links(part)
                for part in link_parts:
                    new_node = TextNode(part[0], TextType.LINK, part[1])
            else:
                new_node = TextNode(part, TextType.TEXT)
            new_nodes.append(new_node)
    return new_nodes
    

