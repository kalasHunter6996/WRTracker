#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Package the WRTracker source tree into a .mtmod archive.

The compiled Scaleform SWF must exist at:
  build/kalas.wrtracker.WrTrackerView.swf
"""
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
SWF = ROOT / "build" / "kalas.wrtracker.WrTrackerView.swf"
OUT = ROOT / "build" / "WRTracker-0.1.0.mtmod"

if not SWF.is_file():
    raise SystemExit(
        "Missing compiled SWF: %s\n"
        "Compile as3/src/wrtracker/WrTrackerView.as first." % SWF
    )

entries = [
    (ROOT / "meta.xml", "meta.xml"),
    (SWF, "res/packages/kalas/wrtracker/kalas.wrtracker.WrTrackerView.swf"),
]

# Python files are loaded from res/scripts/client by the game mod loader.
for path in sorted((ROOT / "res" / "scripts" / "client").rglob("*.py")):
    entries.append((path, path.relative_to(ROOT).as_posix()))

OUT.parent.mkdir(parents=True, exist_ok=True)
with ZipFile(OUT, "w", ZIP_DEFLATED) as zf:
    for source, archive_name in entries:
        zf.write(source, archive_name)

print("Created:", OUT)
