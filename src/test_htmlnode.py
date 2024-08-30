import unittest

from htmlnode import HTMLNode
from textnode import TextNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode("h1", "This is a text node", None, {"href": "https://www.google.com"})
        node2 = HTMLNode("h1", "This is a text node", None, {"href": "https://www.google.com"})
        self.assertEqual(node1, node2)

    def test_props_to_html(self):
        node = HTMLNode("h1", "This is a text node", None, {"href": "https://www.google.com", "h1": "normal"})
        self.assertEqual(node.props_to_html(), 'href="https://www.google.com" h1="normal"')

    def test_object_verables(self):
        Text_node1 = TextNode("this is bad", "bold", "http://localhost:80")
        Text_node2 = TextNode("this is good", "italic", "https://www.boot.dev/")
        HTML_node = HTMLNode("h1", "This is a text node", [Text_node1, Text_node2], {"href": "https://www.google.com"})
        self.assertEqual(HTML_node.tag, "h1")
        self.assertEqual(HTML_node.value, "This is a text node")
        self.assertEqual(HTML_node.children, [Text_node1, Text_node2])
        self.assertEqual(HTML_node.props, {"href": "https://www.google.com"})


if __name__ == "__main__":
    unittest.main()