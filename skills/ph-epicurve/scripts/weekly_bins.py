# -*- coding: utf-8 -*-
"""Count rows by ISO week. Does not read the network or print cell text."""
from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from datetime import datetime, timedelta

CANDIDATES = ("original_date", "onset_date", "date", "发病日期", "日期")


def parse_day(value: str):
    text = value.strip()
    if not text:
        return None
    head = text.replace("/", "-").split()[0].split("T")[0]
    try:
        return datetime.strptime(head, "%Y-%m-%d").date()
    except ValueError:
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Bin a date column into ISO weeks")
    parser.add_argument("csv_path")
    parser.add_argument("--date-column", default="")
    args = parser.parse_args()
    with open(args.csv_path, encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            print("no header", file=sys.stderr)
            return 1
        column = args.date_column or next(
            (name for name in CANDIDATES if name in reader.fieldnames), ""
        )
        if not column:
            print("date column missing", file=sys.stderr)
            print("headers: " + ",".join(reader.fieldnames), file=sys.stderr)
            return 1
        counts: Counter[str] = Counter()
        missing = 0
        unparsed = 0
        rows = 0
        for row in reader:
            rows += 1
            parsed = parse_day(row.get(column) or "")
            if parsed is None:
                missing += 1
                continue
            if parsed is False:
                unparsed += 1
                continue
            monday = parsed - timedelta(days=parsed.weekday())
            counts[monday.isoformat()] += 1
    print("date_column\t%s" % column)
    print("rows\t%d" % rows)
    print("missing_date\t%d" % missing)
    print("unparsed_date\t%d" % unparsed)
    print("week_start\tcount")
    for start in sorted(counts):
        print("%s\t%d" % (start, counts[start]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
