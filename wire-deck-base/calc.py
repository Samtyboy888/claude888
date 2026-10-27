#!/usr/bin/env python3
"""Sizing calculator for the expandable wire-deck bench/seat base.

Fixed 30" depth, width adjustable toward 36" via three telescoping plastic
stretchers (front, center, back) sliding between two fixed-length side
rails. Load deck is a welded steel wire grid (4.0mm wire, 50mm pitch) in
two overlapping panels that slide past each other as the frame widens.

Run with no arguments for the default case (36" max width, 24" assumed
min width -- confirm the real minimum before cutting tooling).
"""

import argparse

MM_PER_IN = 25.4


def open_area_pct(wire_d_mm: float, pitch_mm: float) -> float:
    """Open area % for a square welded wire grid: ((pitch - wire_d) / pitch)^2.

    This is the open-area fraction between wire centerlines, not counting
    perspective/weld overlap at crossings -- the standard first-order
    check vendors quote for mesh ventilation/open-area specs.
    """
    if wire_d_mm >= pitch_mm:
        raise ValueError("wire diameter must be smaller than pitch")
    return ((pitch_mm - wire_d_mm) / pitch_mm) ** 2 * 100.0


def panel_sizing(min_width_in: float, max_width_in: float, overlap_margin_mm: float):
    """Minimum wire-panel width (in the adjustable direction) so the two
    panels never gap apart, across the full travel range.

    Panel A is fixed to the left side rail and extends right; panel B is
    fixed to the right (moving) side rail and extends left. At minimum
    width they stack with maximum overlap (fine -- they're flat sheets on
    offset planes); at maximum width they must still overlap by at least
    `overlap_margin_mm` so there's never a structural gap in the deck.

    Simplest workable split: both panels the same width w. Full coverage
    at max width requires 2w >= max_width + overlap_margin, i.e.
        w >= (max_width + overlap_margin) / 2
    """
    max_w_mm = max_width_in * MM_PER_IN
    min_w_mm = min_width_in * MM_PER_IN
    travel_mm = max_w_mm - min_w_mm
    panel_w_mm = (max_w_mm + overlap_margin_mm) / 2.0
    overlap_at_min_mm = 2 * panel_w_mm - min_w_mm
    overlap_at_max_mm = 2 * panel_w_mm - max_w_mm
    return {
        "travel_mm": travel_mm,
        "travel_in": travel_mm / MM_PER_IN,
        "panel_width_mm": panel_w_mm,
        "panel_width_in": panel_w_mm / MM_PER_IN,
        "overlap_at_min_mm": overlap_at_min_mm,
        "overlap_at_max_mm": overlap_at_max_mm,
    }


def stretcher_engagement(min_width_in: float, max_width_in: float,
                          stretcher_nominal_len_in: float, min_engagement_mm: float):
    """How much the inner/outer telescoping stretcher tubes still overlap
    at full extension -- the shear load path that keeps the frame from
    racking. Fails (returns negative margin) if the stretchers aren't long
    enough for the required travel plus a minimum engagement length.
    """
    travel_mm = (max_width_in - min_width_in) * MM_PER_IN
    nominal_mm = stretcher_nominal_len_in * MM_PER_IN
    engagement_at_max_mm = nominal_mm - travel_mm
    margin_mm = engagement_at_max_mm - min_engagement_mm
    return {
        "travel_mm": travel_mm,
        "engagement_at_max_mm": engagement_at_max_mm,
        "margin_mm": margin_mm,
        "ok": margin_mm >= 0,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--wire-d", type=float, default=4.0, help="wire diameter, mm")
    ap.add_argument("--pitch", type=float, default=50.0, help="wire grid pitch, mm")
    ap.add_argument("--min-width-in", type=float, default=24.0,
                     help="assumed minimum width, inches (CONFIRM -- not given in the brief)")
    ap.add_argument("--max-width-in", type=float, default=36.0, help="max width, inches")
    ap.add_argument("--overlap-margin-mm", type=float, default=50.0,
                     help="minimum structural overlap to keep at max extension")
    ap.add_argument("--stretcher-len-in", type=float, default=24.0,
                     help="nominal (closed) length of each telescoping stretcher half, inches")
    ap.add_argument("--min-engagement-mm", type=float, default=40.0,
                     help="minimum tube-in-tube engagement needed to resist racking")
    args = ap.parse_args()

    oa = open_area_pct(args.wire_d, args.pitch)
    print(f"Wire grid open area: {oa:.1f}%  "
          f"(wire {args.wire_d}mm @ {args.pitch}mm pitch; target 85%)")

    sizing = panel_sizing(args.min_width_in, args.max_width_in, args.overlap_margin_mm)
    print(f"\nWidth travel: {sizing['travel_in']:.1f}in ({sizing['travel_mm']:.0f}mm)")
    print(f"Each wire panel needs width >= {sizing['panel_width_in']:.1f}in "
          f"({sizing['panel_width_mm']:.0f}mm)")
    print(f"  overlap at min width: {sizing['overlap_at_min_mm']:.0f}mm")
    print(f"  overlap at max width: {sizing['overlap_at_max_mm']:.0f}mm "
          f"(>= {args.overlap_margin_mm:.0f}mm margin, by construction)")

    eng = stretcher_engagement(args.min_width_in, args.max_width_in,
                                args.stretcher_len_in, args.min_engagement_mm)
    status = "OK" if eng["ok"] else "TOO SHORT"
    print(f"\nStretcher tube engagement at max width: "
          f"{eng['engagement_at_max_mm']:.0f}mm [{status}] "
          f"(margin {eng['margin_mm']:.0f}mm over the {args.min_engagement_mm:.0f}mm minimum)")


if __name__ == "__main__":
    main()
