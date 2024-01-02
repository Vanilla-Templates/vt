#!/usr/bin/env python3
"""
This is the `Vanilla Templates` html parser
"""
import os
import shutil
from pathlib import Path
from .render_vanilla_template import render_html
from .vt_logger import logger, print_success, print_info
from .config import __build_dir__, __use_pub_dir__, __index_files__



directory_path = Path(__build_dir__)


def main(index_file: str = "index.html"):
    """program entry point
    """
    print_info(f"\n================= {index_file} =================")

    soup = render_html(index_file)

    # Create the directory
    directory_path.mkdir(parents=True, exist_ok=True)

    source_directory = "public"
    destination_directory = __build_dir__

    if __use_pub_dir__:
        shutil.copytree(source_directory, os.path.join(destination_directory, source_directory), dirs_exist_ok=True)
    else:
        shutil.copytree(source_directory, destination_directory, dirs_exist_ok=True)

    # - generated final html doc in vt-dist directory
    with open(directory_path / index_file, "w", encoding='utf-8') as vt_f:
        vt_f.write(soup)

    print(f"\nYou can view your generated file" +
           f" in '{directory_path}/{index_file}'")

if __name__ == "__main__":
    if len(__index_files__) > 1:
        print_info(f"\n * Vanilla Templates is generating your site...")
        for file in __index_files__:
            main(file)
    else:
        main()

    print_info("\n * Thank you for using Vanilla Templates.\n")

    # with open("vt/vt_static/logo_bg.txt") as vt_l:
    #     print(vt_l.read())