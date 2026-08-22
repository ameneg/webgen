import re
from enum import Enum

from htmlnode import ParentNode, LeafNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = []
    for raw_block in markdown.split("\n\n"):
        block = raw_block.strip()
        if block == "":
            continue
        blocks.append(block)
    return blocks


def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")

    if re.match(r"#{1,6} ", block):
        return BlockType.HEADING

    if block.startswith("```") and block.endswith("```") and len(block) >= 6:
        return BlockType.CODE

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    if all(line.startswith(f"{i + 1}. ") for i, line in enumerate(lines)):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def text_to_children(text: str) -> list:
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(text_node) for text_node in text_nodes]


def paragraph_to_html_node(block: str) -> ParentNode:
    text = " ".join(block.split("\n"))
    return ParentNode("p", text_to_children(text))


def heading_to_html_node(block: str) -> ParentNode:
    level = 0
    while block[level] == "#":
        level += 1
    text = block[level + 1:]
    return ParentNode(f"h{level}", text_to_children(text))


def code_to_html_node(block: str) -> ParentNode:
    text = block[3:]
    if text.startswith("\n"):
        text = text[1:]
    text = text[:-3]
    code = LeafNode("code", text)
    return ParentNode("pre", [code])


def quote_to_html_node(block: str) -> ParentNode:
    lines = [line.lstrip(">").strip() for line in block.split("\n")]
    text = " ".join(lines)
    return ParentNode("blockquote", text_to_children(text))


def unordered_list_to_html_node(block: str) -> ParentNode:
    items = []
    for line in block.split("\n"):
        text = line[2:]
        items.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ul", items)


def ordered_list_to_html_node(block: str) -> ParentNode:
    items = []
    for i, line in enumerate(block.split("\n")):
        text = line[len(f"{i + 1}. "):]
        items.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ol", items)


def block_to_html_node(block: str) -> ParentNode:
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_to_html_node(block)
        case _:
            raise ValueError(f"unknown block type: {block_type}")


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    children = [block_to_html_node(block) for block in blocks]
    return ParentNode("div", children)
