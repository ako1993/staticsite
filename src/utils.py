from textnode import TextType, TextNode, text_node_to_html_node
from htmlnode import HTMLNode
from blocks import markdown_to_blocks, block_to_blocktype, BlockType
from parentnode import ParentNode
from leafnode import LeafNode
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

def text_to_textnodes(text: str)->list[TextNode]:
    node = TextNode(text, TextType.TEXT)
    bold = split_nodes_delimiter([node], "**", TextType.BOLD)
    italic = split_nodes_delimiter(bold, "_", TextType.ITALIC)
    code = split_nodes_delimiter(italic, "`", TextType.CODE)
    images = split_nodes_image(code)
    links = split_nodes_link(images)
    return links


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block: str) -> ParentNode:
    block_type = block_to_blocktype(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block: str) -> ParentNode:
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block: str) -> ParentNode:
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block: str) -> ParentNode:
    items = block.split("\n")
    html_items = []
    for item in items:
        parts = item.split(". ", 1)
        text = parts[1]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block: str) -> ParentNode:
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)



    

