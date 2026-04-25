#!/usr/bin/env python3
"""Compare two FCStd files: feature trees, dimensions, topology similarity.

Usage:
    python3 compare_fcstd.py original.FCStd reproduction.FCStd
"""
import sys
from collections import Counter
from parse_fcstd import parse_fcstd


def compare(a_path, b_path):
    a = parse_fcstd(a_path)
    b = parse_fcstd(b_path)

    print(f"=== A: {a_path} ===")
    print(f"  {len(a['objects'])} objects, {a['dims_count']} dims")
    print(f"=== B: {b_path} ===")
    print(f"  {len(b['objects'])} objects, {b['dims_count']} dims")
    print()

    # Type counts diff
    a_tc = Counter(a["type_counts"])
    b_tc = Counter(b["type_counts"])
    print("Feature type counts (A | B | Δ):")
    keys = sorted(set(a_tc) | set(b_tc))
    for k in keys:
        av, bv = a_tc.get(k, 0), b_tc.get(k, 0)
        marker = "" if av == bv else ("  ⬆" if bv > av else "  ⬇")
        if av or bv:
            print(f"  {k:35s} {av:4d} | {bv:4d} | {bv-av:+d}{marker}")

    # Feature sequences
    a_seq = [(o["type"].split("::")[-1], o["name"])
             for o in a["objects"]
             if o["type"].startswith("PartDesign::") and o["type"] != "PartDesign::Body"]
    b_seq = [(o["type"].split("::")[-1], o["name"])
             for o in b["objects"]
             if o["type"].startswith("PartDesign::") and o["type"] != "PartDesign::Body"]
    print(f"\nFeature sequence:")
    print(f"  A: {[t for t, _ in a_seq]}")
    print(f"  B: {[t for t, _ in b_seq]}")

    # Similarity score (feature type bag-of-words)
    a_types = Counter(t for t, _ in a_seq)
    b_types = Counter(t for t, _ in b_seq)
    inter = sum((a_types & b_types).values())
    union = sum((a_types | b_types).values())
    jaccard = inter / union if union else 0
    print(f"\nType similarity (Jaccard on multiset): {jaccard:.2%}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    compare(sys.argv[1], sys.argv[2])
