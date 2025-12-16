import re
import unicodedata
from pathlib import Path
import urllib.parse

ROOT = Path(".")

# Index existing .md files, separating Academy and Commands to resolve name collisions
academy_index = {}
comandos_index = {}
other_index = {}

for p in ROOT.rglob("*.md"):
    key = p.stem.lower()
    p_str = p.as_posix()

    if "/Penetration Tester Path/Comandos/" in p_str or "/Comandos/" in p_str:
        comandos_index[key] = p
    elif "/Penetration Tester Path/Academy/" in p_str or "/Academy/" in p_str:
        academy_index[key] = p
    else:
        other_index[key] = p


def slugify_github(text: str) -> str:
    """
    Generate EXACT GitHub anchors:
    - lowercase
    - no accents
    - no symbols
    - spaces -> hyphens
    """
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def is_in_academy(current_path: Path) -> bool:
    s = current_path.as_posix()
    return "/Penetration Tester Path/Academy/" in s or "/Academy/" in s


def is_in_comandos(current_path: Path) -> bool:
    s = current_path.as_posix()
    return "/Penetration Tester Path/Comandos/" in s or "/Comandos/" in s


def find_file(name: str, current_path: Path):
    """
    Resolve a note name (without path) to a real Path.
    Key rule:
      - If the current file is in Academy and a homonym exists in Commands, use Commands.
      - In general, prefer Commands > Academy > others.
    """
    # Ignore old paths, keep only the filename
    key = name.strip().split("/")[-1].replace(".md", "").lower()

    if is_in_academy(current_path):
        # From Academy: prioritize Commands if it exists
        if key in comandos_index:
            return comandos_index[key]
        if key in academy_index:
            return academy_index[key]
        return other_index.get(key)

    if is_in_comandos(current_path):
        # From Commands: keep natural preference for Commands
        if key in comandos_index:
            return comandos_index[key]
        if key in academy_index:
            return academy_index[key]
        return other_index.get(key)

    # From any other location: prefer Commands, then Academy
    if key in comandos_index:
        return comandos_index[key]
    if key in academy_index:
        return academy_index[key]
    return other_index.get(key)


def convert_md(path: Path):
    text = path.read_text(encoding="utf-8")

    pattern = r"\[\[([^\]|#]+)(?:#([^\]|]+))?(?:\|([^\]]+))?\]\]"

    def repl(match):
        full, anchor, alias = match.groups()

        filename = full.split("/")[-1]
        alias = alias or filename

        target = find_file(filename, path)

        if not target:
            # Do not delete content: keep visible text
            return alias

        # Absolute path from repo root (GitHub-friendly)
        rel = "/" + urllib.parse.quote(str(target.relative_to(ROOT)).replace("\\", "/"))

        if anchor:
            fixed_anchor = slugify_github(anchor)
            return f"[{alias}]({rel}#{fixed_anchor})"

        return f"[{alias}]({rel})"

    new_text = re.sub(pattern, repl, text)
    path.write_text(new_text, encoding="utf-8")


for md in ROOT.rglob("*.md"):
    convert_md(md)

print("[OK] Wikilinks successfully converted for GitHub (Commands preferred over Academy)")