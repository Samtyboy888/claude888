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

## Assumptions to confirm (not in the brief)

- **Locking mechanism.** Nothing in the brief says how the width setting
  is held once extended — no pin, cam lock, or detent implied. Without
  one, a seated/leaned-on load can push the frame to slide. This needs an
  answer before the stretcher cross-section is finalized.
- **Wire panel vertical offset.** For two flat wire panels to telescope
  past each other without snagging, they need to ride on slightly
  different planes (a few mm apart) within the deck's overall thickness —
  not specified yet.
- **Corrosion protection** on the welded wire grid (zinc/powder coat) —
  not specified; matters if this is for outdoor/patio use.
