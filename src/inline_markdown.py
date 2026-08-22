from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception("invalid markdown syntax")
        for i, part in enumerate(parts):
            if i % 2 == 0:
                part_type = TextType.TEXT
            else:
                part_type = text_type
            new_nodes.append(TextNode(part, part_type))
    return new_nodes

def extract_markdown_images(text: str) -> list[tuple]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue
        remaining = node.text
        for image_alt, image_link in images:
            before, remaining = remaining.split(f"![{image_alt}]({image_link})", 1)
            if before != "":
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
        if remaining != "":
            new_nodes.append(TextNode(remaining, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
        remaining = node.text
        for link_text, link_url in links:
            before, remaining = remaining.split(f"[{link_text}]({link_url})", 1)
            if before != "":
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
        if remaining != "":
            new_nodes.append(TextNode(remaining, TextType.TEXT))
    return new_nodes
