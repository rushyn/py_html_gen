class HTMLNode():
    def __init__(self, tag=None, value=None, children=[None], props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, HTML_node):
        if self.tag == HTML_node.tag and self.value == HTML_node.value and self.children == HTML_node.children and self.props == HTML_node.props:
            return True
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None:
            return
        return " ".join(list((f'{key}="{value}"') for (key, value) in self.props.items()))
    
    def __repr__(self):
        return(self.tag, self.value, self.children, self.props)
    

# def test():
#     node = HTMLNode("h1", "This is a text node", None, {"href": "https://www.google.com", "h1": "normal"})

#     print(f'|{node.props_to_html()}|')

# test()