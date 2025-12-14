#!/bin/bash

IMAGE_DIR="images"
OUT="cambios.txt"

# Vaciar archivo de cambios
echo "" > "$OUT"

echo "[INFO] Renombrando imágenes..."

find "$IMAGE_DIR" -type f | while read img; do
    base=$(basename "$img")
    dir=$(dirname "$img")

    new=$(echo "$base" \
        | tr '[:upper:]' '[:lower:]' \
        | sed 's/ /_/g' \
        | sed 's/-/_/g' \
        | sed 's/[^a-zA-Z0-9._]//g')

    # Guardar en tabla de cambios
    echo "$base|$new" >> "$OUT"

    # Renombrar si es necesario
    if [[ "$base" != "$new" ]]; then
        mv "$img" "$dir/$new"
        echo "[RENAMED] $base → $new"
    fi
done

echo "[INFO] Archivo generado: $OUT"
