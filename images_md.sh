#!/bin/bash

IMAGE_DIR="images"
CHANGES="cambios.txt"

echo "[INFO] Normalizing images for GitHub..."

# 1. Convert Obsidian syntax and broken syntax
find . -type f -name "*.md" | while read -r md; do

    # ![[image.png]]
    perl -pi -e 's|!\[\[([^]]+\.png)\]\]|![\1](/images/\1)|gi' "$md"
    perl -pi -e 's|!\[\[([^]]+\.jpg)\]\]|![\1](/images/\1)|gi' "$md"
    perl -pi -e 's|!\[\[([^]]+\.jpeg)\]\]|![\1](/images/\1)|gi' "$md"
    perl -pi -e 's|!\[\[([^]]+\.gif)\]\]|![\1](/images/\1)|gi' "$md"

    # ![[images/image.png]]
    perl -pi -e 's|!\[\[images/([^]]+)\]\]|![\1](/images/\1)|gi' "$md"

    # ![alt]/images/image.png (broken syntax)
    perl -pi -e 's|!\[[^]]*\]/images/([^ )]+)|![\1](/images/\1)|gi' "$md"

done

echo "[INFO] Syntax fixed"

# 2. Apply renames from cambios.txt
if [[ -f "$CHANGES" ]]; then
    while IFS="|" read -r old new; do
        [[ -z "$old" || "$old" == "$new" ]] && continue

        find . -type f -name "*.md" | while read -r md; do
            perl -pi -e "s|/images/$old|/images/$new|g" "$md"
            perl -pi -e "s|$old|$new|g" "$md"
        done
    done < "$CHANGES"
fi

echo "[OK] All images are correct for GitHub"
