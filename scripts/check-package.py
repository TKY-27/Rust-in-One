#!/usr/bin/env python3
"""Check distributable files and local Markdown links; not a schema validator."""
from pathlib import Path
import re
import shutil
import tempfile
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "rust-in-one"


def check_links(root: Path) -> None:
    for source in root.rglob("*.md"):
        for target in re.findall(r"\[[^\]]*\]\(([^\s)]+)\)", source.read_text()):
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            destination = (source.parent / unquote(parsed.path)).resolve()
            if not destination.is_relative_to(root.resolve()):
                raise ValueError(f"{source}: link escapes package: {target}")
            if not destination.exists():
                raise ValueError(f"{source}: missing link: {target}")


def main() -> None:
    assert (SKILL / "LICENSE.txt").read_bytes() == (ROOT / "LICENSE").read_bytes()
    assert "MIT License" in (SKILL / "LICENSE.txt").read_text()
    for path in SKILL.rglob("*"):
        if path.is_symlink():
            raise ValueError(f"Installation must be self-contained: {path}")
        if path.is_file() and path.suffix not in {".md", ".txt"}:
            raise ValueError(f"Unexpected file in instruction-only package: {path}")
    check_links(ROOT / "skills")
    # Verify the actual copy installation documented in README, without checkout context.
    with tempfile.TemporaryDirectory() as directory:
        installed = Path(directory) / "rust-in-one"
        shutil.copytree(SKILL, installed)
        check_links(installed)
        assert (installed / "SKILL.md").is_file()
        assert (installed / "LICENSE.txt").is_file()
    # README links can also point outside the installable skill, but not outside the repo.
    for target in re.findall(r"\[[^\]]*\]\(([^\s)]+)\)", (ROOT / "README.md").read_text()):
        parsed = urlsplit(target)
        if not parsed.scheme and parsed.path:
            assert (ROOT / unquote(parsed.path)).exists(), target
    print("Package copy, local file links, and MIT notices passed (schema/URL anchors not checked).")


if __name__ == "__main__":
    main()
