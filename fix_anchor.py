import os
import re

# Root folder: the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def slugify(text):
    """
    Generate anchors:
    - lowercase
    - keeps ñ and accents
    - removes dots
    - symbols → spaces
    - spaces → hyphens
    - NORMALIZES hyphens (--- → --)
    """
    text = text.lower()

    # GitHub removes dots
    text = text.replace(".", "")

    # Anything that is NOT a Unicode letter, number, space, _ or - → space
    text = re.sub(r"[^\w\s\-ñáéíóúü]", " ", text, flags=re.UNICODE)

    # Spaces → hyphens
    text = re.sub(r"\s+", "-", text)

    # Normalize hyphens: 3 or more → exactly 2
    text = re.sub(r"-{3,}", "--", text)

    return text.strip("-")


def is_indice_heading(line):
    m = re.match(r"^\s*#{1,6}\s+(.*)$", line)
    if not m:
        return False
    return m.group(1).strip().lower() == "indice"


def is_valid_heading(title):
    if title.startswith(("/", "<")):
        return False
    if len(title) > 80:
        return False
    return True


def remove_old_index(lines):
    new_lines = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        if is_indice_heading(line):
            i += 1
            while i < n and (
                lines[i].strip() == "" or re.match(r"^\s*[-*]\s+", lines[i])
            ):
                i += 1
            continue
        new_lines.append(line)
        i += 1

    return new_lines


def build_index(lines):
    headings = []
    in_code_block = False

    for line in lines:
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue

        if in_code_block:
            continue

        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if not m:
            continue

        hashes, title = m.groups()
        title = title.strip()

        if is_indice_heading(line):
            continue

        if not is_valid_heading(title):
            continue

        level = len(hashes)
        anchor = slugify(title)
        headings.append((level, title, anchor))

    if not headings:
        return ""

    out = ["# Indice", ""]
    for level, title, anchor in headings:
        indent = "    " * (level - 1)
        out.append(f"{indent}- [{title}](#{anchor})")
    out.append("")
    return "\n".join(out)


def process_md(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    lines_no_index = remove_old_index(lines)
    index_block = build_index(lines_no_index)

    if not index_block:
        return

    new_content = index_block + "\n" + "\n".join(lines_no_index) + "\n"

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"[OK] Index regenerated in {path}")


if __name__ == "__main__":
    for root, _, files in os.walk(BASE_DIR):
        for filename in files:
            if filename.endswith(".md"):
                process_md(os.path.join(root, filename))
