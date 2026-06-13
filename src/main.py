from copy_from_src_to_des import copy_from_src_to_des
from generate_page import generate_page_recursive
import sys

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    copy_from_src_to_des("/home/andre/projects/github/ako1993/staticsite/static", "/home/andre/projects/github/ako1993/staticsite/docs")
    generate_page_recursive("/home/andre/projects/github/ako1993/staticsite/content", "template.html", "/home/andre/projects/github/ako1993/staticsite/docs", basepath)
main()