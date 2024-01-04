"""
Contains other vt utilility functions
"""
from bs4 import BeautifulSoup
from .vt_utils import fill_from_md, fill_from_file, fill_from_api,\
      fill_from_list, fill_attrs, fill_parent


def process_template(soup: BeautifulSoup):
    """Fills template with data:\n
    Contains the following functions
    ```
    fill_from_md(soup),
    fill_from_file(soup),
    fill_from_api(soup),
    fill_from_list(soup),
    fill_attrs(soup)
    ```
    """
    soup = fill_from_md(soup)
    soup = fill_from_file(soup)
    soup = fill_from_api(soup)
    soup = fill_from_list(soup)
    soup = fill_attrs(soup)

    return soup
