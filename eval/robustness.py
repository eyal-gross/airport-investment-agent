"""How much does the ranking depend on our choices? Re-scores every airport under changed weights and windows
and reports how far the ranking moves - whichever way it comes out.

    python eval/robustness.py        (needs data/clean/, i.e. a pipeline build on this machine)

Writes eval/results/robustness.md.
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from airport_agent.paths import CLEAN, ROOT, settings  # noqa: E402
from airport_agent.pipeline import score  # noqa: E402
from airport_agent.pipeline.clean import window_ending  # noqa: E402

NEW_ENGLAND = ["CT", "ME", "MA", "NH", "RI", "VT"]


def load_clean() -> dict:
    t = {n: pd.read_parquet(CLEAN / f"{f}.parquet") for n, f in [
        ("airports", "airports"), ("months", "airport_month"), ("delays", "airport_month_delays"),
        ("routes", "airport_year_routes"), ("airlines", "airport_year_airlines"), ("forecast", "airport_forecast")]}
    done = t["months"][t["months"]["is_complete_month"]]
    end = (int(done["year"].max()), int(done[done["year"] == done["year"].max()]["month"].max()))
    t["latest12"] = window_ending(end, 12)
    return t


def scored(clean, cfg, weights):
    m, _ = score.build_metrics(clean, cfg)
    return score.add_scores(m, weights, cfg).set_index("airport_code")


def scale_sides(weights, passenger_share):
    out = {}
    for m, (side, w) in weights.items():
        out[m] = (side, w * (passenger_share / 0.5 if side == "passenger" else (1 - passenger_share) / 0.5))
    return out


def main():
    cfg = settings()
    clean = load_clean()
    base_w = score.load_weights()
    half_lf = dict(base_w)
    half_lf.update(load_factor_pct=("passenger", 0.125), passenger_growth_since_2019_pct=("passenger", 0.1875),
                   forecast_passenger_growth_pct=("passenger", 0.1875))
    equal = {m: (s, 0.2) for m, (s, _) in base_w.items()}
    # the two FAA forecasts carry 37.5% together; halve them, the freed weight staying on the same side
    half_fc = dict(base_w)
    half_fc.update(forecast_passenger_growth_pct=("passenger", 0.0625), load_factor_pct=("passenger", 0.25 + 0.0625 * 2 / 3),
                   passenger_growth_since_2019_pct=("passenger", 0.125 + 0.0625 / 3),
                   forecast_flight_growth_pct=("flight", 0.125), system_delay_rate_pct=("flight", 0.375))
    scenarios = [
        ("Load factor at half weight (12.5%; the rest of the passenger side shared by the two growth metrics)", cfg, half_lf),
        ("Growth window changed: passenger growth since 2022 instead of 2019", dict(cfg, baseline_year=2022), base_w),
        ("Weights shifted to the passenger side (60 / 40)", cfg, scale_sides(base_w, 0.6)),
        ("Weights shifted to the flight side (40 / 60)", cfg, scale_sides(base_w, 0.4)),
        ("Delay window of 12 months instead of 36", dict(cfg, delay_window_months=12), base_w),
        ("All five metrics weighted equally (20% each)", cfg, equal),
        ("FAA forecasts at half weight (18.75% together, not 37.5%; the freed weight stays on the same side)", cfg, half_fc),
    ]
    base = scored(clean, cfg, base_w)
    b = base[base["total_score"].notna()]
    rows = []
    for name, c, w in scenarios:
        s = scored(clean, c, w)
        s = s[s["total_score"].notna()]
        both = b.index.intersection(s.index)
        rho = b.loc[both, "total_score"].rank().corr(s.loc[both, "total_score"].rank())
        overlap, total = 0, 0
        for size in ["large", "medium", "small", "nonhub"]:
            tb = set(b[b["size_class"] == size].nlargest(10, "total_score").index)
            ts = set(s[s["size_class"] == size].nlargest(10, "total_score").index)
            overlap += len(tb & ts)
            total += len(tb)
        same_first = sum(b[b["size_class"] == z]["total_score"].idxmax() == s[s["size_class"] == z]["total_score"].idxmax()
                         for z in ["large", "medium", "small", "nonhub"])
        ne_b = list(b[b["state"].isin(NEW_ENGLAND)].nlargest(5, "total_score").index)
        ne_s = list(s[s["state"].isin(NEW_ENGLAND)].nlargest(5, "total_score").index)
        move = (b.loc[both, "total_score"].rank(ascending=False) - s.loc[both, "total_score"].rank(ascending=False)).abs()
        rows.append({"Scenario": name, "Airports ranked": len(s), "Rank correlation with the baseline": round(float(rho), 3),
                     "Top 10 per size class kept": f"{overlap} of {total}", "Size classes with the same #1": f"{same_first} of 4",
                     "New England top 5": " ".join(ne_s) + (" (same order)" if ne_s == ne_b else (" (same set)" if set(ne_s) == set(ne_b) else " (changed)")),
                     "Median rank move": int(move.median()), "Largest rank move": int(move.max())})
    out = pd.DataFrame(rows)
    ne_base = " ".join(b[b["state"].isin(NEW_ENGLAND)].nlargest(5, "total_score").index)
    lines = ["# Robustness: how much the ranking depends on our choices", "",
             f"Baseline: {len(b)} airports ranked, score version {cfg['score_version']}. Baseline New England top 5: {ne_base}.",
             "Each row re-scores every airport with one choice changed and compares the ranking with the baseline.",
             "Rank correlation is Spearman's (1.0 = identical order).", "",
             "| " + " | ".join(out.columns) + " |", "|" + "---|" * len(out.columns)]
    lines += ["| " + " | ".join(str(v) for v in r) + " |" for r in out.itertuples(index=False)]
    dest = ROOT / "eval" / "results" / "robustness.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
