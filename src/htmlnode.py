

class HTMLNode():
    def __init__(self, tag: str=None, value: str=None, children: "list[HTMLNode]"=None, props: dict[str, str]=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None:
            return "" 
        result = ""
        for prop in self.props:
            result = f'{result} {prop}="{self.props[prop]}"'
        return result
            
    def __repr__(self):
        return f'tag: {self.tag}\nvalue: {self.value}\nchildren: {self.children}\nprops: {self.props}'

    

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value:str, props: dict[str, str]=None):
        super(LeafNode, self).__init__(tag, value, props=props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    
    def __repr__(self):
        return f'tag: {self.tag}\nvalue: {self.value}\nprops: {self.props}'

    
class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: "list[HTMLNode]", props: dict[str, str]=None):
        super(ParentNode, self).__init__(tag=tag, children=children, props=props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("tag missing")
        if not self.children:
            raise ValueError("children missing")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f'<{self.tag}>{children_html}</{self.tag}>'
        