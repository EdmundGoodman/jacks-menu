#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""."""

from jacks_menu.constants import NAMED_DATES
from jacks_menu.menu import Menu
from datetime import datetime, timezone
from enum import Enum, auto


class MenuParseState(Enum):
    """Enum containing parser states for the menu."""

    Date = auto()
    Items = auto()
    Done = auto()


class MenuParseError(Exception):
    """Custom error for parsing logic failing on the menu data."""


def parse_menu(location: str, menu_text: str) -> Menu:
    lines = menu_text.splitlines()

    date: str | None = None
    items: list[str] = []
    menu_parse_state = MenuParseState.Date

    for line in lines:
        if menu_parse_state == MenuParseState.Date:
            # Last non-empty line before dash is the date
            if line == "-":
                menu_parse_state = MenuParseState.Items
            elif line:
                date = line
        elif menu_parse_state == MenuParseState.Items:
            # All non-empty lines before "Single scoop" are items
            if line.startswith("Single Scoop"):
                menu_parse_state = MenuParseState.Done
                break
            elif line:
                items.append(line)

    if menu_parse_state != MenuParseState.Done:
        raise MenuParseError("Could not parse menu!")
    return Menu(location, date, items)
