#!/usr/bin/env python3
"""Parametric generator for sofa-riser base prototype parts (binary STL, millimeters).

Picks up the "Riser pdf" concept: a perimeter frame assembled from three part
types that snap/glue together with half-lap joints:

  - segment(L)  an extruded-profile channel, cut to any length L, that
                carries the 2.5" foam ring and rides on floor-contact feet.
  - corner()    a 90-degree L bracket joining two segments.
  - tee()       a T bracket joining three segments (for linking adjacent
                sofa/loveseat modules into one continuous riser frame).

Joint rule
----------
Every part edge is either an "A" end or a "B" end of a half-lap splice:
  A end = only the LOWER half-thickness (z: 0..HALF) is present at that tip
  B end = only the UPPER half-thickness (z: HALF..T) is present at that tip
A single straight segment has one A end and one B end. corner() and tee()
have ONLY A ends (at every arm tip), so a segment's B end always faces into
a corner or tee, and a segment's A end always faces another segment's B end
mid-run. Lapped together, the two half-thicknesses sum back to the full
plate thickness T, so the top (foam) and bottom (floor) faces stay flush
across the joint. Glue or solvent-weld the lap; it isn't meant to come apart.

Print / install orientation
----------------------------
Printed as-is, the smooth foam-contact face of the plate sits DOWN on the
print bed (best surface finish where the foam presses against it) and the
feet print pointing UP, unsupported. After printing, FLIP each part over to
install: the plate now faces UP to carry the foam, and the feet point DOWN
to the floor.

This script has no third-party dependencies (stdlib + optional numpy-free
box-to-STL triangulator) so it runs anywhere Python 3 runs.
"""

import argparse
import os
import struct

# ---------------------------------------------------------------------------
# Parameters (millimeters). Defaults match the original "Riser pdf" sketch.
# ---------------------------------------------------------------------------
W = 75.0            # channel width -- matches the foam ring width
H = 12.0            # total part height (plate + feet), as printed
T = 3.0             # plate thickness
LAP = 20.0          # half-lap joint length
HALF = T / 2.0       # half-lap split height
FOOT_L = 30.0        # foot length along a segment
FOOT_GAP = 50.0      # gap between feet
CORNER_ARM = 115.0   # corner bracket arm length (prototype coupon size)
TEE_BAR = 230.0      # tee bracket through-bar length (prototype coupon size)
TEE_STEM = 115.0     # tee bracket stem length
# CORNER_ARM / TEE_STEM must exceed W + LAP (95mm) so each arm/stem has a
# nonzero full-thickness body between the junction and its A-end lap zone.
# The original "Riser pdf" sketch used 80mm here, which is too short for a
# 75mm-wide channel with 20mm laps -- bumped to 115mm.

Box = tuple  # (x0, x1, y0, y1, z0, z1)


def feet_positions(L):
    """Evenly space floor-contact feet along a run of length L, clear of
    the half-lap zones at both ends."""
    lo, hi = LAP + 5.0, L - LAP - 5.0
    usable = hi - lo
    n = max(1, int((usable + FOOT_GAP) // (FOOT_L + FOOT_GAP)))
    span = n * FOOT_L + (n - 1) * FOOT_GAP
    start = lo + (usable - span) / 2.0
    return [
        (start + i * (FOOT_L + FOOT_GAP), start + i * (FOOT_L + FOOT_GAP) + FOOT_L)
        for i in range(n)
    ]


def segment(L):
    """Straight extruded-profile channel, length L. One A end (x=L), one B
    end (x=0)."""
    assert L > 2 * LAP, f"segment length {L} too short for two {LAP}mm laps"
    boxes = [
        (LAP, L - LAP, 0, W, 0, T),       # full-thickness body
        (L - LAP, L, 0, W, 0, HALF),      # A end: lower half only
        (0, LAP, 0, W, HALF, T),          # B end: upper half only
    ]
    for x0, x1 in feet_positions(L):
        boxes.append((x0, x1, 0, W, T, H))
    return boxes


def corner():
    """90-degree L bracket. Arms run +x and +y from the junction at the
    origin. Both arm tips are A ends."""
    a = CORNER_ARM
    boxes = [
        (0, W, 0, W, 0, T),              # junction square, full thickness
        (W, a - LAP, 0, W, 0, T),         # +x arm body
        (a - LAP, a, 0, W, 0, HALF),      # +x arm tip: A end
        (0, W, W, a - LAP, 0, T),         # +y arm body
        (0, W, a - LAP, a, 0, HALF),      # +y arm tip: A end
        (15, 60, 15, 60, T, H),           # floor-contact pad at the junction
    ]
    return boxes


def tee():
    """T bracket: a through-bar (two A ends) with a perpendicular stem
    (one A end), for tying the frame across adjoining sofa modules."""
    bar, stem = TEE_BAR, TEE_STEM
    sx0, sx1 = bar / 2.0 - W / 2.0, bar / 2.0 + W / 2.0
    boxes = [
        (LAP, bar - LAP, 0, W, 0, T),           # bar body
        (0, LAP, 0, W, 0, HALF),                # bar left tip: A end
        (bar - LAP, bar, 0, W, 0, HALF),        # bar right tip: A end
        (sx0, sx1, W, stem - LAP, 0, T),        # stem body
        (sx0, sx1, stem - LAP, stem, 0, HALF),  # stem tip: A end
        (sx0 + 7, sx1 - 7, 15, 60, T, H),        # foot pad near the junction
    ]
    for x0, x1 in [(30, 30 + FOOT_L), (bar - 30 - FOOT_L, bar - 30)]:
        boxes.append((x0, x1, 0, W, T, H))      # feet on the through-bar
    return boxes


# ---------------------------------------------------------------------------
# Box soup -> binary STL. No CSG/boolean union: each box is independently a
# valid closed, outward-facing manifold, which is sufficient for FDM slicing
# even where boxes abut or overlap. Not meant as a CAD-authoritative solid.
# ---------------------------------------------------------------------------
_FACES = [
    # (vertex index tuples, normal) for a unit box, CCW looking from outside
    ((0, 1, 2), (0, 1, 2, 3), (0, 0, -1)),
    ((4, 5, 6), (4, 5, 6, 7), (0, 0, 1)),
    ((0, 1, 5), (0, 1, 5, 4), (0, -1, 0)),
    ((2, 3, 7), (2, 3, 7, 6), (0, 1, 0)),
    ((0, 3, 7), (0, 3, 7, 4), (-1, 0, 0)),
    ((1, 2, 6), (1, 2, 6, 5), (1, 0, 0)),
]


def box_triangles(box):
    x0, x1, y0, y1, z0, z1 = box
    v = [
        (x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
        (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1),
    ]
    tris = []
    quads = [
        ((0, 1, 2, 3), (0, 0, -1)),
        ((4, 5, 6, 7), (0, 0, 1)),
        ((0, 1, 5, 4), (0, -1, 0)),
        ((3, 2, 6, 7), (0, 1, 0)),
        ((0, 3, 7, 4), (-1, 0, 0)),
        ((1, 2, 6, 5), (1, 0, 0)),
    ]
    for (a, b, c, d), n in quads:
        tris.append((v[a], v[b], v[c], n))
        tris.append((v[a], v[c], v[d], n))
    return tris


def write_stl(path, boxes, name="riser_part"):
    tris = []
    for box in boxes:
        x0, x1, y0, y1, z0, z1 = box
        assert x1 > x0 and y1 > y0 and z1 > z0, f"degenerate box {box}"
        tris.extend(box_triangles(box))

    with open(path, "wb") as f:
        header = f"binary STL: {name}".encode("ascii")
        f.write(header.ljust(80, b"\0")[:80])
        f.write(struct.pack("<I", len(tris)))
        for p0, p1, p2, n in tris:
            f.write(struct.pack("<3f", *n))
            for p in (p0, p1, p2):
                f.write(struct.pack("<3f", *p))
            f.write(struct.pack("<H", 0))
    return len(tris)


PARTS = {
    "corner": lambda args: corner(),
    "tee": lambda args: tee(),
    "segment": lambda args: segment(args.length),
}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--part", choices=[*PARTS, "all"], default="all")
    ap.add_argument("--length", type=float, default=400.0,
                     help="segment length in mm (default: 400)")
    ap.add_argument("--out-dir", default="stl_out")
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    parts = PARTS if args.part == "all" else {args.part: PARTS[args.part]}
    for name, fn in parts.items():
        boxes = fn(args)
        suffix = f"_{int(args.length)}mm" if name == "segment" else ""
        out_path = os.path.join(args.out_dir, f"riser_{name}{suffix}.stl")
        n_tris = write_stl(out_path, boxes, name=f"riser_{name}")
        print(f"{out_path}: {len(boxes)} boxes, {n_tris} triangles")


if __name__ == "__main__":
    main()
