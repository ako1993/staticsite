from utils import markdown_to_html_node
from extract_title import extract_title
from split_and_replace import split_and_replace
from pathlib import Path
import os
import shutil

def generate_page(from_path:str, template_path:str, dest_path:str):
    print(f"Generating page {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as file:
        contents = file.read()
    page_content = markdown_to_html_node(contents)
    page_content = page_content.to_html()
    title = extract_title(contents)
    with open(template_path, 'r') as file:
        template_html = file.read()
    full_html_page = split_and_replace(template_html, page_content, title)
    dest_path = Path(dest_path)
    dest_path.parent.mkdir(parents=True, exist_ok = True)
    dest_path.write_text(full_html_page)

def generate_page_recursive(dir_path_content:str, template_path:str, dest_dir_path:str):
    for root, dirs, files in os.walk(dir_path_content):
        rel_path = os.path.relpath(root, dir_path_content)
        des_path = os.path.join(dest_dir_path, rel_path)
        os.makedirs(des_path, exist_ok=True)
        for file in files:
            src_file = os.path.join(root, file)
            file = file.replace(".md", ".html")
            dest_file = os.path.join(des_path, file)
            generate_page(src_file, template_path, dest_file)

    
