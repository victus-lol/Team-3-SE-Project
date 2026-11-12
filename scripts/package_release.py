"""Package the tested Task Manager web application for a versioned release."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from datetime import UTC, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._+-]*$")


def build_release(version: str, commit: str, output_dir: Path) -> tuple[Path, Path]:
    """Create a frontend-plus-Flask deployment bundle and SHA-256 sidecar."""
    if not VERSION_PATTERN.fullmatch(version):
        raise ValueError("Version may contain only letters, digits, dots, underscores, plus, and hyphens.")

    frontend_dist = ROOT / "client" / "dist"
    if not (frontend_dist / "index.html").is_file():
        raise FileNotFoundError(f"Frontend build not found: {frontend_dist / 'index.html'}")

    required_files = [
        ROOT / "README.md",
        ROOT / "docs" / "DEPLOYMENT.md",
        ROOT / "server" / "run.py",
        ROOT / "server" / "requirements.txt",
    ]
    for path in required_files:
        if not path.is_file():
            raise FileNotFoundError(f"Required release file not found: {path}")

    output_dir.mkdir(parents=True, exist_ok=True)
    archive_path = output_dir / f"task-manager-webapp-{version}.zip"
    checksum_path = Path(f"{archive_path}.sha256")
    manifest = {
        "name": "task-manager-webapp",
        "version": version,
        "commit": commit,
        "built_at_utc": datetime.now(UTC).isoformat(),
        "python_runtime": "3.12",
        "contents": ["client/dist", "server/app", "server/migrations"],
    }

    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in required_files:
            archive.write(path, path.relative_to(ROOT).as_posix())

        for directory in (ROOT / "server" / "app", ROOT / "server" / "migrations", frontend_dist):
            for path in sorted(directory.rglob("*")):
                if not path.is_file() or "__pycache__" in path.parts or path.suffix in {".pyc", ".pyo"}:
                    continue
                archive.write(path, path.relative_to(ROOT).as_posix())

        archive.writestr(
            "manifest.json",
            json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        )

    digest = hashlib.sha256(archive_path.read_bytes()).hexdigest()
    checksum_path.write_text(f"{digest}  {archive_path.name}\n", encoding="utf-8")
    return archive_path, checksum_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", required=True, help="Release version or snapshot identifier")
    parser.add_argument("--commit", required=True, help="Git commit SHA included in the build")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "build" / "release",
        help="Directory for the ZIP bundle and checksum file",
    )
    args = parser.parse_args()

    archive, checksum = build_release(args.version, args.commit, args.output_dir)
    print(f"Created {archive}")
    print(checksum.read_text(encoding="utf-8").strip())


if __name__ == "__main__":
    main()
