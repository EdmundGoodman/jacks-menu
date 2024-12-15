#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""."""

from pathlib import Path

from jacks_menu.menu import Menu
from jacks_menu.parser import MenuParseState, MenuParseError, parse_menu

TEST_MENU_DIRECTORY = Path(__file__).parent / "test_menus"

def test_parse_menu():
    """."""
    # raise ValueError(TEST_MENU_DIRECTORY)
    for menu_file in TEST_MENU_DIRECTORY.iterdir():
        menu_text = menu_file.read_text()
        parse_menu("location", menu_text)