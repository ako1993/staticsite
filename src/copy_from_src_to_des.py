import os
import shutil
def copy_from_src_to_des(src:str, des:str):
    if not os.path.exists(des):
        os.makedirs(des)
    for item in os.listdir(des):
        item_path = os.path.join(des, item)
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.unlink(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)
    print(f"All items in {des} have been removed")
    if not os.path.exists(src):
        print(f"{src} does not exist")
        return
    if not os.path.isdir(src):
        print(f"{src} is not a file")
        return
    for root, dirs, files in os.walk(src):
        rel_path = os.path.relpath(root, src)
        target_dir = os.path.join(des, rel_path)

        os.makedirs(target_dir, exist_ok=True)

        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(target_dir, file)
            shutil.copy2(src_file, dst_file)
    print(f"files copied from {src} to {des}")