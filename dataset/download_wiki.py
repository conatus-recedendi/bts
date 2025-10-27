#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Korean Wikipedia dump -> plain text lines (one sentence per line).

Usage:
  python extract_kowiki.py \
    --out ./data/wiki.txt \
    [--dump ./kowiki-latest-pages-articles.xml.bz2] \
    [--no-download] [--paragraph]
"""

import argparse
import os
import sys
import bz2
import re
import html
import urllib.request
from urllib.error import HTTPError, URLError
from contextlib import contextmanager
from xml.etree import ElementTree as ET
from pathlib import Path

WIKI_URL = (
    "https://dumps.wikimedia.org/kowiki/latest/kowiki-latest-pages-articles.xml.bz2"
)
DEFAULT_DUMP = "kowiki-latest-pages-articles.xml.bz2"

# --- Utilities ---------------------------------------------------------------


def human_bytes(n: int) -> str:
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if n < 1024.0:
            return f"{n:3.1f}{unit}"
        n /= 1024.0
    return f"{n:.1f}PB"


def ensure_parent(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)


def strip_ns(tag: str) -> str:
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


# --- Downloader with resume --------------------------------------------------


def download_with_resume(url: str, dest: Path) -> None:
    tmp = dest.with_suffix(dest.suffix + ".part")
    exist = tmp.exists()
    start = tmp.stat().st_size if exist else 0

    headers = {}
    if exist and start > 0:
        headers["Range"] = f"bytes={start}-"

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp, open(tmp, "ab") as f:
            # Determine total size for progress if provided
            total = resp.headers.get("Content-Length")
            if total is not None:
                total = int(total) + start
            downloaded = start

            chunk = 1024 * 1024  # 1MB
            while True:
                data = resp.read(chunk)
                if not data:
                    break
                f.write(data)
                downloaded += len(data)
                if total:
                    pct = downloaded / total * 100
                    print(
                        f"\rDownloading: {human_bytes(downloaded)} / {human_bytes(total)} ({pct:5.1f}%)",
                        end="",
                        flush=True,
                    )
                else:
                    print(
                        f"\rDownloading: {human_bytes(downloaded)}", end="", flush=True
                    )
        print()
        tmp.replace(dest)
    except (HTTPError, URLError) as e:
        print(f"\n[ERROR] Download failed: {e}", file=sys.stderr)
        if not dest.exists():
            raise


# --- Wikimarkup cleaning -----------------------------------------------------

TEMPLATE_RE = re.compile(r"\{\{[^{}]*\}\}")
COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
REF_TAG_RE = re.compile(
    r"<ref\b[^>/]*?/?>.*?</ref>|<ref\b[^>/]*/>", re.DOTALL | re.IGNORECASE
)
HTML_TAG_RE = re.compile(r"<[^>]+>")
FILE_LINK_RE = re.compile(
    r"\[\[(파일|그림|File|Image):.*?\]\]", re.IGNORECASE | re.DOTALL
)
CATEGORY_LINK_RE = re.compile(r"\[\[(분류|Category):.*?\]\]", re.IGNORECASE | re.DOTALL)
EXTERNAL_LINK_RE = re.compile(r"\[(https?://[^\s\]]+)(?:\s+([^\]]+))?\]")
INTERNAL_LINK_RE = re.compile(r"\[\[([^|\]]+)\|([^\]]+)\]\]")  # [[A|B]] -> B
INTERNAL_LINK_SIMPLE_RE = re.compile(r"\[\[([^\]]+)\]\]")  # [[A]] -> A
MULTI_BRACKETS_RE = re.compile(r"[{}]")
MULTI_SPACES_RE = re.compile(r"[ \t\u00A0]{2,}")
WIKI_TABLE_RE = re.compile(
    r"^\{\|.*?$.*?^\|\}$", re.MULTILINE | re.DOTALL
)  # remove tables

# Namespaces to skip (Korean prefixes)
SKIP_PREFIXES = (
    "위키백과:",
    "사용자:",
    "파일:",
    "그림:",
    "분류:",
    "틀:",
    "도움말:",
    "포털:",
    "책:",
    "초안:",
    "틀토론:",
    "분류토론:",
    "위키백과토론:",
    "사용자토론:",
    "파일토론:",
    "그림토론:",
    "도움말토론:",
    "포털토론:",
    "책토론:",
    "초안토론:",
)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Korean Wikipedia dump -> plain text lines (one sentence per line).

Usage:
  python extract_kowiki.py \
    --out ./data/wiki.txt \
    [--dump ./kowiki-latest-pages-articles.xml.bz2] \
    [--no-download] [--paragraph]
"""

import argparse
import os
import sys
import bz2
import re
import html
import urllib.request
from urllib.error import HTTPError, URLError
from contextlib import contextmanager
from xml.etree import ElementTree as ET
from pathlib import Path

WIKI_URL = (
    "https://dumps.wikimedia.org/kowiki/latest/kowiki-latest-pages-articles.xml.bz2"
)
DEFAULT_DUMP = "kowiki-latest-pages-articles.xml.bz2"

# --- Utilities ---------------------------------------------------------------


def human_bytes(n: int) -> str:
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if n < 1024.0:
            return f"{n:3.1f}{unit}"
        n /= 1024.0
    return f"{n:.1f}PB"


def ensure_parent(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)


def strip_ns(tag: str) -> str:
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


# --- Downloader with resume --------------------------------------------------


def download_with_resume(url: str, dest: Path) -> None:
    tmp = dest.with_suffix(dest.suffix + ".part")
    exist = tmp.exists()
    start = tmp.stat().st_size if exist else 0

    headers = {}
    if exist and start > 0:
        headers["Range"] = f"bytes={start}-"

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp, open(tmp, "ab") as f:
            # Determine total size for progress if provided
            total = resp.headers.get("Content-Length")
            if total is not None:
                total = int(total) + start
            downloaded = start

            chunk = 1024 * 1024  # 1MB
            while True:
                data = resp.read(chunk)
                if not data:
                    break
                f.write(data)
                downloaded += len(data)
                if total:
                    pct = downloaded / total * 100
                    print(
                        f"\rDownloading: {human_bytes(downloaded)} / {human_bytes(total)} ({pct:5.1f}%)",
                        end="",
                        flush=True,
                    )
                else:
                    print(
                        f"\rDownloading: {human_bytes(downloaded)}", end="", flush=True
                    )
        print()
        tmp.replace(dest)
    except (HTTPError, URLError) as e:
        print(f"\n[ERROR] Download failed: {e}", file=sys.stderr)
        if not dest.exists():
            raise


# --- Wikimarkup cleaning -----------------------------------------------------

TEMPLATE_RE = re.compile(r"\{\{[^{}]*\}\}")
COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
REF_TAG_RE = re.compile(
    r"<ref\b[^>/]*?/?>.*?</ref>|<ref\b[^>/]*/>", re.DOTALL | re.IGNORECASE
)
HTML_TAG_RE = re.compile(r"<[^>]+>")
FILE_LINK_RE = re.compile(
    r"\[\[(파일|그림|File|Image):.*?\]\]", re.IGNORECASE | re.DOTALL
)
CATEGORY_LINK_RE = re.compile(r"\[\[(분류|Category):.*?\]\]", re.IGNORECASE | re.DOTALL)
EXTERNAL_LINK_RE = re.compile(r"\[(https?://[^\s\]]+)(?:\s+([^\]]+))?\]")
INTERNAL_LINK_RE = re.compile(r"\[\[([^|\]]+)\|([^\]]+)\]\]")  # [[A|B]] -> B
INTERNAL_LINK_SIMPLE_RE = re.compile(r"\[\[([^\]]+)\]\]")  # [[A]] -> A
MULTI_BRACKETS_RE = re.compile(r"[{}]")
MULTI_SPACES_RE = re.compile(r"[ \t\u00A0]{2,}")
WIKI_TABLE_RE = re.compile(
    r"^\{\|.*?$.*?^\|\}$", re.MULTILINE | re.DOTALL
)  # remove tables

# Namespaces to skip (Korean prefixes)
SKIP_PREFIXES = (
    "위키백과:",
    "사용자:",
    "파일:",
    "그림:",
    "분류:",
    "틀:",
    "도움말:",
    "포털:",
    "책:",
    "초안:",
    "틀토론:",
    "분류토론:",
    "위키백과토론:",
    "사용자토론:",
    "파일토론:",
    "그림토론:",
    "도움말토론:",
    "포털토론:",
    "책토론:",
    "초안토론:",
)


def clean_wikitext(text: str) -> str:
    # remove comments, tables, refs, html
    s = COMMENT_RE.sub(" ", text)
    s = WIKI_TABLE_RE.sub(" ", s)
    s = REF_TAG_RE.sub(" ", s)
    s = HTML_TAG_RE.sub(" ", s)

    # iteratively remove templates {{ ... }} (shallow nesting)
    prev = None
    while prev != s:
        prev = s
        s = TEMPLATE_RE.sub(" ", s)

    # remove files/categories
    s = FILE_LINK_RE.sub(" ", s)
    s = CATEGORY_LINK_RE.sub(" ", s)

    # external links: keep label if exists, else drop
    def _ext_repl(m):
        return m.group(2) if m.group(2) else " "

    s = EXTERNAL_LINK_RE.sub(_ext_repl, s)

    # internal links: [[A|B]] -> B ; [[A]] -> A
    s = INTERNAL_LINK_RE.sub(r"\2", s)
    s = INTERNAL_LINK_SIMPLE_RE.sub(r"\1", s)

    # remove leftover braces
    s = MULTI_BRACKETS_RE.sub(" ", s)

    # unescape HTML
    s = html.unescape(s)

    # normalize spaces
    s = s.replace("\r", "\n")
    s = MULTI_SPACES_RE.sub(" ", s)
    # collapse multiple newlines
    s = re.sub(r"\n{3,}", "\n\n", s)

    return s.strip()


# Sentence splitter (simple heuristic for Korean + punctuation)
SENT_SPLIT_RE = re.compile(r"(?<=[\.!?…])\s+|(?<=(?:다|요|함|됨|임)\.)\s+")


def sentences(text: str):
    # first split by newlines into paragraphs, then by sentence-ish boundaries
    for para in (p.strip() for p in text.split("\n") if p.strip()):
        parts = re.split(SENT_SPLIT_RE, para)
        for sent in parts:
            s = sent.strip()
            if len(s) >= 2:
                yield s


# --- XML streaming -----------------------------------------------------------


def extract_dump(dump_path: Path, out_path: Path, paragraph_mode: bool = False):
    ensure_parent(out_path)
    count_pages = count_lines = 0

    with bz2.open(dump_path, "rb") as f, open(out_path, "w", encoding="utf-8") as out:
        # iterparse end events for memory efficiency
        context = ET.iterparse(f, events=("end",))
        title = None
        for event, elem in context:
            tag = strip_ns(elem.tag)
            if tag == "title":
                title = elem.text or ""
            elif tag == "text":
                text = elem.text or ""
                # filter namespaces by title
                if title and any(title.startswith(pref) for pref in SKIP_PREFIXES):
                    pass
                else:
                    cleaned = clean_wikitext(text)
                    if cleaned:
                        if paragraph_mode:
                            for line in (
                                p.strip() for p in cleaned.split("\n") if p.strip()
                            ):
                                out.write(line + "\n")
                                count_lines += 1
                        else:
                            for s in sentences(cleaned):
                                out.write(s + "\n")
                                count_lines += 1
                # clear siblings upward to free memory
                parent = elem
                while parent is not None:
                    parent.clear()
                    break
            elif tag == "page":
                count_pages += 1
                if count_pages % 500 == 0:
                    print(
                        f"\rProcessed pages: {count_pages:,} | lines: {count_lines:,}",
                        end="",
                        flush=True,
                    )
                # clear page to free memory
                elem.clear()
        print(
            f"\nDone. Pages: {count_pages:,} | lines written: {count_lines:,} -> {out_path}"
        )


def main():
    ap = argparse.ArgumentParser(
        description="Extract Korean Wikipedia dump to plain text lines."
    )
    ap.add_argument(
        "--dump",
        type=str,
        default=DEFAULT_DUMP,
        help="Path to kowiki .xml.bz2 (will download if missing).",
    )
    ap.add_argument(
        "--out", type=str, default="./data/wiki.txt", help="Output text file (UTF-8)."
    )
    ap.add_argument(
        "--no-download",
        action="store_true",
        help="Do not attempt to download the dump.",
    )
    ap.add_argument(
        "--paragraph",
        action="store_true",
        help="Write one paragraph per line (instead of sentence per line).",
    )
    args = ap.parse_args()

    dump_path = Path(args.dump)
    out_path = Path(args.out)

    if not dump_path.exists():
        if args.no_download:
            print(
                f"[ERROR] Dump not found: {dump_path}. Provide --dump or remove --no-download.",
                file=sys.stderr,
            )
            sys.exit(1)
        print(f"Dump not found at {dump_path}. Downloading from {WIKI_URL} ...")
        download_with_resume(WIKI_URL, dump_path)
    else:
        print(
            f"Found dump: {dump_path} ({human_bytes(dump_path.stat().st_size)}) — skipping download."
        )

    print(f"Extracting to: {out_path} (UTF-8). Paragraph mode: {args.paragraph}")
    extract_dump(dump_path, out_path, paragraph_mode=args.paragraph)


if __name__ == "__main__":
    main()


# Sentence splitter (simple heuristic for Korean + punctuation)
SENT_SPLIT_RE = re.compile(r"(?<=[\.!?…])\s+|(?<=(?:다|요|함|됨|임)\.)\s+")


def sentences(text: str):
    # first split by newlines into paragraphs, then by sentence-ish boundaries
    for para in (p.strip() for p in text.split("\n") if p.strip()):
        parts = re.split(SENT_SPLIT_RE, para)
        for sent in parts:
            s = sent.strip()
            if len(s) >= 2:
                yield s


# --- XML streaming -----------------------------------------------------------


def extract_dump(dump_path: Path, out_path: Path, paragraph_mode: bool = False):
    ensure_parent(out_path)
    count_pages = count_lines = 0

    with bz2.open(dump_path, "rb") as f, open(out_path, "w", encoding="utf-8") as out:
        # iterparse end events for memory efficiency
        context = ET.iterparse(f, events=("end",))
        title = None
        for event, elem in context:
            tag = strip_ns(elem.tag)
            if tag == "title":
                title = elem.text or ""
            elif tag == "text":
                text = elem.text or ""
                # filter namespaces by title
                if title and any(title.startswith(pref) for pref in SKIP_PREFIXES):
                    pass
                else:
                    cleaned = clean_wikitext(text)
                    if cleaned:
                        if paragraph_mode:
                            for line in (
                                p.strip() for p in cleaned.split("\n") if p.strip()
                            ):
                                out.write(line + "\n")
                                count_lines += 1
                        else:
                            for s in sentences(cleaned):
                                out.write(s + "\n")
                                count_lines += 1
                # clear siblings upward to free memory
                parent = elem
                while parent is not None:
                    parent.clear()
                    break
            elif tag == "page":
                count_pages += 1
                if count_pages % 500 == 0:
                    print(
                        f"\rProcessed pages: {count_pages:,} | lines: {count_lines:,}",
                        end="",
                        flush=True,
                    )
                # clear page to free memory
                elem.clear()
        print(
            f"\nDone. Pages: {count_pages:,} | lines written: {count_lines:,} -> {out_path}"
        )


def main():
    ap = argparse.ArgumentParser(
        description="Extract Korean Wikipedia dump to plain text lines."
    )
    ap.add_argument(
        "--dump",
        type=str,
        default=DEFAULT_DUMP,
        help="Path to kowiki .xml.bz2 (will download if missing).",
    )
    ap.add_argument(
        "--out", type=str, default="./data/wiki.txt", help="Output text file (UTF-8)."
    )
    ap.add_argument(
        "--no-download",
        action="store_true",
        help="Do not attempt to download the dump.",
    )
    ap.add_argument(
        "--paragraph",
        action="store_true",
        help="Write one paragraph per line (instead of sentence per line).",
    )
    args = ap.parse_args()

    dump_path = Path(args.dump)
    out_path = Path(args.out)

    if not dump_path.exists():
        if args.no_download:
            print(
                f"[ERROR] Dump not found: {dump_path}. Provide --dump or remove --no-download.",
                file=sys.stderr,
            )
            sys.exit(1)
        print(f"Dump not found at {dump_path}. Downloading from {WIKI_URL} ...")
        download_with_resume(WIKI_URL, dump_path)
    else:
        print(
            f"Found dump: {dump_path} ({human_bytes(dump_path.stat().st_size)}) — skipping download."
        )

    print(f"Extracting to: {out_path} (UTF-8). Paragraph mode: {args.paragraph}")
    extract_dump(dump_path, out_path, paragraph_mode=args.paragraph)


if __name__ == "__main__":
    main()
