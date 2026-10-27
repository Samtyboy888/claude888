#!/usr/bin/env python3
"""Parametric generator for wire-deck-base prototype parts (binary STL, mm).

Produces printable test coupons for the four highest-risk mechanical
features flagged in README.md's "Durability assurance" punch list --
this is for physically testing fit and mechanism, not a finished
production part (the real parts would be extruded/molded, with features
like the pin spring housing and insert threading added at assembly, not
printed).

Parts:
  rail(length)              straight bar -- fits the corner bracket's
                             rail-arm trough. Represents the side rail.
  sleeve(length)             U-channel tube, stretcher OUTER half --
                             receives tube() in a sliding fit.
  tube(length)               solid bar, stretcher INNER half -- slides
                             inside sleeve(); drill pin-lock holes along it.
  corner_bracket()           L-shaped bracket, rail-arm trough + stretcher-
                             arm trough + a leg boss with an insert hole.
  mid_bracket()              small leg boss on a mounting pad -- sofa
                             variant's mid-span leg, bonds directly to tube().

Print orientation: everything prints flat-bottom, as generated, no flip
needed (unlike the sofa riser's two-sided design).
"""

import argparse
import os
import struct

# ---------------------------------------------------------------------------
# Cross-sections (mm). Simplified vs. the real extrusion profiles in the
# design brief -- solid bars instead of hollow extrusions (an FDM print
# doesn't need to be hollow to test fit; infill handles material use),
# sized to validate clearances and mechanism, not to carry real load.
# ---------------------------------------------------------------------------
RAIL_W, RAIL_H = 25.0, 15.0          # side rail, solid bar
SLEEVE_OUTER_W, SLEEVE_OUTER_H = 32.0, 20.0
SLEEVE_WALL = 3.0
SLEEVE_CAVITY_W = SLEEVE_OUTER_W - 2 * SLEEVE_WALL   # 26.0
SLEEVE_CAVITY_H = SLEEVE_OUTER_H - 2 * SLEEVE_WALL   # 14.0
TUBE_CLEARANCE = 0.6                  # per-side sliding clearance
TUBE_W = SLEEVE_CAVITY_W - 2 * TUBE_CLEARANCE   # 24.8
TUBE_H = SLEEVE_CAVITY_H - 2 * TUBE_CLEARANCE   # 12.8

PIN_HOLE_D = 4.0            # through-hole for the detent pin/bushing test
PIN_PITCH = 50.8            # 2in in mm, matches the named-width lock spacing
PIN_POSITIONS = 5           # print a 5-hole test coupon regardless of variant

CORNER_ARM = 45.0           # each bracket arm's trough length
LEG_BOSS_D = 22.0
LEG_BOSS_H = 12.0
INSERT_HOLE_D = 8.0         # placeholder -- match to the real insert's spec

Box = tuple  # (x0, x1, y0, y1, z0, z1)


# ---------------------------------------------------------------------------
# Box soup -> binary STL (same approach as riser/generate_riser_stl.py --
# no CSG union; each box is independently a valid closed manifold, which
# FDM slicers handle fine even where boxes overlap or abut).
# ---------------------------------------------------------------------------
def box_triangles(box):
    x0, x1, y0, y1, z0, z1 = box
    v = [
        (x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
        (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1),
    ]
    quads = [
        ((0, 1, 2, 3), (0, 0, -1)), ((4, 5, 6, 7), (0, 0, 1)),
        ((0, 1, 5, 4), (0, -1, 0)), ((3, 2, 6, 7), (0, 1, 0)),
        ((0, 3, 7, 4), (-1, 0, 0)), ((1, 2, 6, 5), (1, 0, 0)),
    ]
    tris = []
    for (a, b, c, d), n in quads:
        tris.append((v[a], v[b], v[c], n))
        tris.append((v[a], v[c], v[d], n))
    return tris


def write_stl(path, boxes, name="part"):
    tris = []
    for box in boxes:
        x0, x1, y0, y1, z0, z1 = box
        assert x1 > x0 and y1 > y0 and z1 > z0, f"degenerate box {box}"
        tris.extend(box_triangles(box))
    with open(path, "wb") as f:
        f.write(f"binary STL: {name}".encode("ascii").ljust(80, b"\0")[:80])
        f.write(struct.pack("<I", len(tris)))
        for p0, p1, p2, n in tris:
            f.write(struct.pack("<3f", *n))
            for p in (p0, p1, p2):
                f.write(struct.pack("<3f", *p))
            f.write(struct.pack("<H", 0))
    return len(tris)


def pin_holes_as_gaps(length, start=20.0):
    """Returns the hole center x-positions that fall within [0, length],
    for drilling pin-lock test holes along a tube. Holes aren't subtracted
    from the solid (this generator is additive-only) -- drill them in the
    slicer/CAD after printing, or treat the printed positions as markers."""
    return [start + i * PIN_PITCH for i in range(PIN_POSITIONS)
            if start + i * PIN_PITCH < length - 10.0]


def rail(length):
    return [(0, length, 0, RAIL_W, 0, RAIL_H)]


def sleeve(length):
    """U-channel: base + two side walls, open top, sized to receive tube()."""
    w, h, t = SLEEVE_OUTER_W, SLEEVE_OUTER_H, SLEEVE_WALL
    return [
        (0, length, 0, w, 0, t),            # base
        (0, length, 0, t, t, h),             # left wall
        (0, length, w - t, w, t, h),         # right wall
    ]


def tube(length):
    boxes = [(0, length, 0, TUBE_W, 0, TUBE_H)]
    holes = pin_holes_as_gaps(length)
    print(f"  tube({length}mm): mark/drill {len(holes)} pin holes at x = "
          f"{[round(x, 1) for x in holes]} (not cut in the STL -- additive-only "
          f"generator; drill post-print or add as a CAD cutout)")
    return boxes


def corner_bracket():
    """L bracket: rail-arm trough + stretcher-arm trough, meeting at a
    junction block with a leg boss underneath."""
    jt = 10.0  # junction block thickness/footprint margin
    t = SLEEVE_WALL
    fit = 0.4  # total printable clearance added to each trough's interior

    # Trough OUTER width = the part's width + fit clearance + both walls,
    # so the part's actual cross-section drops into the channel instead of
    # overlapping the walls. (An earlier version of this sized the trough's
    # outer width to the part's width directly, which made the interior
    # narrower than the part -- doesn't fit. Fixed here.)
    rail_trough_w = RAIL_W + fit + 2 * t
    stretcher_trough_w = SLEEVE_OUTER_W + fit + 2 * t
    rh, sh = RAIL_H, SLEEVE_OUTER_H

    junction_w = max(rail_trough_w, stretcher_trough_w) + jt
    boxes = [(0, junction_w, 0, junction_w, 0, t)]  # junction block

    # rail-arm trough (+x direction): base + 2 walls, rail drops in between
    arm0 = junction_w
    boxes += [
        (arm0, arm0 + CORNER_ARM, 0, rail_trough_w, 0, t),                 # base
        (arm0, arm0 + CORNER_ARM, 0, t, t, t + rh),                        # wall
        (arm0, arm0 + CORNER_ARM, rail_trough_w - t, rail_trough_w, t, t + rh),  # wall
    ]
    # stretcher-arm trough (+y direction): base + 2 walls, sleeve drops in
    arm1 = junction_w
    boxes += [
        (0, stretcher_trough_w, arm1, arm1 + CORNER_ARM, 0, t),
        (0, t, arm1, arm1 + CORNER_ARM, t, t + sh),
        (stretcher_trough_w - t, stretcher_trough_w, arm1, arm1 + CORNER_ARM, t, t + sh),
    ]
    # leg boss under the junction block (square, not round -- easier to
    # print without supports, equally valid for a fit test)
    boxes.append((0, LEG_BOSS_D, 0, LEG_BOSS_D, -LEG_BOSS_H, 0))
    print(f"  corner_bracket(): rail trough interior {rail_trough_w - 2*t:.1f}mm "
          f"(rail is {RAIL_W}mm), stretcher trough interior "
          f"{stretcher_trough_w - 2*t:.1f}mm (sleeve is {SLEEVE_OUTER_W}mm)")
    print(f"  corner_bracket(): drill/mark a {INSERT_HOLE_D}mm hole through "
          f"the leg boss center for the insert -- not cut in this STL")
    return boxes


def mid_bracket():
    """Sofa-variant mid-span leg: a mounting pad (bonds to tube()) with a
    leg boss beneath it."""
    pad_w, pad_h = TUBE_W, 30.0
    boxes = [
        (0, pad_w, 0, pad_h, 0, SLEEVE_WALL),  # mounting pad, bonds to tube top
        (0, LEG_BOSS_D, (pad_h - LEG_BOSS_D) / 2, (pad_h + LEG_BOSS_D) / 2,
         -LEG_BOSS_H, 0),
    ]
    return boxes


PARTS = {
    "rail": lambda a: rail(a.length),
    "sleeve": lambda a: sleeve(a.length),
    "tube": lambda a: tube(a.length),
    "corner": lambda a: corner_bracket(),
    "mid": lambda a: mid_bracket(),
}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--part", choices=[*PARTS, "all"], default="all")
    ap.add_argument("--length", type=float, default=260.0,
                     help="test-coupon length in mm for rail/sleeve/tube "
                          "(default 260mm -- long enough to show the pin "
                          "lock pattern, short enough to print quickly)")
    ap.add_argument("--out-dir", default="stl_out")
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    parts = PARTS if args.part == "all" else {args.part: PARTS[args.part]}
    for name, fn in parts.items():
        boxes = fn(args)
        suffix = f"_{int(args.length)}mm" if name in ("rail", "sleeve", "tube") else ""
        out_path = os.path.join(args.out_dir, f"wiredeck_{name}{suffix}.stl")
        n_tris = write_stl(out_path, boxes, name=f"wiredeck_{name}")
        print(f"{out_path}: {len(boxes)} boxes, {n_tris} triangles")


if __name__ == "__main__":
    main()
