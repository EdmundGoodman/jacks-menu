#!/usr/bin/env python3
"""Logic to parse the menu."""

from enum import Enum, auto

from jacks_menu.menu import Menu


class MenuParseState(Enum):
    """Enum containing parser states for the menu."""

    Date = auto()
    Items = auto()
    Done = auto()


class MenuParseError(Exception):
    """Custom error for parsing logic failing on the menu data."""


def neaten_date(date: str) -> str:
    """Neaten the date field.

    This includes remove leading spaces before commas.

    Args:
        date: The date to neaten

    Returns:
        The neatened date
    """
    return ", ".join([s.strip() for s in date.split(", ")])


def parse_menu(  # noqa: C901
    location: str, web: str, menu_text: str, debug: bool = False
) -> Menu:
    """Parse the menu data.

    Args:
        location: The location of the menu.
        web: The web address of the menu.
        menu_text: The menu text to parse.
        debug: Whether to show debugging information about the parsing state.

    Returns:
        The parsed menu.
    """
    lines = [line.strip() for line in menu_text.splitlines()]

    non_empty_lines: int = 0
    date: str | None = None
    items: list[str] = []
    menu_parse_state = MenuParseState.Date

    for i, line in enumerate(lines):
        if line.strip() != "":
            non_empty_lines += 1

        if debug:
            print(
                f"{i+1 :<2} | {non_empty_lines :<2} "
                f"| {menu_parse_state.name :<5} | {line}"
            )

        if menu_parse_state == MenuParseState.Date:
            # Last non-empty line before dash is the date
            if line in ("-", "–") or non_empty_lines > 2:  # noqa: RUF001, PLR2004
                menu_parse_state = MenuParseState.Items
            elif line:
                date = neaten_date(line)
        elif menu_parse_state == MenuParseState.Items:
            # All non-empty lines before "Single scoop" are items
            if line.lower().startswith("single scoop"):
                menu_parse_state = MenuParseState.Done
                break
            if line:
                items.append(line)

    if menu_parse_state != MenuParseState.Done:
        raise MenuParseError("Could not parse menu!")
    assert date is not None
    return Menu(location, web, date, items)
