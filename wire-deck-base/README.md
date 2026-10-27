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
24"-36" (12" of travel, 4 legs), and a **loveseat/sofa**, width adjustable
56"-90" (34" of travel, 6 legs — the longer span needs 2 mid-span legs on
top of the 4 corners; one SKU covers 2-seat loveseats through 3-seat
sofas). See "Two sizes: chair and sofa" below.

Sales model: sold to the sofa manufacturer, who passes the cost through to
their own customer as a line-item add-on rather than marking it up the way
they would the sofa itself. Sourced, made, and sold in China (Xiamen to
Guangdong, ~550km) — materials and tooling are domestic, not imported,
and freight/packaging are factory-to-factory, not export.

Foam retention: a front-stretcher adhesive Velcro strip stops the foam
body sliding forward (the dominant failure direction — people sit down
and push off from the front edge). See "Foam retention" below for the
PP-adhesion caveat.

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

## Foam retention — front Velcro

Nothing stops the foam body from sliding on a bare wire deck. The
dominant failure direction is forward (people sit down and push off from
the front edge), so an adhesive-backed hook Velcro strip along the front
stretcher is the minimum worthwhile fix, mating to a loop strip the
manufacturer applies to the sofa's underside.

**Caveat:** PP is a low-surface-energy plastic — adhesives don't bond to
it reliably long-term. Spec a Velcro product rated for polyolefins, or
mold a shallow mounting slot into the stretcher's top face and
mechanically fasten the strip through it rather than relying on adhesive
alone. If prototype testing shows sideways or backward slip is also a
problem, the same strip and mounting detail extends cheaply to the back
stretcher or the side rails.

## Printable prototype parts

`generate_prototype_stl.py` outputs test coupons for the four highest-risk
mechanical features from "Path to the business-model decision" below —
this is what a physical prototype test actually needs, not a finished
production part. Solid bars instead of hollow extrusions (FDM infill
handles material efficiency; a real production part would be hollow), no
threaded inserts or pin/spring hardware printed in (those are off-the-shelf,
added at assembly).

```
python3 generate_prototype_stl.py --part all --length 260
```

Parts: `rail` (side rail test length), `sleeve` + `tube` (the telescoping
stretcher pair — print both and test the sliding fit and the 0.6mm/side
clearance directly), `corner` (the L-bracket with both troughs and the leg
boss), `mid` (sofa variant's mid-span leg mount). `--length` sets the
rail/sleeve/tube coupon length (default 260mm — long enough to show the
5-hole pin-lock pattern, short enough to print quickly).

This generator caught a real bug before it reached a printer: the first
version sized each bracket trough's *outer* width to the part it was
supposed to receive, which made the trough's *interior* narrower than the
part — neither the rail nor the sleeve would have physically fit. Fixed by
sizing the trough's interior to the part's width plus a 0.4mm printable
clearance, with the walls added outside that.

Pin-lock holes and the insert hole aren't cut into the STL (this generator
only adds material, it doesn't subtract) — the script prints their
intended positions to the console; drill them post-print or treat them as
placement marks for now.

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
vendor-blog/marketplace pricing (not real quotes — see sources below).
Sourced, made, and sold in China (Xiamen to Guangdong, ~550km): resin,
wire mesh, legs, hardware and tooling are all assumed domestic, not
imported; freight and packaging are factory-to-factory, not export.
Resin dropped from a ~$1.10/kg global-blended figure to the ~$0.99/kg
China-specific number found in the same search. Tooling quotes are left
as a conservative high-side placeholder since the only sources found were
Western-facing rapid-tooling platforms, not direct Chinese toolmaker
pricing — a real domestic quote will likely come in lower.

**This is a rough order of magnitude, not a quote.** Get real numbers from
an extruder, a molder, and a wire-mesh supplier before budgeting against
it.

### Two sizes: chair and loveseat/sofa

Same mechanism, same 30" depth, same shared tooling (3 extrusion dies +
the corner-bracket mold) — only the width range and leg count differ:

| | Chair | Loveseat/sofa |
|---|---|---|
| Width | 24"-36" | 56"-90" |
| Legs | 4 (corners only) | 6 (4 corners + 2 mid-span) |
| Stretcher mass | ~1.5kg | ~3.63kg |
| Wire deck mass | ~2.94kg | ~7.12kg |
| New tooling vs. the other variant | — (baseline) | ~$4,000 (mid-span leg bracket mold) |

**Why the sofa needs mid-span legs:** the chair's 3 stretchers (front,
center, back) span only 24"-36", short enough for 4 corner legs alone. At
up to 90" that span is too long to leave unsupported in the middle. Since
nothing can sit at a single fixed world-position across both telescoping
halves at once, each half gets its own mid-span leg, on a small bracket
bonded to the center stretcher — no rail junction needed, unlike the
corner brackets.

**Why sofa tooling is mostly shared:** an extrusion die produces a
constant cross-section cut to any length, so the same 3 dies work for
both variants. The corner bracket design doesn't change with sofa width
either. Only the new mid-span leg bracket needs its own mold.

**Why the range goes down to 56", not just 82"-90":** one SKU this way
covers 2-seat loveseats through 3-seat sofas. Widening the minimum width
costs nothing extra — stretcher tube length is set by the *maximum* width
(90") plus lock-engagement margin, not by the travel range, so a lower
minimum just means more overlap/nesting at the narrow end, which is free.
56" is an assumed loveseat floor (real loveseats commonly run ~52"-65") —
confirm before tooling. The lock uses 5 named standard widths rather than
a uniform fine pitch, since 34" of travel at a 2" pitch would need 18
holes per stretcher (too many stress risers for one tube), and real
furniture sells specific SKU sizes anyway.

### Wholesale price, B2B sale

This is a component sale to sofa manufacturers, not a retail product —
no retail multiple applies. At a 30% OEM margin (judgment default,
`--oem-margin-pct` in `cost_calc.py`), with chair tooling already in place:

| Variant | Landed cost, 1k units | Landed cost, 10k units | Wholesale, 10k (30%) |
|---|---|---|---|
| Chair (own tooling) | $41.74 | $23.64 | $28.39 |
| Loveseat/sofa (own tooling) | $60.56 | $37.68 | $48.98 |
| Loveseat/sofa (chair tooling exists) | $42.56 | $35.88 | $46.64 |

The manufacturer is expected to pass this through to their own customer
close to as-is, as a line-item add-on, not mark it up the way they would
the sofa itself. Run `python3 cost_calc.py --variant chair` or
`--variant sofa` for the full per-line breakdown, or `--variant both`
(default) for the side-by-side.

### Domestic China freight

Xiamen-to-Guangdong trucking (~550km) at the published China domestic LTL
range (roughly RMB 0.2-1.25/kg — sources disagree, no single reliable
figure found) works out to about $0.59/unit for the chair and $1.21/unit
for the sofa by weight alone. `cost_calc.py` uses $1.00/$2.00 as a
rounder, slightly conservative placeholder to cover typical LTL
minimum-charge overhead. No ocean freight, no duties, no export dunnage —
this changes materially if the manufacturer customer isn't actually in
Guangdong.

### Foam savings — doesn't close the gap yet, for either size

The real pitch: this base replaces ~4" of structural foam height (legs 3"
+ frame ~0.47" + wire-panel offset ~0.79") with cheap plastic/wire/leg
structure, so the manufacturer never molds that extra foam.

- **Chair** (30"x30" footprint): 2.08 ft³ avoided.
- **Loveseat/sofa** (30"x73" footprint, midpoint of the range): 5.07 ft³ avoided.

**No real bulk/OEM foam price was found** — web search turned up only a
single retail sheet-foam listing (~$12/ft³) and density specs, no
wholesale number. At an unsourced $4.50/ft³ placeholder:

| Variant | Foam saved | vs. wholesale price (10k) |
|---|---|---|
| Chair | ~$9.38 | $28.39 — well short |
| Loveseat/sofa | ~$22.81 | $46.64 — closer proportionally, still short |

Run `python3 cost_calc.py --foam-cost-per-ft3 <real number>` once you have
a real quote. Until then, lead with raise + style; foam savings is not yet
a standalone justification for the price on either size.

### Cost sources (web search, late Oct 2026 — vendor blogs/marketplaces, not price surveys)

- PP resin, **China-specific**: ~$0.99/kg (China, Q4 2025) — [Expert Market Research](https://www.expertmarketresearch.com/price-forecast/polypropylene-price-trends); Northeast Asia ~$1.05/kg — [IMARC](https://www.imarcgroup.com/polypropylene-pricing-report); used in place of the ~$1.10-1.20/kg global-blended figure the same searches also returned ([Intratec](https://www.intratec.us/chemical-markets/polypropylene-price))
- Welded wire mesh, 4mm wire, **not China-specific**: [~4.0kg/m² weight figure, Alibaba](https://www.alibaba.com/product-introduction/Welded-Wire-Mesh-Weight-Per-Square_60794829193.html); per-kg price only found as single-seller India listings (~$0.65-0.70/kg equivalent) — thin data, flagged, highest-priority item for a real China quote
- Small injection mold tooling, **not China-specific**: single-cavity bracket mold $5,000-$12,000 — [TeamRapidTooling](https://www.teamrapidtooling.com/blog/wp-json/wp/v2/posts/2397), [Formlabs](https://formlabs.com/blog/injection-molding-cost/), [ABIS Mould](https://www.abismould.com/info/breaking-down-injection-mold-costs-103163410.html) — these are Western-facing rapid-tooling quote platforms; a direct Chinese toolmaker-to-manufacturer quote likely comes in lower
- Screw-in/metal furniture legs: $0.37-$1.50/pc bulk — [Accio B2B aggregator](https://www.accio.com/biz-cheap/supply-cheap-y-shape-sofa-leg); leveling feet retail ~$0.86/ea — eBay listing
- Plastic extrusion die: simple structural profile $500-$3,000 — [DFMA](https://www.dfma.com/resources/plastic-extrusion-cost.asp), [Lakeland Plastics](https://lakelandplastics.com/plastic-extrusion-cost-factors/)
- China domestic LTL/FTL trucking: $1.20-$2.00/km FTL, ~RMB 0.2-1.25/kg at 500km (conflicting sources) — [Sino-Shipping](https://www.sino-shipping.com/zh/road-inland-trucking-from-china/costs/how-ltl-ftl-pricing-works-in-china/)

## Path to the business-model decision

Direct-sell-vs-royalty (see chat) waits on two things: cost confirmed with
real numbers, and durability proven on a real prototype. Punch list for
both, pulled together from everything flagged elsewhere in this doc.

### Cost confirmation — replace every placeholder with a real quote

Every number in `cost_calc.py` today comes from a public vendor-blog or
marketplace listing, not a quote. In rough order of leverage (biggest
unknowns, or the ones a whole pitch pillar depends on, first):

1. **Bulk/OEM foam cost, $/ft³** — the single highest-leverage number.
   Search found no real bulk price at all; the whole "save foam costs"
   pillar of the pitch is unverified until this exists. Get this before
   anything else.
2. **Welded wire mesh, $/kg** — thinnest data of the component costs
   (single-seller India listings only); it's also the single largest BOM
   line on both variants.
3. **Extrusion quote** (3 dies + per-kg run cost) from an actual
   extruder, PP resin grade specified.
4. **Injection mold quotes** (corner bracket + mid-span bracket) from 2-3
   toolmakers, with the real part drawings, not a generic "bracket."
5. **Domestic freight** — get an actual Xiamen-Guangdong LTL/FTL quote;
   the published rate data disagreed by 5-6x.
6. **Leg, pin assembly, insert, bushing, Velcro, assembly-labor** costs —
   lower leverage individually (commodity hardware, labor), but add them
   up from a real contract manufacturer's quote rather than the
   placeholders.

Re-run `python3 cost_calc.py` with each real number as it comes in
(`--foam-cost-per-ft3`, `--oem-margin-pct`, or edit the constants
directly) to see how the wholesale price and the foam-savings case move.

### Durability assurance — prove it on a real prototype

- **Detent pin wear** — prototype the hole + steel bushing and cycle it;
  repeated engagement is more likely to loosen the lock over the
  product's life than the pin itself.
- **Ledge height vs. final stretcher profile** — the ~20mm wire-panel
  offset is estimated from a typical 8mm welded-node thickness; confirm
  against the actual wire vendor's spec once sourced.
- **Sustained-load sag** — the wire grid's whole justification is
  distributing load to reduce creep in the plastic stretchers; load-test
  it under a realistic seated weight over time, not just a static check.
- **Velcro adhesion to PP** — the front-stretcher strip is the one part
  of this design most likely to just fail quietly over time. Pull-test
  it, and test the mechanical-fastening fallback if the adhesive alone
  doesn't hold.
- **Corner/mid-span bracket joint strength** — the bonded/riveted
  tube-to-bracket joint carries the whole structural load path; it's
  described as permanent but hasn't been load- or fatigue-tested.
- **Frame racking** — check lateral stability at mid-adjustment, between
  locked positions, since the telescoping stretchers alone don't resist
  racking the way a fully assembled rigid frame would.
- **Corrosion protection** on the welded wire grid (zinc/powder coat) —
  not specified; matters if this is for outdoor/patio use.
