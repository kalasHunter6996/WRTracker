#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build a Mir Tankov MTMOD package.

MTMOD is a ZIP container with STORE/no compression entries. The game also
expects client Python mods in compiled Python-2.7 bytecode (.pyc), as in the
reference mod supplied for this project.
"""
from pathlib import Path
from zipfile import ZIP_STORED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
SWF = ROOT / "build" / "kalas.wrtracker.WrTrackerView.swf"
OUT = ROOT / "build" / "WRTracker-0.1.1.mtmod"

if not SWF.is_file():
    raise SystemExit("Missing compiled SWF: %s" % SWF)

pyc_files = sorted((ROOT / "res" / "scripts" / "client").rglob("*.pyc"))
if not pyc_files:
    raise SystemExit("No .pyc files found. The WoT Python modules must be compiled first.")

entries = [
    (ROOT / "meta.xml", "meta.xml"),
    (SWF, "res/gui/flash/kalas.wrtracker.WrTrackerView.swf"),
]

for path in pyc_files:
    entries.append((path, path.relative_to(ROOT).as_posix()))

OUT.parent.mkdir(parents=True, exist_ok=True)
with ZipFile(OUT, "w", compression=ZIP_STORED, allowZip64=False) as zf:
    for source, archive_name in entries:
        zf.write(source, archive_name, compress_type=ZIP_STORED)

# Verify the actual central-directory compression method and package contents
# before publishing the artifact. Every entry must be method 0 (STORE).
with ZipFile(OUT, "r") as zf:
    infos = zf.infolist()
    if not infos:
        raise SystemExit("MTMOD is empty")
    for info in infos:
        if info.compress_type != ZIP_STORED:
            raise SystemExit("Non-STORE entry found: %s (method=%s)" %
                             (info.filename, info.compress_type))
        print("STORE:", info.filename)

print("Created verified STORE-only MTMOD:", OUT)
