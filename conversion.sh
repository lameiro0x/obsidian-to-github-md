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

echo "[OK] Everything executed successfully in the correct order"
