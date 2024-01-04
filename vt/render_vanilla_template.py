#!/usr/bin/env python3
"""
This is the `Vanilla Templates` html parser
"""
import os
import re
from bs4 import BeautifulSoup
from .vt_utils import get_imports, get_props, fill_template, fill_parent
from .vt_logger import logger, print_success, print_info
from .vt_utils2 import process_template

def render_html(vt_html_doc: str ="index.html"):
    """Render Vanilla template
    vt_html_doc: main index template html file
    """
    # Read the main html doc

    with open(vt_html_doc, "r", encoding="utf-8") as f:
        html_doc = f.read()

    if not len(html_doc) > 0:
        raise ValueError(f"'{vt_html_doc}' document is empty!")

    print_info(f"\n * compiling '{vt_html_doc}'...\n")
    # main soup
    soup = BeautifulSoup(html_doc, "html.parser")

    soup = fill_parent(soup)
    # get component imports from main
    imports = get_imports(str(soup))

    soup = process_template(soup)

    if imports and len(imports):
        for file in imports:
            path = file
            file = file.split("/")[len(file.split("/")) - 1]

            # check if files are valid
            if not os.path.exists(path):
                logger(f"in index file: '{vt_html_doc}'", 2)
                raise FileNotFoundError(f"'{file}' does not exist on specified path '{path}'")
            elif not os.path.isfile(path):
                logger(f"in index file: '{vt_html_doc}'", 2)
                raise ValueError(f"{file} is not a file")

            # check  if component not in main doc:
            component_name = file.split(".")[0]
            component_soup = soup.find_all(component_name)
            if not len(component_soup) > 0:
                raise ValueError(f"'{file}' imported but not used")

            props = get_props(doc=str(soup), component=file)

            filled_components = fill_template(path, props)

            for i, component in enumerate(component_soup):
                component.replace_with(filled_components[i])

        # delete main imports
    del soup.html.attrs["vt_imports"]

    new_imports = soup.find_all(attrs={"vt_imports": True})

    # stores the already imported and expanded components
    imported = set()

    while len(new_imports):
        component_imports = new_imports[0].attrs["vt_imports"]

        soup = fill_parent(soup)
        soup =process_template(soup)

        # e.g <tag vt_imports='["components/vt_footer"]'>...</tag>
        for file in set(eval(component_imports)):
            path = file
            file = file.split("/")[len(file.split("/")) - 1]

            # check if files are valid
            if not os.path.exists(path):
                logger(f"in index file: '{vt_html_doc}'", 2)
                error = f"'{file}' does not exist on" +\
                        f" specified path '{path}'"
                raise FileNotFoundError(error)
            elif not os.path.isfile(path):
                logger(f"in index file: '{vt_html_doc}'", 2)
                raise ValueError(f"{file} is not a file")

            # check  if component not in main html:
            component_soup = soup.find_all(f"{file.split('.')[0]}")

            # if imported and not used
            if not len(component_soup) > 0 and file not in imported:
                logger(f"in index file: '{vt_html_doc}'", 2)
                raise ValueError(f"The component '{file}' is imported but not used")

            if not len(component_soup) > 0:
                logger(f"'{file}' already imported ")
                continue

            props = get_props(doc=str(soup), component=file)

            filled_components = fill_template(path, props)

            for i, component in enumerate(component_soup):
                component.replace_with(filled_components[i])

            imported.update([file])

        del new_imports[0].attrs["vt_imports"]

        new_imports = soup.find_all(attrs={"vt_imports": True})

    vt_attrs = soup.find_all(lambda tag: any(re.match('vt:.*', key)
                                             for key in tag.attrs))

    # clean main file (remove vt:\* attrs)
    for vt_tag in vt_attrs:
        for key in list(vt_tag.attrs.keys()):
            if re.match('vt:.*', key):
                del vt_tag[key]

    vt_components = soup.find_all(re.compile("vt_*"))

    if len(vt_components):
        for vt_tag in vt_components:
            if len(vt_tag.find_all(recursive=False)):
                if vt_tag.name != 'vt_frag':
                    logger(f"The tag '{vt_tag.name}' will unwrap. Please use native tags to map data.", 1)
                vt_tag.unwrap()
            else:
                logger(f"A component named '{vt_tag.name}' was not imported, so it wasn't parsed",1)

    soup.html['made-with-vanilla-t'] = 'true❤'
    print_info("\n * Done!")
    return str(soup)