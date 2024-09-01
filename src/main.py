import shutil
import os
from textnode import *
from htmlnode import *
from leafnode import *

def copy(src, des):
    os.mkdir(des)
    list = os.listdir(src)
    for item in list:
        if os.path.isdir(src + item) == True:
            copy(src + item + "/", des + item + "/")
        else:
            print(shutil.copy(src + item, des + item))

def delete_public():
    if os.path.exists("./public/") == True:
        shutil.rmtree("public")
    copy("./static/", "./public/")
    


def main():
    delete_public()

    text_node = TextNode("This is a text node", "bold", "https://www.boot.dev")
    print(text_node.__repr__())

delete_public()