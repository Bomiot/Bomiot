from os.path import join, isdir
from os import makedirs, listdir
import shutil


def copy_files(src_folder, dst_folder):
    makedirs(dst_folder, exist_ok=True)
    for item in listdir(src_folder):
        source_item = join(src_folder, item)
        destination_item = join(dst_folder, item)
        if isdir(source_item):
            if item != '.quasar' and item != '.vscode':
                copy_files(source_item, destination_item)
        else:
            shutil.copy2(source_item, destination_item)