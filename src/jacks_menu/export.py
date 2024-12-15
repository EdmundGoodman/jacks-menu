#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""."""

from datetime import datetime, timezone
from jacks_menu.menu import Menu


NOW = datetime.now(timezone.utc)

HEADER = f"""---
title: "Jack's Gelato Menus"
author: "Edmund Goodman"
date: {NOW}
---

"""

FOOTER = """All menu information is property of Jack's Gelato. This page is
updated daily at 10:20am -- see my
[blog post]({{< ref "/posts/a_faster_gelato" >}}) for why I made it.
"""


def export_menu(menu: Menu) -> None:
    pass
