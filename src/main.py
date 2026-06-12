from textnode import TextNode
from copy_from_static_to_public import copy_from_static_to_public
from generate_page import generate_page
from generate_page import generate_page_recursive

def main():
    ##copy_from_static_to_public()
    ##generate_page("content/index.md", "template.html", "public/index.html")
    generate_page_recursive("/home/andre/projects/github/ako1993/staticsite/content", "template.html", "/home/andre/projects/github/ako1993/staticsite/public")
main()