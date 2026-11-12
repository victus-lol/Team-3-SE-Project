#!/usr/bin/env python3
"""Measure authenticated task-list latency with concurrent standard-library clients."""

import argparse
import http.cookiejar
import json
import math
import statistics
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path


def _request(opener, url, *, method="GET", payload=None, headers=None):
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(url, data=body, headers=headers or {}, method=method)
    with opener.open(request, timeout=10) as response:
        return response.status, json.loads(response.read().decode("utf-8"))


def _session(base_url, email, password):
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar())
    )
    _, csrf_payload = _request(opener, f"{base_url}/api/auth/csrf")
    csrf_token = csrf_payload["data"]["csrf_token"]
    status, login_payload = _request(
        opener,
        f"{base_url}/api/auth/login",
        method="POST",
        payload={"email": email, "password": password},
        headers={"Content-Type": "application/json", "X-CSRFToken": csrf_token},
    )
    if status != 200 or not login_payload.get("success"):
        raise RuntimeError("Performance user authentication failed.")
    return opener


def run_load(base_url, email, password, vus, duration, max_p90_ms, output=None):
    sessions = []
    setup_errors = []
    for _ in range(vus):
        try:
            sessions.append(_session(base_url, email, password))
        except (urllib.error.URLError, urllib.error.HTTPError, KeyError, RuntimeError) as exc:
            setup_errors.append(type(exc).__name__)
    if setup_errors:
        raise RuntimeError(f"Could not prepare all virtual users ({len(setup_errors)} setup errors).")

    start_gate = threading.Barrier(vus)
    timings = []
    failures = []
    lock = threading.Lock()

    def worker(opener):
        try:
            start_gate.wait(timeout=30)
        except threading.BrokenBarrierError:
            with lock:
                failures.append("barrier")
            return
        deadline = time.monotonic() + duration
        while time.monotonic() < deadline:
            started = time.perf_counter()
            try:
                status, payload = _request(opener, f"{base_url}/api/tasks?page=1&per_page=20")
                elapsed_ms = (time.perf_counter() - started) * 1000
                if status != 200 or not payload.get("success") or not isinstance(payload.get("data"), list):
                    raise RuntimeError("Task-list response failed its contract.")
                with lock:
                    timings.append(elapsed_ms)
            except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, RuntimeError, ValueError) as exc:
                with lock:
                    failures.append(type(exc).__name__)

    threads = [threading.Thread(target=worker, args=(opener,), daemon=True) for opener in sessions]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=duration + 45)
    alive = [thread for thread in threads if thread.is_alive()]
    if alive:
        failures.extend(["worker-timeout"] * len(alive))

    if not timings:
        raise RuntimeError("No task-list samples were recorded.")
    ordered = sorted(timings)
    p90_ms = ordered[max(0, math.ceil(0.90 * len(ordered)) - 1)]
    report = {
        "virtual_users": vus,
        "duration_seconds": duration,
        "requests": len(timings),
        "failures": len(failures),
        "p50_ms": round(statistics.median(ordered), 2),
        "p90_ms": round(p90_ms, 2),
        "max_ms": round(max(ordered), 2),
        "requests_per_second": round(len(timings) / duration, 2),
        "p90_limit_ms": max_p90_ms,
    }
    rendered = json.dumps(report, indent=2)
    print(rendered)
    if output:
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered + "\n", encoding="utf-8")
    if failures:
        print(f"Failure categories: {', '.join(sorted(set(failures)))}")
    if failures or p90_ms > max_p90_ms:
        raise SystemExit(1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://127.0.0.1:5000")
    parser.add_argument("--email", default="e2e.user@example.com")
    parser.add_argument("--password", default="password123")
    parser.add_argument("--vus", type=int, default=20)
    parser.add_argument("--duration", type=int, default=30)
    parser.add_argument("--max-p90-ms", type=float, default=3000)
    parser.add_argument("--output", help="Optional JSON report path")
    args = parser.parse_args()
    if min(args.vus, args.duration) < 1:
        parser.error("--vus and --duration must be positive")
    run_load(
        args.base_url.rstrip("/"),
        args.email,
        args.password,
        args.vus,
        args.duration,
        args.max_p90_ms,
        args.output,
    )


if __name__ == "__main__":
    main()
