#!/bin/bash

IMAGE_DIR="images"
OUT="cambios.txt"

# Clear changes file
echo "" > "$OUT"

echo "[INFO] Renaming images..."

find "$IMAGE_DIR" -type f | while read img; do
    base=$(basename "$img")
    dir=$(dirname "$img")

    new=$(echo "$base" \
        | tr '[:upper:]' '[:lower:]' \
        | sed 's/ /_/g' \
        | sed 's/-/_/g' \
        | sed 's/[^a-zA-Z0-9._]//g')

    # Store mapping in changes table
    echo "$base|$new" >> "$OUT"

    # Rename if needed
    if [[ "$base" != "$new" ]]; then
        mv "$img" "$dir/$new"
        echo "[RENAMED] $base → $new"
    fi
done

echo "[INFO] File generated: $OUT"
