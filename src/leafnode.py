from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return str(self.value)
        if self.props == None:
            return (f'<{self.tag}>{self.value}</{self.tag}>')
        return (f'<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>')

