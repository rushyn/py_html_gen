import unittest

from textnode import TextNode



class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node1, node2)

    def test_object_verables(self):
        node = TextNode("this is bad", "bold", "http://localhost:80")
        self.assertEqual(node.text, "this is bad")
        self.assertEqual(node.text_type, "bold")
        self.assertEqual(node.url, "http://localhost:80")

    def test_object_url_none(self):
        node = TextNode("this is bad", "bold")
        self.assertEqual(node.url, None)



if __name__ == "__main__":
    unittest.main()