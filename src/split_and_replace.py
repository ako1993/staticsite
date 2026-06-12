

def split_and_replace(content:str, body_to_replace:str, title_to_replace:str)->str:
    content = content.strip()
    content = content.replace("{{ Title }}", title_to_replace)
    content = content.replace("{{ Content }}", body_to_replace)
    return content