#!/bin/bash
# Renders every size of the post from post.html using headless Chrome.
# Usage: bash render.sh   (from this folder or anywhere)
set -e
cd "$(dirname "$0")"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT="../exports"
mkdir -p "$OUT"

render () {  # name width height
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 \
    --window-size="$2,$3" --virtual-time-budget=10000 \
    --screenshot="$OUT/$1@2x.png" "file://$PWD/post.html#$1" >/dev/null 2>&1
  python3 -c "
from PIL import Image
im=Image.open('$OUT/$1@2x.png'); im.resize(($2,$3),Image.LANCZOS).save('$OUT/$1.png')"
  echo "rendered $1 ($2x$3)"
}

render portrait  1080 1350
render square    1080 1080
render landscape 1200 630
