# Sofa Riser — base frame prototype

Raises a legless foam modular sofa/loveseat ~2.5–3" off the floor. A 2.5"
(63.5mm) foam ring, wrapped in non-woven fabric with hook-and-loop on top,
sits in a plastic perimeter frame that gives it floor contact and keeps
multiple risers tied together under one sofa section (or across sections,
via the tee piece).

See the design brief (link shared in chat) for the cross-section, joinery,
and manufacturing rationale.

## Generating prototype STL files

```
python3 generate_riser_stl.py --part all --length 400 --out-dir stl_out
```

- `--part {segment,corner,tee,all}` — which part(s) to generate
- `--length` — segment length in mm (segments are cut to length; default 400mm)
- `--out-dir` — output directory for `.stl` files (default `stl_out`)

No third-party dependencies — stdlib only.

### Print orientation

Print each part as generated: plate down, feet up (best surface finish on
the foam-contact face, no supports needed under the feet). **Flip the part
over before installing** — plate up to carry the foam, feet down to the floor.

### Joint assembly

Every part edge is an "A" end (lower half-thickness) or a "B" end (upper
half-thickness). Segments have one of each; corner and tee pieces have only
A ends. Always mate a segment's B end into a corner or tee's A end, and a
segment's A end into the next segment's B end. Glue or solvent-weld the lap
— it's a permanent joint, not a fastener.

### Known deviation from the original sketch

`CORNER_ARM` and `TEE_STEM` were bumped from 80mm to 115mm. At 80mm, with a
75mm-wide channel and 20mm lap zones, the arm body length goes negative
(80 − 20 = 60 < 75mm channel width) — the part is geometrically impossible.
115mm leaves a real full-thickness body between the junction and the lap.
