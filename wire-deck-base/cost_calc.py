#!/usr/bin/env python3
"""Rough order-of-magnitude cost estimate for the expandable wire-deck base
at production scale.

NOT A QUOTE. Every unit price below is a placeholder pulled from public
vendor-blog and marketplace listings (see README.md "Cost sources"), not a
real supplier quote. Treat the output as a starting point for budgeting and
for sanity-checking real quotes, not as a number to commit to.

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
    ("Packaging (corrugated + foam corners)", 4.00, 1, "judgment estimate"),
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


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--retail-multiple", type=float, default=3.0,
                     help="rule-of-thumb landed-cost-to-MSRP multiple (default 3.0x)")
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
          f"{'Landed cost/unit':>17} | {'Rule-of-thumb MSRP':>19}")
    print("-" * 85)
    for v in VOLUME_TIERS:
        recurring, tool_per, total = unit_cost(v)
        msrp = total * args.retail_multiple
        print(f"{v:>10,} | ${recurring:>13.2f} | ${tool_per:>11.2f} | "
              f"${total:>15.2f} | ${msrp:>17.2f}")


if __name__ == "__main__":
    main()
