# Expandable Wire-Deck Base

A B2B component sold to foam sofa manufacturers, not an aftermarket retail
product. A legless floor-sofa module sits low by design — raising it to
standard American seat height (~17-19") the obvious way, by molding taller
foam, costs more foam *and* loses the low, grounded profile that's the
point of that style. This base adds the height from underneath instead,
so the foam body stays unchanged: fixed 30" depth, plastic frame (two
fixed-length side rails + three telescoping stretchers — front, center,
back), topped with a welded steel wire grid deck (4.0mm wire, 50mm pitch)
in two overlapping panels that slide past each other as the frame widens.
3" screw-in legs. No integrated foam — bare structural deck.

Same mechanism, two sizes: a **chair/loveseat module**, width adjustable
24"-36" (12" of travel, 4 legs), and a **full sofa**, width adjustable
82"-90" (8" of travel, 6 legs — the longer span needs 2 mid-span legs on
top of the 4 corners). See "Two sizes: chair and sofa" below.

Sales model: sold to the sofa manufacturer, who passes the cost through to
their own customer as a line-item add-on rather than marking it up the way
they would the sofa itself.

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

## Isometric illustration

No photorealistic rendering available in this session — `isometric_view.py`
generates a 2:1 isometric exploded-view SVG instead (line-art technical
illustration, embedded in the design brief artifact). Not a CAD export.

```
python3 isometric_view.py > isometric_view.svg.inc
```

Prints inner SVG markup (no outer `<svg>` tag) sized to the drawing's
bounding box, reported on stderr, for pasting into a `viewBox`.

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

## Cost estimate at scale

`cost_calc.py` builds a bottom-up landed-cost estimate from public
vendor-blog/marketplace pricing (not real quotes — see sources below):

| Volume | Recurring/unit | Tooling/unit | Landed cost/unit | Rule-of-thumb MSRP (3x) |
|---|---|---|---|---|
| 1,000 | $32.43 | $18.00 | **$50.43** | $151 |
| 10,000 | $29.84 | $1.80 | **$31.64** | $95 |
| 100,000 | $27.57 | $0.18 | **$27.75** | $83 |

Tooling ($18,000: 3 extrusion dies @ ~$2,000 + a shared injection mold for
both corner-bracket variants @ ~$12,000) drives the scale curve, not the
recurring BOM — the BOM barely moves beyond a modest bulk-procurement
discount. Run `python3 cost_calc.py` for the full line-item breakdown.

**This is a rough order of magnitude, not a quote.** Get real numbers from
an extruder, a molder, and a wire-mesh supplier before budgeting against
it.

### Two sizes: chair and sofa

Same mechanism, same 30" depth, same shared tooling (3 extrusion dies +
the corner-bracket mold) — only the width range and leg count differ:

| | Chair | Sofa |
|---|---|---|
| Width | 24"-36" | 82"-90" |
| Legs | 4 (corners only) | 6 (4 corners + 2 mid-span) |
| Stretcher mass | ~1.5kg | ~3.63kg |
| Wire deck mass | ~2.94kg | ~7.12kg |
| New tooling vs. the other variant | — (baseline) | ~$4,000 (mid-span leg bracket mold) |

**Why the sofa needs mid-span legs:** the chair's 3 stretchers (front,
center, back) span only 24"-36", short enough for 4 corner legs alone. At
82"-90" that span is too long to leave unsupported in the middle. Since
nothing can sit at a single fixed world-position across both telescoping
halves at once, each half gets its own mid-span leg, on a small bracket
bonded to the center stretcher — no rail junction needed, unlike the
corner brackets.

**Why sofa tooling is mostly shared:** an extrusion die produces a
constant cross-section cut to any length, so the same 3 dies work for
both variants. The corner bracket design doesn't change with sofa width
either. Only the new mid-span leg bracket needs its own mold.

### Wholesale price, B2B sale

This is a component sale to sofa manufacturers, not a retail product —
no retail multiple applies. At a 30% OEM margin (judgment default,
`--oem-margin-pct` in `cost_calc.py`), with chair tooling already in place:

| Variant | Landed cost, 1k units | Landed cost, 10k units | Wholesale, 10k (30%) |
|---|---|---|---|
| Chair (own tooling) | $48.10 | $29.50 | $38.14 |
| Sofa (own tooling) | $73.58 | $49.65 | $64.55 |
| Sofa (chair tooling exists) | $55.58 | $47.85 | $62.21 |

The manufacturer is expected to pass this through to their own customer
close to as-is, as a line-item add-on, not mark it up the way they would
the sofa itself. Run `python3 cost_calc.py --variant chair` or
`--variant sofa` for the full per-line breakdown, or `--variant both`
(default) for the side-by-side.

### Foam savings — doesn't close the gap yet, for either size

The real pitch: this base replaces ~4" of structural foam height (legs 3"
+ frame ~0.47" + wire-panel offset ~0.79") with cheap plastic/wire/leg
structure, so the manufacturer never molds that extra foam.

- **Chair** (30"x30" footprint): 2.08 ft³ avoided.
- **Sofa** (30"x86" footprint): 5.97 ft³ avoided.

**No real bulk/OEM foam price was found** — web search turned up only a
single retail sheet-foam listing (~$12/ft³) and density specs, no
wholesale number. At an unsourced $4.50/ft³ placeholder:

| Variant | Foam saved | vs. wholesale price (10k) |
|---|---|---|
| Chair | ~$9.38 | $38.14 — well short |
| Sofa | ~$26.88 | $62.21 — closer proportionally, still short |

Run `python3 cost_calc.py --foam-cost-per-ft3 <real number>` once you have
a real quote. Until then, lead with raise + style; foam savings is not yet
a standalone justification for the price on either size.

### Cost sources (web search, late Oct 2026 — vendor blogs/marketplaces, not price surveys)

- PP resin ~$1.00-1.20/kg bulk: [Expert Market Research](https://www.expertmarketresearch.com/price-forecast/polypropylene-price-trends), [IMARC](https://www.imarcgroup.com/polypropylene-pricing-report), [Intratec](https://www.intratec.us/chemical-markets/polypropylene-price)
- Welded wire mesh, 4mm wire: [~4.0kg/m² weight figure, Alibaba](https://www.alibaba.com/product-introduction/Welded-Wire-Mesh-Weight-Per-Square_60794829193.html); per-kg price only found as single-seller India listings (~$0.65-0.70/kg equivalent) — thin data, flagged
- Small injection mold tooling: single-cavity bracket mold $5,000-$12,000 — [TeamRapidTooling](https://www.teamrapidtooling.com/blog/wp-json/wp/v2/posts/2397), [Formlabs](https://formlabs.com/blog/injection-molding-cost/), [ABIS Mould](https://www.abismould.com/info/breaking-down-injection-mold-costs-103163410.html)
- Screw-in/metal furniture legs: $0.37-$1.50/pc bulk — [Accio B2B aggregator](https://www.accio.com/biz-cheap/supply-cheap-y-shape-sofa-leg); leveling feet retail ~$0.86/ea — eBay listing
- Plastic extrusion die: simple structural profile $500-$3,000 — [DFMA](https://www.dfma.com/resources/plastic-extrusion-cost.asp), [Lakeland Plastics](https://lakelandplastics.com/plastic-extrusion-cost-factors/)

## To validate before tooling

- **Detent pin wear** — prototype the hole + steel bushing and cycle it;
  repeated engagement is more likely to loosen the lock over the
  product's life than the pin itself.
- **Ledge height vs. final stretcher profile** — the ~20mm offset is
  estimated from a typical 8mm welded-node thickness; confirm against
  the actual wire vendor's spec once sourced.
- **Corrosion protection** on the welded wire grid (zinc/powder coat) —
  not specified; matters if this is for outdoor/patio use.
