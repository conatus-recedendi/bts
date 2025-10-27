#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import html
import re
import sys
import unicodedata
from pathlib import Path

# --- robust decode -----------------------------------------------------------

# 인코딩 후보 (BOM 우선, 그 다음 흔한 한국어 인코딩)
CANDIDATE_ENCODINGS = (
    "utf-8-sig",  # BOM 있는 UTF-8
    "utf-16",  # BOM 있으면 자동 판단
    "utf-16-le",
    "utf-16-be",
    "utf-32",
    "utf-32-le",
    "utf-32-be",
    "utf-8",  # BOM 없는 UTF-8
    "cp949",
    "euc-kr",
)


def decode_best(raw: bytes, path: Path) -> str:
    for enc in CANDIDATE_ENCODINGS:
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    # 마지막 안전장치: 대체 문자로라도 보존 (원인 파악 위해 경고)
    print(
        f"[WARN] {path}: could not decode with common encodings, using utf-8(replace)",
        file=sys.stderr,
    )
    return raw.decode("utf-8", errors="replace")


# --- regex (문자열 단계에서 태그 처리) ----------------------------------------

HAS_TAG_RE_STR = re.compile(r"<\s*/?\s*[A-Za-z][^>]*>")
TAG_RE_STR = re.compile(r"<[^>]+>")
MULTI_SPACES_RE = re.compile(r"[ \t\u00A0]{2,}")
ZERO_WIDTH_RE = re.compile(r"[\u200B-\u200D\uFEFF]")

# 허용: 한글(가-힣, 자모), 영문, 숫자, 공백
NON_ALLOWED_RE = re.compile(r"[^0-9A-Za-z가-힣ㄱ-ㅎㅏ-ㅣ\s]")


def extract_lines_from_text(s: str):
    # 태그 없으면 무시(요구사항)
    if not HAS_TAG_RE_STR.search(s):
        return []

    # 1) 태그를 개행으로 치환 → 태그 경계마다 라인 분리
    s = TAG_RE_STR.sub("\n", s)

    # 2) HTML 엔티티 해제 + 정규화 + 제로폭 제거
    s = html.unescape(s)
    s = unicodedata.normalize("NFC", s)
    s = ZERO_WIDTH_RE.sub("", s)

    # 3) 허용 문자만 남기기
    s = NON_ALLOWED_RE.sub(" ", s)

    # 4) 개행/공백 정리 후 라인화
    s = s.replace("\r", "\n")
    out = []
    for chunk in s.split("\n"):
        chunk = MULTI_SPACES_RE.sub(" ", chunk).strip()
        if chunk:
            out.append(chunk)
    return out


# --- IO ----------------------------------------------------------------------


def iter_txt_files(dirs):
    for d in dirs:
        p = Path(d)
        if not p.exists():
            continue
        for f in sorted(p.rglob("*.txt")):
            if f.is_file():
                yield f


def process_dirs(in_dirs, out_path: Path, min_len: int = 1):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    files = lines_out = 0

    with open(out_path, "wb") as out_f:
        for f in iter_txt_files(in_dirs):
            files += 1
            try:
                raw = f.read_bytes()
            except Exception as e:
                print(f"[WARN] Skip {f}: {e}", file=sys.stderr)
                continue

            text = decode_best(raw, f)
            lines = extract_lines_from_text(text)

            for line in lines:
                if len(line) >= min_len:
                    out_f.write(line.encode("utf-8") + b"\n")
                    lines_out += 1

            if files % 100 == 0:
                print(
                    f"\rProcessed files: {files:,} | lines written: {lines_out:,}",
                    end="",
                    flush=True,
                )

    print(f"\nDone. Files: {files:,} | lines written: {lines_out:,} -> {out_path}")


def main():
    ap = argparse.ArgumentParser(
        description="Sejong extractor (decode first, strip tags in text, keep KOR/ENG/DIGIT)."
    )
    ap.add_argument(
        "--in",
        nargs="+",
        default=["./sejong/colloquial_raw", "./sejong/written_raw"],
        help="Input directories (recursively scan for *.txt)",
    )
    ap.add_argument(
        "--out", type=str, default="./data/sejong.txt", help="Output UTF-8 text file"
    )
    ap.add_argument(
        "--min-len", type=int, default=1, help="Minimum length for a kept line"
    )
    args = ap.parse_args()

    in_dirs = args.__dict__["in"]
    out_path = Path(args.out)
    print("Inputs:")
    for d in in_dirs:
        print("  ", Path(d).resolve())
    print("Output:\n  ", out_path.resolve())

    process_dirs(in_dirs, out_path, min_len=args.min_len)


if __name__ == "__main__":
    main()
