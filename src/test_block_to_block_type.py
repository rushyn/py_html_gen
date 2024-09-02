import unittest 
from functions import block_to_block_type

class Test_Block_To_Block_Type(unittest.TestCase):
    def test_block_to_block_type(self):
        input = [
                "# Heading 1",
                "## Heading 2",
                "### Heading 3",
                "#### Heading 4",
                "##### Heading 5",
                "###### Heading 6",
                "This is a paragraph of text.",
                ("* Item 1\n"
                 "* Item 2\n"
                 "* Item 3"),
                ("1. Item 1\n"
                 "2. Item 2\n"
                 "3. Item 3"),
                 "> This is a quote.",
                ("```\n"
                 "This is code\n"
                 "```")
        ]
        
        results = [
                    "h1",
                    "h2",
                    "h3",
                    "h4",
                    "h5",
                    "h6",
                    "p",
                    "ol",
                    "ul",
                    "blockquote",
                    "code"
        ]
        
        for i in range(0, len(input)):
            self.assertEqual(block_to_block_type(input[i]), results[i])
    



if __name__ == "__main__":
    unittest.main()