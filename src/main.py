from textnode import *
from htmlnode import *
from leafnode import *

def main():
    text_node = TextNode("This is a text node", "bold", "https://www.boot.dev")
    print(text_node.__repr__())

main()