import re
from textnode import *
from htmlnode import *
from leafnode import *
from parentnode import *
from constant import *

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextCode.text:
            return LeafNode(None, text_node.text)
        case TextCode.bold:
            return LeafNode("b", text_node.text)
        case TextCode.italic:
            return LeafNode("i", text_node.text)
        case TextCode.code:
            return LeafNode("code", text_node.text)
        case TextCode.link:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextCode.image:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError ("Invalid text type")
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextCode.text:

            old_node_text = node.text

            while len(old_node_text) != 0:

                if old_node_text.find(delimiter) == -1:
                    new_nodes.append(TextNode(old_node_text, "text"))
                    old_node_text = ""

                elif old_node_text.find(delimiter) > 0:
                    new_nodes.append(TextNode(old_node_text[:(old_node_text.find(delimiter))], "text"))
                    old_node_text = old_node_text[(old_node_text.find(delimiter)):]

                else:
                    old_node_text = old_node_text[len(delimiter):]
                    if old_node_text.find(delimiter) == -1:
                        raise Exception ("Termineter for text_type not found in string.")
                    new_nodes.append(TextNode(old_node_text[:(old_node_text.find(delimiter))], text_type))
                    old_node_text = old_node_text[(old_node_text.find(delimiter)) + len(delimiter):]
        else:
            new_nodes.append(node)

    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        link_list = extract_markdown_images(old_node.text)
        if len(link_list) == 0:
            new_nodes.append(TextNode(old_node.text,old_node.text_type, old_node.url))
            continue
        old_text = old_node.text
        for link in link_list:
            text = ((old_text.split(f"![{link[0]}]({link[1]})", 1))[0])
            if text != "":
                new_nodes.append(TextNode(text, TextCode.text))
            old_text = old_text.replace(text, "", 1)
            new_nodes.append(TextNode(link[0], TextCode.image, link[1]))
            old_text = old_text.replace(f"![{link[0]}]({link[1]})", "", 1)
        if old_text != "":
            new_nodes.append(TextNode(old_text, TextCode.text))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        link_list = extract_markdown_links(old_node.text)
        if len(link_list) == 0:
            new_nodes.append(TextNode(old_node.text, old_node.text_type, old_node.url))
            continue
        old_text = old_node.text
        for link in link_list:
            text = ((old_text.split(f"[{link[0]}]({link[1]})", 1))[0])
            if text != "":
                new_nodes.append(TextNode(text, TextCode.text))
            old_text = old_text.replace(text, "", 1)
            new_nodes.append(TextNode(link[0], TextCode.link, link[1]))
            old_text = old_text.replace(f"[{link[0]}]({link[1]})", "", 1)
        if old_text != "":
            new_nodes.append(TextNode(old_text, TextCode.text))

    return new_nodes
    

def text_to_textnodes(text):
    nodes = [TextNode(text, TextCode.text)]
    nodes = split_nodes_delimiter(nodes, "**", TextCode.bold)
    nodes = split_nodes_delimiter(nodes, "*", TextCode.italic)
    nodes = split_nodes_delimiter(nodes, "`", TextCode.code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def markdown_to_blocks(markdown):
    text_blocks = markdown.split("\n\n")
    for i in range (0, len(text_blocks)):
        text_blocks[i] = text_blocks[i].lstrip()
    for text in text_blocks:
        if text == "":
            text_blocks.remove(text)

    return text_blocks
    
def block_to_block_type (markdown):
    if markdown[0] == "#":
        for i in range (1, 7):
            if markdown[i] != "#":
                return BlockCode.heading + str(i)
    
    if markdown[:3] == "```" and markdown[-3:] == "```":
        return BlockCode.code
    
    if markdown[0] == ">":
        return BlockCode.blockquote
    
    if markdown[0] == "*" or markdown[0] == "-":
        return BlockCode.ordered_list

    if markdown[:3] == "1. ":
        return BlockCode.unordered_list
    
    return BlockCode.paragraphs

def block_format(block, type):
    if BlockCode.heading in type:
        level = int(type[1]) + 1
        type = "h"
    match type:
        case BlockCode.heading:
            return block[level:].split("\n")
        case BlockCode.code:
            return block[3:-3].split("\n")
        case BlockCode.blockquote:
            block = block.split("\n")
            for i in range(0, len(block)):
                block[i] = block[i][2:]
            return block
        case BlockCode.ordered_list:
            block = block.split("\n")
            for i in range(0, len(block)):
                block[i] = block[i][2:]
            return block
        case BlockCode.unordered_list:
            block = block.split("\n")
            for i in range(0, len(block)):
                block[i] = block[i][3:]
            return block
        case BlockCode.paragraphs:
            return block.split("\n")
    



def text_to_children(block):
    block_type = block_to_block_type(block)
    string_list = block_format(block, block_type)
    text_nodes = []
    leaf_nodes = []
    for string in string_list:
        text_nodes = text_to_textnodes(string)
        for node in text_nodes:
            leaf_nodes.append(text_node_to_html_node(node))
    if block_type in [BlockCode.code, BlockCode.unordered_list, BlockCode.ordered_list]:
        for node in leaf_nodes:
            if node.tag == None:
                match block_type:
                    case BlockCode.code:
                        node.tag = "pre"
                    case BlockCode.unordered_list:
                        node.tag = "li"
                    case BlockCode.ordered_list:
                        node.tag = "li"
    return leaf_nodes




def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in markdown_blocks:
        nodes.append(ParentNode(block_to_block_type(block), text_to_children(block)))
    return HTMLNode("div", None, nodes)


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

# node0 = markdown_to_html_node(markdown)


# print("++++++++++++++++++++++")
# print("++++++++++++++++++++++")
# print("++++++++++++++++++++++")
# print("++++++++++++++++++++++")
# print(f"{node0.tag} | {node0.value} | {node0.props}")
# for node in node0.children:
#     print("-----------------")
#     print(len(node.children))
#     print(f"{node.tag} | {node.value} | {node.props}")
#     print("-----------------")
#     for n in node.children:
#         print(f"{n.tag} | {n.value} | {n.props}")
# print("++++++++++++++++++++++")
