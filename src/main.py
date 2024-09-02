import shutil
import os
from textnode import *
from htmlnode import *
from leafnode import *
from functions import generate_page

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    list = os.listdir(dir_path_content)
    for item in list:
        if os.path.isdir(dir_path_content + item) == True:
            generate_pages_recursive(dir_path_content + item + "/", template_path, dest_dir_path + item +"/")
        elif item[-3:] == ".md":
            generate_page(dir_path_content + item, template_path, dest_dir_path + item[:-3] + ".html")



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
    generate_pages_recursive("./content/", "./template.html", "./public/")


main()