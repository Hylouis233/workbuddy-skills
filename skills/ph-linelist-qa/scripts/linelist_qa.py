# -*- coding: utf-8 -*-
"""Stop when a linelist header or cell looks like a direct identifier.

Prints column names and counts only.
"""
from __future__ import annotations

import argparse
import csv
import re
import sys

HEADER_RULES = (
    ("id-document", re.compile(r"身份证|证件号|idcard|id_card|id-card", re.I)),
    ("phone", re.compile(r"手机|电话|phone|mobile|(^|_)tel($|_)", re.I)),
    ("person-name", re.compile(r"姓名|患者名|full_name|patient_name|^name$", re.I)),
    ("street-address", re.compile(r"详细住址|详细地址|门牌|home_address", re.I)),
)
ID_VALUE = re.compile(r"^\d{17}[\dXx]$")
PHONE_VALUE = re.compile(r"^1[3-9]\d{9}$")


def compact(value: str) -> str:
    return re.sub(r"[\s\-]", "", value.strip())


def header_hits(names: list[str]) -> list[str]:
    hits = []
    for name in names:
        for label, pattern in HEADER_RULES:
            if pattern.search(name.strip()):
                hits.append("%s:%s" % (label, name))
    return hits


def main() -> int:
    parser = argparse.ArgumentParser(description="Check a de-identified linelist")
    parser.add_argument("csv_path")
    parser.add_argument("--date-column", default="")
    parser.add_argument("--id-column", default="case_id")
    args = parser.parse_args()
    with open(args.csv_path, encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        names = list(reader.fieldnames or [])
        if not names:
            print("status\tno_header")
            return 1
        hits = header_hits(names)
        if hits:
            print("status\tstopped")
            print("reason\tidentifier_column")
            for hit in hits:
                print("column\t%s" % hit)
            return 2
        date_column = args.date_column
        if not date_column:
            for candidate in ("onset_date", "original_date", "date", "发病日期"):
                if candidate in names:
                    date_column = candidate
                    break
        rows = 0
        missing_date = 0
        duplicate_ids = 0
        seen = set()
        for index, row in enumerate(reader, start=1):
            rows += 1
            for name in names:
                token = compact(row.get(name) or "")
                if ID_VALUE.fullmatch(token) or PHONE_VALUE.fullmatch(token):
                    print("status\tstopped")
                    print("reason\tidentifier_like_value")
                    print("column\t%s" % name)
                    print("row\t%d" % index)
                    return 2
            if date_column and not (row.get(date_column) or "").strip():
                missing_date += 1
            if args.id_column in names:
                mark = (row.get(args.id_column) or "").strip()
                if mark:
                    if mark in seen:
                        duplicate_ids += 1
                    seen.add(mark)
    print("status\tok")
    print("rows\t%d" % rows)
    print("columns\t%d" % len(names))
    if date_column:
        print("date_column\t%s" % date_column)
        print("missing_date\t%d" % missing_date)
    else:
        print("date_column\tmissing")
    if args.id_column in names:
        print("duplicate_ids\t%d" % duplicate_ids)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
