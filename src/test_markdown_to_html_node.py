import unittest 
from functions import markdown_to_html_node



class test_markdown_to_html_node(unittest.TestCase):
    def test_markdown_to_html_node1(self):
        markdown = (
            "# Heading of All Headings!\n"
            "\n"
            "###### Heading of All Headings!\n"
            "\n"
            "She didn't understand how changed **worked**. When she looked at *today* compared to yesterday.\n"
            "It went through such rapid contortions that the little bear was forced to change his hold on it so many times he became confused in the darkness.\n"
            "\n"
            "This is a paragraph with a [link](https://www.google.com).\n"
            "\n"
            "![alt text for image](http://image.glob/.info.jpg)\n"
            "\n"
            "* Cat 1\n"
            "* Cat 2\n"
            "* Cat 3\n"
            "\n"
            "1. Dog 1\n"
            "2. Dog 2\n"
            "3. Dog 3\n"
            "\n"
            "> Today is a good day.\n"
            "\n"
            "```\n"
            "for item in something:\n"
            "```"
            )
        
        results = [
                    ["div", None, None],
                    ["h1", None, None],
                    [None, "Heading of All Headings!", None],
                    ["h6", None, None],
                    [None, "Heading of All Headings!", None],
                    ["p", None, None],
                    ["p", None, None],
                    [None, "She didn't understand how changed ", None],
                    ["b", "worked", None],
                    [None, ". When she looked at ", None],
                    ["i", "today", None],
                    [None, " compared to yesterday.", None],
                    ["p", None, None],
                    [None, "It went through such rapid contortions that the little bear was forced to change his hold on it so many times he became confused in the darkness.", None],
                    ["p", None, None],
                    [None, "This is a paragraph with a ", None],
                    ["a", "link", {'href': 'https://www.google.com'}],
                    [None, ".", None],
                    ["p", None, None],
                    ["img", "", {'src': 'http://image.glob/.info.jpg', 'alt': 'alt text for image'}],
                    ["ol", None, None],
                    ["li", None, None],
                    [None, "Cat 1", None],
                    ["li", None, None],
                    [None, "Cat 2", None],
                    ["li", None, None],
                    [None, "Cat 3", None],
                    ["ul", None, None],
                    ["li", None, None],
                    [None, "Dog 1", None],
                    ["li", None, None],
                    [None, "Dog 2", None],
                    ["li", None, None],
                    [None, "Dog 3", None],
                    ["blockquote", None, None],
                    [None, "Today is a good day.", None],
                    ["code", None, None],
                    [None, "for item in something:", None],
                ]
        html_main = markdown_to_html_node(markdown)


        
        i = 0
        #print(i)
        self.assertEqual(html_main.tag,     results[i][0])
        self.assertEqual(html_main.value,   results[i][1])
        self.assertEqual(html_main.props,   results[i][2])
        i += 1
        for html_node in html_main.children:
            #print(i)
            self.assertEqual(html_node.tag,     results[i][0])
            self.assertEqual(html_node.value,   results[i][1])
            self.assertEqual(html_node.props,   results[i][2])
            i += 1
            for node in html_node.children:
                #print(i)
                self.assertEqual(node.tag,     results[i][0])
                self.assertEqual(node.value,   results[i][1])
                self.assertEqual(node.props,   results[i][2])
                i += 1
                if node.children == None:
                    continue
                for n in node.children:
                    #print(i)
                    self.assertEqual(n.tag,     results[i][0])
                    self.assertEqual(n.value,   results[i][1])
                    self.assertEqual(n.props,   results[i][2])
                    i += 1












if __name__ == "__main__":
    unittest.main()