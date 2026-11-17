#!/bin/sh
# SPDX-License-Identifier: MPL-2.0
# Copyright (C) 2026 Charles Vestal
# Build AMB-1 with fm1-base (base/, a git submodule).
#   ./build.sh [--release X.Y] [--host | --web]
#   JIELI_TOOLCHAIN  JieLi Linux toolchain (default: ~/.jieli/toolchain)
#   AC79_SDK         JieLi AC79 SDK checkout (default: ~/fw-AC79_AIoT_SDK)
#   PYTHON           a Python with Pillow (and libraqm, for the fonts)
set -e
cd "$(dirname "$0")"
export JIELI_TOOLCHAIN="${JIELI_TOOLCHAIN:-$HOME/.jieli/toolchain}"
export AC79_SDK="${AC79_SDK:-$HOME/fw-AC79_AIoT_SDK}"
PY="${PYTHON:-python3}"
[ -f base/tools/build.py ] || { echo "build.sh: no fm1-base in base/ (git submodule update --init --recursive)"; exit 1; }
"$PY" -c 'import PIL' 2>/dev/null || { echo "build.sh: $PY has no Pillow (pip3 install Pillow)"; exit 1; }
# fm1-base appends the version to id_prefix (FM-1_8 + 0.1.1 -> FM-1_8000101). POND's identity is the prefix alone.
mkdir -p app/build
cp base/tools/build.py app/build/build.py.orig
restore_build() { cp app/build/build.py.orig base/tools/build.py; }
trap restore_build EXIT
"$PY" - << 'PY'
from pathlib import Path
p = Path("base/tools/build.py")
t = p.read_text()
old = [
    'PRODUCT = prefix + "00"',
    'PRODUCT = prefix + "%02d%02d%02d" % (int(m[1]), int(m[2]), int(m[3] or 0))',
]
if any(s not in t for s in old):
    raise SystemExit("build.sh: the identity lines in base/tools/build.py have changed")
for s in old:
    t = t.replace(s, "PRODUCT = prefix", 1)
p.write_text(t)
PY
"$PY" base/tools/build.py app "$@"
