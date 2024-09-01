import unittest 
from functions import text_to_textnodes
from constant import TextCode
from textnode import TextNode



class Test_text_to_textnodes(unittest.TestCase):
    def test_basic_test1(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        result_nodes = [
                        TextNode("This is ",        TextCode.text),
                        TextNode("text",            TextCode.bold),
                        TextNode(" with an ",       TextCode.text),
                        TextNode("italic",          TextCode.italic),
                        TextNode(" word and a ",    TextCode.text),
                        TextNode("code block",      TextCode.code),
                        TextNode(" and an ",        TextCode.text),
                        TextNode("obi wan image",   TextCode.image, "https://i.imgur.com/fJRm4Vk.jpeg"),
                        TextNode(" and a ",         TextCode.text),
                        TextNode("link",            TextCode.link, "https://boot.dev"),
                    ]
        
        self.assertEqual(len(nodes), len(result_nodes))
        for i in range(0, len(nodes)):
            self.assertEqual(nodes[i], result_nodes[i])

    def test_basic_test2(self):
        text = "[link](https://boot.dev) This is **I have no idea why** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a "
        nodes = text_to_textnodes(text)
        result_nodes = [
                        TextNode("link",                TextCode.link, "https://boot.dev"),
                        TextNode(" This is ",            TextCode.text),
                        TextNode("I have no idea why",  TextCode.bold),
                        TextNode(" with an ",           TextCode.text),
                        TextNode("italic",              TextCode.italic),
                        TextNode(" word and a ",        TextCode.text),
                        TextNode("code block",          TextCode.code),
                        TextNode(" and an ",            TextCode.text),
                        TextNode("obi wan image",       TextCode.image, "https://i.imgur.com/fJRm4Vk.jpeg"),
                        TextNode(" and a ",             TextCode.text),
                    ]
        
        self.assertEqual(len(nodes), len(result_nodes))
        for i in range(0, len(nodes)):
            self.assertEqual(nodes[i], result_nodes[i])

    def test_link_only(self):
        text = "![alt text for image](http://image.glob/.info.jpg)\n"
        result_node = TextNode("alt text for image",       TextCode.image, "http://image.glob/.info.jpg")
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes[0], result_node)
        
if __name__ == "__main__":
    unittest.main()