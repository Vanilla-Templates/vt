#!/usr/bin/env python3
"""
Contains helper functions and other program utilities
"""
from bs4 import BeautifulSoup
import markdown
import json
import sys
from .vt_logger import logger


def get_imports(doc: str) -> list[str]:
    """
    returns imports in .html file

    params:\n
    doc: the stringified html document
    """
    assert len(doc) > 0

    soup = BeautifulSoup(doc, 'html.parser')

    if 'vt_imports' in soup.html.attrs:
        return eval(soup.html.attrs['vt_imports'])  # Using eval to parse the list
    else:
        logger("No imports found", 0)


def get_props(component: str, doc: str) -> list[dict]:
    """
    gets props for a certain component

    params:\n
        component: component for which to get props\n
        doc: the stringified html document\n
    returns:\n
        list[dict]: list of all props where dict is {prop: value}
    """
    # e.g a component may be named 'vt_card' so this gets all the components in
    # in the html named 'vt_card'

    if component.endswith(".html"):
        component = component.split(".")[0]

    logger(f"- getting props from components '{component}'")

    soup = BeautifulSoup(doc, 'html.parser')

    components = soup.find_all(component)

    attrs_ls = [comp.attrs for comp in components]

    for attrs in attrs_ls:
        for key, val in attrs.items():
            try:
                # this prevents numeric strings from being parsed to their numeric equivalent
                attrs[key] = eval(str(val)) if str.isnumeric(eval(val)) else eval(val)
            except Exception as _:
                # there is an inevitable error when parsing strings using
                #  eval()
                # e.g eval("name") yields name, which isnt defined, so error😒
                continue
    return attrs_ls


def is_iterable(obj):
    """checks if is iterable duh😒"""
    try:
        iter(obj)
        return True
    except TypeError:
        return False


def fill_parent(soup: BeautifulSoup):
    """Wraps parent of components that have `vt:parent`
    """
    children_soup = soup.find_all(attrs={"vt:parent":True})

    if not len(children_soup):
        return soup

    for i, tag in enumerate(children_soup):
        parent_name = tag.attrs.get("vt:parent")

        if not parent_name:
            raise ValueError(f"'{tag.name}'s' parent is invalid!")

        with open(parent_name, "r", encoding="utf-8") as f:
            doc = f.read()
            if not len(doc):
                raise ValueError(f"'{parent_name}' is empty!")

        parent_temp = None

        for prop, value in tag.attrs.items():
            parent_temp = BeautifulSoup(str(doc).replace(f"{{{prop}}}", value), "html.parser")

        if parent_temp.find("vt_child"):
            soup.find_all(attrs={"vt:parent":True})[i].replace_with(parent_temp)
            soup.find("vt_child").replace_with(tag)
        else:
            raise ValueError(f"parent template '{parent_name}' doesn't have any 'vt_child' component")
        del tag["vt:parent"]
    return soup


def fill_from_md(soup: BeautifulSoup):
    """Fill template from markdown files using `vt:from-md`

    ```
    <vt_frag vt:from-md="content.md"/>
    ```
    """
    md_soup = soup.find_all(attrs={"vt:from-md":True})

    for tag in md_soup:
        filename: str = tag.attrs.get("vt:from-md")

        if not filename.endswith(".md"):
            raise ValueError(f"'{filename}' is not an .md file! (file should have '.md' file extension)")

        with open(filename, "r", encoding="utf-8") as f:
            md = f.read()

        tag.append(BeautifulSoup(markdown.markdown(md), "html.parser"))

        del tag["vt:from-md"]

    return soup


def fill_attrs_from_file(soup: BeautifulSoup):
    """Fill template from json file using `vt:from-file`

    e.g \n
    Consider `file.json` which contains:
    ```
    {"brand":"VT", "link":"https://vt.org"}
    ```
    The component is:
    ```
        <vt_nav vt:from-file="file.json"/>
    ```
    The resultant component returned by this function is:
    ```
        <vt_nav brand="VT" link="https://vt.org" />
    ```
    `NOTE`: Also allows data from a prop accessor:
    ```
        <vt_nav vt:from-file="file.json:header"/>
    ```
    """

    tags_soup = soup.find_all(attrs={"vt:from-file": True})

    if not len(tags_soup):
        return soup

    for tag in tags_soup:
        attr_toks = tag.attrs["vt:from-file"].split("::")
        path = attr_toks[0]

        logger(f"\t- Opening file: '{path}'")

        with open(path, "r", encoding="utf-8") as f:
            if len(attr_toks) > 1:
                attr_dict = json.load(f)[attr_toks[1]]
            else:
                attr_dict = json.load(f)
        if not isinstance(attr_dict, dict):
            raise Exception("'vt:from*' data must be a dictionary")

        tag["vt:from"] = json.dumps(attr_dict)
    for tag in soup.find_all(attrs={"vt:from-file": True}):
        if tag.attrs.get("vt:from-file"):
            del tag.attrs["vt:from-file"]

    return soup


def fill_from_file(soup: BeautifulSoup):
    """Fills template using `vt:map-from-file` or `vt:from-file` from any
      json file stored in the working directory.

    e.g `<vt_main vt:map-from-file="file.json" />`
    e.g `<vt_main vt:from-file="file.json" />`


    `NOTE:` The data schema should be a list of dictionaries
    (that map to the template placeholders).\n
    ```e.g [{
    "userId": 1,
    "id": 1,
    "title": "delectus aut autem",
    "completed": false
    }, {
    "userId": 1,
    "id": 2,
    "title": "quis ut nam facilis et officia qui",
    "completed": false
    }...]
    ```
    should map to the template:\n
    ```
    <div class="card">
        <span>{id}</span>
        <h3>{userId}</h3>
        <h4>{title}</h4>
        <p{completed}></p>
    </div>
    ```
    """

    soup = fill_attrs_from_file(soup)
    maps_soup = soup.find_all(attrs={"vt:map-from-file": True})

    if not len(maps_soup):
        return soup

    for tag in maps_soup:
        attr_toks = tag.attrs["vt:map-from-file"].split("::")
        path = attr_toks[0]

        logger(f"\t- Opening file: '{path}'")

        with open(path, "r",encoding="utf-8") as f:
            if len(attr_toks) > 1:
                map_data = json.load(f)[attr_toks[1]]
            else:
                map_data = json.load(f)

        if not isinstance(map_data, list):
            raise Exception("'vt:map-from*' data must be a list")

        tag["vt:map-from"] = json.dumps(map_data)

    for tag in soup.find_all(attrs={"vt:map-from-file": True}):
        if tag.attrs.get("vt:map-from-file"):
            del tag.attrs["vt:map-from-file"]

    return soup


def fill_attrs_from_api(soup: BeautifulSoup):
    """Fills data from api using `vt:from-api`
    """
    import requests

    tags_soup = soup.find_all(attrs={"vt:from-api": True})

    if not len(tags_soup):
        return soup

    for tag in tags_soup:
        attr_toks = tag.attrs["vt:from-api"].split("::")
        url = attr_toks[0]

        logger(f"\t- making request to '{url}'")

        resp = requests.get(url)

        if resp.status_code != 200:
            logger(f"\t - status [{resp.status_code}]", log_type=2)
            raise Exception(resp.text)

        logger(f"\t- status code: [{resp.status_code}]")

        # if property accessor
        if len(attr_toks) > 1:
            attr_data = resp.json()[attr_toks[1]]
        else:
            attr_data = resp.json()

        if not isinstance(attr_data, dict):
            raise TypeError("'vt:from*' data must be a dict")

        tag["vt:from"] = json.dumps(attr_data)

    # clean up the attribute
    for tag in soup.find_all(attrs={"vt:from-api": True}):
        if tag.attrs.get("vt:from-api"):
            del tag.attrs["vt:from-api"]

    return soup


def fill_from_api(soup: BeautifulSoup):
    """Fills template from an api endpoint using the attribute
    `vt:map-from-api`:\n
        e.g `<vt_product vt:map-from-api="https://myapi.com/items"/>`
    - It makes a request to the endpoint retrieves the data from it.

    `NOTE:` The data schema should be a list of dictionaries
    (that map to the template placeholders).\n
    ```e.g [{
    "userId": 1,
    "id": 1,
    "title": "delectus aut autem",
    "completed": false
    }, {
    "userId": 1,
    "id": 2,
    "title": "quis ut nam facilis et officia qui",
    "completed": false
    }...]
    ```
    should map to the template:\n
    ```
    <div class="card">
        <span>{id}</span>
        <h3>{userId}</h3>
        <h4>{title}</h4>
        <p{completed}></p>
    </div>
    ```
    """
    import requests

    soup = fill_attrs_from_api(soup)
    maps_soup = soup.find_all(attrs={"vt:map-from-api": True})

    if not len(maps_soup):
        return soup

    for tag in maps_soup:
        attr_toks = tag.attrs["vt:map-from-api"].split("::")
        url = attr_toks[0]

        logger(f"\t- making request to '{url}'")

        resp = requests.get(url)

        if resp.status_code != 200:
            logger(f"\t - status [{resp.status_code}]", log_type=2)
            raise Exception(resp.text)

        logger(f"\t- status code: [{resp.status_code}]")

        # if property accessor
        if len(attr_toks) > 1:
            map_data = resp.json()[attr_toks[1]]
        else:
            map_data = resp.json()

        if not isinstance(map_data, list):
            raise TypeError("'vt:map-from*' data must be a list")

        tag["vt:map-from"] = json.dumps(map_data)

    # clean up the attribute
    for tag in soup.find_all(attrs={"vt:map-from-api": True}):
        if tag.attrs.get("vt:map-from-api"):
            del tag.attrs["vt:map-from-api"]

    return soup

def fill_components_w_children_from_list(tag: BeautifulSoup):
    """
    Fill components that have children from `vt:map-from`
    """
    map_list = tag.attrs.get("vt:map-from")

    if not map_list:
        return tag

    new_vt_frag = BeautifulSoup().new_tag("vt_frag")
    frags = []
    for data in json.loads(map_list):
        for key, val in data.items():
            tag = BeautifulSoup(str(tag).replace(f"{{{key}}}", str(val)), "html.parser")
        frags.append(tag)

    for tag in frags:
        new_vt_frag.append(tag)

    for tag in new_vt_frag:
        if tag.attrs.get("vt:map-from"):
            del tag.attrs["vt:map-from"]

    return new_vt_frag


def fill_components_w_children(tag: BeautifulSoup):
    """Fills the components that have children
       e.g The component:
    ```
        <vt_card vt:from="{'key1':'value1', 'key2':'value2'}">
            <h4>{key1}</h4>
            <p>{key2}</p>
        </vt_card>
    ```
    """
    attr_from = tag.attrs.get("vt:from")

    if not attr_from:
        return tag
    attr_dict: dict = json.loads(attr_from)

    for key, val in attr_dict.items():
        tag.replace_with(BeautifulSoup(str(tag).replace(f"{{{key}}}", str(val)), "html.parser"))

    del tag.attrs["vt:from"]

    return tag


def fill_attrs(soup: BeautifulSoup):
    """Fills template using `vt:from` from `dict` or any other data
      type that is not an iterable object.\n
      e.g The component:
    ```
        <vt_card vt:from="{'key1':'value1', 'key2':'value2'}" />
    ```
    should map to:
    ```
      <div class="card">
        <p>{key1}</p>
        <p>{key2}</p>
      </div>
    ```
      """

    maps_soup = soup.find_all(attrs={"vt:from": True})

    if not len(maps_soup):
        return soup

    for tag in maps_soup:
        attr_dict = json.loads(tag.attrs.get("vt:from"))

        # if tag has children
        if (len(tag.find_all(recursive=False))):
            tag = fill_components_w_children(tag)

        # 'fill_components_w_children(tag)' function clears the attr vt:from
        if not attr_dict:
            continue

        if not isinstance(attr_dict, dict):
            raise TypeError(f"'vt:from*' data must be a dictionary (in '{tag.name}')")
        for key, val in attr_dict.items():
            tag[key] = val

    # remove vt:from tags
    for tag in soup.find_all(attrs={"vt:from": True}):
        if tag.attrs.get("vt:from"):
            del tag.attrs["vt:from"]

    return soup


def fill_from_list(soup: BeautifulSoup):
    """ fills template from list using `vt:map-from` attribute
    soup: the template used to fill\n

    procedure:\n
    - gets all components with the 'vt:map-from' attribute\n
    - parses the data from the attr (should be a list of dictionary,
    i.e records)\n
    - for data in parsed data:\n
      - clone component\n
      - create attribute matching data key\n
      - copy the value into it.\n
    e.g if a component is:\n
        ```
        <vt_card vt:map-from="[{key1:val1, key2:val2}, {key1:val1, key2:val2}]"}
        ```
    The resultant component is:\n
        ```
        <vt_card key1="val1" key2="val2" .../>
        <vt_card key1="val1" key2="val2" .../>
        ```
    `NOTE:` The data schema should be a list of dictionaries
    (that map to the template placeholders).\n
    ```e.g [{
    "userId": 1,
    "id": 1,
    "title": "delectus aut autem",
    "completed": false
    }, {
    "userId": 1,
    "id": 2,
    "title": "quis ut nam facilis et officia qui",
    "completed": false
    }...]
    ```
    should map to the template:\n
    ```
    <div class="card">
        <span>{id}</span>
        <h3>{userId}</h3>
        <h4>{title}</h4>
        <p{completed}></p>
    </div>
    ```
    """

    maps_soup = soup.find_all(attrs={"vt:map-from": True})

    if not len(maps_soup):
        return soup

    for tag in maps_soup:
        map_data = json.loads(tag.attrs["vt:map-from"])
        if len(tag.find_all(recursive=False)):
            tag = fill_components_w_children(tag)

        if not isinstance(map_data, list):
            raise Exception("'vt:map-from*' data must be a list")
        for data in map_data:
            new_tag = soup.new_tag(tag.name)
            new_tag.attrs = dict(tag.attrs)

            for key, val in data.items():
                new_tag[key] = val
            tag.parent.append(new_tag)
        # removes the og tag
        tag.decompose()

    # remove all the 'vt:map-from' tags
    for tag in soup.find_all(attrs={"vt:map-from": True}):
        if tag.attrs.get("vt:map-from"):
            del tag.attrs["vt:map-from"]
    return soup


def fill_template(component_path: str,
                  component_data: list[dict]) -> list[BeautifulSoup]:
    """Fills in the template and returns html with data in it

    params:\n
    component_path: path of the template to fill in\n
    component_data: the data to fill in the template\n
                    ({prop: value} for data in component_data)\n
    """
    with open(component_path, "r", encoding="utf-8") as f:
        component = f.read()

    component_soups = []
    # if component does not have data, return the template as is
    if not component_data:
        component_soups.append(BeautifulSoup(component, "html.parser"))
        return component_soups

    # data here is a list of dictionaries: containing data
    # from all instances of a certain component
    for data in component_data:
        soup = BeautifulSoup(component, 'html.parser')
        for prop, value in data.items():
            if type(value) == dict:
                for key, val in value.items():
                    soup = BeautifulSoup(str(soup).replace(f"{{{key}}}", val),
                                         'html.parser')
            else:  # other types to be dealt with here
                # if data is a str and not an iterable
                soup = BeautifulSoup(str(soup).replace(f"{{{prop}}}",
                                                       str(value)),
                                     'html.parser')
        component_soups.append(soup)

    return component_soups
