"""Validate a measured load-test report and emit its GitHub summary table."""

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    parser.add_argument("--max-p90-ms", type=float, default=3000.0)
    args = parser.parse_args()

    try:
        report = json.loads(args.report.read_text(encoding="utf-8"))
        virtual_users = int(report["virtual_users"])
        duration = int(report["duration_seconds"])
        requests = int(report["requests"])
        failures = int(report["failures"])
        p50_ms = float(report["p50_ms"])
        p90_ms = float(report["p90_ms"])
        max_ms = float(report["max_ms"])
        rate = float(report["requests_per_second"])
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"Invalid performance report {args.report}: {exc}", file=sys.stderr)
        return 2

    valid = (
        virtual_users == 20
        and duration == 30
        and requests > 0
        and failures == 0
        and p90_ms <= args.max_p90_ms
    )
    status = "✅ PASSED" if valid else "❌ FAILED"
    summary = [
        f"| Authenticated performance | {status} | {virtual_users} users for {duration}s; p90 limit {args.max_p90_ms:.0f}ms. |",
        "",
        "| Metric | Measured result |",
        "|---|---:|",
        f"| Requests / failures | {requests} / {failures} |",
        f"| p50 / p90 | {p50_ms:.2f} / {p90_ms:.2f} ms |",
        f"| Maximum latency | {max_ms:.2f} ms |",
        f"| Throughput | {rate:.2f} requests/s |",
        "",
    ]
    rendered = "\n".join(summary)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(rendered)
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
