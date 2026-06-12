

def extract_title(markdown:str)->str:
    markdown = markdown.strip()
    lines = markdown.splitlines()
    for line in lines:
        line = line.strip()
        if line.startswith("#"):
            title = line[1:]
            title = title.strip()
            return title
    return Exception("No header found")