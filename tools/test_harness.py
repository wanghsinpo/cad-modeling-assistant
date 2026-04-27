#!/usr/bin/env python3
"""End-to-end test harness.

For each spec in example_specs/, runs:
  1. spec → macro (via generate_macro.py)
  2. macro → FCStd (via freecadcmd)
  3. FCStd → feature tree (via parse_fcstd.py)
  4. Assert expected features are present

Usage:
    python3 test_harness.py
"""
import subprocess
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).parent
FCCMD = "/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd"
OUT = Path("/tmp/cad_test_out")
OUT.mkdir(exist_ok=True)

from parse_fcstd import parse_fcstd

EXPECTATIONS = {
    "simple_flange": {
        "features": ["PartDesign::Pad", "PartDesign::Pocket", "PartDesign::Hole",
                     "PartDesign::PolarPattern", "PartDesign::Fillet"],
        "polar_occurrences": [4],
    },
    "castellated_ring": {
        "features": ["PartDesign::Pad", "PartDesign::Pocket",
                     "PartDesign::PolarPattern", "PartDesign::Hole",
                     "PartDesign::Chamfer"],
        "polar_occurrences": [4, 4],
    },
    "shaft_stepped": {
        "features": ["PartDesign::Revolution", "PartDesign::Chamfer"],
    },
    "ke_bh_072_reproduction": {
        "features": ["PartDesign::Pad", "PartDesign::Pocket",
                     "PartDesign::PolarPattern", "PartDesign::Hole",
                     "PartDesign::Chamfer"],
        "polar_occurrences": [8, 4],
        "has_techdraw": True,
    },
    "ke_bh_072_v2": {
        "features": ["PartDesign::Pad", "PartDesign::Pocket",
                     "PartDesign::PolarPattern", "PartDesign::Hole",
                     "PartDesign::Chamfer"],
        "has_techdraw": True,
    },
    "shaft_with_oring_groove": {
        "features": ["PartDesign::Pad", "PartDesign::Groove", "PartDesign::Chamfer"],
    },
    "bracket_primitives": {
        "features": ["PartDesign::AdditiveBox", "PartDesign::AdditiveCylinder",
                     "PartDesign::SubtractiveCylinder"],
    },
    "plate_with_patterns": {
        "features": ["PartDesign::Pad", "PartDesign::Hole",
                     "PartDesign::LinearPattern", "PartDesign::Mirrored"],
    },
    "hole_test_matrix": {
        "features": ["PartDesign::Pad", "PartDesign::Hole"],
    },
    "funnel_loft": {
        "features": ["PartDesign::AdditiveLoft"],
    },
    "plate_with_slots": {
        "features": ["PartDesign::Pad", "PartDesign::Pocket"],
    },
    "parametric_flange": {
        "features": ["PartDesign::Pad", "PartDesign::Pocket", "PartDesign::Hole",
                     "PartDesign::PolarPattern"],
    },
}


def run(name, spec_path):
    print(f"\n=== {name} ===")
    macro = OUT / f"{name}.py"
    fcstd = OUT / f"{name}.FCStd"

    # Step 1: generate macro
    r = subprocess.run([sys.executable, str(HERE / "generate_macro.py"),
                        str(spec_path), str(macro)], capture_output=True, text=True)
    if r.returncode:
        print(f"  FAIL: macro gen: {r.stderr}")
        return False
    assert macro.exists(), "macro not created"

    # Step 2: run in FreeCAD
    if fcstd.exists():
        fcstd.unlink()
    r = subprocess.run([FCCMD, str(macro)], capture_output=True, text=True, timeout=120)
    # Filter only meaningful errors
    err_lines = [l for l in (r.stdout + r.stderr).split("\n")
                 if ("Error" in l or "Exception" in l or "invalid" in l)
                 and "3Dconnexion" not in l and "dlopen" not in l
                 and "free and open-source" not in l]
    if err_lines:
        print(f"  Errors:")
        for l in err_lines[:5]:
            print(f"    {l}")
    if not fcstd.exists():
        print(f"  FAIL: FCStd not saved")
        return False

    # Step 3: parse
    parsed = parse_fcstd(fcstd)
    if "error" in parsed:
        print(f"  FAIL: parse {parsed['error']}")
        return False

    # Step 4: check
    expect = EXPECTATIONS.get(name, {})
    got_types = [o["type"] for o in parsed["objects"]]
    ok = True
    for want in expect.get("features", []):
        if want not in got_types:
            print(f"  MISSING feature type: {want}")
            ok = False
    if "has_techdraw" in expect:
        has = any("TechDraw" in t for t in got_types)
        if has != expect["has_techdraw"]:
            print(f"  TechDraw expect={expect['has_techdraw']} got={has}")
            ok = False

    # Report feature sequence
    seq = [o["name"] for o in parsed["objects"]
           if o["type"].startswith("PartDesign::") and o["type"] != "PartDesign::Body"]
    print(f"  Features ({len(seq)}): {seq}")
    print(f"  Dims: {parsed.get('dims_count', 0)}")
    print(f"  Type counts:", parsed.get("type_counts", {}))
    print(f"  {'PASS' if ok else 'PARTIAL'}")
    return ok


def main():
    specs_dir = HERE / "example_specs"
    passed = 0
    total = 0
    for spec in sorted(specs_dir.glob("*.json")):
        total += 1
        name = spec.stem
        if run(name, spec):
            passed += 1
    print(f"\n=== {passed}/{total} passed ===")


if __name__ == "__main__":
    main()
