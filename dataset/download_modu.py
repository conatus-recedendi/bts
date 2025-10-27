#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Read MODU newspaper CSVs and write one cleaned sentence per line.

- Input CSV header example:
  file_id,doc_id,title,author,publisher,date,topic,original_topic,sentence_id,sentence

- We read: ./modu/NIKL_NEWSPAPER_2020_1.csv ... _6.csv (configurable by --glob)
- For each row, take only the 'sentence' field
- Keep ONLY Korean (가-힣/자모), English letters, digits, and whitespace
- Output as UTF-8 text, one sentence per line (whitespace normalized)

Usage:
  python extract_modu_sentences.py --out ./data/modu_sentences.txt
  # or custom glob
  python extract_modu_sentences.py --glob "./modu/NIKL_NEWSPAPER_2020_*.csv" --out ./data/modu_sentences.txt
"""

import argparse
import csv
import html
import io
import re
import sys
import unicodedata
from glob import glob
from pathlib import Path

# ---- robust per-file decoding ----------------------------------------------

CANDIDATE_ENCODINGS = (
    "utf-8-sig", "utf-16", "utf-16-le", "utf-16-be",
    "utf-32", "utf-32-le", "utf-32-be",
    "utf-8", "cp949", "euc-kr"
)

def decode_best(raw: bytes, path: Path) -> str:
    for enc in CANDIDATE_ENCODINGS:
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    print(f"[WARN] {path}: decode fallback (utf-8 with replacement)", file=sys.stderr)
    return raw.decode("utf-8", errors="replace")

# ---- cleaning ---------------------------------------------------------------

NON_ALLOWED_RE  = re.compile(r"[^0-9A-Za-z가-힣ㄱ-ㅎㅏ-ㅣ\s]")
MULTI_SPACES_RE = re.compile(r"[ \t\u00A0]{2,}")
ZERO_WIDTH_RE   = re.compile(r"[\u200B-\u200D\uFEFF]")

def clean_sentence(s: str) -> str:
    # HTML 엔티티 해제, 정규화, 제로폭 제거
    s = html.unescape(s)
    s = unicodedata.normalize("NFC", s)
    s = ZERO_WIDTH_RE.sub("", s)
    # 허용 문자만 남기기 (한글/자모, 영문, 숫자, 공백)
    s = NON_ALLOWED_RE.sub(" ", s)
    # 공백 정규화, 개행 제거
    s = s.replace("\r", " ").replace("\n", " ")
    s = MULTI_SPACES_RE.sub(" ", s).strip()
    return s

# ---- core -------------------------------------------------------------------

def process_csv_text(csv_text: str, out_fh) -> tuple[int, int]:
    """
    csv_text: decoded CSV content
    out_fh: opened binary file handle (wb/ab) to write UTF-8 lines
    Returns: (rows_read, lines_written)
    """
    rows = 0
    written = 0
    # csv expects text stream
    reader = csv.DictReader(io.StringIO(csv_text))
    # try to locate 'sentence' column robustly
    if reader.fieldnames is None:
        return 0, 0
    fields_lower = [f.lower() for f in reader.fieldnames]
    try:
        sent_key = reader.fieldnames[fields_lower.index("sentence")]
    except ValueError:
        print(f"[WARN] CSV has no 'sentence' column; fields={reader.fieldnames}", file=sys.stderr)
        return 0, 0

    for row in reader:
        rows += 1
        sent = row.get(sent_key, "")
        if not sent:
            continue
        cleaned = clean_sentence(sent)
        if cleaned:
            out_fh.write(cleaned.encode("utf-8") + b"\n")
            written += 1
    return rows, written

def main():
    ap = argparse.ArgumentParser(description="Extract sentences from MODU CSVs.")
    ap.add_argument("--glob", type=str, default="./modu/NIKL_NEWSPAPER_2020_*.csv",
                    help="Glob pattern for input CSVs")
    ap.add_argument("--out", type=str, default="./data/modu_sentences.txt",
                    help="Output UTF-8 txt (one sentence per line)")
    ap.add_argument("--append", action="store_true",
                    help="Append to output instead of overwrite")
    args = ap.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    in_files = sorted(glob(args.glob))
    if not in_files:
        print(f"[ERROR] No CSVs matched: {args.glob}", file=sys.stderr)
        sys.exit(1)

    mode = "ab" if args.append else "wb"
    total_rows = total_lines = 0
    with open(out_path, mode) as out_fh:
        for i, fp in enumerate(in_files, 1):
            p = Path(fp)
            try:
                raw = p.read_bytes()
            except Exception as e:
                print(f"[WARN] Skip {p}: {e}", file=sys.stderr)
                continue

            text = decode_best(raw, p)
            rows, lines = process_csv_text(text, out_fh)
            total_rows += rows
            total_lines += lines

            print(f"\r[{i}/{len(in_files)}] {p.name}: rows={rows:,}, written={lines:,}", end="", flush=True)

    print(f"\nDone. Files: {len(in_files)}, rows read: {total_rows:,}, lines written: {total_lines:,} -> {out_path}")

if __name__ == "__main__":
    main()
