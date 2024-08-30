import unittest 

from leafnode import LeafNode


class Test_Leafnode(unittest.TestCase):
    def test_eq(self):
        node1 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node1, node2)

    def test_to_html(self):
        node1 = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node1.to_html(), "<p>This is a paragraph of text.</p>")
        self.assertEqual(node2.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_object_verables(self):
        Leaf_Node = LeafNode("h1", "This is a text node", {"href": "https://www.google.com"})
        self.assertEqual(Leaf_Node.tag, "h1")
        self.assertEqual(Leaf_Node.value, "This is a text node")
        self.assertEqual(Leaf_Node.children, None)
        self.assertEqual(Leaf_Node.props, {"href": "https://www.google.com"})

if __name__ == "__main__":
    unittest.main()