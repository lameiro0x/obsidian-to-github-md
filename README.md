# Obsidian to GitHub Markdown Converter

This repository contains a small toolchain designed to convert **Obsidian Markdown vaults** into **GitHub-compatible Markdown**, ensuring that:

- Internal file links work correctly on GitHub
- Header anchors and table-of-contents references are fixed
- Image links are normalized and correctly rendered
- The resulting repository is clean, navigable, and recruiter-friendly

The goal is to make technical notes written in Obsidian fully usable as **public GitHub documentation**, portfolios, or knowledge bases.

---

## Why this exists

Obsidian Markdown is optimized for local knowledge management, not for GitHub rendering.  
When publishing notes directly to GitHub, common issues appear:

- Broken links between files
- Incorrect anchors for headers
- Non-standard image paths
- Indexes or references that do not resolve correctly

This toolchain automates the conversion process in a **repeatable and deterministic way**, making it suitable for technical documentation, cybersecurity notes, and learning repositories.

---

## What the toolchain does

The conversion process is executed in a fixed order:

1. **Rename images** to ensure consistent and safe filenames
2. **Normalize image references** inside Markdown files
3. **Fix header anchors and internal indexes**
4. **Fix links between Markdown files**

All steps are orchestrated by a single entrypoint script.

---

## Main script

`conversion.sh` is the main entrypoint and must be executed from the root of the notes directory.

```bash
#!/bin/bash
set -e

echo "[STEP 1] Renaming images..."
bash rename.sh

echo "[STEP 2] Normalizing images in Markdown..."
bash images_md.sh

echo "[STEP 3] Fixing indexes and anchors..."
python3 fix_anchor.py

echo "[STEP 4] Fixing links between files..."
python3 fix_links.py

echo "[OK] All steps executed successfully in the correct order"
```

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

