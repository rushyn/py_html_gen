import re
import os
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
        text_blocks[i] = text_blocks[i].strip()
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
    
    if markdown[:2] == "> ":
        return BlockCode.blockquote
    
    if markdown[:2] == "* " or markdown[:2] == "- ":
        return BlockCode.unordered_list

    if markdown[:3] == "1. ":
        return BlockCode.ordered_list
    
    return BlockCode.paragraphs

def block_format(block, type):
    if BlockCode.heading in type:
        level = int(type[1]) + 1
        type = "h"
    match type:
        case BlockCode.heading:
            return block[level:].strip().split("\n")
        case BlockCode.code:
            return block[3:-3].strip().split("\n")
        case BlockCode.blockquote:
            block = block.strip().split("\n")
            for i in range(0, len(block)):
                block[i] = block[i][2:]
            return block
        case BlockCode.ordered_list:
            block = block.strip().split("\n")
            for i in range(0, len(block)):
                block[i] = block[i][3:]
            return block
        case BlockCode.unordered_list:
            block = block.strip().split("\n")
            for i in range(0, len(block)):
                block[i] = block[i][2:]
            return block
        case BlockCode.paragraphs:
            return block.strip().split("\n")
    


def line_type(block_type):
    if block_type in [BlockCode.code, BlockCode.unordered_list, BlockCode.ordered_list]:
        match block_type:
            case BlockCode.code:
                return "pre"
            case BlockCode.unordered_list:
                return "li"
            case BlockCode.ordered_list:
                return "li"    

def text_to_children(block):
    block_type = block_to_block_type(block)
    string_list = block_format(block, block_type)
    text_nodes = []
    parent_nodes = []
    for string in string_list:
        text_nodes = text_to_textnodes(string)
        leaf_nodes = []
        for node in text_nodes:
            leaf_nodes.append(text_node_to_html_node(node))
        if len(string_list) == 1:
            return leaf_nodes
        parent_nodes.append(ParentNode(line_type(block_type), leaf_nodes))
    return parent_nodes




def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in markdown_blocks:
        nodes.append(ParentNode(block_to_block_type(block), text_to_children(block)))
    return ParentNode("div", nodes)


def extract_title(markdown):
    markdown = markdown.split("\n")
    for line in markdown:
        if line[:2] == "# ":
            return (line[2:]).strip()
    raise Exception ("No H1 header found!!!")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {template_path} using {dest_path}")
    with open(from_path, "r") as file:
        markdown = file.read()
        file.close()
    with open(template_path, "r") as file:
        template = file.read()
        file.close()
    html_main_node = markdown_to_html_node(markdown)
    html = html_main_node.to_html()
    titel = extract_title(markdown)
    template = template.replace("{{ Content }}", html, 1)
    template = template.replace("{{ Title }}", titel, 1)
    print(template)
    with open(dest_path, "w") as page:
        page.write(template)
        page.close()