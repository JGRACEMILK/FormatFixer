#!/usr/bin/env python3

import argparse
import re
import sys

def main():
    parser = argparse.ArgumentParser(
        description="Fix TSV rows with embedded newlines using a row-start regex pattern."
    )
    parser.add_argument(
        "--input", required=True, help="Input TSV file (possibly broken)"
    )
    parser.add_argument(
        "--output", required=True, help="Output TSV file (fixed)"
    )
    parser.add_argument(
        "--row-start-pattern",
        required=True,
        help=r"Regex that identifies the start of a new row (e.g. ^\d{4}\t\d{10}\t)",
    )
    parser.add_argument(
        "--join-with",
        default=" ",
        help="String used to join continuation lines (default: space)",
    )
    parser.add_argument(
        "--has-header",
        action="store_true",
        help="Indicates that the first line is a header row",
    )
    parser.add_argument(
        "--fail-on-orphans",
        action="store_true",
        help="Exit with error if orphan continuation lines are found",
    )

    args = parser.parse_args()

    row_start_re = re.compile(args.row_start_pattern)

    rows = []
    header = None
    current_row = None
    orphan_lines = 0

    with open(args.input, "r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.rstrip("\n")

            # --- Header handling ---
            if lineno == 1 and args.has_header:
                header = line
                continue

            if row_start_re.match(line):
                # Start of a new logical row
                if current_row is not None:
                    rows.append(current_row)
                current_row = line
            else:
                # Continuation line
                if current_row is None:
                    orphan_lines += 1
                    continue
                current_row += args.join_with + line.strip()

    if current_row is not None:
        rows.append(current_row)

    # --- Write output ---
    with open(args.output, "w", encoding="utf-8") as f:
        if header is not None:
            f.write(header + "\n")
        for row in rows:
            f.write(row + "\n")

    # --- Exit handling ---
    if orphan_lines > 0:
        print(
            f"WARNING: {orphan_lines} orphan continuation lines ignored",
            file=sys.stderr,
        )
        if args.fail_on_orphans:
            sys.exit(1)

    print(f"SUCCESS: {len(rows)} rows written")
    sys.exit(0)


if __name__ == "__main__":
    main()
