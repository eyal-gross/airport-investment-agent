"""Honesty safeguards that do not depend on the LLM behaving.

1. Number check: every number in the answer must match a number in a tool result still in the conversation
   (or in the user's current question, or in the background the model was given). It checks the value, not which airport or metric the value belongs to.
2. Footer: data period, assumptions and confidence are built by code from the tool results.
3. Confidence: High / Medium / Low by fixed rules, never the model's own opinion.
4. Warnings: taken from the tool results and printed under the answer, whether or not the model mentioned them.
5. Fallback: if the answer still fails the number check after one rewrite, show an answer built by code.
"""
import re

# ---------- 1. number check ----------

_NUM = re.compile(r"(?<![\w.])([-+]?\$?\d[\d,]*(?:\.\d+)?)(\s*(?:million|billion|thousand|[mMkKbB])\b)?(\s*%)?")
_SCALE = {"million": 1e6, "m": 1e6, "billion": 1e9, "b": 1e9, "thousand": 1e3, "k": 1e3}
ALWAYS_OK = {100.0}                 # the 0-100 scale
YEAR_RANGE = (1990, 2060)


def numbers_in_data(obj, acc=None) -> set:
    """Every number that appears anywhere in a tool result: values, and numbers inside text fields."""
    acc = set() if acc is None else acc
    if isinstance(obj, bool) or obj is None:
        return acc
    if isinstance(obj, (int, float)):
        acc.add(float(obj))
    elif isinstance(obj, str):
        for m in _NUM.finditer(obj):
            v = _parse(m)
            if v is not None:
                acc.add(v[0])
    elif isinstance(obj, dict):
        for v in obj.values():
            numbers_in_data(v, acc)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            numbers_in_data(v, acc)
    return acc


def _parse(m):
    """Returns (value, tolerance, raw text, is_plain_integer). The tolerance is half a unit of the last digit
    written, so a written number passes when some tool number rounds to it."""
    raw = m.group(1).lstrip("+$").replace("$", "")
    digits = raw.replace(",", "").lstrip("-")
    try:
        value = float(raw.replace(",", ""))
    except ValueError:
        return None
    scale = _SCALE.get((m.group(2) or "").strip().lower(), 1.0)
    if "." in digits:
        unit = 10 ** -len(digits.split(".")[1])
    else:
        stripped = digits.rstrip("0")
        unit = 10 ** (len(digits) - len(stripped)) if stripped and len(digits) > 3 else 1   # 108,000 -> thousands
    tol = 0.5 * unit * scale
    value *= scale
    if abs(value) >= 100:
        tol = max(0.5, min(tol, 0.025 * abs(value)))     # round numbers may be approximate, but not by more than 2.5%
    plain_int = "." not in digits and scale == 1.0 and not m.group(3)
    return value, tol + 1e-9, m.group(0).strip(), plain_int


def unverified_numbers(answer: str, data_numbers: set, allowed_text: str = "") -> list[str]:
    """Numbers written in the answer that no tool result supports. Not flagged: years, small counts
    ("top 5", list numbering), the 0-100 scale, and numbers the user typed themselves.
    A number written with a sign must match a tool number of that sign; an unsigned one matches either, because
    prose carries the direction in words ("down 5.0%"). This is a membership check: it catches invented values,
    not a real value attached to the wrong airport or metric."""
    allowed = numbers_in_data(allowed_text)
    pool = sorted(data_numbers | allowed)
    text = re.sub(r"\b[A-Z]{2,3}\d+\b", " ", answer)                       # codes like T100
    text = re.sub(r"\bT-100\b|\b24/7\b", " ", text)
    text = re.sub(r"\b\d{4}-\d{2}(?:-\d{2})?\b", " ", text)                # months and dates like 2025-10
    missing = []
    for m in _NUM.finditer(text):
        parsed = _parse(m)
        if parsed is None:
            continue
        value, tol, raw, plain_int = parsed
        a = abs(value)
        if plain_int and (a <= 12 or YEAR_RANGE[0] <= a <= YEAR_RANGE[1]):
            continue
        if a in ALWAYS_OK:
            continue
        lead = m.group(1)[0]
        before = text[m.start() - 1] if m.start() else " "
        sign = 1 if lead == "+" else -1 if lead == "-" and (before.isspace() or before == "(") else 0   # "4.8%-5.0%" is a range
        if any(abs(a - abs(p)) <= tol and sign * p >= 0 for p in pool):
            continue
        if raw not in missing:
            missing.append(raw)
    return missing


# ---------- 2-4. footer, confidence, warnings ----------

RANK_ORDER = {"high": 0, "medium": 1, "low": 2}


def has_figures(text: str) -> bool:
    """True when the text contains at least one number the check would examine (not a year, small count or the scale)."""
    for m in _NUM.finditer(text or ""):
        parsed = _parse(m)
        if parsed and not (parsed[3] and (abs(parsed[0]) <= 12 or YEAR_RANGE[0] <= abs(parsed[0]) <= YEAR_RANGE[1])) and abs(parsed[0]) not in ALWAYS_OK:
            return True
    return False


def _data_tools(trace: list[dict], answer_text: str = "") -> list[dict]:
    """The tool results an answer's figures rest on. find_airport only identifies airports, so it counts as a data
    source only when it is the sole tool used and the answer nevertheless quotes figures (its headline scores)."""
    ok = [t for t in trace if not t.get("is_error") and isinstance(t["output"], dict) and "meta" in t["output"]]
    data = [t for t in ok if t["name"] != "find_airport"]
    if not data and has_figures(answer_text):
        data = [t for t in ok if t["output"]["result"].get("candidates")]
    return data


def rests_on_data(trace: list[dict], answer_text: str = "") -> bool:
    """True when this turn's own tool results carry the answer's figures."""
    return bool(_data_tools(trace, answer_text))


def collect_warnings(trace: list[dict], limit: int = 12) -> list[dict]:
    seen, out = set(), []
    for t in _data_tools(trace):
        for w in t["output"].get("warnings", []):
            key = (w["airport_code"], w["type"], w["message"])
            if key not in seen:
                seen.add(key)
                out.append(w)
    out.sort(key=lambda w: (w["type"] != "legal_limit", w["severity"] != "blocking"))
    return out[:limit] + ([dict(airport_code="", type="more", severity="info", message=f"... and {len(out) - limit} more warnings; ask about a specific airport to see them.")] if len(out) > limit else [])


PROXY_WORDS = re.compile(r"score|delay|congest|how full|planes full|load factor|forecast|unmet|strain", re.IGNORECASE)


def confidence(trace: list[dict], answer_text: str = "") -> tuple[str, str]:
    """Fixed rules (RISKS.md section 5).
    Low: partial or thin data, or a small sample, for an airport in the answer.
    Medium: a proxy is used, a legal limit applies, sources disagree, a name was resolved by default, or a partial year.
    High: full data, a direct measure, no data warnings (a business-risk warning such as a dominant airline does not lower it).
    In a ranking, a minority of weaker airports (a third or fewer of those listed) lowers the label to Medium, not Low,
    and they are named."""
    data = _data_tools(trace, answer_text)
    if not data:
        return "n/a", "no data figures were used in this reply"
    low, medium = [], []
    for t in data:
        out = t["output"]
        quality = out.get("data_quality", [])
        if t["name"] == "find_airport":      # only the candidates the answer actually talks about
            quality = [q for q in quality if q["airport_code"] in answer_text] or quality[:1]
        weak = []
        for q in quality:
            if q["data_tier"] != "full":
                weak.append(f"{q['airport_code']} has {'partial' if q['data_tier'] == 'partial' else 'too little'} data")
            elif q["data_confidence"] == "low":
                weak.append(f"{q['airport_code']}: {q['data_confidence_reason']}")
            elif q["data_confidence"] == "medium":
                medium.append(f"{q['airport_code']}: {q['data_confidence_reason']}")
        if weak and t["name"] == "rank_airports" and len(weak) <= len(quality) / 3:
            medium = [f"{len(weak)} of the {len(quality)} listed airports {'has' if len(weak) == 1 else 'have'} weaker data ({'; '.join(weak[:3])})"] + medium
        else:
            low += weak
        if out["meta"].get("uses_proxy") and (not answer_text or PROXY_WORDS.search(answer_text)):
            medium.append("the answer uses proxy measures (scores, system delay rate, load factor or forecasts)")
        if "PARTIAL" in str(out.get("result", {}).get("period", "")):
            medium.append("a partial year is involved")
    for t in trace:
        if t["name"] == "find_airport" and isinstance(t["output"], dict) and t["output"].get("meta", {}).get("resolved_by_default"):
            medium.append("an airport name was resolved by default")
    uniq = lambda xs: list(dict.fromkeys(xs))
    if low:
        return "Low", "; ".join(uniq(low)[:4])
    if medium:
        return "Medium", "; ".join(uniq(medium)[:4])
    return "High", "full data, direct measures, no data warnings"


# Which words in the answer make a source or a proxy relevant to it. A profile returns everything about an airport,
# so the footer lists only what the answer actually talks about (and everything, if nothing matches).
SOURCE_WORDS = {
    "BTS T-100 airport-month summary": r"passenger|how full|planes full|load factor|seat|growth|busiest|domestic",
    "FAA Terminal Area Forecast": r"forecast|unmet|takeoffs",
    "BTS Airline Delay Causes": r"delay|congest|strain",
    "FAA passenger boarding data CY2025": r"boarding|size class|hub",
    "BTS T-100 Segment": r"long-haul|long haul|cargo|airline|miles|passenger flights",
}
METRIC_WORDS = {
    "total_score": r"score", "passenger_score": r"passenger[- ]side", "flight_score": r"flight[- ]side",
    "load_factor_pct": r"how full|planes full|load factor|full planes|fuller", "forecast_passenger_growth_pct": r"forecast",
    "forecast_flight_growth_pct": r"forecast|unmet", "system_delay_rate_pct": r"system delay|congest",
}


def footer(trace: list[dict], answer_text: str = "") -> dict:
    """The three fixed lines under every answer, built from the tool results."""
    data = _data_tools(trace, answer_text)
    level, why = confidence(trace, answer_text)
    if not data:
        return dict(data_period="no data was used in this reply", assumptions="none", confidence=level, confidence_reason=why)
    said = lambda pattern: not answer_text or re.search(pattern, answer_text, re.IGNORECASE) is not None
    by_source, proxies, extra = {}, [], []
    for t in data:
        out = t["output"]
        res = out.get("result", {})
        for mid, d in out.get("definitions", {}).items():
            if d["source"] != "Computed":
                by_source.setdefault(d["source"], [])
                if d["period"] not in by_source[d["source"]]:
                    by_source[d["source"]].append(d["period"])
            if d.get("proxy_note") and d["name"] not in proxies and said(METRIC_WORDS.get(mid, ".")):
                proxies.append(d["name"])
        lh = res.get("long_haul") if isinstance(res, dict) else None
        if lh and t["name"] == "airport_profile" and said(r"long-haul|long haul"):
            extra.append(f"long-haul means {lh['headline_cutoff_miles']:,} miles or more (our definition; adjustable)")
        if isinstance(res, dict) and res.get("flight_demand") and said(r"unmet"):
            extra.append("'unmet flight demand' is an estimate from the FAA forecast, used only when the airport is strained today")
    for t in trace:
        if t["name"] == "find_airport" and isinstance(t["output"], dict) and t["output"].get("meta", {}).get("resolved_by_default"):
            code = t["output"]["result"].get("default_airport_code")
            extra.append(f"'{t['input'].get('query')}' was taken to mean {code}")
    assumptions = []
    if proxies:
        assumptions.append("proxies, not direct measurements: " + ", ".join(proxies[:6]))
    assumptions += list(dict.fromkeys(extra))
    if any(set(t["output"].get("definitions", {})) & {"total_score", "passenger_score", "flight_score"} for t in data) and said(r"score"):
        assumptions.append("scores are relative (position among full-data airports) and rank upside, not return - no cost data exists")
    relevant = {src: pers for src, pers in by_source.items() if said(SOURCE_WORDS.get(src, "."))} or by_source
    period_line = "; ".join(f"{src}, {' / '.join(pers[:2])}" for src, pers in relevant.items())
    return dict(data_period=period_line or "see the tool trace", assumptions="; ".join(assumptions) or "none beyond the definitions shown",
                confidence=level, confidence_reason=why)


def footer_markdown(f: dict) -> str:
    return (f"**Data period:** {f['data_period']}\n\n**Assumptions:** {f['assumptions']}\n\n"
            f"**Confidence:** {f['confidence']} - {f['confidence_reason']}")


# ---------- 5. fallback answer built by code ----------

def _fmt(v):
    if v is None:
        return "not available"
    if isinstance(v, bool):
        return "yes" if v else "no"
    if isinstance(v, (int, float)) and abs(v) >= 1000:
        return f"{v:,.0f}"
    return str(v)


def fallback_answer(trace: list[dict]) -> str:
    """A plain answer assembled from the tool results, with no LLM-written numbers."""
    lines = ["I could not verify every number in my written answer against the data, so here are the figures straight from the data instead."]
    for t in _data_tools(trace):
        out, res = t["output"], t["output"]["result"]
        name = lambda m: out["definitions"].get(m, {}).get("name", m)
        if t["name"] == "rank_airports":
            lines.append(f"\n**Ranking by {name(res['sorted_by'])}** ({', '.join(res['scope'])}; {res['airports_ranked']} airports ranked)")
            groups = res["ranking"] if isinstance(res["ranking"], dict) else {"": res["ranking"]}
            for g, rows in groups.items():
                if g:
                    lines.append(f"\n*{g}*")
                for r in rows:
                    lines.append(f"{r['position']}. {r['name']} ({r['airport_code']}, {r['state']}) - {name(res['sorted_by'])}: {_fmt(r['sort_value'])}; "
                                 f"passenger side {_fmt(r['passenger_score'])}, flight side {_fmt(r['flight_score'])}; boardings 2025: {_fmt(r['boardings_2025'])}")
            for e in res["excluded"]:
                lines.append(f"\nLeft out ({e['count']}): {e['reason']} - {', '.join(e['airports'])}")
        elif t["name"] == "compare_airports":
            lines.append(f"\n**Comparison** ({res['period']})")
            for c in res["comparisons"]:
                ratio = f", ratio {c['ratio_a_to_b']}" if "ratio_a_to_b" in c else ""
                lines.append(f"- {name(c['metric'])}: {c['a']} {_fmt(c['a_value'])} vs {c['b']} {_fmt(c['b_value'])} (difference {_fmt(c['difference_a_minus_b'])}{ratio})")
        elif t["name"] == "airport_profile":
            a = res["airport"]
            lines.append(f"\n**{a['name']} ({a['airport_code']})**")
            if "scored_metrics" in res:
                lines.append(f"- Scores: total {_fmt(a['total_score'])}, passenger side {_fmt(a['passenger_score'])}, flight side {_fmt(a['flight_score'])}")
                for m, v in res["scored_metrics"].items():
                    lines.append(f"- {name(m)}: {_fmt(v['value'])}")
                fd = res["flight_demand"]
                lines.append(f"- {fd['label']}: {_fmt(fd['forecast_extra_operations'])} extra takeoffs and landings a year by 2035 (FAA forecast)")
            elif res.get("year_values"):
                for k, v in res["year_values"].items():
                    lines.append(f"- {k}: {_fmt(v)}")
            lh = res.get("long_haul")
            if lh:
                lines.append(f"- Long-haul ({lh['headline_cutoff_miles']:,}+ miles, {lh['year']}): {_fmt(lh['headline_share_of_passenger_flights_pct'])}% of passenger flights; "
                             f"{_fmt(lh['headline_share_of_all_flights_including_cargo_pct'])}% of all flights including cargo")
        elif t["name"] == "airport_trend":
            lines.append(f"\n**{res['airport']['name']} - {name(res['metric'])}, {res['period']}**")
            lines.append(f"- Highest: {res['highest']['month']} ({_fmt(res['highest']['value'])}); lowest: {res['lowest']['month']} ({_fmt(res['lowest']['value'])})")
            pk = res["peak_calendar_month"]
            lines.append(f"- Peak calendar month: {pk['calendar_month']} ({_fmt(pk['value'])})")
    return "\n".join(lines)
