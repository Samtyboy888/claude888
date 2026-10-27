#!/usr/bin/env python3
"""Generates an isometric exploded-view SVG of the wire-deck base assembly.

Not a CAD export -- a technical illustration for the design brief, drawn as
simple axis-aligned boxes in a 2:1 isometric projection (the standard
projection used for pixel-art / technical isometric diagrams).

Layer order, bottom to top (an exploded view, each layer separated along
the vertical axis to show how the assembly stacks):
    legs  ->  frame (side rails + stretchers + corner brackets)  ->
    wire panel A  ->  wire panel B

The panel-A/panel-B vertical separation mirrors the stepped-ledge offset
proposed in README.md -- this drawing shows it directly.

Usage: python3 isometric_view.py > isometric_view.svg.inc
Prints the inner SVG markup (no outer <svg> tag) so it can be pasted into
an existing <svg viewBox="..."> wrapper.
"""

import math

COS30 = math.cos(math.radians(30))
SIN30 = math.sin(math.radians(30))


def proj(x, y, z):
    sx = (x - y) * COS30
    sy = (x + y) * SIN30 - z
    return sx, sy


def pts(*coords):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in coords)


def box_svg(box, top_fill, x_fill, y_fill, stroke="var(--line)", sw=1.0, group_class=""):
    """box = (x0,x1,y0,y1,z0,z1). Draws the 3 camera-visible faces."""
    x0, x1, y0, y1, z0, z1 = box
    top = [proj(x0, y0, z1), proj(x1, y0, z1), proj(x1, y1, z1), proj(x0, y1, z1)]
    face_x = [proj(x0, y0, z0), proj(x0, y1, z0), proj(x0, y1, z1), proj(x0, y0, z1)]
    face_y = [proj(x0, y0, z0), proj(x1, y0, z0), proj(x1, y0, z1), proj(x0, y0, z1)]
    g = [f'<g class="{group_class}">'] if group_class else []
    g.append(f'<polygon points="{pts(*face_x)}" fill="{x_fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    g.append(f'<polygon points="{pts(*face_y)}" fill="{y_fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    g.append(f'<polygon points="{pts(*top)}" fill="{top_fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    if group_class:
        g.append("</g>")
    return "\n".join(g)


def explode_line(x, y, z_from, z_to):
    p0 = proj(x, y, z_from)
    p1 = proj(x, y, z_to)
    return (f'<line x1="{p0[0]:.1f}" y1="{p0[1]:.1f}" x2="{p1[0]:.1f}" y2="{p1[1]:.1f}" '
            f'stroke="var(--rule)" stroke-width="0.6" stroke-dasharray="2 2"/>')


# ---------------------------------------------------------------------------
# Scene (illustrative units, not to spec -- WIDTH shown mid-travel)
# ---------------------------------------------------------------------------
WIDTH = 320
DEPTH = 300
T = 24  # rail/stretcher cross-section + frame height

FRAME_Z = (0, T)
LEG_Z = (-90, -20)
FOOT_Z = (-96, -90)
PANEL_A_Z = (50, 58)
PANEL_B_Z = (66, 74)

frame_parts = [
    (0, T, 0, DEPTH, *FRAME_Z),                      # side rail, left
    (WIDTH - T, WIDTH, 0, DEPTH, *FRAME_Z),           # side rail, right
    (T, WIDTH - T, 0, T, *FRAME_Z),                   # stretcher, front
    (T, WIDTH - T, DEPTH - T, DEPTH, *FRAME_Z),       # stretcher, back
    (T, WIDTH - T, DEPTH / 2 - 12, DEPTH / 2 + 12, *FRAME_Z),  # stretcher, center
]

corner_centers = [(0, 0), (0, DEPTH), (WIDTH, 0), (WIDTH, DEPTH)]
brackets = [(cx - 16, cx + 16, cy - 16, cy + 16, *FRAME_Z) for cx, cy in corner_centers]
legs = [(cx - 7, cx + 7, cy - 7, cy + 7, *LEG_Z) for cx, cy in corner_centers]
feet = [(cx - 11, cx + 11, cy - 11, cy + 11, *FOOT_Z) for cx, cy in corner_centers]

panel_a = (8, WIDTH - 40, 10, DEPTH - 10, *PANEL_A_Z)
panel_b = (40, WIDTH - 8, 10, DEPTH - 10, *PANEL_B_Z)


def grid_lines(box, n=5):
    x0, x1, y0, y1, z0, z1 = box
    out = []
    for i in range(1, n):
        x = x0 + (x1 - x0) * i / n
        p0, p1 = proj(x, y0, z1), proj(x, y1, z1)
        out.append(f'<line x1="{p0[0]:.1f}" y1="{p0[1]:.1f}" x2="{p1[0]:.1f}" y2="{p1[1]:.1f}" '
                    f'stroke="var(--line)" stroke-width="0.4" opacity="0.5"/>')
    for i in range(1, n):
        y = y0 + (y1 - y0) * i / n
        p0, p1 = proj(x0, y, z1), proj(x1, y, z1)
        out.append(f'<line x1="{p0[0]:.1f}" y1="{p0[1]:.1f}" x2="{p1[0]:.1f}" y2="{p1[1]:.1f}" '
                    f'stroke="var(--line)" stroke-width="0.4" opacity="0.5"/>')
    return "\n".join(out)


def main():
    out = []

    # explosion alignment lines, drawn first (behind the solids)
    for cx, cy in corner_centers:
        out.append(explode_line(cx, cy, FOOT_Z[1], FRAME_Z[0]))
        out.append(explode_line(cx, cy, FRAME_Z[1], PANEL_A_Z[0]))
        out.append(explode_line(cx, cy, PANEL_A_Z[1], PANEL_B_Z[0]))

    out.append('<g id="feet">')
    for f in feet:
        out.append(box_svg(f, "var(--hatch)", "var(--line)", "var(--line)", sw=0.8))
    out.append("</g>")

    out.append('<g id="legs">')
    for l in legs:
        out.append(box_svg(l, "var(--hatch)", "var(--hatch)", "var(--hatch)", sw=0.8))
    out.append("</g>")

    out.append('<g id="frame">')
    for p in frame_parts:
        out.append(box_svg(p, "var(--paper)", "var(--hatch)", "var(--hatch)", sw=1))
    out.append("</g>")

    out.append('<g id="brackets">')
    for b in brackets:
        out.append(box_svg(b, "var(--accent-soft)", "var(--accent-soft)", "var(--accent-soft)", stroke="var(--accent)", sw=1))
    out.append("</g>")

    out.append('<g id="panel-a">')
    out.append(box_svg(panel_a, "var(--paper)", "var(--accent-soft)", "var(--accent-soft)", stroke="var(--accent)", sw=1))
    out.append(grid_lines(panel_a))
    out.append("</g>")

    out.append('<g id="panel-b">')
    out.append(box_svg(panel_b, "var(--paper)", "var(--accent-soft)", "var(--accent-soft)", stroke="var(--accent)", sw=1))
    out.append(grid_lines(panel_b))
    out.append("</g>")

    print("\n".join(out))

    # report the drawing's screen-space bounding box, for sizing the viewBox
    all_boxes = frame_parts + brackets + legs + feet + [panel_a, panel_b]
    xs, ys = [], []
    for x0, x1, y0, y1, z0, z1 in all_boxes:
        for x in (x0, x1):
            for y in (y0, y1):
                for z in (z0, z1):
                    sx, sy = proj(x, y, z)
                    xs.append(sx)
                    ys.append(sy)
    import sys
    print(f"<!-- bbox: x [{min(xs):.1f}, {max(xs):.1f}]  y [{min(ys):.1f}, {max(ys):.1f}] -->",
          file=sys.stderr)


if __name__ == "__main__":
    main()
