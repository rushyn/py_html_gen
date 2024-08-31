import unittest 
from textnode import *
from htmlnode import *
from leafnode import *
from constant import *
from functions import split_nodes_delimiter


class Split_Nodes_Delimiter(unittest.TestCase):
    def test_base_case(self):
        nodes = split_nodes_delimiter([TextNode("This is text with `a` `code block` word", "text")], "`", "code")
        self.assertEqual(len(nodes), 5)

        results = [
            ["This is text with ", "text"],
            ["a", "code"],
            [" ", "text"],
            ["code block", "code"],
            [" word", "text"],
        ]

        i = 0
        for node in nodes:
            self.assertEqual([node.text, node.text_type], results[i])
            i += 1

    def test_multy_node(self):
        input_nodes = [
                    TextNode("This is text with `a` `code block` word", "text"),
                    TextNode("today is a sunny day", "bold"),
                    TextNode("lets **run** for it!", "text"),
                    TextNode("*i have no idea* maybe we can cook, *but we have to go shopping first.*", "text"),
                    ]
        
        nodes = split_nodes_delimiter(input_nodes, "`", "code")
        nodes = split_nodes_delimiter(nodes, "**", "bold")
        nodes = split_nodes_delimiter(nodes, "*", "italic")

        self.assertEqual(len(nodes), 5 + 1 + 3 + 3)

        results = [
            ["This is text with ", "text"],
            ["a", "code"],
            [" ", "text"],
            ["code block", "code"],
            [" word", "text"],
            ["today is a sunny day", "bold"],
            ["lets ", "text"],
            ["run", "bold"],
            [" for it!", "text"],
            ["i have no idea", "italic"],
            [" maybe we can cook, ", "text"],
            ["but we have to go shopping first.", "italic"],
        ]

        i = 0
        for node in nodes:
            self.assertEqual([node.text, node.text_type], results[i])
            i += 1

    def test_exception(self):
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([TextNode("This is text with `a` `code block` word", "text")], "`", "code")
            self.assertEqual(str(context.exception), "Termineter for text_type not found in string.")


if __name__ == "__main__":
     unittest.main()