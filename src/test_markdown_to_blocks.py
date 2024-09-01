import unittest 
from functions import markdown_to_blocks

class Test_Markdown_To_Blocks(unittest.TestCase):
    def test_markdown_to_blocks_basic(self):
        input = ("# This is a heading"
                "\n"
                "\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it."
                "\n"
                "\n* This is the first list item in a list block"
                "\n* This is a list item"
                "\n* This is another list item"
                )
        
        output = [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                ("* This is the first list item in a list block"
                 "\n* This is a list item"
                 "\n* This is another list item")
                ]
        self.assertEqual(markdown_to_blocks(input), output)

    def test_markdown_to_blocks_basic_multy_blank_in(self):
        input = ("# This is a heading"
                "\n"
                "\n"
                "\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it."
                "\n"
                "\n"
                "\n"
                "\n"
                "\n* This is the first list item in a list block"
                "\n* This is a list item"
                "\n* This is another list item"
                "\n"
                "\n"
                "\n"
                )
        
        output = [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                ("* This is the first list item in a list block"
                 "\n* This is a list item"
                 "\n* This is another list item")
                ]
        self.assertEqual(markdown_to_blocks(input), output)

if __name__ == "__main__":
    unittest.main()