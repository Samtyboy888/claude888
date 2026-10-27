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

## Assumptions to confirm (not in the brief)

- **Locking mechanism.** Nothing in the brief says how the width setting
  is held once extended — no pin, cam lock, or detent implied. Without
  one, a seated/leaned-on load can push the frame to slide. This needs an
  answer before the stretcher cross-section is finalized.
- **Wire panel vertical offset.** For two flat wire panels to telescope
  past each other without snagging, they need to ride on slightly
  different planes (a few mm apart) within the deck's overall thickness —
  not specified yet.
- **Leg mounting.** 3" screw-in legs — standard threaded insert assumed,
  exact thread/size and mounting points (rail ends vs. stretcher ends) not
  specified.
- **Corrosion protection** on the welded wire grid (zinc/powder coat) —
  not specified; matters if this is for outdoor/patio use.
