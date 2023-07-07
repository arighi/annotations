#!/usr/bin/env python3
# -*- mode: python -*-
# Try to automatically sanitize an old annotations file, dropping all the
# deprecated flags, arbitrary enforcements rules, etc.
# Copyright © 2023 Canonical Ltd.

import sys

sys.dont_write_bytecode = True  # pylint: disable=E0402

import re
import argparse
from argcomplete import autocomplete

from kconfig.utils import autodetect_annotations, arg_fail
from kconfig.version import VERSION


def make_parser():
    parser = argparse.ArgumentParser(
        description="Santizie old Ubuntu kernel annotations file",
    )
    parser.add_argument(
        "--version", "-v", action="version", version=f"%(prog)s {VERSION}"
    )
    parser.add_argument(
        "--file",
        "-f",
        action="store",
        help="Specify annotations file to be sanitized",
    )

    return parser


_ARGPARSER = make_parser()


def remove_flags_and_drop_lines(file_path):
    # Read the contents of the file
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Check if the file has the required headers
    lines = content.splitlines()
    if (
        len(lines) < 2
        or lines[0].strip() != "# Menu: HEADER"
        or lines[1].strip() != "# FORMAT: 4"
    ):
        print(f"ERROR: {file_path} doesn't have a valid header")
        print(
            "Fix the headers as explained here: "
            + "https://discourse.ubuntu.com/t/kernel-configuration-in-ubuntu/35857"
        )
        sys.exit(1)

    # Remove unsupported annotations
    updated_content = re.sub(r"(flag|mark)<.*?>", "", content)

    # Drop lines with a single word and trailing spaces
    updated_content = re.sub(r"^\w+\s*$", "", updated_content, flags=re.MULTILINE)

    # Add a space after all caps followed by 'policy'
    updated_content = re.sub(r"([A-Z]+)(policy)", r"\1 \2", updated_content)

    # Add 'note' if missing
    updated_content = re.sub(r"(\s+)(<.*?>)", r"\1note\2", updated_content)

    # Write the updated contents back to the file
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(updated_content)


def main():
    autocomplete(_ARGPARSER)
    args = _ARGPARSER.parse_args()

    if args.file is None:
        args.file = autodetect_annotations()
        if args.file is None:
            arg_fail(
                _ARGPARSER,
                "error: could not determine DEBDIR, try using: --file/-f",
                show_usage=False,
            )
    remove_flags_and_drop_lines(args.file)


if __name__ == "__main__":
    main()
