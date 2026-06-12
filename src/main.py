from textnode import TextNode
from copy_from_static_to_public import copy_from_static_to_public
from generate_page import generate_page

def main():
    copy_from_static_to_public()
    generate_page("content/index.md", "template.html", "public/index.html")
main()