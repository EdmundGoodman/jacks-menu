#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""."""

from time import sleep
from contextlib import contextmanager
from re import match as re_match
from typing import ContextManager
from tempfile import NamedTemporaryFile
from pathlib import Path

import gdown
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from seleniumwire import webdriver


GOOGLE_DOC_PATTERN = r"https://docs.google.com/document/d/(.*)/preview"
WIX_DOC_ID = "11pi6xxtRoM2rF9XlgVhe46UQqCVbBrtqk2YBBwPkKN4"


@contextmanager
def headless_firefox_driver() -> ContextManager[webdriver.Firefox]:
    """Context manager for a headless firefox driver."""
    options = FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    try:
        yield driver
    finally:
        driver.quit()


def get_iframe_doc_id(url: str) -> str:
    """Get the Google doc id for a Jack's Gelato menu iFrame.

    Args:
        url: The URL of the menu webpage to get the doc url id from.

    Returns:
        The Google doc url id.
    """
    with headless_firefox_driver() as driver:
        driver.get(url)

        # Because the wix google doc embedding is very silly, we need an
        # unconditional wait for >5 seconds, hence the `sleep(10)`
        driver.implicitly_wait(10)
        sleep(15)

        for request in driver.requests:
            if request.response:
                match = re_match(GOOGLE_DOC_PATTERN, request.url)
                if match and (doc_id := match.group(1)) != WIX_DOC_ID:
                    return doc_id


def get_menu_text(doc_id: str) -> str | None:
    """Get the text content of menu given its Google doc id."""
    url = f"https://docs.google.com/uc?id={doc_id}"
    with NamedTemporaryFile() as tmp_handle:
        try:
            gdown.download(url, tmp_handle.name, quiet=False, format="txt")
        except gdown.FileURLRetrievalError:
            return None
        return Path(tmp_handle.name).read_text()


if __name__ == "__main__":
    print(get_menu_doc_id("https://www.jacksgelato.com/bene-t-street-menu"))