#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A tool to scrape the Jack's Gelato menu."""

from jacks_menu.website import get_menu_text
from jacks_menu.parser import parse_menu
from jacks_menu.constants import MENU_LOCATIONS, MENU_KNOWN_IDS
from jacks_menu.export import export_menu

def main() -> None:
    """Run the tool."""
    # for location, url in MENU_LOCATIONS.items():
    #     print(location, get_iframe_doc_id(url))

    for location, url in MENU_LOCATIONS.items():
        doc_id = MENU_KNOWN_IDS[url]
        menu_text = get_menu_text(doc_id)
        menu = parse_menu(location, menu_text)
        print(menu)
        export_menu(menu)


if __name__ == "__main__":
    main()
