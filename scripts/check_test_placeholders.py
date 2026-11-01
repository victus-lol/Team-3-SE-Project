#!/usr/bin/env python3
"""
Pending Test Placeholders Inventory Checker.
Owner: Akash Pawar (PES2UG24CS041)

Inventories all pending/skipped test markers across backend, frontend, and E2E.
Groups them by owner and sprint, prints counts, and validates:
  - Owner is specified
  - Requirement ID (TMA-*) is specified
  - Backlog ID (S1-* or S2-*) is specified

Exit code:
  - 0: All pending tests properly documented
  - 1: One or more pending tests missing metadata, or (--fail-on-pending specified and count > 0)
"""

import os
import re
import sys
import argparse
from pathlib import Path
from collections import defaultdict

ROOT_DIR = Path(__file__).resolve().parent.parent

def scan_files():
    patterns = [
        (ROOT_DIR / "server" / "tests", re.compile(r'@pytest\.mark\.skip\(reason=[\'"]Pending implementation:?\s*([^\'"]*)[\'"]\)')),
        (ROOT_DIR / "client" / "src" / "tests", re.compile(r'it\.skip\([\'"]([^\'"]*)[\'"]')),
        (ROOT_DIR / "tests" / "e2e", re.compile(r'test\.skip\([\'"]([^\'"]*)[\'"]')),
    ]

    inventory = []
    missing_metadata = []

    for search_dir, regex in patterns:
        if not search_dir.exists():
            continue
        for file_path in search_dir.rglob("*"):
            if not file_path.is_file() or file_path.suffix not in (".py", ".jsx", ".js"):
                continue
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                lines = content.splitlines()

            for i, line in enumerate(lines):
                match = regex.search(line)
                if match:
                    # Look around next 10 lines for metadata comments/docstring
                    context = "\n".join(lines[i:min(len(lines), i + 10)])

                    owner_match = re.search(r'Owner:\s*([A-Za-z+]+)', context, re.IGNORECASE)
                    req_match = re.search(r'Requirement:\s*(TMA-[A-Z]+-[0-9]+)', context, re.IGNORECASE)
                    backlog_match = re.search(r'Backlog:\s*(S[12]-[0-9]+)', context, re.IGNORECASE)
                    tc_match = re.search(r'(TC-[A-Za-z]+-[0-9]+)', context)

                    owner = owner_match.group(1) if owner_match else "UNKNOWN"
                    req = req_match.group(1) if req_match else "UNKNOWN"
                    backlog = backlog_match.group(1) if backlog_match else "UNKNOWN"
                    tc_id = tc_match.group(1) if tc_match else "TC-UNKNOWN"

                    item = {
                        "file": file_path.relative_to(ROOT_DIR),
                        "line": i + 1,
                        "tc_id": tc_id,
                        "owner": owner,
                        "req": req,
                        "backlog": backlog,
                    }
                    inventory.append(item)

                    if "UNKNOWN" in (owner, req, backlog):
                        missing_metadata.append(item)

    return inventory, missing_metadata

def main():
    parser = argparse.ArgumentParser(description="Check pending test placeholders")
    parser.add_argument("--fail-on-pending", action="store_true", help="Fail if any pending tests exist (release gate)")
    args = parser.parse_args()

    inventory, missing_metadata = scan_files()

    print("=" * 60)
    print(f"PENDING TEST PLACEHOLDERS INVENTORY (Total: {len(inventory)})")
    print("=" * 60)

    by_owner = defaultdict(list)
    by_backlog = defaultdict(list)

    for item in inventory:
        by_owner[item["owner"]].append(item)
        by_backlog[item["backlog"]].append(item)

    print("\n--- Breakdown by Owner ---")
    for owner, items in sorted(by_owner.items()):
        print(f"  {owner:<15}: {len(items)} pending tests")

    print("\n--- Breakdown by Backlog Item ---")
    for b_id, items in sorted(by_backlog.items()):
        print(f"  {b_id:<15}: {len(items)} pending tests")

    if missing_metadata:
        print("\n" + "!" * 60)
        print(f"ERROR: {len(missing_metadata)} pending test(s) missing required metadata (Owner, Requirement, Backlog):")
        for item in missing_metadata:
            print(f"  {item['file']}:{item['line']} -> {item}")
        print("!" * 60)
        return 1

    if args.fail_on_pending and len(inventory) > 0:
        print("\n" + "!" * 60)
        print("ERROR: --fail-on-pending is set, but pending tests still exist!")
        print("!" * 60)
        return 1

    print("\n[OK] All pending tests have valid metadata (Owner, Requirement ID, Backlog ID).")
    return 0

if __name__ == "__main__":
    sys.exit(main())

