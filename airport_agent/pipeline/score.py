"""Step 4 of the write path: compute every metric, score, tier, warning and confidence, and write the serving
tables. Deterministic: the same clean tables and settings always give the same output.
"""
import pandas as pd

from ..paths import CONFIG
from . import formulas as F
from .clean import window_ending

SCORED = ["load_factor_pct", "passenger_growth_since_2019_pct", "forecast_passenger_growth_pct",
          "system_delay_rate_pct", "forecast_flight_growth_pct"]
CAUSES = [("system", "system_delays"), ("airline", "airline_delays"), ("late_aircraft", "late_aircraft_delays"),
          ("weather", "weather_delays"), ("security", "security_delays")]
MONTH_NAMES = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
               "November", "December"]


def load_weights() -> dict:
    cat = pd.read_csv(CONFIG / "metrics.csv")
    scored = cat[cat["role"] == "scored"]
    return {r.metric_id: (r.side, float(r.weight)) for r in scored.itertuples()}


def _ym(df):
    return df["year"] * 100 + df["month"]


def _period(keys):
    return f"{keys[0][0]}-{keys[0][1]:02d} to {keys[-1][0]}-{keys[-1][1]:02d}"


def _int(v):
    return None if v is None or pd.isna(v) else int(round(v))


# ---------- metrics (no scores yet) ----------

def build_metrics(clean: dict, cfg: dict) -> tuple[pd.DataFrame, dict]:
    """One row per airport with every raw metric. Returns (table, periods)."""
    airports, months, delays = clean["airports"], clean["months"], clean["delays"]
    routes, airlines, forecast = clean["routes"], clean["airlines"], clean["forecast"]
    latest12 = clean["latest12"]
    base_year = cfg["baseline_year"]
    k12 = [y * 100 + m for y, m in latest12]

    m12 = months[_ym(months).isin(k12)]
    mbase = months[months["year"] == base_year]
    g12 = {c: g for c, g in m12.groupby("airport_code")}
    gbase = {c: g for c, g in mbase.groupby("airport_code")}

    delay_end = (int(delays["year"].max()), int(delays[delays["year"] == delays["year"].max()]["month"].max()))
    dwin = window_ending(delay_end, cfg["delay_window_months"])
    d12 = window_ending(delay_end, 12)
    dcols = ["arriving_flights", "delayed_flights"] + [c for _, c in CAUSES]
    dsum_win = delays[_ym(delays).isin([y * 100 + m for y, m in dwin])].groupby("airport_code")[dcols].sum()
    dsum_12 = delays[_ym(delays).isin([y * 100 + m for y, m in d12])].groupby("airport_code")[dcols].sum()
    min_win = min_year = cfg["min_delay_flights"]

    ry = cfg["route_year_latest_full"]
    r_now = {c: g for c, g in routes[routes["year"] == ry].groupby("airport_code")}
    r_base = {c: g for c, g in routes[routes["year"] == base_year].groupby("airport_code")}
    a_now = {c: g for c, g in airlines[airlines["year"] == ry].groupby("airport_code")}

    fb, ft = cfg["forecast_base_year"], cfg["forecast_base_year"] + cfg["forecast_horizon_years"]
    fc = forecast.set_index(["airport_code", "fiscal_year"])

    def fval(code, year, col):
        try:
            v = fc.at[(code, year), col]
        except KeyError:
            return None
        return None if pd.isna(v) else float(v)

    rows = []
    for a in airports.to_dict("records"):
        c = a["airport_code"]
        row = dict(a)
        # --- passengers and seats (BTS summary) ---
        g = g12.get(c)
        have = 0 if g is None else int((g["passengers"] > 0).sum())
        p12 = None if g is None else float(g["passengers"].sum())
        s12 = None if g is None else float(g["seats"].sum())
        enough = have >= cfg["min_months_latest"]
        row["months_in_latest_12"] = have
        row["passengers_latest_12_months"] = _int(p12) if have else None
        row["load_factor_pct"] = F.load_factor(p12, s12) if enough else None
        gb = gbase.get(c)
        base_p = 0.0 if gb is None else float(gb["passengers"].sum())
        base_s = 0.0 if gb is None else float(gb["seats"].sum())
        base_ok = gb is not None and len(gb) >= 10 and base_p >= cfg["min_baseline_passengers"]
        row["passengers_2019"] = _int(base_p) if gb is not None else None
        row["passenger_growth_since_2019_pct"] = F.growth_pct(p12, base_p) if enough and base_ok else None
        row["seats_change_since_2019_pct"] = F.growth_pct(s12, base_s) if enough and base_ok else None
        if have:
            dom, intl = float(g["domestic_passengers"].sum()), float(g["international_passengers"].fillna(0).sum())
            row["domestic_share_pct"] = F.rate_pct(dom, dom + intl)
            bm = g.loc[g["passengers"].idxmax()]
            row["busiest_month"] = f"{MONTH_NAMES[int(bm['month']) - 1]} {int(bm['year'])}"
            row["busiest_month_passengers"] = _int(bm["passengers"])
            row["busiest_month_load_factor_pct"] = F.load_factor(float(bm["passengers"]), float(bm["seats"]))
        # --- FAA forecast ---
        b0, b1 = fval(c, fb, "boardings"), fval(c, ft, "boardings")
        o0, o1 = fval(c, fb, "commercial_operations"), fval(c, ft, "commercial_operations")
        row["forecast_passenger_growth_pct"] = F.growth_pct(b1, b0)
        row["forecast_flight_growth_pct"] = F.growth_pct(o1, o0)
        row["forecast_boardings_2025"], row["forecast_boardings_2035"] = _int(b0), _int(b1)
        row["forecast_operations_2025"], row["forecast_operations_2035"] = _int(o0), _int(o1)
        row["forecast_extra_boardings"] = _int(b1 - b0) if b0 and b1 else None
        row["forecast_extra_operations"] = _int(o1 - o0) if o0 and o1 else None
        # --- delays (BTS Airline Delay Causes), three-year rate from summed counts ---
        if c in dsum_win.index:
            d = dsum_win.loc[c]
            n = float(d["arriving_flights"])
            row["arriving_flights_3_years"] = _int(n)
            row["system_delay_rate_pct"] = F.rate_pct(float(d["system_delays"]), n, min_win)
            row["total_delay_rate_pct"] = F.rate_pct(float(d["delayed_flights"]), n, min_win)
            if n >= min_win:
                for name, col in CAUSES:
                    row[f"delay_cause_{name}_pct"] = F.rate_pct(float(d[col]), float(d["delayed_flights"]))
        if c in dsum_12.index:
            d = dsum_12.loc[c]
            row["arriving_flights_latest_12_months"] = _int(d["arriving_flights"])
            row["system_delay_rate_latest_year_pct"] = F.rate_pct(float(d["system_delays"]), float(d["arriving_flights"]), min_year)
        # --- routes, cargo, airlines (BTS T-100 Segment) ---
        r = r_now.get(c)
        if r is not None and r["passenger_flights"].sum() > 0:
            pf, af, px = float(r["passenger_flights"].sum()), float(r["all_flights"].sum()), float(r["passengers"].sum())
            row["passenger_flights"] = _int(pf)
            row["all_flights_including_cargo"] = _int(af)
            row["cargo_share_of_flights_pct"] = F.rate_pct(af - pf, af)
            row["passengers_per_flight"] = round(px / pf, 1)
            triples = r[["distance_miles", "passenger_flights", "all_flights"]].values.tolist()
            for cut in cfg["long_haul_cutoffs"]:
                sfx = "" if cut == cfg["long_haul_miles_default"] else f"_{cut}"
                row[f"long_haul_share{sfx}_pct"] = F.long_haul_share(triples, cut, True)
                row[f"long_haul_share_all_flights{sfx}_pct"] = F.long_haul_share(triples, cut, False)
            al = a_now.get(c)
            if al is not None and len(al):
                top = al.sort_values(["passengers", "airline"], ascending=[False, True]).iloc[0]
                row["top_airline"] = top["airline"]
                row["top_airline_share_pct"] = F.rate_pct(float(top["passengers"]), float(al["passengers"].sum()))
            rb = r_base.get(c)
            if rb is not None and rb["passenger_flights"].sum() > 0:
                bpf = float(rb["passenger_flights"].sum())
                row["passengers_per_flight_2019"] = round(float(rb["passengers"].sum()) / bpf, 1)
                row["passenger_flights_change_since_2019_pct"] = F.growth_pct(pf, bpf)
        rows.append(row)

    df = pd.DataFrame(rows)
    periods = dict(
        passenger_period=_period(latest12) + " (latest 12 complete months)",
        delay_period=_period(dwin) + " (three years)",
        delay_latest_period=_period(d12) + " (latest 12 months)",
        route_period=f"calendar {ry}",
        forecast_edition=cfg["faa_forecast_edition"] + f" {ft} vs {fb}",
        size_period=f"calendar {cfg['faa_boardings_year']}",
    )
    return df, periods


# ---------- scores ----------

def add_scores(df: pd.DataFrame, weights: dict, cfg: dict) -> pd.DataFrame:
    """Rank-based 0-100 per metric among full-data airports, then the weighted side scores and the total.

    A missing metric is never 0 and weights never shift, with one stated exception: an airport with no
    meaningful 2019 base has the demand half of its passenger side rest on the FAA forecast alone.
    """
    df = df.copy()
    has = lambda col: df[col].notna()
    core = has("load_factor_pct") & has("forecast_passenger_growth_pct") & has("system_delay_rate_pct") & has("forecast_flight_growth_pct")
    df["data_tier"] = "partial"
    df.loc[core, "data_tier"] = "full"
    df.loc[~has("load_factor_pct"), "data_tier"] = "too_thin"
    df["no_2019_base"] = has("load_factor_pct") & ~has("passenger_growth_since_2019_pct")
    full = df["data_tier"] == "full"

    for m in SCORED:
        ref = dict(zip(df.loc[full, "airport_code"], df.loc[full, m]))
        ranks = F.percentiles({k: (None if pd.isna(v) else v) for k, v in ref.items()})
        ref_vals = [v for v in ref.values() if not pd.isna(v)]
        col = m.replace("_pct", "_score")
        df[col] = [ranks.get(c) if is_full else F.position_among(None if pd.isna(v) else v, ref_vals)
                   for c, v, is_full in zip(df["airport_code"], df[m], full)]

    def side(row, side_name):
        w = {m: wt for m, (s, wt) in weights.items() if s == side_name}
        if side_name == "passenger" and row["no_2019_base"]:
            # the exception: forecast passenger growth carries the whole demand half
            w["forecast_passenger_growth_pct"] += w.pop("passenger_growth_since_2019_pct")
        scores = [(row[m.replace("_pct", "_score")], wt) for m, wt in w.items()]
        return F.weighted_score([(None if pd.isna(sc) else sc, wt) for sc, wt in scores])

    df["passenger_score"] = [side(r, "passenger") for r in df.to_dict("records")]
    df["flight_score"] = [side(r, "flight") if r["data_tier"] == "full" else None for r in df.to_dict("records")]
    pw = sum(w for s, w in weights.values() if s == "passenger")
    fw = sum(w for s, w in weights.values() if s == "flight")
    df["total_score"] = [F.weighted_score([(None if pd.isna(p) else p, pw), (None if pd.isna(f) else f, fw)]) if t == "full" else None
                         for p, f, t in zip(df["passenger_score"], df["flight_score"], df["data_tier"])]
    df["rank_overall"] = df["total_score"].rank(ascending=False, method="min").astype("Int64")
    df["rank_in_size_class"] = df.groupby("size_class")["total_score"].rank(ascending=False, method="min").astype("Int64")
    df["ranked_airports_overall"] = int(df["total_score"].notna().sum())
    df["ranked_airports_in_size_class"] = df.groupby("size_class")["total_score"].transform(lambda s: int(s.notna().sum()))
    df["is_strained"] = (df["system_delay_rate_score"] >= cfg["strained_percentile"]) & full
    return df


# ---------- flags, warnings, confidence ----------

def add_flags(df: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    df = df.copy()
    pg, fl, se = df["passenger_growth_since_2019_pct"], df["passenger_flights_change_since_2019_pct"], df["seats_change_since_2019_pct"]
    df["flag_flights_flat_passengers_up"] = (fl <= cfg["flights_flat_max_pct"]) & (pg >= cfg["passengers_up_min_pct"])
    df["flag_capacity_cut"] = (se <= cfg["seats_cut_max_pct"]) & (pg <= cfg["passengers_flat_max_pct"])
    return df


def build_warnings(df: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    legal = pd.read_csv(CONFIG / "legal_limits.csv")
    legal_by = {c: g for c, g in legal.groupby("airport_code")}
    min_win = cfg["min_delay_flights"]
    out = []

    def add(code, kind, severity, message, affects):
        out.append(dict(airport_code=code, warning_type=kind, severity=severity, message=message, affects=affects))

    for r in df.to_dict("records"):
        c = r["airport_code"]
        nn = lambda k: r.get(k) is not None and not pd.isna(r.get(k))
        for lim in (legal_by[c].to_dict("records") if c in legal_by else []):
            binding = lim["binding"] == "yes"
            add(c, "legal_limit" if binding else "schedule_coordination", "caution" if binding else "info",
                f"{'LEGAL LIMIT' if binding else 'Not a hard cap'} ({lim['limit_type']}): {lim['description']} "
                f"Source confidence: {lim['confidence']}; checked {lim['checked_date']}. The legal-limits list is hand-made and partial.",
                "whether added capacity can be used; not in the score")
        if not nn("load_factor_pct"):
            add(c, "no_passenger_data", "blocking", "Not enough passenger and seat data in the latest 12 months to compute any passenger metric.", "all passenger metrics and scores")
        if not nn("arriving_flights_3_years"):
            add(c, "no_delay_data", "blocking", "No delay data: the airlines serving this airport do not report delays. No system delay rate, no flight-side score and no total score.", "system_delay_rate_pct, flight_score, total_score")
        elif not nn("system_delay_rate_pct"):
            add(c, "small_sample", "blocking", f"Too few flights in the delay data ({r['arriving_flights_3_years']:,} arriving flights in three years; the minimum is {min_win:,}) to trust a delay rate. No flight-side score and no total score.", "system_delay_rate_pct, flight_score, total_score")
        elif r["arriving_flights_3_years"] < cfg["small_sample_delay_flights"]:
            add(c, "small_sample", "caution", f"The delay rate rests on a small sample ({r['arriving_flights_3_years']:,} arriving flights in three years).", "system_delay_rate_pct, flight_score")
        if not nn("forecast_passenger_growth_pct"):
            add(c, "no_forecast", "blocking", "No FAA forecast was found for this airport, so there are no forecast metrics and no scores.", "forecast metrics and all scores")
        if r.get("no_2019_base"):
            add(c, "no_2019_base", "caution", "Little or no airline service in 2019, so growth since 2019 is not meaningful. The demand half of the passenger-side score rests on the FAA forecast alone.", "passenger_growth_since_2019_pct, passenger_score")
        if nn("passengers_latest_12_months") and r["boardings_2025"]:
            ratio = r["passengers_latest_12_months"] / r["boardings_2025"]
            if abs(ratio - 1) > cfg["sources_disagree_pct"] / 100:
                add(c, "sources_disagree", "caution", f"The BTS passenger count ({r['passengers_latest_12_months']:,}) differs from FAA boardings ({int(r['boardings_2025']):,}) by more than {cfg['sources_disagree_pct']}% (often multi-stop flights counted at each stop, or a fast-changing airport). Treat passenger metrics with care.", "passenger metrics")
        if nn("cargo_share_of_flights_pct") and r["cargo_share_of_flights_pct"] >= cfg["cargo_heavy_pct"]:
            add(c, "cargo_heavy", "caution", f"Cargo is {r['cargo_share_of_flights_pct']}% of flights here. Cargo competes for the same runways and is not in the score; the FAA flight forecast includes it.", "flight-side reading")
        if nn("top_airline_share_pct") and r["top_airline_share_pct"] >= cfg["dominant_airline_pct"]:
            add(c, "single_airline", "caution", f"One airline dominates: {r['top_airline']} carries {r['top_airline_share_pct']}% of passengers. Demand here depends on that airline's plans; if it cuts service, the forecast growth may not arrive. Not in the score.", "investment risk; not in the score")
        if r["faa_code"] in ("LGA", "DCA"):
            add(c, "forecast_constrained", "caution", "The FAA flight forecast here already has the slot limits built in, so it is not an unconstrained demand estimate.", "forecast_flight_growth_pct, flight_score")
        if r.get("flag_capacity_cut") is True:
            add(c, "capacity_cut", "caution", f"Capacity was cut: seats are {r['seats_change_since_2019_pct']}% vs 2019 while passengers are {r['passenger_growth_since_2019_pct']}%. Full planes here reflect fewer seats, not rising demand.", "load_factor_pct, passenger_score")
        if r.get("flag_flights_flat_passengers_up") is True:
            add(c, "flights_flat_passengers_up", "info", f"Passenger flights are {r['passenger_flights_change_since_2019_pct']}% vs 2019 while passengers are +{r['passenger_growth_since_2019_pct']}%: airlines are using bigger planes instead of adding flights. At a congested airport this can mean flights are blocked; at a small one it is often just the retirement of small jets.", "context")
        if r["boardings_2025"] and r["boardings_2025"] < cfg["small_forecast_boardings"] and nn("forecast_passenger_growth_pct"):
            add(c, "small_airport_forecast", "caution", "Under 100,000 boardings a year: the FAA forecast for airports this small uses simple trend methods, so forecast metrics deserve less trust.", "forecast metrics")
        if r.get("is_territory"):
            add(c, "us_territory", "info", "This airport is in a US territory, not a state.", "context")
    return pd.DataFrame(out)


TIER_NOTE = {
    "full": "Full data: all scored metrics are available, so the airport has a total score and both sub-scores and is ranked.",
    "partial": "Partial data: passenger data exists but there is no usable system delay rate or forecast. Passenger-side score only, no total score, and left out of rankings by default.",
    "too_thin": "Not enough data: no usable passenger data in the latest 12 months. No scores.",
}


def add_confidence(df: pd.DataFrame, warnings: pd.DataFrame) -> pd.DataFrame:
    """Data confidence per airport, by fixed rules. (The per-answer label also considers proxies and how the
    airport name was resolved - see safeguards.)"""
    df = df.copy()
    caution = warnings[warnings["severity"] == "caution"].groupby("airport_code")["warning_type"].apply(list).to_dict()
    conf, reasons, notes = [], [], []
    for r in df.to_dict("records"):
        kinds = [k for k in caution.get(r["airport_code"], []) if k != "single_airline"]   # a business risk says nothing about the data
        if r["data_tier"] != "full":
            level, why = "low", "partial data" if r["data_tier"] == "partial" else "not enough data"
        elif "small_sample" in kinds:
            level, why = "low", "small delay sample"
        elif kinds:
            level, why = "medium", ", ".join(sorted(set(k.replace("_", " ") for k in kinds)))
        else:
            level, why = "high", "full data, no data warnings"
        conf.append(level)
        reasons.append(why)
        missing = [m for m in SCORED if pd.isna(r[m])]
        notes.append(TIER_NOTE[r["data_tier"]] + (" Missing: " + ", ".join(missing) + "." if missing else ""))
    df["confidence"], df["confidence_reason"], df["data_quality_note"] = conf, reasons, notes
    return df


# ---------- per-year and per-month serving tables ----------

def build_year_table(clean: dict, cfg: dict) -> pd.DataFrame:
    months, delays, routes = clean["months"], clean["delays"], clean["routes"]
    y = months.groupby(["airport_code", "year"], as_index=False).agg(
        months_of_data=("month", "nunique"), passengers=("passengers", "sum"), seats=("seats", "sum"), flights=("flights", "sum"))
    y["is_partial_year"] = y["months_of_data"] < 12
    y["load_factor_pct"] = [F.load_factor(p, s) for p, s in zip(y["passengers"], y["seats"])]
    d = delays.groupby(["airport_code", "year"], as_index=False).agg(
        delay_months_of_data=("month", "nunique"), arriving_flights=("arriving_flights", "sum"),
        system_delays=("system_delays", "sum"), delayed_flights=("delayed_flights", "sum"))
    mn = cfg["min_delay_flights"]
    d["system_delay_rate_pct"] = [F.rate_pct(s, n, mn) for s, n in zip(d["system_delays"], d["arriving_flights"])]
    d["total_delay_rate_pct"] = [F.rate_pct(s, n, mn) for s, n in zip(d["delayed_flights"], d["arriving_flights"])]
    d = d.drop(columns=["system_delays", "delayed_flights"])
    rr = []
    for (c, yr), g in routes.groupby(["airport_code", "year"]):
        pf, af = float(g["passenger_flights"].sum()), float(g["all_flights"].sum())
        triples = g[["distance_miles", "passenger_flights", "all_flights"]].values.tolist()
        rr.append(dict(airport_code=c, year=yr, route_months_of_data=int(g["months_of_data"].iloc[0]),
                       long_haul_share_pct=F.long_haul_share(triples, cfg["long_haul_miles_default"], True),
                       long_haul_share_all_flights_pct=F.long_haul_share(triples, cfg["long_haul_miles_default"], False),
                       cargo_share_of_flights_pct=F.rate_pct(af - pf, af)))
    out = y.merge(d, on=["airport_code", "year"], how="outer").merge(pd.DataFrame(rr), on=["airport_code", "year"], how="outer")
    for col in ["passengers", "seats", "flights", "arriving_flights", "months_of_data", "delay_months_of_data", "route_months_of_data"]:
        out[col] = out[col].round().astype("Int64")
    return out.sort_values(["airport_code", "year"]).reset_index(drop=True)


def build_month_table(clean: dict) -> pd.DataFrame:
    m = clean["months"][["airport_code", "year", "month", "passengers", "seats", "flights", "is_complete_month"]]
    d = clean["delays"][["airport_code", "year", "month", "arriving_flights", "delayed_flights", "system_delays"]]
    out = m.merge(d, on=["airport_code", "year", "month"], how="outer")
    out["load_factor_pct"] = [F.load_factor(p, s) if pd.notna(p) and pd.notna(s) else None for p, s in zip(out["passengers"], out["seats"])]
    # a single month needs at least 100 arriving flights before a rate is shown
    out["system_delay_rate_pct"] = [F.rate_pct(s, n, 100) if pd.notna(n) else None for s, n in zip(out["system_delays"], out["arriving_flights"])]
    out["total_delay_rate_pct"] = [F.rate_pct(s, n, 100) if pd.notna(n) else None for s, n in zip(out["delayed_flights"], out["arriving_flights"])]
    for col in ["passengers", "seats", "flights", "arriving_flights"]:
        out[col] = out[col].round().astype("Int64")
    out["system_delays"] = out["system_delays"].round(2)
    return out.sort_values(["airport_code", "year", "month"]).reset_index(drop=True)


def run(clean: dict, cfg: dict) -> dict:
    weights = load_weights()
    metrics, periods = build_metrics(clean, cfg)
    metrics = add_flags(add_scores(metrics, weights, cfg), cfg)
    warnings = build_warnings(metrics, cfg)
    metrics = add_confidence(metrics, warnings)
    for k, v in periods.items():
        metrics[k] = v
    metrics["score_version"] = str(cfg["score_version"])
    routes = clean["routes"][["airport_code", "year", "destination_code", "distance_miles", "passenger_flights",
                              "all_flights", "passengers", "seats", "months_of_data"]]
    return dict(airport_metrics=metrics, airport_warnings=warnings, airport_year=build_year_table(clean, cfg),
                airport_month=build_month_table(clean), airport_routes=routes, periods=periods)
