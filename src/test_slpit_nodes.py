import unittest 
from functions import split_nodes_image, split_nodes_link
from textnode import TextNode
from constant import TextCode

class Test_Split_Nodes(unittest.TestCase):
    def test_split_link_basic(self):
        node = TextNode(
                "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                TextCode.text,
                )
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 4)
        results = [
                    ["This is text with a link ",   TextCode.text,  None],
                    ["to boot dev",                 TextCode.link,  "https://www.boot.dev"],
                    [" and ",                       TextCode.text,  None],
                    ["to youtube",                  TextCode.link,  "https://www.youtube.com/@bootdotdev"],
                ]
        i = 0
        for node in new_nodes:
            self.assertEqual(node.text,        results[i][0])
            self.assertEqual(node.text_type,   results[i][1])
            self.assertEqual(node.url,         results[i][2])
            i += 1


    def test_split_image_basic(self):
        node = TextNode(
                "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
                TextCode.text,
                )
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 4)
        results = [
                    ["This is text with a ",    TextCode.text,      None],
                    ["rick roll",               TextCode.image,     "https://i.imgur.com/aKaOqIh.gif"],
                    [" and ",                   TextCode.text,      None],
                    ["obi wan",                 TextCode.image,     "https://i.imgur.com/fJRm4Vk.jpeg"],
                ]
        i = 0
        for node in new_nodes:
            self.assertEqual(node.text,        results[i][0])
            self.assertEqual(node.text_type,   results[i][1])
            self.assertEqual(node.url,         results[i][2])
            i += 1


    def test_split_link_multy_node_input(self):
        nodes = [
            TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextCode.text,
            ),
            TextNode(
            "Link to google [google link](https://www.google.com) and [to bing](https://www.bing.com) thats all for now",
            TextCode.text,
            ),
            TextNode(
                "Dude won just by waiting", TextCode.text
            ),
            TextNode(
                "[steam](https://steamcommunity.com)", TextCode.text
            )
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertEqual(len(new_nodes), 11)

        results = [
            ["This is text with a link ",   TextCode.text,  None],
            ["to boot dev",                 TextCode.link,  "https://www.boot.dev"],
            [" and ",                       TextCode.text,  None],
            ["to youtube",                  TextCode.link,  "https://www.youtube.com/@bootdotdev"],
            ["Link to google ",             TextCode.text,  None],
            ["google link",                 TextCode.link,  "https://www.google.com"],
            [" and ",                       TextCode.text,  None],
            ["to bing",                     TextCode.link,  "https://www.bing.com"],
            [" thats all for now",          TextCode.text,  None],
            ["Dude won just by waiting",    TextCode.text,  None],
            ["steam",                       TextCode.link,  "https://steamcommunity.com"],
        ]
        i = 0
        for node in new_nodes:
            self.assertEqual(node.text,        results[i][0])
            self.assertEqual(node.text_type,   results[i][1])
            self.assertEqual(node.url,         results[i][2])
            i += 1

    def test_split_multy_node_input(self):
        nodes = [
                TextNode(
                    "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
                    TextCode.text,
                ),
                TextNode(
                    "this is a funny screen cap ![rick roll](https://i.imgur.com/capsscren.jpg) thats all for now",
                    TextCode.text,
                ),
                TextNode(
                    "no image here",
                    TextCode.text
                ),
                TextNode(
                    "![steam](http://nowimage.com/Castle_Geyser.jpg)",
                    TextCode.text
                )
        ]

        new_nodes = split_nodes_image(nodes)
        self.assertEqual(len(new_nodes), 9)
        results = [
                    ["This is text with a ",        TextCode.text,      None],
                    ["rick roll",                   TextCode.image,     "https://i.imgur.com/aKaOqIh.gif"],
                    [" and ",                       TextCode.text,      None],
                    ["obi wan",                     TextCode.image,     "https://i.imgur.com/fJRm4Vk.jpeg"],
                    ["this is a funny screen cap ", TextCode.text,      None],
                    ["rick roll",                   TextCode.image,     "https://i.imgur.com/capsscren.jpg"],
                    [" thats all for now",           TextCode.text,      None],
                    ["no image here",               TextCode.text,      None],
                    ["steam",                       TextCode.image,     "http://nowimage.com/Castle_Geyser.jpg"],
                ]
        i = 0
        for node in new_nodes:
            print(i)
            self.assertEqual(node.text,        results[i][0])
            self.assertEqual(node.text_type,   results[i][1])
            self.assertEqual(node.url,         results[i][2])
            i += 1   

if __name__ == "__main__":
    unittest.main()