#!/usr/bin/env python3
"""Rough order-of-magnitude cost estimate for the expandable wire-deck base,
in two sizes: a chair/loveseat module (24-36in wide) and a full sofa
(82-90in wide). Both share the same depth (30in) and mechanism.

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

Sofa-length structural note: the chair variant's 3 stretchers (front,
center, back) span only 24-36in, short enough for 4 corner legs alone.
At 82-90in that span is too long to leave unsupported in the middle --
this adds 2 mid-span legs (one per telescoping half, since nothing can
sit at a single fixed world-position across both sliding halves at once),
each on its own small bracket bonded to the center stretcher, no rail
junction needed.

Tooling note: the 3 extrusion dies and the corner-bracket mold are SHARED
between variants (a die produces a constant profile cut to any length; the
corner bracket design doesn't change with sofa width). Only the new
mid-span leg bracket needs its own (smaller, cheaper) mold -- so adding
the sofa variant on top of an already-tooled chair variant is a small
incremental spend, not a second full tooling bill.

Two cost buckets:
  - Recurring (BOM + labor + packaging + freight): scales per unit, improves
    only modestly with volume (bulk component pricing).
  - Non-recurring (tooling): fixed one-time spend, amortized per unit --
    this is where "cost at scale" mostly comes from for a product this size.
"""

import argparse

RESIN_PER_KG = 2.50   # PP, material + extrusion process, all-in
WIRE_PER_KG = 1.50    # welded mesh steel, landed + powder-coated
WIRE_KG_PER_M2 = 4.0  # 4mm wire @ 50mm pitch (Alibaba spec sheet)
IN2_PER_M2 = 1550.0031

# ---------------------------------------------------------------------------
# Variant parameters. Side rails are identical in both (depth is fixed at
# 30in either way) -- only the width-direction parts scale.
# ---------------------------------------------------------------------------
VARIANTS = {
    "chair": dict(
        width_range_in=(24, 36),
        stretcher_kg=1.5,     # 3 stretchers combined, 2-part telescoping
        legs=4,
        mid_brackets=0,
        pin_positions=7,      # 12in travel / 2in pitch + 1
        assembly=4.00,
        packaging=1.50,
        freight=5.00,
    ),
    "sofa": dict(
        width_range_in=(82, 90),
        stretcher_kg=3.63,    # scaled ~2.42x vs. chair, by wire-panel-width ratio
        legs=6,               # 4 corner + 2 mid-span (one per telescoping half)
        mid_brackets=2,
        pin_positions=5,      # 8in travel / 2in pitch + 1
        assembly=6.00,
        packaging=3.00,
        freight=9.00,
    ),
}

DEPTH_IN = 30.0
RAIL_KG = 0.69          # 2 side rails combined -- depth-only, same in both variants
CORNER_BRACKET_EACH = 0.60
MID_BRACKET_EACH = 0.40  # smaller/simpler than a corner bracket -- no rail junction
LEG_EACH = 0.60
INSERT_EACH = 0.10
PIN_ASSEMBLY_EACH = 1.20
PINNED_STRETCHERS = 2     # front + back, locked; center rides free
BUSHING_EACH = 0.08
MISC_FASTENERS = {"chair": 1.00, "sofa": 1.50}

# ---------------------------------------------------------------------------
# Non-recurring tooling (USD, one-time)
# ---------------------------------------------------------------------------
SHARED_TOOLING = [
    ("Extrusion die, side rail profile", 2000,
     "simple structural profile die, $500-3000 range (vendor estimates); "
     "SHARED -- a die cuts any length, so this doesn't repeat per variant"),
    ("Extrusion die, stretcher outer sleeve profile", 2000, "same basis, shared"),
    ("Extrusion die, stretcher inner tube profile", 2000, "same basis, shared"),
    ("Injection mold, corner brackets (shared family mold, 2 variants)", 12000,
     "single-cavity bracket mold quoted $5,000-12,000; family mold at the "
     "high end; SHARED -- same bracket design regardless of sofa width"),
]
SOFA_ONLY_TOOLING = [
    ("Injection mold, mid-span leg bracket", 4000,
     "smaller/simpler single-cavity mold than the corner bracket; "
     "SOFA VARIANT ONLY"),
]

VOLUME_TIERS = [1000, 10000, 100000]

# Modest bulk-pricing improvement on the recurring BOM as volume climbs --
# a judgment curve (procurement leverage on resin/hardware), not sourced data.
VOLUME_DISCOUNT = {1000: 1.00, 10000: 0.92, 100000: 0.85}


def wire_mass_kg(width_in, depth_in=DEPTH_IN, overlap_margin_mm=50.0):
    """2 panels, each sized per calc.py's panel_sizing (width_in = MAX width)."""
    panel_width_in = (width_in * 25.4 + overlap_margin_mm) / 2.0 / 25.4
    panel_area_in2 = panel_width_in * depth_in
    total_area_m2 = 2 * panel_area_in2 / IN2_PER_M2
    return total_area_m2 * WIRE_KG_PER_M2


def bom(variant_name):
    v = VARIANTS[variant_name]
    max_width_in = v["width_range_in"][1]
    wire_kg = wire_mass_kg(max_width_in)
    bushings = v["pin_positions"] * PINNED_STRETCHERS

    lines = [
        ("Side rails, PP extrusion (material + process)",
         RAIL_KG * RESIN_PER_KG, 1,
         f"~{RAIL_KG}kg @ ${RESIN_PER_KG}/kg -- depth-only, same in both variants"),
        ("Stretchers, PP extrusion, 2-part telescoping",
         v["stretcher_kg"] * RESIN_PER_KG, 1,
         f"~{v['stretcher_kg']}kg @ ${RESIN_PER_KG}/kg"),
        ("Corner brackets, injection molded", CORNER_BRACKET_EACH, 4,
         "material + machine time"),
    ]
    if v["mid_brackets"]:
        lines.append(("Mid-span leg brackets, injection molded", MID_BRACKET_EACH,
                       v["mid_brackets"], "smaller than corner bracket, no rail junction"))
    lines += [
        ("Wire deck, welded mesh steel", wire_kg * WIRE_PER_KG, 1,
         f"~{wire_kg:.2f}kg @ {WIRE_KG_PER_M2}kg/m2, ${WIRE_PER_KG}/kg landed+coated "
         f"(thin market data, flagged)"),
        ("Screw-in legs, 3in", LEG_EACH, v["legs"],
         "bulk metal furniture leg listings, $0.37-1.50/pc by finish/MOQ"),
        ("Threaded inserts, 3/8-16 brass", INSERT_EACH, v["legs"], "commodity hardware"),
        ("Detent pin assembly (spring + ball detent)", PIN_ASSEMBLY_EACH,
         PINNED_STRETCHERS, "bulk OEM sourcing estimate"),
        ("Steel bushings, pin holes", BUSHING_EACH, bushings,
         f"{v['pin_positions']} positions x {PINNED_STRETCHERS} locked stretchers"),
        ("Misc fasteners / wire-panel retention clips", MISC_FASTENERS[variant_name], 1,
         "lump-sum estimate"),
        ("Assembly labor (contract manufacturing)", v["assembly"], 1, "judgment estimate"),
        ("Packaging (bulk/palletized, no retail box)", v["packaging"], 1,
         "judgment estimate -- ships to mfr's factory, no retail/branding requirement"),
    ]
    return lines


def tooling_total(variant_name, incremental):
    """incremental=True assumes chair tooling already exists (shared tooling
    already paid for); only the variant-specific tooling is new spend."""
    total = sum(cost for _, cost, _ in SOFA_ONLY_TOOLING) if variant_name == "sofa" else 0
    if not incremental:
        total += sum(cost for _, cost, _ in SHARED_TOOLING)
    return total


def unit_cost(variant_name, volume, freight_per_unit, incremental_tooling):
    v = VARIANTS[variant_name]
    bom_subtotal = sum(cost * qty for _, cost, qty, _ in bom(variant_name))
    recurring = (bom_subtotal + freight_per_unit) * VOLUME_DISCOUNT[volume]
    tooling_per_unit = tooling_total(variant_name, incremental_tooling) / volume
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
HEIGHT_REPLACED_IN = 4.0   # legs (3in) + frame (~0.47in) + wire-panel offset (~0.79in)


def foam_savings(width_in, depth_in=DEPTH_IN, height_in=HEIGHT_REPLACED_IN,
                  foam_cost_per_ft3=FOAM_COST_PER_FT3):
    volume_ft3 = (width_in * depth_in * height_in) / 1728.0  # in^3 -> ft^3
    return volume_ft3, volume_ft3 * foam_cost_per_ft3


def print_variant(name, args):
    v = VARIANTS[name]
    lo, hi = v["width_range_in"]
    print(f"\n{'=' * 90}\n{name.upper()} -- {lo:.0f}-{hi:.0f}in wide x {DEPTH_IN:.0f}in deep, "
          f"{v['legs']} legs\n{'=' * 90}")

    print("BOM (per unit, at baseline/1000-unit pricing):")
    for item_name, cost, qty, basis in bom(name):
        line = cost * qty
        print(f"  {item_name:<52} ${line:7.2f}   [{basis}]")
    print(f"  {'Freight + duties (per unit, estimate)':<52} ${v['freight']:7.2f}")

    print("\nTooling (one-time, non-recurring):")
    for item_name, cost, basis in SHARED_TOOLING:
        print(f"  {item_name:<60} ${cost:>8,.0f}   [{basis}]")
    if name == "sofa":
        for item_name, cost, basis in SOFA_ONLY_TOOLING:
            print(f"  {item_name:<60} ${cost:>8,.0f}   [{basis}]")

    print(f"\n{'Volume':>10} | {'Recurring/unit':>15} | {'Tooling/unit (standalone)':>26} | "
          f"{'Landed (standalone)':>20} | {'Landed (chair tooling exists)':>30}")
    print("-" * 115)
    for vol in VOLUME_TIERS:
        rec, tool_standalone, total_standalone = unit_cost(name, vol, v["freight"], False)
        _, tool_incr, total_incr = unit_cost(name, vol, v["freight"], True)
        print(f"{vol:>10,} | ${rec:>13.2f} | ${tool_standalone:>24.2f} | "
              f"${total_standalone:>18.2f} | ${total_incr:>28.2f}")

    rec10k, _, total10k = unit_cost(name, 10000, v["freight"], True)
    wholesale10k = total10k * (1 + args.oem_margin_pct)
    print(f"\nWholesale price to mfr @ 10,000 units, {args.oem_margin_pct:.0%} margin, "
          f"chair tooling already exists: ${wholesale10k:.2f}")

    vol_ft3, savings = foam_savings((lo + hi) / 2.0, foam_cost_per_ft3=args.foam_cost_per_ft3)
    print(f"Foam savings @ {(lo+hi)/2:.0f}in width (UNSOURCED foam price): "
          f"{vol_ft3:.2f} ft3 -> ${savings:.2f}; "
          f"net vs. wholesale: ${savings - wholesale10k:+.2f}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--variant", choices=[*VARIANTS, "both"], default="both")
    ap.add_argument("--oem-margin-pct", type=float, default=0.30,
                     help="markup over landed cost sold to the sofa manufacturer, "
                          "as a fraction (default 0.30 = 30%%). B2B component sale, "
                          "not retail -- no retail multiple applies.")
    ap.add_argument("--foam-cost-per-ft3", type=float, default=FOAM_COST_PER_FT3,
                     help="bulk/OEM foam cost, $/ft3 -- UNSOURCED placeholder, "
                          "plug in a real quote once you have one")
    args = ap.parse_args()

    names = VARIANTS if args.variant == "both" else [args.variant]
    for name in names:
        print_variant(name, args)


if __name__ == "__main__":
    main()
