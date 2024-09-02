from htmlnode import HTMLNode
from leafnode import LeafNode

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag, None, children, props)
        if self.children == None or [] or "":
            raise ValueError ("Must have self.children")
        for object in self.children:
            if not isinstance(object, (ParentNode, LeafNode)):
                raise ValueError ("self.children Must have ParentNode, LeafNode objects")

    def to_html(self):
        if self.tag == None:
            raise ValueError ("self.tag is NONE")
        if self.children == None:
            raise ValueError ("Must have self.children")
        return (f'<{self.tag}>{"".join(list(node.to_html() for node in self.children))}</{self.tag}>')
    
