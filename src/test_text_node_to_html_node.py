import unittest 
from functions import text_node_to_html_node
from textnode import *
from htmlnode import *
from leafnode import *

class Text_Node_To_Html_Node(unittest.TestCase):    
    def test_conversion(self):
        text_type_text      = TextNode("simple words for simpe text", "text")
        text_type_bold      = TextNode("WE ARE GOING TO WIN!!!", "bold")
        text_type_italic    = TextNode("i have no idea what I am doing", "italic")
        text_type_code      = TextNode("if something do something", "code")
        text_type_link      = TextNode("go to boot.dev", "link", "http://boot.dev")
        text_type_image     = TextNode("no image", "image", "http://image.no/none.jpg")

        leafnode_text      = text_node_to_html_node(text_type_text)
        leafnode_bold      = text_node_to_html_node(text_type_bold)
        leafnode_italic    = text_node_to_html_node(text_type_italic)
        leafnode_code      = text_node_to_html_node(text_type_code)
        leafnode_link      = text_node_to_html_node(text_type_link)
        leafnode_image     = text_node_to_html_node(text_type_image)

        self.assertEqual(leafnode_text.to_html(),   "simple words for simpe text")
        self.assertEqual(leafnode_bold.to_html(),   "<b>WE ARE GOING TO WIN!!!</b>")
        self.assertEqual(leafnode_italic.to_html(), "<i>i have no idea what I am doing</i>")
        self.assertEqual(leafnode_code.to_html(),   "<code>if something do something</code>")
        self.assertEqual(leafnode_link.to_html(),   '<a href="http://boot.dev">go to boot.dev</a>')
        self.assertEqual(leafnode_image.to_html(),  '<img src="http://image.no/none.jpg" alt="no image"></img>')

    def test_invalid_tag(self):
        with self.assertRaises(ValueError) as context:
            text_type_invalid   = TextNode("today is a good day", "good", "http://good.day")
            text_node_to_html_node(text_type_invalid)
            self.assertEqual(str(context.exception), "Invalid text type")

if __name__ == "__main__":
     unittest.main()

