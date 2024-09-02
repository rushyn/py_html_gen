from functions import extract_title
import unittest

class Test_Extract_Title(unittest.TestCase):
    def test_extract_title_esay1(self):
        markdown = "# This is a unit"
        self.assertEqual(extract_title(markdown), "This is a unit")

    def test_extract_title_esay2(self):
        markdown = "# This is a unit "
        self.assertEqual(extract_title(markdown), "This is a unit")

    def test_extract_title1(self):
        markdown = "# This is a unit \n Today is a good day. \n Now we can have fun!"
        self.assertEqual(extract_title(markdown), "This is a unit")
    
    def test_extract_title2(self):
        markdown = "This is a unit \n# Today is a good day. \n Now we can have fun!"
        self.assertEqual(extract_title(markdown), "Today is a good day.")

    def test_extract_title_exception(self):
        with self.assertRaises(Exception) as context:
            markdown = "This is a unit \n Today is a good day. \n Now we can have fun!"
            self.assertEqual(extract_title(markdown), "No H1 header found!!!")


if __name__ == "__main__":
    unittest.main()