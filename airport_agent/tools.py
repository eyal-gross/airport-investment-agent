"""The five read-only tools the agent can call. They only filter, sort and label pre-computed serving tables.

Every result has the same shape:
    result        the numbers
    definitions   what each metric is, its unit, source and period (from the metric catalog)
    warnings      warnings for the airports in the result (printed by the chat screen, not left to the LLM)
    data_quality  the data tier and data confidence of each airport
    notes         how to read the result and what it cannot show
    meta          facts the safeguards use (airports involved, whether a proxy is used, ...)

A bad input never raises: it returns {"error": ..., "valid_options": ...} so the LLM can correct itself.
"""
import json
import math
import re
from functools import lru_cache

import pandas as pd

from .paths import CONFIG, SERVING, settings
from .pipeline import formulas as F

SIZE_CLASSES = ["large", "medium", "small", "nonhub"]
RANK_METRICS = ["total_score", "passenger_score", "flight_score", "load_factor_pct", "passenger_growth_since_2019_pct",
                "forecast_passenger_growth_pct", "system_delay_rate_pct", "forecast_flight_growth_pct",
                "total_delay_rate_pct", "boardings_2025", "forecast_extra_boardings", "forecast_extra_operations",
                "cargo_share_of_flights_pct", "long_haul_share_pct", "top_airline_share_pct", "seats_change_since_2019_pct"]
YEAR_METRICS = ["load_factor_pct", "system_delay_rate_pct", "total_delay_rate_pct", "passengers",
                "long_haul_share_pct", "cargo_share_of_flights_pct"]
MONTH_METRICS = ["load_factor_pct", "system_delay_rate_pct", "total_delay_rate_pct", "passengers"]
TREND_METRICS = ["passengers", "seats", "flights", "load_factor_pct", "system_delay_rate_pct", "total_delay_rate_pct"]
PROXY_METRICS = {"total_score", "passenger_score", "flight_score", "system_delay_rate_pct", "load_factor_pct",
                 "forecast_passenger_growth_pct", "forecast_flight_growth_pct"}
SCORE_COLS = ["total_score", "passenger_score", "flight_score"]
FIVE = ["load_factor_pct", "passenger_growth_since_2019_pct", "forecast_passenger_growth_pct", "system_delay_rate_pct",
        "forecast_flight_growth_pct"]
SEASONS = {"winter": [12, 1, 2], "spring": [3, 4, 5], "summer": [6, 7, 8], "fall": [9, 10, 11]}
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
STATES = {"alabama": "AL", "alaska": "AK", "arizona": "AZ", "arkansas": "AR", "california": "CA", "colorado": "CO",
          "connecticut": "CT", "delaware": "DE", "district of columbia": "DC", "florida": "FL", "georgia": "GA",
          "hawaii": "HI", "idaho": "ID", "illinois": "IL", "indiana": "IN", "iowa": "IA", "kansas": "KS",
          "kentucky": "KY", "louisiana": "LA", "maine": "ME", "maryland": "MD", "massachusetts": "MA", "michigan": "MI",
          "minnesota": "MN", "mississippi": "MS", "missouri": "MO", "montana": "MT", "nebraska": "NE", "nevada": "NV",
          "new hampshire": "NH", "new jersey": "NJ", "new mexico": "NM", "new york": "NY", "north carolina": "NC",
          "north dakota": "ND", "ohio": "OH", "oklahoma": "OK", "oregon": "OR", "pennsylvania": "PA",
          "rhode island": "RI", "south carolina": "SC", "south dakota": "SD", "tennessee": "TN", "texas": "TX",
          "utah": "UT", "vermont": "VT", "virginia": "VA", "washington": "WA", "west virginia": "WV",
          "wisconsin": "WI", "wyoming": "WY", "puerto rico": "PR", "guam": "GU", "us virgin islands": "VI",
          "american samoa": "AS", "northern mariana islands": "MP"}
EXTRA_DEFS = {
    "passengers": dict(display_name="Passengers on departing flights", unit="passengers", source="BTS T-100 airport-month summary",
                       definition="Passengers on board departing flights. Through passengers are counted on each leg."),
    "seats": dict(display_name="Seats on departing flights", unit="seats", source="BTS T-100 airport-month summary", definition="Seats offered on departing flights."),
    "flights": dict(display_name="Departing flights (all types)", unit="departures", source="BTS T-100 airport-month summary",
                    definition="Departing flights of all types, as counted by BTS. Not comparable with FAA operations, which count takeoffs plus landings."),
}


# ---------- loading ----------

class DataMissing(RuntimeError):
    pass


@lru_cache(maxsize=1)
def store() -> dict:
    need = ["airport_metrics", "airport_warnings", "airport_year", "airport_month", "airport_routes"]
    missing = [n for n in need if not (SERVING / f"{n}.parquet").exists()]
    if missing:
        raise DataMissing("The data tables are missing. Run:  python -m airport_agent.pipeline.build")
    s = {n: pd.read_parquet(SERVING / f"{n}.parquet") for n in need}
    s["by_code"] = s["airport_metrics"].set_index("airport_code", drop=False)
    s["faa_to_code"] = dict(zip(s["airport_metrics"]["faa_code"], s["airport_metrics"]["airport_code"]))
    s["catalog"] = pd.read_csv(CONFIG / "metrics.csv").set_index("metric_id")
    reg = pd.read_csv(CONFIG / "regions.csv")
    s["regions"] = {r: sorted(g["state"]) for r, g in reg.groupby("region")}
    s["aliases"] = {r.alias: (r.target_type, r.target) for r in pd.read_csv(CONFIG / "aliases.csv").itertuples()}
    s["manifest"] = json.loads((SERVING / "fetch_manifest.json").read_text(encoding="utf-8"))
    s["cfg"] = settings()
    return s


def _v(x):
    """Make a value JSON-safe. Missing stays None - never 0."""
    if x is None or x is pd.NA:
        return None
    if isinstance(x, (bool,)):
        return x
    if hasattr(x, "item"):
        x = x.item()
    if isinstance(x, float):
        if math.isnan(x):
            return None
        return int(x) if x == int(x) and abs(x) >= 1000 else round(x, 2)
    return x


def _err(message, **valid):
    return dict(error=message, valid_options=valid or None)


def _resolve(code):
    s = store()
    c = str(code or "").strip().upper()
    if c in s["by_code"].index:
        return c
    return s["faa_to_code"].get(c)


def _unknown(code):
    return _err(f"'{code}' is not the code of a covered airport. Call find_airport with the airport or city name first.")


def _definitions(metric_ids, period_override=None):
    s = store()
    periods = s["manifest"]["periods"]
    out = {}
    for m in metric_ids:
        if m in s["catalog"].index:
            r = s["catalog"].loc[m]
            d = dict(name=r["display_name"], unit=r["unit"], definition=r["definition"], source=r["source"],
                     period=period_override or periods.get(r["period_key"], ""))
            if r["is_proxy"] == "yes":
                d["proxy_note"] = r["proxy_note"]
            out[m] = d
        elif m in EXTRA_DEFS:
            out[m] = dict(name=EXTRA_DEFS[m]["display_name"], unit=EXTRA_DEFS[m]["unit"], definition=EXTRA_DEFS[m]["definition"],
                          source=EXTRA_DEFS[m]["source"], period=period_override or periods["passenger_period"])
    return out


def _warnings(codes, severities=("caution", "blocking")):
    s = store()
    w = s["airport_warnings"]
    w = w[w["airport_code"].isin(codes) & w["severity"].isin(severities)]
    order = {c: i for i, c in enumerate(codes)}
    rows = sorted(w.to_dict("records"), key=lambda r: (order[r["airport_code"]], r["severity"] != "blocking"))
    return [dict(airport_code=r["airport_code"], type=r["warning_type"], severity=r["severity"], message=r["message"]) for r in rows]


def _quality(codes):
    s = store()
    return [dict(airport_code=c, data_tier=s["by_code"].at[c, "data_tier"], note=s["by_code"].at[c, "data_quality_note"],
                 data_confidence=s["by_code"].at[c, "confidence"], data_confidence_reason=s["by_code"].at[c, "confidence_reason"])
            for c in codes]


def _identity(r):
    return dict(airport_code=r["airport_code"], name=r["name"], serves=_v(r["served_city"]) or f"{r['city']}, {r['state']}",
                state=r["state"], size_class=r["size_class"], boardings_2025=_v(r["boardings_2025"]),
                is_us_territory=bool(r["is_territory"]))


def _summary(r):
    d = _identity(r)
    d.update({k: _v(r[k]) for k in SCORE_COLS + FIVE})
    d.update(rank_in_size_class=_v(r["rank_in_size_class"]), ranked_airports_in_size_class=_v(r["ranked_airports_in_size_class"]),
             rank_overall=_v(r["rank_overall"]), ranked_airports_overall=_v(r["ranked_airports_overall"]),
             forecast_extra_boardings=_v(r["forecast_extra_boardings"]), seats_change_since_2019_pct=_v(r["seats_change_since_2019_pct"]),
             capacity_was_cut=bool(r["flag_capacity_cut"]), flights_flat_while_passengers_rise=bool(r["flag_flights_flat_passengers_up"]),
             is_strained=bool(r["is_strained"]), data_tier=r["data_tier"], data_confidence=r["confidence"])
    return d


def _wrap(tool, inputs, result, metric_ids, codes, notes, period_override=None, **meta):
    s = store()
    codes = list(dict.fromkeys(codes))
    return dict(tool=tool, inputs=inputs, result=result, definitions=_definitions(metric_ids, period_override),
                warnings=_warnings(codes), data_quality=_quality(codes), notes=notes,
                meta=dict(airports=codes, uses_proxy=bool(set(metric_ids) & PROXY_METRICS), periods=s["manifest"]["periods"],
                          score_version=s["manifest"]["score_version"], **meta))


# ---------- 1. find_airport ----------

def _word_match(needle, text):
    return bool(text) and re.search(r"(?<![a-z])" + re.escape(needle) + r"(?![a-z])", str(text).lower()) is not None


def find_airport(query: str) -> dict:
    s = store()
    df = s["airport_metrics"]
    raw = str(query or "").strip()
    if not raw:
        return _err("Give an airport code, airport name or city.")
    q = re.sub(r"\b(international|intl|airport|regional|municipal)\b", " ", raw.lower())
    q = re.sub(r"\s+", " ", q).strip(" ,.")
    code = _resolve(raw)
    if code and len(raw.strip()) == 3 and raw.strip().lower() not in s["aliases"]:
        r = s["by_code"].loc[code]
        return _wrap("find_airport", dict(query=raw), dict(match_type="exact code", default_airport_code=code, candidates=[_summary(r)],
                     guidance="Exact code match."), SCORE_COLS, [code], [], resolved_by_default=False)

    state_filter = None
    if q in STATES and q not in ("washington", "new york"):
        return _err(f"'{raw}' is a state, not an airport. Use rank_airports with states=['{STATES[q]}'] to list its airports.")
    m = re.match(r"^(.*?)[, ]+([a-z .]+)$", q)
    if m:
        tail = m.group(2).strip()
        st = STATES.get(tail) or (tail.upper() if len(tail) == 2 and tail.upper() in STATES.values() and "," in q else None)
        if st and m.group(1).strip():
            state_filter, q = st, m.group(1).strip(" ,")

    alias = s["aliases"].get(q)
    if alias and alias[0] == "airport":
        code = alias[1]
        r = s["by_code"].loc[code]
        mates = df[(df["metro_id"] == r["metro_id"]) & (df["airport_code"] != code)].sort_values("boardings_2025", ascending=False)
        return _wrap("find_airport", dict(query=raw), dict(match_type="known name", default_airport_code=code, candidates=[_summary(r)],
                     same_metro_area=[_identity(x) for x in mates.to_dict("records")], guidance="Known name for one airport."),
                     SCORE_COLS, [code], [], resolved_by_default=False)
    needle = alias[1].lower() if alias else q

    direct = df[[_word_match(needle, n) or _word_match(needle, c) or _word_match(needle, sc)
                 for n, c, sc in zip(df["name"], df["city"], df["served_city"])]]
    if direct.empty and " " in needle:
        # several words ("boston logan"): every word must appear somewhere in the name or the cities
        words = [w for w in needle.split() if len(w) > 2]
        direct = df[[bool(words) and all(_word_match(w, f"{n} {c} {sc}") for w in words)
                     for n, c, sc in zip(df["name"], df["city"], df["served_city"])]]
    if state_filter:
        direct = direct[direct["state"] == state_filter]
    direct = direct.sort_values("boardings_2025", ascending=False)
    if direct.empty:
        return _wrap("find_airport", dict(query=raw), dict(match_type="none", default_airport_code=None, candidates=[],
                     guidance=f"No airport among the {len(df)} FAA primary airports matches '{raw}'. It may be outside the covered set "
                              "(for example a private-aviation, military, foreign or very small airport). Say so; do not guess."),
                     [], [], [], resolved_by_default=False)

    city_states = {r["state"] for r in direct.to_dict("records") if _word_match(needle, r["city"]) or _word_match(needle, r["served_city"])}
    multi_state = len(city_states) > 1
    default = None if multi_state else F.pick_default([(r["airport_code"], int(r["boardings_2025"])) for r in direct.to_dict("records")])
    metro_ids = set(direct["metro_id"].dropna())
    mates = df[df["metro_id"].isin(metro_ids) & ~df["airport_code"].isin(direct["airport_code"]) & (df["metro_airport_count"] > 1)]
    mates = mates.sort_values("boardings_2025", ascending=False)
    if multi_state:
        guidance = "The name matches cities in different states. Ask the user which one they mean."
    elif len(direct) == 1 and len(mates):
        guidance = (f"One airport matches the city itself ({default}); its metro area also has other airports (same_metro_area). "
                    "Use the default, say that you assumed it, and name the others.")
    elif len(direct) == 1:
        guidance = "Single match."
    elif default:
        guidance = (f"Several airports match, and {default} clearly dominates (at least twice the boardings of the next). "
                    "Use it, say that you assumed it, and mention the others.")
    else:
        guidance = "Several airports match and none clearly dominates. Ask the user which one, or cover all of them."
    cands = [_summary(r) for r in direct.head(8).to_dict("records")]
    codes = [c["airport_code"] for c in cands]
    return _wrap("find_airport", dict(query=raw), dict(
        match_type="name or city", default_airport_code=default, candidates=cands,
        same_metro_area=[_identity(x) for x in mates.head(8).to_dict("records")], guidance=guidance),
        SCORE_COLS, codes, [], resolved_by_default=bool(default and (len(direct) > 1 or (len(mates) > 0 and alias is not None))))


# ---------- 2. rank_airports ----------

def _month_values(df_codes, metric, months, year, season=None):
    """Value of a monthly metric for one calendar month or one season (three months): those months in `year`, or summed
    over the latest three years that have all of them. Rates come from summed counts.
    Returns (values by code, period text, excluded-too-small, minimum flights)."""
    s = store()
    mt = s["airport_month"]
    mt = mt[mt["airport_code"].isin(df_codes) & mt["month"].isin(months)]
    label = f"{season} ({', '.join(MONTHS[m - 1] for m in months)})" if season else MONTHS[months[0] - 1]
    col = "passengers" if metric in ("passengers", "load_factor_pct") else "arriving_flights"
    if year:
        mt = mt[mt["year"] == year]
        have = sorted(int(m) for m in mt[mt[col].notna()]["month"].unique())
        period = f"{label} {year}" if not season else f"{label} of calendar {year}"
        if season and len(have) < len(months):
            period += (f" - PARTIAL: only {', '.join(MONTHS[m - 1] for m in have)} " + ("has" if len(have) == 1 else "have") + " data"
                       if have else " - NO DATA for these months yet")
    else:
        per_year = mt[mt[col].notna()].groupby("year")["month"].nunique()
        years = sorted(per_year[per_year == len(months)].index)[-3:]     # only years that have every month asked for
        mt = mt[mt["year"].isin(years)]
        period = f"{label} of {', '.join(str(int(y)) for y in years)} (summed)"
    g = mt.groupby("airport_code")[["passengers", "seats", "arriving_flights", "delayed_flights", "system_delays"]].sum(min_count=1)
    min_f = 100 * max(1, len(mt[["year", "month"]].drop_duplicates()))     # 100 arriving flights per month included
    vals, small = {}, []
    for c, r in g.iterrows():
        if metric == "passengers":
            vals[c] = _v(r["passengers"])
        elif metric == "load_factor_pct":
            vals[c] = F.load_factor(_v(r["passengers"]), _v(r["seats"]))
        else:
            num = r["system_delays"] if metric == "system_delay_rate_pct" else r["delayed_flights"]
            n = r["arriving_flights"]
            if pd.isna(n) or n < min_f:
                small.append(c)
                continue
            vals[c] = F.rate_pct(float(num), float(n))
    return vals, period, small, min_f


def rank_airports(region=None, states=None, metro_of=None, size_classes=None, airport_codes=None, sort_by="total_score",
                  order="descending", year=None, month=None, min_value=None, max_value=None, limit=5,
                  include_partial_data=False, min_data_confidence=None, group_by_size_class=None, season=None) -> dict:
    s = store()
    df = s["airport_metrics"]
    inputs = {k: v for k, v in dict(region=region, states=states, metro_of=metro_of, size_classes=size_classes,
              airport_codes=airport_codes, sort_by=sort_by, order=order, year=year, month=month, season=season, min_value=min_value,
              max_value=max_value, limit=limit, include_partial_data=include_partial_data,
              min_data_confidence=min_data_confidence, group_by_size_class=group_by_size_class).items() if v is not None}
    pool = df
    scope = []
    # --- validate and filter ---
    if region:
        rg = str(region).strip().lower()
        if rg not in s["regions"]:
            return _err(f"Unknown region '{region}'.", region=sorted(s["regions"]), hint="Or pass states=[two-letter codes].")
        pool = pool[pool["state"].isin(s["regions"][rg])]
        scope.append(f"region {rg} ({', '.join(s['regions'][rg])})")
    if states:
        st = [STATES.get(str(x).strip().lower(), str(x).strip().upper()) for x in ([states] if isinstance(states, str) else states)]
        bad = [x for x in st if x not in set(df["state"])]
        if bad:
            return _err(f"Unknown state(s) {bad}. Use two-letter codes.", states=sorted(set(df["state"])))
        pool = pool[pool["state"].isin(st)]
        scope.append(f"states {', '.join(st)}")
    if metro_of:
        code = _resolve(metro_of)
        if not code:
            return _unknown(metro_of)
        pool = pool[pool["metro_id"] == s["by_code"].at[code, "metro_id"]]
        scope.append(f"metro area of {code} ({s['by_code'].at[code, 'metro_name']})")
    if size_classes:
        sz = [str(x).strip().lower() for x in ([size_classes] if isinstance(size_classes, str) else size_classes)]
        bad = [x for x in sz if x not in SIZE_CLASSES]
        if bad:
            return _err(f"Unknown size class {bad}.", size_classes=SIZE_CLASSES, hint="'small airports' means the FAA small-hub class; nonhub is smaller still.")
        pool = pool[pool["size_class"].isin(sz)]
        scope.append(f"size class {', '.join(sz)}")
    if airport_codes:
        codes = [_resolve(c) for c in airport_codes]
        if None in codes:
            return _unknown(airport_codes[codes.index(None)])
        pool = pool[pool["airport_code"].isin(codes)]
        scope.append(f"airports {', '.join(codes)}")
    if order not in ("descending", "ascending"):
        return _err("order must be 'descending' or 'ascending'.", order=["descending", "ascending"])
    try:
        limit = max(1, min(int(limit), 30))     # 30 = the whole FAA large-hub class in one table
    except (TypeError, ValueError):
        return _err("limit must be a whole number from 1 to 30.")
    if min_data_confidence and min_data_confidence not in ("high", "medium"):
        return _err("min_data_confidence must be 'high' or 'medium'.", min_data_confidence=["high", "medium"])
    if month is not None and (not isinstance(month, int) or not 1 <= month <= 12):
        return _err("month must be a whole number from 1 (January) to 12 (December).")
    if season is not None:
        season = str(season).strip().lower()
        season = {"autumn": "fall"}.get(season, season)
        if season not in SEASONS:
            return _err(f"Unknown season '{season}'.", season=list(SEASONS))
        if month is not None:
            return _err("Pass month or season, not both.")

    years_available = sorted(int(y) for y in s["airport_year"]["year"].unique())
    notes, period_override, small_sample = [], None, []
    if month is not None or season is not None:
        view = "season" if season else "month"
        if sort_by not in MONTH_METRICS:
            return _err(f"'{sort_by}' is not available by {view}.", **{f"sort_by_with_{view}": MONTH_METRICS})
        if year is not None and year not in years_available:
            return _err(f"No data for {year}.", year=years_available)
        vals, period_override, small_sample, min_f = _month_values(set(pool["airport_code"]), sort_by,
                                                                   SEASONS[season] if season else [month], year, season)
        pool = pool.assign(_sort=pool["airport_code"].map(vals))
        notes.append(f"{'Season' if season else 'Monthly'} view: {period_override}. Scores do not exist by {view}; this ranks one raw metric. "
                     f"A delay rate needs at least {min_f} arriving flights in the period.")
        if season:
            notes.append("Seasons are meteorological: winter = December to February, spring = March to May, summer = June to August, "
                         "fall = September to November. Winter takes January, February and December of the same calendar year(s). "
                         "Passengers are the total over the months and years in the period.")
    elif year is not None:
        if year not in years_available:
            return _err(f"No data for {year}.", year=years_available)
        if sort_by not in YEAR_METRICS:
            return _err(f"'{sort_by}' is not available per year. The score exists for the latest period only, so past-year rankings by score cannot be produced.",
                        sort_by_with_year=YEAR_METRICS)
        yt = s["airport_year"]
        yt = yt[yt["year"] == year].set_index("airport_code")
        pool = pool.assign(_sort=pool["airport_code"].map(yt[sort_by]))
        mo = yt["delay_months_of_data"] if "delay" in sort_by else yt["months_of_data"]
        n_mo = int(mo.dropna().max()) if mo.notna().any() else 0
        period_override = f"calendar {year}" + (f" (PARTIAL year: {n_mo} months of data)" if n_mo < 12 else "")
        notes.append(f"Year view: {period_override}. Past years return raw metrics only; scores are for the latest period.")
    else:
        if sort_by not in RANK_METRICS:
            return _err(f"Cannot sort by '{sort_by}'.", sort_by=RANK_METRICS)
        pool = pool.assign(_sort=pool[sort_by])

    considered = len(pool)
    excluded = []

    def drop(mask, reason):
        nonlocal pool
        gone = pool[mask]
        if len(gone):
            excluded.append(dict(reason=reason, count=len(gone),
                                 airports=[f"{r['airport_code']} ({r['name']})" for r in gone.sort_values("boardings_2025", ascending=False).head(12).to_dict("records")],
                                 list_was_cut=len(gone) > 12))
        pool = pool[~mask]

    if not include_partial_data:
        drop(pool["data_tier"] != "full", "partial or thin data (no total score) - left out by default; set include_partial_data=true to include them")
    if small_sample:
        drop(pool["airport_code"].isin(small_sample), "too few arriving flights in that period to trust a delay rate")
    drop(pool["_sort"].isna(), f"no value for {sort_by}")
    if min_data_confidence:
        ok = ["high"] if min_data_confidence == "high" else ["high", "medium"]
        drop(~pool["confidence"].isin(ok), f"data confidence below {min_data_confidence}")
    if min_value is not None:
        pool = pool[pool["_sort"] >= float(min_value)]
    if max_value is not None:
        pool = pool[pool["_sort"] <= float(max_value)]

    asc = order == "ascending"
    national = not (region or states or metro_of or airport_codes)
    if group_by_size_class is None:
        group_by_size_class = national and not size_classes and sort_by in SCORE_COLS

    def rows_for(sub, cap=limit):
        sub = sub.sort_values(["_sort", "boardings_2025"], ascending=[asc, False])
        out = []
        sv = list(sub["_sort"])
        for i, r in enumerate(sub.head(cap).to_dict("records")):
            d = dict(position=i + 1, sort_value=_v(r["_sort"]),
                     tied_with_neighbour=(i > 0 and sv[i] == sv[i - 1]) or (i + 1 < len(sv) and sv[i] == sv[i + 1]))
            d.update(_summary(r))
            out.append(d)
        return out

    if group_by_size_class:
        per_class = min(limit, 10)      # four groups: keep the result readable
        result_rows = {sz: rows_for(pool[pool["size_class"] == sz], per_class) for sz in SIZE_CLASSES if (pool["size_class"] == sz).any()}
        if limit > per_class:
            notes.append(f"Grouped rankings show at most {per_class} airports per size class. Filter by size_classes to see more of one class.")
        shown = [r for rows in result_rows.values() for r in rows]
        notes.append("Shown per FAA size class, because size is not in the score: without grouping, small leisure airports top a national list. "
                     "Size (boardings_2025) and forecast_extra_boardings show the size of the prize.")
    else:
        result_rows = rows_for(pool)
        shown = result_rows
    codes = [r["airport_code"] for r in shown]
    if any(r["is_us_territory"] for r in shown):
        notes.append("Some airports shown are in US territories (see is_us_territory).")
    if sort_by in SCORE_COLS:
        notes.append("Scores are relative: 0-100 position among full-data airports. A high score means more strained and faster-growing than peers, "
                     "not that the airport must expand. They rank upside (how much added capacity would be filled), a proxy for profit; no cost data exists.")
    notes.append("No public data measures terminal or gate utilization directly; 'terminal expansion' candidates are judged on the passenger-side and flight-side signals.")
    metric_ids = list(dict.fromkeys([sort_by] + SCORE_COLS + FIVE + ["boardings_2025", "forecast_extra_boardings", "seats_change_since_2019_pct"]))
    out = _wrap("rank_airports", inputs,
                dict(scope=scope or ["all covered airports (national)"], sorted_by=sort_by, order=order,
                     airports_in_scope=considered, airports_ranked=len(pool), airports_shown=len(shown),
                     list_was_cut=len(pool) > len(shown) and not group_by_size_class, excluded=excluded, ranking=result_rows),
                metric_ids, codes, notes, period_override=None)
    if period_override:
        out["definitions"][sort_by]["period"] = period_override
    return out


# ---------- 3. compare_airports ----------

COMPARE_METRICS = SCORE_COLS + FIVE + ["system_delay_rate_latest_year_pct", "total_delay_rate_pct", "boardings_2025",
                                         "passengers_latest_12_months", "forecast_extra_boardings", "forecast_extra_operations",
                                         "cargo_share_of_flights_pct", "long_haul_share_pct", "top_airline_share_pct",
                                         "domestic_share_pct", "seats_change_since_2019_pct"]


def _differences(codes, values_by_code, metrics):
    """Differences and ratios, computed here so the LLM never does arithmetic."""
    out = []
    base = codes[0]
    for other in codes[1:]:
        for m in metrics:
            a, b = values_by_code[base].get(m), values_by_code[other].get(m)
            if a is None or b is None:
                continue
            d = dict(metric=m, a=base, b=other, a_value=a, b_value=b, difference_a_minus_b=_v(round(a - b, 1)),
                     higher=base if a > b else (other if b > a else "equal"))
            if b not in (0, None) and a >= 0 and b > 0:
                d["ratio_a_to_b"] = round(a / b, 2)
            out.append(d)
    return out


def compare_airports(airport_codes, year=None) -> dict:
    s = store()
    if not isinstance(airport_codes, (list, tuple)) or not 2 <= len(airport_codes) <= 5:
        return _err("airport_codes must be a list of 2 to 5 airport codes.")
    codes = [_resolve(c) for c in airport_codes]
    if None in codes:
        return _unknown(airport_codes[codes.index(None)])
    codes = list(dict.fromkeys(codes))
    if len(codes) < 2:
        return _err("Give at least two different airports.")
    years_available = sorted(int(y) for y in s["airport_year"]["year"].unique())
    notes = ["Differences are a minus b, in the metric's own unit (percentage points for percents). Ratios are a divided by b."]
    if year is not None:
        if year not in years_available:
            return _err(f"No data for {year}.", year=years_available)
        yt = s["airport_year"]
        yt = yt[yt["year"] == year].set_index("airport_code")
        vals, airports = {}, []
        for c in codes:
            ident = _identity(s["by_code"].loc[c])
            if c in yt.index:
                r = yt.loc[c]
                v = {m: _v(r[m]) for m in YEAR_METRICS}
                ident.update(v, months_of_passenger_data=_v(r["months_of_data"]), months_of_delay_data=_v(r["delay_months_of_data"]),
                             arriving_flights_in_delay_data=_v(r["arriving_flights"]), is_partial_year=bool(r["is_partial_year"]) if pd.notna(r["is_partial_year"]) else None)
            else:
                v = {}
                ident["note"] = f"no data for {year}"
            vals[c] = v
            airports.append(ident)
        partial = any(a.get("is_partial_year") for a in airports) or any((a.get("months_of_delay_data") or 12) < 12 for a in airports)
        period = f"calendar {year}" + (" (PARTIAL year - see months_of_passenger_data and months_of_delay_data)" if partial else "")
        notes += [f"Year view: {period}. Past years return raw metrics only; scores exist for the latest period only.",
                  f"Years available: {years_available[0]} to {years_available[-1]}. Long-haul and cargo shares exist only for {sorted(int(y) for y in s['airport_routes']['year'].unique())}.",
                  "Warnings below describe the airports today (for example legal limits) and still apply."]
        return _wrap("compare_airports", dict(airport_codes=codes, year=year),
                     dict(period=period, airports=airports, comparisons=_differences(codes, vals, YEAR_METRICS)),
                     YEAR_METRICS, codes, notes, period_override=period)

    vals, airports = {}, []
    for c in codes:
        r = s["by_code"].loc[c]
        v = {m: _v(r[m]) for m in COMPARE_METRICS}
        vals[c] = v
        d = _summary(r)
        d.update(v)
        d.update(delay_causes_share_of_delays_pct={k: _v(r[f"delay_cause_{k}_pct"]) for k in ["system", "airline", "late_aircraft", "weather", "security"]},
                 arriving_flights_3_years=_v(r["arriving_flights_3_years"]), top_airline=_v(r["top_airline"]),
                 busiest_month=_v(r["busiest_month"]), busiest_month_load_factor_pct=_v(r["busiest_month_load_factor_pct"]),
                 rank_overall=_v(r["rank_overall"]), ranked_airports_overall=_v(r["ranked_airports_overall"]))
        airports.append(d)
    notes += ["For 'congestion', the closest measures are system_delay_rate_pct (three years, drives the score), its latest-12-months value, and total_delay_rate_pct. "
              "The system delay category is coded by airlines and includes ordinary weather, so it is mostly, not purely, congestion.",
              "FAA forecast operations count takeoffs plus landings and include cargo; never compare them with BTS departures."]
    return _wrap("compare_airports", dict(airport_codes=codes),
                 dict(period="latest period (see definitions for each metric's period)", airports=airports,
                      comparisons=_differences(codes, vals, COMPARE_METRICS)),
                 COMPARE_METRICS, codes, notes)


# ---------- 4. airport_profile ----------

def _long_haul_table(code, year, cutoffs):
    s = store()
    rt = s["airport_routes"]
    rt = rt[(rt["airport_code"] == code) & (rt["year"] == year)]
    if rt.empty:
        return None
    triples = rt[["distance_miles", "passenger_flights", "all_flights"]].values.tolist()
    pf, af = float(rt["passenger_flights"].sum()), float(rt["all_flights"].sum())
    rows = []
    for cut in cutoffs:
        lp = sum(t[1] for t in triples if t[0] >= cut)
        la = sum(t[2] for t in triples if t[0] >= cut)
        rows.append(dict(cutoff_miles=cut, share_of_passenger_flights_pct=F.long_haul_share(triples, cut, True),
                         share_of_all_flights_including_cargo_pct=F.long_haul_share(triples, cut, False),
                         long_haul_passenger_flights=_v(lp), long_haul_flights_including_cargo=_v(la)))
    months = int(rt["months_of_data"].iloc[0])
    return dict(year=year, is_partial_year=months < 12, months_of_data=months, passenger_flights=_v(pf), all_flights_including_cargo=_v(af),
                cargo_and_other_non_passenger_flights=_v(af - pf), by_cutoff=rows)


def _recent_delay_pattern(code):
    """Is the latest-12-month system delay rate driven by its newest months? Compared with the same months a year earlier (so a
    normal busy season does not count) and with the rest of the latest 12. Rates from summed counts."""
    s = store()
    n, ratio = s["cfg"]["recent_spike_months"], s["cfg"]["recent_spike_ratio"]
    mt = s["airport_month"]
    mt = mt[(mt["airport_code"] == code) & mt["system_delay_rate_pct"].notna()].copy()
    mt["ym"] = mt["year"] * 100 + mt["month"]
    latest = mt.sort_values("ym").tail(12)
    if len(latest) < 12:
        return None
    recent, rest = latest.tail(n), latest.head(12 - n)
    year_ago = mt[mt["ym"].isin(recent["ym"] - 100)]
    if len(year_ago) < n:
        return None

    def rate(g):
        return F.rate_pct(float(g["system_delays"].sum()), float(g["arriving_flights"].sum()))

    def span(g):
        a, b = g.iloc[0], g.iloc[-1]
        return f"{int(a['year'])}-{int(a['month']):02d} to {int(b['year'])}-{int(b['month']):02d}"

    r_recent, r_rest, r_ago = rate(recent), rate(rest), rate(year_ago.sort_values("ym"))
    if None in (r_recent, r_rest, r_ago):
        return None
    concentrated = r_recent >= ratio * r_ago and r_recent >= ratio * r_rest
    return dict(
        rise_is_concentrated_in_recent_months=bool(concentrated),
        recent_months=span(recent), recent_months_system_delay_rate_pct=r_recent,
        same_months_a_year_earlier_system_delay_rate_pct=r_ago,
        other_months_of_latest_12=span(rest), other_months_system_delay_rate_pct=r_rest,
        note=(f"The latest-12-month rate is driven by its newest {n} months, which run at least {ratio}x the same months a year earlier and "
              f"{ratio}x the rest of the latest 12. This can be a temporary event (for example runway work or one bad season), which is not "
              "in the data. Report it as a recent spike, not as a steady worsening.") if concentrated else
             f"The newest {n} months are in line with the same months a year earlier or with the rest of the latest 12: no recent spike.")


def airport_profile(airport_code, year=None, long_haul_miles=None) -> dict:
    s = store()
    cfg = s["cfg"]
    code = _resolve(airport_code)
    if not code:
        return _unknown(airport_code)
    r = s["by_code"].loc[code]
    route_years = sorted(int(y) for y in s["airport_routes"]["year"].unique())
    years_available = sorted(int(y) for y in s["airport_year"]["year"].unique())
    if year is not None and year not in years_available:
        return _err(f"No data for {year}.", year=years_available)
    cutoffs = list(cfg["long_haul_cutoffs"])
    headline_cut = cfg["long_haul_miles_default"]
    if long_haul_miles is not None:
        try:
            headline_cut = int(long_haul_miles)
        except (TypeError, ValueError):
            return _err("long_haul_miles must be a number of miles, for example 2300.")
        if not 500 <= headline_cut <= 8000:
            return _err("long_haul_miles must be between 500 and 8000.")
        cutoffs = sorted(set(cutoffs + [headline_cut]))
    lh_year = year if year in route_years else (cfg["route_year_latest_full"] if year is None else None)
    lh = _long_haul_table(code, lh_year, cutoffs) if lh_year else None
    long_haul = None
    if lh:
        head = next(x for x in lh["by_cutoff"] if x["cutoff_miles"] == headline_cut)
        long_haul = dict(headline_cutoff_miles=headline_cut, headline_share_of_passenger_flights_pct=head["share_of_passenger_flights_pct"],
                         headline_share_of_all_flights_including_cargo_pct=head["share_of_all_flights_including_cargo_pct"], **lh,
                         note="Share of DEPARTING flights flying at least the cutoff distance, domestic plus international, all airlines. "
                              "There is no official definition of long-haul; 3,000 miles is our default and the cutoff is adjustable. "
                              "Passenger flights are the headline; the cargo-included share is shown because at cargo hubs the two differ a lot.")
    history = [dict(year=int(h["year"]), months_of_passenger_data=_v(h["months_of_data"]), is_partial_year=bool(h["is_partial_year"]) if pd.notna(h["is_partial_year"]) else None,
                    passengers=_v(h["passengers"]), load_factor_pct=_v(h["load_factor_pct"]), months_of_delay_data=_v(h["delay_months_of_data"]),
                    system_delay_rate_pct=_v(h["system_delay_rate_pct"]), total_delay_rate_pct=_v(h["total_delay_rate_pct"]))
               for h in s["airport_year"][s["airport_year"]["airport_code"] == code].to_dict("records")]

    if year is not None:
        h = next((x for x in history if x["year"] == year), None)
        period = f"calendar {year}" + (" (PARTIAL year)" if h and (h["is_partial_year"] or (h["months_of_delay_data"] or 12) < 12) else "")
        notes = [f"Year view: {period}. Past years return raw metrics only; scores exist for the latest period only.",
                 f"Long-haul and cargo shares exist only for {route_years}.",
                 "Warnings below describe the airport today (for example legal limits) and still apply."]
        return _wrap("airport_profile", dict(airport_code=code, year=year, long_haul_miles=long_haul_miles),
                     dict(airport=_identity(r), period=period, year_values=h, long_haul=long_haul, all_years=history),
                     YEAR_METRICS, [code], notes, period_override=period)

    d = _summary(r)
    d.update(faa_code=r["faa_code"], metro_area=_v(r["metro_name"]), rank_overall=_v(r["rank_overall"]),
             ranked_airports_overall=_v(r["ranked_airports_overall"]), data_quality_note=r["data_quality_note"])
    scored_detail = {m: dict(value=_v(r[m]), position_among_full_data_airports_0_to_100=_v(r[m.replace("_pct", "_score")])) for m in FIVE}
    strained = bool(r["is_strained"])
    extra_ops, g = _v(r["forecast_extra_operations"]), _v(r["forecast_flight_growth_pct"])
    flight_demand = dict(
        label="unmet flight demand (estimate)" if strained else "forecast flight growth (NOT called unmet demand: this airport is not strained)",
        is_strained=strained,
        forecast_extra_operations=extra_ops, forecast_operations_2025=_v(r["forecast_operations_2025"]),
        forecast_operations_2035=_v(r["forecast_operations_2035"]), forecast_flight_growth_pct=g,
        system_delay_rate_pct=_v(r["system_delay_rate_pct"]), system_delay_rate_latest_year_pct=_v(r["system_delay_rate_latest_year_pct"]),
        system_delay_rate_position_0_to_100=_v(r["system_delay_rate_score"]), flight_score=_v(r["flight_score"]),
        method=("Estimate, not a measurement: FAA forecast commercial operations (takeoffs plus landings, cargo included) in fiscal 2035 minus fiscal 2025. "
                "Unmet demand cannot be observed directly. The gap is called unmet demand only when the airport is strained today "
                f"(system delay rate in the top quarter of full-data airports), because growth is only unmet if the airport cannot absorb it. "
                "The FAA tends to over-forecast."))
    result = dict(
        airport=d, scored_metrics=scored_detail,
        flight_demand=flight_demand,
        passenger_demand=dict(forecast_extra_boardings=_v(r["forecast_extra_boardings"]), forecast_boardings_2025=_v(r["forecast_boardings_2025"]),
                              forecast_boardings_2035=_v(r["forecast_boardings_2035"]), passengers_latest_12_months=_v(r["passengers_latest_12_months"]),
                              passengers_2019=_v(r["passengers_2019"]), seats_change_since_2019_pct=_v(r["seats_change_since_2019_pct"])),
        delays=dict(system_delay_rate_pct=_v(r["system_delay_rate_pct"]), system_delay_rate_latest_year_pct=_v(r["system_delay_rate_latest_year_pct"]),
                    total_delay_rate_pct=_v(r["total_delay_rate_pct"]), arriving_flights_3_years=_v(r["arriving_flights_3_years"]),
                    latest_12_months_pattern=_recent_delay_pattern(code),
                    causes_share_of_delayed_flights_pct={k: _v(r[f"delay_cause_{k}_pct"]) for k in ["system", "airline", "late_aircraft", "weather", "security"]},
                    causes_note="Shares of flights delayed 15+ minutes, by the cause the airline reported, three years. 'system' = airport and air-traffic system (includes ordinary weather); 'weather' = extreme weather only."),
        long_haul=long_haul,
        context=dict(cargo_share_of_flights_pct=_v(r["cargo_share_of_flights_pct"]), top_airline=_v(r["top_airline"]),
                     top_airline_share_pct=_v(r["top_airline_share_pct"]), domestic_share_pct=_v(r["domestic_share_pct"]),
                     busiest_month=_v(r["busiest_month"]), busiest_month_passengers=_v(r["busiest_month_passengers"]),
                     busiest_month_load_factor_pct=_v(r["busiest_month_load_factor_pct"]),
                     passengers_per_flight=_v(r["passengers_per_flight"]), passengers_per_flight_2019=_v(r["passengers_per_flight_2019"]),
                     passenger_flights_change_since_2019_pct=_v(r["passenger_flights_change_since_2019_pct"])),
        history_by_year=history,
        info_notes=[w["message"] for w in _warnings([code], severities=("info",))])
    notes = ["Scores are relative positions (0-100) among full-data airports and a proxy for profit: they rank how much added capacity would be filled. No cost or return data exists.",
             "No public data measures terminal or gate utilization, or peak-hour demand. The score does not know about capacity already under construction.",
             "FAA operations (takeoffs plus landings, cargo included) are not comparable with BTS departures."]
    metric_ids = SCORE_COLS + FIVE + ["system_delay_rate_latest_year_pct", "total_delay_rate_pct", "boardings_2025", "forecast_extra_boardings",
                                     "forecast_extra_operations", "cargo_share_of_flights_pct", "long_haul_share_pct", "top_airline_share_pct",
                                     "domestic_share_pct", "seats_change_since_2019_pct", "passengers_latest_12_months",
                                     "passenger_flights_change_since_2019_pct", "passengers_per_flight"]
    return _wrap("airport_profile", {k: v for k, v in dict(airport_code=code, long_haul_miles=long_haul_miles).items() if v is not None},
                 result, metric_ids, [code], notes)


# ---------- 5. airport_trend ----------

def _parse_month(text):
    m = re.match(r"^(\d{4})-(\d{1,2})$", str(text).strip())
    if not m or not 1 <= int(m.group(2)) <= 12:
        return None
    return int(m.group(1)) * 100 + int(m.group(2))


def airport_trend(airport_code, metric, start_month=None, end_month=None) -> dict:
    s = store()
    code = _resolve(airport_code)
    if not code:
        return _unknown(airport_code)
    if metric not in TREND_METRICS:
        return _err(f"'{metric}' has no monthly series.", metric=TREND_METRICS)
    mt = s["airport_month"]
    mt = mt[mt["airport_code"] == code].copy()
    mt["ym"] = mt["year"] * 100 + mt["month"]
    mt = mt[mt[metric].notna()]
    if mt.empty:
        return _err(f"No monthly {metric} data for {code}." + (" The airlines serving it do not report delays." if "delay" in metric else ""))
    first, last = int(mt["ym"].min()), int(mt["ym"].max())
    lo = _parse_month(start_month) if start_month else None
    hi = _parse_month(end_month) if end_month else None
    if (start_month and lo is None) or (end_month and hi is None):
        return _err("Months must look like 2024-08.", available=f"{first // 100}-{first % 100:02d} to {last // 100}-{last % 100:02d}")
    hi = hi or last
    if lo is None:
        y, m = hi // 100, hi % 100
        lo = (y - 3) * 100 + m + 1 if m < 12 else (y - 2) * 100 + 1   # default: the latest 36 months
    mt = mt[(mt["ym"] >= lo) & (mt["ym"] <= hi)].sort_values("ym")
    if mt.empty:
        return _err("No data in that range.", available=f"{first // 100}-{first % 100:02d} to {last // 100}-{last % 100:02d}")
    series = [dict(month=f"{int(r['year'])}-{int(r['month']):02d}", value=_v(r[metric])) for r in mt.to_dict("records")]
    top, low = mt.loc[mt[metric].idxmax()], mt.loc[mt[metric].idxmin()]
    # seasonal profile: each calendar month across the range, rates from summed counts
    season = []
    for mo, g in mt.groupby("month"):
        if metric == "load_factor_pct":
            val = F.load_factor(float(g["passengers"].sum()), float(g["seats"].sum()))
        elif metric == "system_delay_rate_pct":
            val = F.rate_pct(float(g["system_delays"].sum()), float(g["arriving_flights"].sum()))
        elif metric == "total_delay_rate_pct":
            val = F.rate_pct(float(g["delayed_flights"].sum()), float(g["arriving_flights"].sum()))
        else:
            val = _v(round(float(g[metric].mean())))
        season.append(dict(calendar_month=MONTHS[int(mo) - 1], value=val, months_included=len(g)))
    peak = max((x for x in season if x["value"] is not None), key=lambda x: x["value"])
    period = f"{series[0]['month']} to {series[-1]['month']}"
    incomplete = mt[mt["is_complete_month"] == False]  # noqa: E712
    notes = [f"Monthly series for {period}. Data available {first // 100}-{first % 100:02d} to {last // 100}-{last % 100:02d}.",
             "seasonal_profile gives each calendar month across the range (rates from summed counts; counts as the average per month).",
             "A monthly delay rate needs at least 100 arriving flights; months below that are left out."]
    if len(incomplete):
        notes.append("The newest month(s) may be incomplete because airlines file late: " + ", ".join(f"{int(r['year'])}-{int(r['month']):02d}" for r in incomplete.to_dict("records")))
    return _wrap("airport_trend", {k: v for k, v in dict(airport_code=code, metric=metric, start_month=start_month, end_month=end_month).items() if v is not None},
                 dict(airport=_identity(s["by_code"].loc[code]), metric=metric, period=period, months_in_series=len(series),
                      highest=dict(month=f"{int(top['year'])}-{int(top['month']):02d}", value=_v(top[metric])),
                      lowest=dict(month=f"{int(low['year'])}-{int(low['month']):02d}", value=_v(low[metric])),
                      peak_calendar_month=peak, seasonal_profile=season, series=series),
                 [metric], [code], notes, period_override=period)


# ---------- registry ----------

TOOLS = {"find_airport": find_airport, "rank_airports": rank_airports, "compare_airports": compare_airports,
         "airport_profile": airport_profile, "airport_trend": airport_trend}


def call(name: str, arguments: dict) -> dict:
    """Run a tool by name. Unknown tools, wrong argument names and bad values come back as errors, never as
    exceptions: an exception here would leave the conversation with a tool call that has no result."""
    if name not in TOOLS:
        return _err(f"Unknown tool '{name}'.", tools=sorted(TOOLS))
    try:
        return TOOLS[name](**(arguments or {}))
    except Exception as err:
        return _err(f"Invalid input for {name}: {err}")
