#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Package WRTracker into an MTMOD archive.

MTMOD packages used by Mir Tankov must be ZIP containers with STORE
(no-compression) entries. Using DEFLATE makes the client reject the package
with: "compression not supported".
"""
from pathlib import Path
from zipfile import ZIP_STORED, ZipFile

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

for path in sorted((ROOT / "res" / "scripts" / "client").rglob("*.py")):
    entries.append((path, path.relative_to(ROOT).as_posix()))

OUT.parent.mkdir(parents=True, exist_ok=True)
with ZipFile(OUT, "w", compression=ZIP_STORED) as zf:
    for source, archive_name in entries:
        zf.write(source, archive_name, compress_type=ZIP_STORED)

print("Created:", OUT)
print("Compression: ZIP_STORED (0 / no compression)")
