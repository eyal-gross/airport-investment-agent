"""Step 3 of the write path: data checks. They sit between the computed tables and the serving folder.
If any check fails, the build stops and the previous serving tables stay in place.
"""
import pandas as pd

from .score import SCORED

COVERAGE_NEED = {"load_factor_pct": 95, "passenger_growth_since_2019_pct": 88, "forecast_passenger_growth_pct": 95,
                 "system_delay_rate_pct": 75, "forecast_flight_growth_pct": 95}
RANGES = {"load_factor_pct": (20, 100), "system_delay_rate_pct": (0, 50), "total_delay_rate_pct": (0, 70),
          "forecast_passenger_growth_pct": (-50, 200), "forecast_flight_growth_pct": (-50, 200),
          "cargo_share_of_flights_pct": (0, 100), "long_haul_share_pct": (0, 100), "top_airline_share_pct": (0, 100),
          "passenger_score": (0, 100), "flight_score": (0, 100), "total_score": (0, 100)}


def run(tables: dict, clean: dict, cfg: dict) -> list[dict]:
    m, w = tables["airport_metrics"], tables["airport_warnings"]
    n = len(m)
    out = []

    def check(name, ok, detail):
        out.append(dict(check=name, ok=bool(ok), detail=str(detail)))

    check("airport count in the expected range", 380 <= n <= 430, f"{n} FAA primary airports")
    check("airport codes are unique", m["airport_code"].is_unique, f"{m['airport_code'].nunique()} unique of {n}")
    matched = clean["forecast"]["airport_code"].nunique()
    unmatched = sorted(set(m["airport_code"]) - set(clean["forecast"]["airport_code"]))
    check("FAA forecast matched for at least 395 airports", matched >= min(395, n - 7), f"{matched} of {n}; unmatched: {unmatched}")
    check("passenger window has 12 months", len(clean["latest12"]) == 12, clean["latest12"][0:1] + clean["latest12"][-1:])
    dmonths = clean["delays"].drop_duplicates(["year", "month"]).shape[0]
    check("delay data covers at least 36 months", dmonths >= 36, f"{dmonths} months")
    for col in ["passengers", "seats", "flights"]:
        check(f"no negative {col}", (clean["months"][col].dropna() >= 0).all(), "airport-month table")
    for col, need in COVERAGE_NEED.items():
        have = int(m[col].notna().sum())
        check(f"coverage {col}", 100 * have / n >= need, f"{have} of {n} ({100 * have / n:.0f}%), need {need}%")
    for col, (lo, hi) in RANGES.items():
        bad = m[m[col].notna() & ~m[col].between(lo, hi)]
        check(f"range {col} in [{lo}, {hi}]", bad.empty, f"{len(bad)} out of range {list(zip(bad['airport_code'], bad[col]))[:6]}")
    for col in SCORED:
        q = m[col].dropna().quantile([0.1, 0.5, 0.9])
        check(f"spread {col}", q[0.9] - q[0.1] > 0, f"10th pct {q[0.1]:.1f}, median {q[0.5]:.1f}, 90th pct {q[0.9]:.1f}")
    both = m[m["passengers_latest_12_months"].notna() & (m["boardings_2025"] > 0)]
    ratio = both["passengers_latest_12_months"].astype(float) / both["boardings_2025"].astype(float)
    within = int(ratio.between(0.85, 1.15).sum())
    check("BTS passengers vs FAA boardings within 15% for most airports", within / len(both) >= 0.85,
          f"{within} of {len(both)} ({100 * within / len(both):.0f}%); median ratio {ratio.median():.3f}")
    large = m[m["size_class"] == "large"]
    check("every large airport has full data", (large["data_tier"] == "full").all(), f"{int((large['data_tier'] == 'full').sum())} of {len(large)}")
    not_full = m[m["data_tier"] != "full"]
    check("no total score without full data", not_full["total_score"].isna().all() and not_full["flight_score"].isna().all(), f"{len(not_full)} non-full airports")
    full = m[m["data_tier"] == "full"]
    check("every full-data airport has a total score", full["total_score"].notna().all(), f"{len(full)} full-data airports")
    legal = set(w[w["warning_type"] == "legal_limit"]["airport_code"])
    check("legal-limit warnings present", {"SNA", "JFK", "LGA", "DCA", "DAL"} <= legal, f"{len(legal)} airports carry a binding legal limit")
    dist = m["confidence"].value_counts().to_dict()
    check("confidence label has a real spread", sum(1 for v in dist.values() if v >= 0.05 * n) >= 2, dist)
    tiers = m["data_tier"].value_counts().to_dict()
    check("data tiers", tiers.get("full", 0) >= 0.7 * n, tiers)
    return out


def summarize(results: list[dict], log=print) -> bool:
    for r in results:
        log(f"  {'PASS' if r['ok'] else 'FAIL'} | {r['check']} | {r['detail']}")
    passed = sum(r["ok"] for r in results)
    log(f"  data checks: {passed} of {len(results)} passed")
    return passed == len(results)
