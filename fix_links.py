import re
import unicodedata
from pathlib import Path
import urllib.parse

ROOT = Path(".")

# Indexar .md existentes, separando Academy y Comandos para resolver colisiones por nombre
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
    Genera anchors EXACTOS como GitHub:
    - minúsculas
    - sin acentos
    - sin símbolos
    - espacios -> -
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
    Resuelve un nombre de nota (sin ruta) a un Path real.
    Regla clave:
      - Si el archivo actual está en Academy y existe homónimo en Comandos, usar Comandos.
      - En general, preferir Comandos > Academy > otros.
    """
    # Ignorar rutas antiguas, quedarse solo con el nombre
    key = name.strip().split("/")[-1].replace(".md", "").lower()

    if is_in_academy(current_path):
        # Desde Academy: priorizar Comandos si existe
        if key in comandos_index:
            return comandos_index[key]
        if key in academy_index:
            return academy_index[key]
        return other_index.get(key)

    if is_in_comandos(current_path):
        # Desde Comandos: mantener preferencia natural a Comandos
        if key in comandos_index:
            return comandos_index[key]
        if key in academy_index:
            return academy_index[key]
        return other_index.get(key)

    # Desde cualquier otra ubicación: preferir Comandos, luego Academy
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
            # No borrar contenido: dejar texto visible
            return alias

        # Ruta absoluta desde la raíz del repo (GitHub-friendly)
        rel = "/" + urllib.parse.quote(str(target.relative_to(ROOT)).replace("\\", "/"))

        if anchor:
            fixed_anchor = slugify_github(anchor)
            return f"[{alias}]({rel}#{fixed_anchor})"

        return f"[{alias}]({rel})"

    new_text = re.sub(pattern, repl, text)
    path.write_text(new_text, encoding="utf-8")


for md in ROOT.rglob("*.md"):
    convert_md(md)

print("[OK] Wikilinks convertidos correctamente para GitHub (Academy -> Comandos preferido)") 