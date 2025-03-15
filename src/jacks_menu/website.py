#!/usr/bin/env python3
"""Logic to retrieve the menu from the website."""

from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from re import match as re_match
from tempfile import NamedTemporaryFile
from time import sleep

import gdown
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from seleniumwire import webdriver

GOOGLE_DOC_PATTERN = r"https://docs.google.com/document/d/(.*)/preview"
WIX_DOC_ID = "11pi6xxtRoM2rF9XlgVhe46UQqCVbBrtqk2YBBwPkKN4"


class MenuRetrievalError(Exception):
    """Custom error for the menu retrieval operation failing."""


class MismatchedDocIdError(Exception):
    """Custom error for mismatched doc ids."""


@contextmanager
def headless_firefox_driver() -> Generator[webdriver.Firefox, None, None]:  # type: ignore[no-any-unimported]
    """Context manager for a headless firefox driver."""
    options = FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    try:
        yield driver
    finally:
        driver.quit()


def get_iframe_doc_id(
    url: str, expected_doc_id: str | None, verbose: bool = False
) -> str:
    """Get the Google doc id for a Jack's Gelato menu iFrame.

    Args:
        url: The URL of the menu webpage to get the doc url id from.
        expected_doc_id: The expected doc id to check against.
        verbose: Whether to show information about the retrieval process.

    Raises:
        MenuRetrievalError: The menu Google doc it retrieval failed.

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
                    if verbose:
                        print(f"Retrieved doc id: {doc_id}")
                    if expected_doc_id and doc_id != expected_doc_id:
                        raise MismatchedDocIdError(
                            "Mismatched doc id!"
                            f" Expected '{expected_doc_id}', got '{doc_id}'"
                        )
                    return doc_id

    raise MenuRetrievalError("Failed to retrieve menu Google doc id!")


def get_menu_text(
    doc_id: str, output_file: Path | None = None, verbose: bool = False
) -> str:
    """Get the text content of menu given its Google doc id.

    Args:
        doc_id: The Google doc id to get the text content from.
        output_file: The output file to write the text content to, if set.
        verbose: Whether to show information about the download process.

    Raises:
        MenuRetrievalError: The menu text retrieval failed.

    Returns:
        The text content of menu given its Google doc id.
    """
    if output_file is not None and output_file.exists():
        if verbose:
            print(f"Output file '{output_file}' already exists.")
        return output_file.read_text()

    url = f"https://docs.google.com/uc?id={doc_id}"
    with NamedTemporaryFile() as tmp_handle:
        try:
            gdown.download(url, tmp_handle.name, format="txt", quiet=not verbose)
        except gdown.exceptions.FileURLRetrievalError as exc:
            raise MenuRetrievalError("Failed to retrieve menu text!") from exc
        menu_text = Path(tmp_handle.name).read_text()

    if output_file is not None:
        with output_file.open("w+") as output_handle:
            output_handle.write(menu_text)

    return menu_text
