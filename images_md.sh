#!/bin/bash

IMAGE_DIR="images"
CHANGES="cambios.txt"

echo "[INFO] Normalizando imágenes para GitHub..."

# 1. Convertir sintaxis Obsidian y sintaxis rota
find . -type f -name "*.md" | while read -r md; do

    # ![[imagen.png]]
    perl -pi -e 's|!\[\[([^]]+\.png)\]\]|![\1](/images/\1)|gi' "$md"
    perl -pi -e 's|!\[\[([^]]+\.jpg)\]\]|![\1](/images/\1)|gi' "$md"
    perl -pi -e 's|!\[\[([^]]+\.jpeg)\]\]|![\1](/images/\1)|gi' "$md"
    perl -pi -e 's|!\[\[([^]]+\.gif)\]\]|![\1](/images/\1)|gi' "$md"

    # ![[images/imagen.png]]
    perl -pi -e 's|!\[\[images/([^]]+)\]\]|![\1](/images/\1)|gi' "$md"

    # ![algo]/images/imagen.png   (sintaxis rota)
    perl -pi -e 's|!\[[^]]*\]/images/([^ )]+)|![\1](/images/\1)|gi' "$md"

done

echo "[INFO] Sintaxis corregida"

# 2. Aplicar renombrados de cambios.txt
if [[ -f "$CHANGES" ]]; then
    while IFS="|" read -r old new; do
        [[ -z "$old" || "$old" == "$new" ]] && continue

        find . -type f -name "*.md" | while read -r md; do
            perl -pi -e "s|/images/$old|/images/$new|g" "$md"
            perl -pi -e "s|$old|$new|g" "$md"
        done
    done < "$CHANGES"
fi

echo "[OK] Todas las imágenes están correctas para GitHub"