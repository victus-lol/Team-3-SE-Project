"""Enforce line and branch coverage thresholds from a coverage.py JSON report."""

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path, help="coverage.py JSON report")
    parser.add_argument("--min-statement", type=float, default=80.0)
    parser.add_argument("--min-branch", type=float, default=60.0)
    args = parser.parse_args()

    try:
        totals = json.loads(args.report.read_text(encoding="utf-8"))["totals"]
        statement_rate = float(totals["percent_statements_covered"])
        branch_rate = float(totals["percent_branches_covered"])
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"Could not read coverage totals from {args.report}: {exc}", file=sys.stderr)
        return 2

    lines = [
        "## Stage 6: Coverage & Quality Gate",
        "",
        "| Metric | Result | Minimum | Status |",
        "|---|---:|---:|---|",
        f"| Statement coverage | {statement_rate:.2f}% | {args.min_statement:.2f}% | {'PASS' if statement_rate >= args.min_statement else 'FAIL'} |",
        f"| Branch coverage | {branch_rate:.2f}% | {args.min_branch:.2f}% | {'PASS' if branch_rate >= args.min_branch else 'FAIL'} |",
        "",
    ]
    print("\n".join(lines))
    if statement_rate < args.min_statement or branch_rate < args.min_branch:
        print("Coverage quality gate did not meet its configured minimums.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
