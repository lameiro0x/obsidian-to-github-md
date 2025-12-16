# Obsidian to GitHub Markdown Converter

This repository contains a small toolchain designed to convert **Obsidian Markdown vaults** into **GitHub-compatible Markdown**, ensuring that:

- Internal file links work correctly on GitHub
- Header anchors and table-of-contents references are fixed
- Image links are normalized and correctly rendered
- The resulting repository is clean, navigable, and recruiter-friendly

The goal is to make technical notes written in Obsidian fully usable as **public GitHub documentation**, portfolios, or knowledge bases.

---

## Important note for external users

To make this pipeline work in your own repository, you **must adapt the hard-coded folder names** (for example `Penetration Tester Path/Comandos` and `Penetration Tester Path/Academy`) to match **your own directory structure**.

Folder names are not auto-detected and must be updated manually (see instructions below).


---

## How to adapt folder names to your own repository

**File to edit:** `fix_links.py`

You must update the folder name checks in **three places**.

### 1. Indexing logic

Locate and modify these conditions:

```python
if "/Penetration Tester Path/Comandos/" in p_str or "/Comandos/" in p_str:
elif "/Penetration Tester Path/Academy/" in p_str or "/Academy/" in p_str:
```

Replace them with your own folder names  
(e.g. `/Notes/Commands/`, `/Notes/Theory/`).

---

### 2. Folder detection helpers

Update the same paths inside:

```python
def is_in_academy(...)
def is_in_comandos(...)
```

The same folder names **must be used consistently**.

---

### Important

The priority rule (**Commands → Academy → others**) depends entirely on these folder name checks.  
If you rename folders without updating all occurrences, link resolution will be incorrect.

---

## Expected repository structure (example)

```
.
├── images/
├── Penetration Tester Path/
│   ├── Comandos/
│   └── Academy/
├── conversion
├── rename.sh
├── images_md.sh
├── fix_anchor.py
└── fix_links.py
```

This pipeline is intentionally opinionated and optimized for pentesting knowledge bases.

---

## Script overview

### rename.sh

Renames all image files inside the `images/` directory to a GitHub-safe format:
- Lowercase
- Underscores instead of spaces or hyphens
- No special characters

Every rename operation is recorded in `cambios.txt`, which is later used to update image references in Markdown files.

This script assumes **all images are stored under `images/`**.

---

### images_md.sh

Scans **all Markdown files** and normalizes image links by:
- Converting Obsidian image syntax (`![[image.png]]`) to standard Markdown
- Fixing broken image syntaxes
- Updating filenames according to `cambios.txt`

The script assumes that all images are referenced from the `images/` directory and generates GitHub-compatible paths (`/images/...`).

---

### fix_anchor.py

Regenerates Markdown indexes automatically for all `.md` files under the script’s base directory.

It works by:
- Removing any existing index section
- Parsing valid Markdown headings
- Generating a clean index with GitHub-compatible anchors
- Ignoring headings inside code blocks

This guarantees that all internal anchors behave exactly as GitHub expects.

---

### fix_links.py

Converts Obsidian-style wikilinks (`[[note]]`, `[[note#section]]`) into absolute, GitHub-compatible Markdown links.

This script is **tailored to a pentesting repository structure** and applies special resolution rules based on specific folder names:

- `Penetration Tester Path/Comandos`
- `Penetration Tester Path/Academy`

When a note exists in multiple locations, the enforced priority is:

**Comandos → Academy → others**

This ensures that operational pentesting command notes take precedence over academy or general material.

All generated links:
- Are absolute paths from the repository root
- Use anchors normalized to match GitHub’s exact behavior
- Preserve visible text if a target file cannot be resolved

---

### conversion

This is the orchestrator script.

It executes all scripts in the correct order:
1. Rename images
2. Normalize image links in Markdown
3. Regenerate indexes and anchors
4. Fix links between Markdown files

The script stops immediately if any step fails, ensuring consistency.

---

## Requirements

- Linux or macOS
- Bash
- Python 3.x

---

## Usage

1. **Clone or download the repository**
   ```bash
   git clone https://github.com/yourusername/obsidian-to-github-md.git
   ```

2. **Place the scripts in your Obsidian vault or notes directory**

3. **Adapt your notes structure or  the scritps, as it is mentioned in this README**

3. **Give execution permissions**
   ```bash
   chmod +x conversion.sh rename.sh images_md.sh
   ```

4. **Run the conversion**
   ```bash
   ./conversion.sh
   ```

After execution, the Markdown files will be GitHub-compatible and ready to be pushed to a public repository.

---

## Known limitations / pending improvements

- In some cases, `fix_anchor.py` may produce incorrect anchors when generating indexes for headers that contain `/` characters.
- GitHub replaces certain symbols with hyphens when computing anchors, and edge cases involving `/` may lead to duplicated or malformed hyphens.
- This behavior is known and documented; improving anchor normalization for these cases is a pending enhancement.

---

## Use cases

- Publishing cybersecurity notes as a public knowledge base
- Creating recruiter-facing technical documentation
- Maintaining clean Markdown repositories without manual fixes
- Automating documentation pipelines

---

## Notes

- The scripts are intentionally simple and readable.
- Each step is isolated to allow customization or extension.
- Designed for reproducibility and transparency.

