import re
from textnode import *
from htmlnode import *
from leafnode import *
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
    
