#!python
"""The copied-loop version of thread rendering.

This walks a Reddit-shaped listing and stops early. Replies nested further
than these loops never appear. Retire it. render_lines in comments.py is
the one function that replaces the copies.
"""

import json
import os
import sys


def _children(listing):
    """Return the child wrappers inside a listing, or nothing for a solid doll."""
    if not listing or not isinstance(listing, dict):
        return []
    return listing["data"]["children"]


def messy_indent(path):
    """Print author lines with copied loops, one extra loop per nesting."""
    with open(path, encoding="utf-8") as handle:
        payload = json.load(handle)
    lines = []
    for top in _children(payload):
        data = top["data"]
        lines.append("{}: {}".format(data["author"], data["body"]))
        for child in _children(data["replies"]):
            child_data = child["data"]
            lines.append("  {}: {}".format(child_data["author"], child_data["body"]))
            for grand in _children(child_data["replies"]):
                grand_data = grand["data"]
                lines.append(
                    "    {}: {}".format(grand_data["author"], grand_data["body"])
                )
    return lines


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "sample_thread.json"
    )
    print("\n".join(messy_indent(path)))


if __name__ == "__main__":
    main()
