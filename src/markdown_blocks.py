from enum import Enum
from htmlnode import ParentNode
from textnode import TextNode, TextType
from util import text_to_textnode, text_node_to_html_node
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = []
    block = markdown.split("\n\n")
    for line in block:
        line = line.strip()
        if line != "":
            blocks.append(line)
    return blocks

def block_to_block_type(block):
    lines = block.strip().split("\n")
    # Code block check (entire block surrounded by three backticks)
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    # Heading check (line starts with 1-6 '#' followed by space)
    if re.match(r"^#{1,6} ", lines[0]):
        return BlockType.HEADING
    # Quote check (every line starts with "> ")
    if all(line.startswith("> ") for line in lines):
        return BlockType.QUOTE
    # Unordered list check (each line starts with "- ")
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    # Ordered list check (each line starts with "1. ", "2. ", etc.)
    if all(re.match(r"^\d+\.\s", line) for line in lines):
        return BlockType.ORDERED_LIST
    # If nothing else matches, it's a paragraph
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
   # split markdown into blocks
   blocks = markdown_to_blocks(markdown)
   children = []
   for block in blocks:
      html_node = block_to_html_node(block)
      children.append(html_node)
   return ParentNode("div", children)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case _:
            raise ValueError(f"invalid block type: {block_type}")

def text_to_children(text):
   text_nodes = text_to_textnode(text)
   nodes = []
   for text_node in text_nodes:
      html_node = text_node_to_html_node(text_node)
      nodes.append(html_node)
   return nodes

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    # count the number of '#' characters at the beginning of the line
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    code = block[4:-3]
    text_node = TextNode(code, TextType.TEXT)
    child = text_node_to_html_node(text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])

def ordered_list_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_item = ParentNode("li", children)
        html_items.append(html_item)
    return ParentNode("ol", html_items)

def unordered_list_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_item = ParentNode("li", children)
        html_items.append(html_item)
    return ParentNode("ul", html_items)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    if len(blocks) > 0:
        for block in blocks:
            block = block.strip()
            if block.startswith("# "):
                return block[2:]
  
    raise Exception("No H1 title found")