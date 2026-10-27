#!/usr/bin/env python3
"""Rough order-of-magnitude cost estimate for the expandable wire-deck base
at production scale.

NOT A QUOTE. Every unit price below is a placeholder pulled from public
vendor-blog and marketplace listings (see README.md "Cost sources"), not a
real supplier quote. Treat the output as a starting point for budgeting and
for sanity-checking real quotes, not as a number to commit to.

Sales model: this is a B2B component sold primarily to foam sofa
manufacturers, who pass its cost straight through to the end customer as a
line-item add-on (e.g. "+ riser kit: $X") rather than marking it up the way
they would the sofa itself. So the number that matters downstream isn't a
retail MSRP -- it's our landed cost plus a wholesale/OEM margin, which is
what shows up on the sofa manufacturer's own BOM and gets passed on close
to as-is.

Two cost buckets:
  - Recurring (BOM + labor + packaging + freight): scales per unit, improves
    only modestly with volume (bulk component pricing).
  - Non-recurring (tooling): fixed one-time spend, amortized per unit --
    this is where "cost at scale" mostly comes from for a product this size.
"""

import argparse

# ---------------------------------------------------------------------------
# Recurring BOM, per unit (USD). Each line: (name, unit_cost, qty, basis)
# ---------------------------------------------------------------------------
BOM = [
    ("Side rails, PP extrusion (material + process, ~0.69kg @ $2.50/kg)", 1.73, 1,
     "resin ~$1.10/kg bulk (Expert Market Research/IMARC 2025); "
     "+processing to a typical $2.50/kg all-in for simple structural profile"),
    ("Stretchers, PP extrusion, 2-part telescoping (~1.5kg @ $2.50/kg)", 3.75, 1,
     "same basis; higher mass for nested outer-sleeve/inner-tube pair"),
    ("Corner brackets, injection molded (material + machine time)", 0.60, 4,
     "small-part injection molding, typical per-part range at volume"),
    ("Wire deck, welded mesh steel (~2.82kg total @ $1.50/kg)", 4.23, 1,
     "4mm wire mesh ~4.0kg/m2 (Alibaba spec sheet) x ~0.71m2 for 2 panels; "
     "$1.50/kg assumes powder-coated, landed -- thin market data, flagged"),
    ("Screw-in legs, 3in", 0.60, 4,
     "bulk metal furniture leg listings, $0.37-1.50/pc depending on finish/MOQ"),
    ("Threaded inserts, 3/8-16 brass", 0.10, 4, "commodity hardware, estimate"),
    ("Detent pin assembly (spring + ball detent)", 1.20, 2,
     "bulk OEM sourcing estimate, well below retail ($5-15/ea at retail)"),
    ("Steel bushings, pin holes (7 positions x 2 stretchers)", 0.08, 14,
     "commodity hardware, estimate"),
    ("Misc fasteners / wire-panel retention clips", 1.00, 1, "lump-sum estimate"),
    ("Assembly labor (contract manufacturing)", 4.00, 1,
     "judgment estimate, moderate-complexity furniture assembly"),
    ("Packaging (bulk/palletized, no retail box — ships to mfr's factory)", 1.50, 1,
     "judgment estimate, lower than DTC retail packaging since there's no "
     "branding/shelf-ready requirement for a B2B factory-floor shipment"),
]

FREIGHT_PER_UNIT = 5.00  # ocean freight + duties, amortized -- highly destination-dependent

# ---------------------------------------------------------------------------
# Non-recurring tooling (USD, one-time)
# ---------------------------------------------------------------------------
TOOLING = [
    ("Extrusion die, side rail profile", 2000,
     "simple structural profile die, $500-3000 range (vendor estimates)"),
    ("Extrusion die, stretcher outer sleeve profile", 2000, "same basis"),
    ("Extrusion die, stretcher inner tube profile", 2000, "same basis"),
    ("Injection mold, corner brackets (shared family mold, 2 variants)", 12000,
     "single-cavity bracket mold quoted $5,000-12,000; family mold at the high end"),
]

VOLUME_TIERS = [1000, 10000, 100000]

# Modest bulk-pricing improvement on the recurring BOM as volume climbs --
# a judgment curve (procurement leverage on resin/hardware), not sourced data.
VOLUME_DISCOUNT = {1000: 1.00, 10000: 0.92, 100000: 0.85}


def bom_total():
    return sum(cost * qty for _, cost, qty, _ in BOM)


def tooling_total():
    return sum(cost for _, cost, _ in TOOLING)


def unit_cost(volume):
    recurring = (bom_total() + FREIGHT_PER_UNIT) * VOLUME_DISCOUNT[volume]
    tooling_per_unit = tooling_total() / volume
    return recurring, tooling_per_unit, recurring + tooling_per_unit


# ---------------------------------------------------------------------------
# Foam savings -- the real pitch to a sofa manufacturer: this base replaces
# structural foam height with cheap plastic/wire/leg, at the same overall
# product height. HEAVILY CAVEATED: web search turned up no real bulk/OEM
# foam price, only a single retail sheet listing (~$12/ft3). Bulk foam
# commonly runs well under retail, but there is no sourced number here --
# this is a framework to plug real quotes into, not a number to pitch with.
# ---------------------------------------------------------------------------
FOAM_COST_PER_FT3 = 4.50  # UNSOURCED placeholder -- see caveat above and README
FOOTPRINT_DEPTH_IN = 30.0
FOOTPRINT_WIDTH_IN = 30.0  # mid-travel width, illustrative
HEIGHT_REPLACED_IN = 4.0   # legs (3in) + frame (~0.47in) + wire-panel offset (~0.79in)


def foam_savings(width_in=FOOTPRINT_WIDTH_IN, depth_in=FOOTPRINT_DEPTH_IN,
                  height_in=HEIGHT_REPLACED_IN, foam_cost_per_ft3=FOAM_COST_PER_FT3):
    volume_ft3 = (width_in * depth_in * height_in) / 1728.0  # in^3 -> ft^3
    return volume_ft3, volume_ft3 * foam_cost_per_ft3


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--oem-margin-pct", type=float, default=0.30,
                     help="markup over landed cost sold to the sofa manufacturer, "
                          "as a fraction (default 0.30 = 30%%). This is a B2B "
                          "component sale, not a retail product -- no retail "
                          "multiple applies. The sofa manufacturer is expected to "
                          "pass this (or close to it) straight through to the end "
                          "customer as a line-item add-on, not mark it up the way "
                          "they would the sofa itself.")
    ap.add_argument("--foam-cost-per-ft3", type=float, default=FOAM_COST_PER_FT3,
                     help="bulk/OEM foam cost, $/ft3 -- UNSOURCED placeholder, "
                          "plug in a real quote once you have one")
    args = ap.parse_args()

    print("BOM (per unit, at baseline/1000-unit pricing):")
    for name, cost, qty, basis in BOM:
        line = cost * qty
        print(f"  {name:<62} ${line:6.2f}   [{basis}]")
    print(f"  {'Freight + duties (per unit, estimate)':<62} ${FREIGHT_PER_UNIT:6.2f}")
    print(f"  {'BOM + freight subtotal':<62} ${bom_total() + FREIGHT_PER_UNIT:6.2f}\n")

    print("Tooling (one-time, non-recurring):")
    for name, cost, basis in TOOLING:
        print(f"  {name:<62} ${cost:>8,.0f}   [{basis}]")
    print(f"  {'Total tooling':<62} ${tooling_total():>8,.0f}\n")

    print(f"{'Volume':>10} | {'Recurring/unit':>15} | {'Tooling/unit':>13} | "
          f"{'Our landed cost':>16} | {'Wholesale price to mfr':>23}")
    print("-" * 90)
    for v in VOLUME_TIERS:
        recurring, tool_per, total = unit_cost(v)
        wholesale = total * (1 + args.oem_margin_pct)
        print(f"{v:>10,} | ${recurring:>13.2f} | ${tool_per:>11.2f} | "
              f"${total:>14.2f} | ${wholesale:>21.2f}")

    vol_ft3, savings = foam_savings(foam_cost_per_ft3=args.foam_cost_per_ft3)
    print(f"\nFoam savings (UNSOURCED placeholder foam price -- see caveat in source):")
    print(f"  Structural height replaced by base: {HEIGHT_REPLACED_IN:.1f}in "
          f"(legs 3.0 + frame ~0.47 + wire-panel offset ~0.79)")
    print(f"  Foam volume no longer needed, {FOOTPRINT_WIDTH_IN:.0f}x{FOOTPRINT_DEPTH_IN:.0f}in "
          f"footprint: {vol_ft3:.2f} ft3")
    print(f"  Foam cost saved @ ${args.foam_cost_per_ft3:.2f}/ft3: ${savings:.2f}")
    print(f"  Net vs. our wholesale price (10k-volume): "
          f"${savings - unit_cost(10000)[2] * (1 + args.oem_margin_pct):+.2f} "
          f"-- NEGATIVE means the component costs the manufacturer more than "
          f"the foam it displaces; get a real foam quote before using this "
          f"to pitch net savings.")


if __name__ == "__main__":
    main()
