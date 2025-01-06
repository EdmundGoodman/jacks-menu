#!/usr/bin/env python3
"""."""

from enum import Enum, auto

from jacks_menu.menu import Menu


class MenuParseState(Enum):
    """Enum containing parser states for the menu."""

    Date = auto()
    Items = auto()
    Done = auto()


class MenuParseError(Exception):
    """Custom error for parsing logic failing on the menu data."""


def parse_menu(location: str, web: str, menu_text: str) -> Menu:
    """Parse the menu data.

    Args:
        location: The location of the menu.
        web: The web address of the menu.
        menu_text: The menu text to parse.

    Returns:
        The parsed menu.
    """
    lines = [line.strip() for line in menu_text.splitlines()]

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
            if line:
                items.append(line)

    if menu_parse_state != MenuParseState.Done:
        raise MenuParseError("Could not parse menu!")
    assert date is not None
    return Menu(location, web, date, items)
