#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A tool to scrape the Jack's Gelato menu."""

from pathlib import Path

import click

from jacks_menu.menu import Menu
from jacks_menu.website import get_iframe_doc_id, get_menu_text, MenuRetrievalError, MismatchedDocIdError
from jacks_menu.parser import parse_menu, MenuParseError
from jacks_menu.constants import (
    MENU_LOCATIONS,
    LOCATIONS_SANITISED,
    MENU_KNOWN_IDS,
    DATE
)
from jacks_menu.export import get_menu_markdown, get_error_markdown, get_blog_markdown


def run(
    raw_directory: Path | None,
    markdown_directory: Path | None,
    retrieve_doc_id: bool = False,
    fail_on_error: bool = False,
    verbose: bool = False,
) -> None:
    """Run the tool."""
    menus_markdown: dict[str, str] = {}

    for location, web in MENU_LOCATIONS.items():
        raw_file = (
            None if raw_directory is None else
            raw_directory / f"{DATE}_{LOCATIONS_SANITISED[location]}.txt"
        )

        doc_id = MENU_KNOWN_IDS[location]
        if retrieve_doc_id:
            doc_id = get_iframe_doc_id(
                web,
                expected_doc_id=doc_id,
                verbose=verbose
            )

        try:
            menu_text = get_menu_text(
                doc_id,
                output_file=raw_file,
                verbose=verbose,
            )
            menu = parse_menu(location, web, menu_text)
            menu_markdown = get_menu_markdown(menu)
        except (MenuRetrievalError, MenuParseError, MismatchedDocIdError) as err:
            if fail_on_error:
                raise err
            menu_markdown = get_error_markdown(location, web)

        menus_markdown[location] = menu_markdown

    blog_markdown = get_blog_markdown(menus_markdown)
    print(blog_markdown)
    if markdown_directory:
        markdown_file = markdown_directory / f"{DATE}.md"
        markdown_file.write_text(blog_markdown)


@click.command()
@click.option(
    "-r", "--raw", type=click.Path(dir_okay=False), default=None,
    help="The directory to output the raw menu file to, if unset it is discarded."
)
@click.option(
    "-m", "--markdown", type=click.Path(dir_okay=False), default=None,
    help="The directory to output the generated markdown menus to, if unset it is only printed."
)
@click.option(
    "-d", "--retrieve-doc-id", is_flag=True, default=False,
    help="Retrieve (slowly...) the Jack's Gelato menu doc ID with selenium."
)
@click.option(
    "-e", "--fail-on-error", is_flag=True, default=False,
    help="Abort and give a non-zero exit code if an error occurs."
)
@click.option(
    "-v", "--verbose", is_flag=True, default=False,
    help="Show verbose output about downloading the menu."
)
def main(
    raw: Path | None,
    markdown: Path | None,
    retrieve_doc_id: bool,
    fail_on_error: bool,
    verbose: bool,
) -> None:
    """."""
    run(
        raw_directory=raw, #BASE_RAW_DIRECTORY,
        markdown_directory=markdown, #BASE_MARKDOWN_DIRECTORY,
        retrieve_doc_id=retrieve_doc_id, #False,
        fail_on_error=fail_on_error, #False,
        verbose=verbose #True,
    )


if __name__ == "__main__":
    main()
