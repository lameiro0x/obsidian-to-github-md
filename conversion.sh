#!/bin/bash
set -e

echo "[STEP 1] Renombrando imágenes..."
bash rename.sh

echo "[STEP 2] Normalizando imágenes en Markdown..."
bash images_md.sh

echo "[STEP 3] Corrigiendo índices y anchors..."
python3 fix_anchor.py

echo "[STEP 4] Corrigiendo enlaces entre archivos..."
python3 fix_links.py

echo "[OK] Todo ejecutado correctamente en el orden correcto"
