import unittest 


from parentnode import ParentNode
from leafnode import LeafNode

class Test_ParentNode(unittest.TestCase):
        def test_to_html(self):
            node = ParentNode(
                "p",
                [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text"),
                ],
            )
            self.assertEqual(node.to_html(), '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')

        def test_parent_in_parent(self):
            node = ParentNode(
                "p",
                [
                    LeafNode("b", "Bold text"),
                    ParentNode("p",
                                [
                                LeafNode(None, "Normal text"),
                                LeafNode("i", "italic text"),
                                LeafNode("b", "Bold text"),
                                LeafNode("b", "Bold text"),
                                LeafNode("i", "italic text"),
                                LeafNode(None, "Normal text"),
                                ]           
                    ),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text"),
                ],
            )
            self.assertEqual(node.to_html(), '<p><b>Bold text</b><p>Normal text<i>italic text</i><b>Bold text</b><b>Bold text</b><i>italic text</i>Normal text</p>Normal text<i>italic text</i>Normal text</p>')

        def test_no_children(self):
            with self.assertRaises(ValueError) as context:
                node = ParentNode("p", None)
                self.assertEqual(str(context.exception), "Must have self.children")
                node = ParentNode("p", [])
                self.assertEqual(str(context.exception), "self.children Must have ParentNode, LeafNode objects")



if __name__ == "__main__":
    unittest.main()