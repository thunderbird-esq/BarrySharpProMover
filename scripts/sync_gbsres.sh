#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Sync .gbsres sidecars
#   1. Move *.gbsres from project/ → assets/ (preserve sub-paths)
#   2. Rename sidecars so they end with the full asset name (foo.png.gbsres)
#   3. Stub-generate any missing sidecars for *.png / *.mod assets
# ---------------------------------------------------------------------------
set -euo pipefail

ROOT=$(cd "${1:-.}" && pwd)          # allow optional path arg, default = .
ASSETS="$ROOT/assets"
PROJ="$ROOT/project"

echo "🔄  Syncing .gbsres files in $ROOT"

# ---------------------------------------------------------------------------
# 1. Move sidecars marooned under project/ → assets/
# ---------------------------------------------------------------------------
if [[ -d $PROJ ]]; then
  echo "→ Relocating sidecars from project/ to assets/"
  find "$PROJ" -type f -name '*.gbsres' | while read -r SRC; do
    REL=${SRC#"$PROJ"/}              # strip leading project/
    DEST="$ASSETS/$REL"
    mkdir -p "$(dirname "$DEST")"
    mv "$SRC" "$DEST"
    echo "   moved   ${DEST#$ROOT/}"
  done
fi

# ---------------------------------------------------------------------------
# 2. Rename orphaned sidecars so they match <asset>.<ext>.gbsres
# ---------------------------------------------------------------------------
echo "→ Renaming mis-named sidecars"
find "$ASSETS" -type f -name '*.gbsres' | while read -r SIDE; do
  DIR=$(dirname "$SIDE")
  BASE=$(basename "$SIDE" .gbsres)     # actor_animated (no ext)
  for EXT in png mod; do
    if [[ -f "$DIR/$BASE.$EXT" && ! -f "$DIR/$BASE.$EXT.gbsres" ]]; then
      mv "$SIDE" "$DIR/$BASE.$EXT.gbsres"
      echo "   renamed ${DIR#$ROOT/}/$BASE.$EXT.gbsres"
      break
    fi
  done
done

# ---------------------------------------------------------------------------
# 3. Create stub sidecars for any asset still missing one
# ---------------------------------------------------------------------------
echo "→ Creating missing sidecars"
find "$ASSETS" -type f \( -name '*.png' -o -name '*.mod' \) | while read -r ASSET; do
  SIDE="$ASSET.gbsres"
  [[ -f "$SIDE" ]] && continue
  cat >"$SIDE" <<'JSON'
{
  "checksum": "",
  "width": 0,
  "height": 0,
  "lastImported": 0
}
JSON
  echo "   created ${SIDE#$ROOT/}"
done

echo "✅  gbsres sync complete."

