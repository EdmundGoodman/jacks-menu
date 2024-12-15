#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""."""

from dataclasses import dataclass
from datetime import datetime

@dataclass
class Menu:
    """Dataclass containing the menu date and items."""

    location: str
    date: str
    items: list[str]

# @dataclass
# class Menu:
#     """Dataclass containing the menu date and items."""
#
#     location: str
#     web: str
#     date: datetime
#     items: list[str]
#
#     @classmethod
#     def get_markdown(
#         cls, location: str, url: str, date: datetime, contents: str
#     ) -> str:
#         """Convert menu data to its markdown representation.
#
#         Args:
#             location: The location of the menu.
#             url: The link back to the real menu site.
#             date: The date of the menu.
#             contents: The contents of the menu text (items or error message).
#
#         Returns:
#             A markdown representation of the menu data.
#         """
#         date_string = datetime.strftime(date, "%A, %d/%m/%Y")
#         title = f"## [{location}]({url}) ({date_string})\n\n"
#         return title + contents + "\n\n"
#
#     def __repr__(self) -> str:
#         """Convert a menu dataclass to its markdown representation.
#
#         Returns:
#             A markdown representation of the menu.
#         """
#         contents = "\n".join(f"- {item}" for item in self.items)
#         return Menu.get_markdown(self.location, self.web, self.date, contents)
