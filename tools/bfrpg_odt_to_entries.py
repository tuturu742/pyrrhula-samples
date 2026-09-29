#!/usr/bin/env python3
"""Convert the Basic Fantasy RPG rulebook (.odt) into one knowledge entry per section.

Provenance for the rulebook inside `greyfen-barrows.pyr`, which is a derivative work of a
CC BY-SA text: this is how it was produced, so anyone can produce it again or check it.

    python3 tools/bfrpg_odt_to_entries.py Basic-Fantasy-RPG-Rules-r142.odt out.json

Writes a JSON list of {part, key, title, h2, body}. Tables are kept as pipe rows; the
introduction chapter is dropped, because it holds no rules and resembles everything (it
was the single most-retrieved entry of an early measured run, in scenes with no rules in
them). Activation keys are NOT written: Pyrrhula derives them from the titles when the
source is published.

Stdlib only.
"""

from __future__ import annotations

import collections
import html
import json
import pathlib
import re
import sys
import unicodedata
import zipfile

# Part headings, and the short name each becomes in an entry key.
PARTS = {
    "PART 1: INTRODUCTION": None,  # dropped: no rules in it
    "PART 2: PLAYER CHARACTERS": "pc",
    "PART 3: SPELLS": "spells",
    "PART 4: THE ADVENTURE": "adventure",
    "PART 5: THE ENCOUNTER": "encounter",
    "PART 6: MONSTERS": "monsters",
    "PART 7: TREASURE": "treasure",
    "PART 8: GAME MASTER INFORMATION": "gm",
}


def to_text(odt: pathlib.Path) -> str:
    """content.xml -> plain text, with headings as #-prefixed lines and tables as rows."""
    xml = zipfile.ZipFile(odt).read("content.xml").decode()
    xml = re.sub(r"<text:note-body>.*?</text:note-body>", "", xml, flags=re.S)

    def cell(match: re.Match[str]) -> str:
        inner = re.sub(r"<text:(p|h)[^>]*>", " ", match.group(1))
        inner = re.sub(r"<text:(tab|line-break)/>|<text:s[^>]*/>", " ", inner)
        inner = html.unescape(re.sub(r"<[^>]+>", "", inner))
        return f" {re.sub(r'\\s+', ' ', inner).strip()} |"

    xml = re.sub(r"<table:table-cell[^>]*>(.*?)</table:table-cell>", cell, xml, flags=re.S)
    xml = re.sub(r"<table:table-cell[^>]*/>", "  |", xml)
    xml = re.sub(r"<table:table-row[^>]*>", "\n|", xml)
    xml = re.sub(r"</table:table-row>|<table:table[^>]*>|</table:table>", "\n", xml)
    xml = re.sub(
        r'<text:h[^>]*outline-level="(\d)"[^>]*>',
        lambda m: "\n" + "#" * int(m.group(1)) + " ",
        xml,
    )
    xml = re.sub(r"<text:(p|list-item)[^>]*>", "\n", xml)
    xml = re.sub(r"<text:tab/>", "\t", xml)
    xml = re.sub(r"<text:s[^>]*/>", " ", xml)
    xml = re.sub(r"<text:line-break/>", "\n", xml)
    return html.unescape(re.sub(r"<[^>]+>", "", xml))


def slug(value: str) -> str:
    ascii_only = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "_", ascii_only.lower()).strip("_")[:60]


def sections(text: str) -> list[dict]:
    parts: list[dict] = []
    current: dict | None = None
    for line in text.splitlines():
        if line.startswith("# "):
            current = {"title": re.sub(r"\s+", " ", line[2:]).strip(), "lines": []}
            parts.append(current)
        elif current is not None:
            current["lines"].append(line)

    out: list[dict] = []
    for part in parts:
        short = PARTS.get(part["title"])
        if short is None:
            continue
        section = {"title": part["title"].title(), "lines": [], "h2": None}
        found = [section]
        for line in part["lines"]:
            heading = re.match(r"^(#{2,3}) (.*)$", line)
            if heading:
                level = len(heading.group(1))
                title = re.sub(r"\s+", " ", heading.group(2)).strip()
                section = {"title": title, "lines": [], "h2": section["h2"] if level == 3 else None}
                if level == 2:
                    section["h2"] = title
                found.append(section)
            else:
                section["lines"].append(line)
        for section in found:
            body = re.sub(r"\n{3,}", "\n\n", "\n".join(section["lines"]).strip())
            if len(body) < 120:
                continue
            title = section["title"].split("\t")[0].strip()
            suffix = section["title"].split("\t", 1)[1].strip() if "\t" in section["title"] else ""
            if suffix:
                body = f"**{re.sub(r'\\s+', ' ', suffix)}**\n\n{body}"
            out.append(
                {"part": short, "key": f"bf_{short}_{slug(title)}", "title": title,
                 "h2": section["h2"], "body": body}
            )

    seen: collections.Counter[str] = collections.Counter()
    for entry in out:
        seen[entry["key"]] += 1
        if seen[entry["key"]] > 1:
            entry["key"] += f"_{seen[entry['key']]}"
    return out


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    entries = sections(to_text(pathlib.Path(sys.argv[1])))
    pathlib.Path(sys.argv[2]).write_text(json.dumps(entries, ensure_ascii=False, indent=1))
    print(f"{len(entries)} entries -> {sys.argv[2]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
