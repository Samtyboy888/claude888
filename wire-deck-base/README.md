# Expandable Wire-Deck Base

A seating/bench base: fixed 30" depth, width adjustable from 24" to 36"
(12" of travel), plastic frame (two fixed-length side rails + three
telescoping stretchers — front, center, back), topped with a welded steel
wire grid deck (4.0mm wire, 50mm pitch) in two overlapping panels that
slide past each other as the frame widens. 3" screw-in legs. No integrated
foam — bare structural deck.

Separate product from the sofa riser (`../riser/`) — unrelated project,
same repo.

## Why the wire grid

Distributes a seated person's load across the plastic stretcher spans
instead of one point load, which matters because plastic creeps under
sustained load more than metal — spreading the load reduces local stress
and long-term sag. It also gives the required ~85% open area for
ventilation.

## Verified

`calc.py` confirms the 85% open-area target: 4.0mm wire at 50mm pitch
gives **84.6%** open area (`((pitch - wire_d) / pitch)^2`), matching the
brief almost exactly.

```
python3 calc.py
```

Flags: `--wire-d`, `--pitch`, `--min-width-in`, `--max-width-in`,
`--overlap-margin-mm`, `--stretcher-len-in`, `--min-engagement-mm`.

## Confirmed

- **Width range: 24"–36"** (12" of travel). Sets the wire panel width
  (≥19" each, per `calc.py`) and the telescoping stretcher length.

## Leg mounting — corner brackets

Legs mount at the four corners, where a side rail meets a stretcher end,
via a molded corner bracket with an integral leg boss:

- **Fixed corner** (left side, ×2) — bracket bonded to the side rail and
  the stretcher's *outer sleeve*. Doesn't move.
- **Sliding corner** (right side, ×2) — bracket bonded to the side rail
  and the stretcher's *inner tube*. This bracket is the rigid tie point
  that keeps the right rail square to all three stretchers as the frame
  slides — not just a leg mount.
- **Insert**: 3/8"-16 threaded brass, heat-set or molded into each
  bracket's boss — the common spec for screw-in furniture legs. Confirm
  against the actual leg hardware before tooling.
- Front/back corners each carry a leg (4 total). The center stretcher's
  rail junctions are plain T-ties with no leg; add a 5th, center leg only
  if the 36" max-width span needs the extra support.
- The bracket-to-tube bond is permanent (riveted/bonded) — it is *not*
  the telescoping joint. The width-adjustment slide stays free until the
  separate locking mechanism (below) engages.

## Width lock — detent pin (proposed)

Spring-loaded ball-detent pull-pin through the outer sleeve of the front
and back stretchers only — the sliding corner brackets already hold all
three stretchers square to each other, so a third pin on the center
stretcher would be redundant and risks the three not aligning exactly.

- Pin drops into one of 7 holes drilled through the inner tube at 2"
  increments, covering the full 24"-36" range.
- Positive mechanical lock, not friction — won't creep under sustained
  seated load the way a cam or screw clamp can.
- Each hole is a stress riser in a load-bearing plastic tube: spec a
  molded-in steel bushing at every hole (repeated pin engagement will
  ovalize/wear a bare plastic hole), and put the holes on the tube's side
  walls near the bending neutral axis, not the top/bottom faces that see
  peak bending stress.

## Wire panel vertical offset (proposed)

Mold two step-height ledges into each stretcher's top face, running the
width direction: a lower ledge carries panel A, an upper ledge (~12mm
higher) carries panel B directly above it.

- A welded-wire node is roughly 2x the wire diameter thick (~8mm at a
  4.0mm wire crossing) — the step has to clear that plus a couple mm of
  running clearance, not just the 4mm single-wire diameter.
- Stack: ~2mm ledge + 8mm panel A + 2mm clearance + 8mm panel B ≈ 20mm
  total, which adds to the overall deck height on top of the stretcher
  profile — fold this into the seat-height calculation once the
  stretcher cross-section is set.
- Each panel is clipped down only at its fixed edge (the end that
  doesn't move); the overlap zone itself is unfastened, just resting in
  its ledge, free to slide.

## To validate before tooling

- **Detent pin wear** — prototype the hole + steel bushing and cycle it;
  repeated engagement is more likely to loosen the lock over the
  product's life than the pin itself.
- **Ledge height vs. final stretcher profile** — the ~20mm offset is
  estimated from a typical 8mm welded-node thickness; confirm against
  the actual wire vendor's spec once sourced.
- **Corrosion protection** on the welded wire grid (zinc/powder coat) —
  not specified; matters if this is for outdoor/patio use.
