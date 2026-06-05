import os
import shutil

def copy_from_static_to_public():
    static = "/home/andre/projects/github/ako1993/staticsite/static"
    public = "/home/andre/projects/github/ako1993/staticsite/public"
    if not os.path.exists(public):
        print(f"Error: invalid filepath {public}")
        return
    if not os.path.isdir(public):
        print(f"Error: {public} is not a directory")
    for item in os.listdir(public):
        item_path = os.path.join(public, item)
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.unlink(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)
    print(f"All items in {public} have been removed")
    if not os.path.exists(static):
        print(f"{static} does not exist")
        return
    if not os.path.isdir(static):
        print(f"{static} is not a file")
        return
    for root, dirs, files in os.walk(static):
        rel_path = os.path.relpath(root, static)
        target_dir = os.path.join(public, rel_path)

        os.makedirs(target_dir, exist_ok=True)

        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(target_dir, file)
            shutil.copy2(src_file, dst_file)
    print(f"files copied from {static} to {public}")