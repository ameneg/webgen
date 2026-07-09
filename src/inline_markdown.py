from textnode import TextNode, TextType

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


        
