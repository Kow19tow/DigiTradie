#!/bin/bash
# Renders posts that use the shared base (social/_shared) into their exports/ folder.
# Usage:  bash social/render.sh <post-folder> [<post-folder> ...]     e.g.  bash social/render.sh ai-do-dont
#         bash social/render.sh all                                    (every folder with source/post.html except the original case study)
set -e
cd "$(dirname "$0")"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

render () {  # folder layout width height
  local out="$1/exports"; mkdir -p "$out"
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 \
    --window-size="$3,$4" --virtual-time-budget=12000 \
    --screenshot="$out/$2@2x.png" "file://$PWD/$1/source/post.html#$2" >/dev/null 2>&1
  python3 -c "
from PIL import Image
im=Image.open('$out/$2@2x.png'); im.resize(($3,$4),Image.LANCZOS).save('$out/$2.png')"
  echo "  $1: $2 ($3x$4)"
}

targets=("$@")
if [ "${targets[0]}" = "all" ]; then
  targets=(); for d in */; do d="${d%/}"; [ "$d" != "_shared" ] && [ "$d" != "renovation-case-study" ] && [ -f "$d/source/post.html" ] && targets+=("$d"); done
fi
for t in "${targets[@]}"; do
  render "$t" portrait 1080 1350
  render "$t" square 1080 1080
  render "$t" landscape 1200 630
done
