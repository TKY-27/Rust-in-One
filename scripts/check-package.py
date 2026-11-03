#!/usr/bin/env python3
"""Check distributable files and local Markdown links; not a schema validator."""
from pathlib import Path
import re
import shutil
import tempfile
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "rust-in-one"


def check_links(sources: list[Path], boundary: Path) -> None:
    for source in sources:
        for target in re.findall(
            r"\[[^\]]*\]\(([^\s)]+)\)", source.read_text(encoding="utf-8")
        ):
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            destination = (source.parent / unquote(parsed.path)).resolve()
            if not destination.is_relative_to(boundary.resolve()):
                raise ValueError(f"{source}: link escapes package: {target}")
            if not destination.exists():
                raise ValueError(f"{source}: missing link: {target}")


def main() -> None:
    if (SKILL / "LICENSE.txt").read_bytes() != (ROOT / "LICENSE").read_bytes():
        raise ValueError("Root and installed MIT notices differ")
    if "MIT License" not in (SKILL / "LICENSE.txt").read_text(encoding="utf-8"):
        raise ValueError("Installed MIT notice is missing")
    if not (SKILL / "SKILL.md").is_file():
        raise ValueError("SKILL.md is missing")
    for path in SKILL.rglob("*"):
        if path.is_symlink():
            raise ValueError(f"Installation must be self-contained: {path}")
        if path.is_file() and path.suffix not in {".md", ".txt"}:
            raise ValueError(f"Unexpected file in instruction-only package: {path}")
    check_links(list(SKILL.rglob("*.md")), SKILL)
    # Verify the actual copy installation documented in README, without checkout context.
    with tempfile.TemporaryDirectory() as directory:
        installed = Path(directory) / "rust-in-one"
        shutil.copytree(SKILL, installed)
        check_links(list(installed.rglob("*.md")), installed)
        source_files = {
            path.relative_to(SKILL): path.read_bytes()
            for path in SKILL.rglob("*") if path.is_file()
        }
        installed_files = {
            path.relative_to(installed): path.read_bytes()
            for path in installed.rglob("*") if path.is_file()
        }
        if source_files != installed_files:
            raise ValueError("Standalone installation differs from source")
    # Check maintained documentation without walking caches or virtual environments.
    documents = list(ROOT.glob("*.md"))
    for directory in ("docs", ".github"):
        documents.extend((ROOT / directory).rglob("*.md"))
    check_links(documents, ROOT)
    print("Package copy, local file links, and MIT notices passed (schema/URL anchors not checked).")


if __name__ == "__main__":
    main()
