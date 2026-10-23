# -*- coding: utf-8 -*-
"""Match a disease name to a user-supplied current notifiable-disease catalog."""
from __future__ import annotations

import argparse
import csv
import sys


def norm(value: str) -> str:
    return "".join(value.strip().lower().split())


def main() -> int:
    parser = argparse.ArgumentParser(description="Check a disease against a supplied catalog")
    parser.add_argument("--disease", required=True)
    parser.add_argument("--catalog", default="")
    args = parser.parse_args()
    if not args.catalog:
        print("status\tunverified")
        print("disease\t%s" % args.disease.strip())
        print("class\t")
        return 0
    with open(args.catalog, encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = set(reader.fieldnames or [])
        if not {"disease", "class"} <= fields:
            print("status\tbad_catalog", file=sys.stderr)
            return 1
        want = norm(args.disease)
        found = 0
        for row in reader:
            if norm(row.get("disease") or "") != want:
                continue
            found += 1
            print("status\tmatched")
            print("disease\t%s" % (row.get("disease") or "").strip())
            print("class\t%s" % (row.get("class") or "").strip())
            print("source\t%s" % (row.get("source") or "").strip())
            print("as_of\t%s" % (row.get("as_of") or "").strip())
        if not found:
            print("status\tnot_in_catalog")
            print("disease\t%s" % args.disease.strip())
            print("class\t")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
