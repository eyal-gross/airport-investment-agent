"""Pure metric formulas. No file access here, so every one is tested with made-up inputs and known answers.

Rule for all of them: when the inputs cannot support a number, return None - never 0.
"""


def load_factor(passengers, seats):
    if not seats or seats <= 0 or passengers is None or passengers < 0:
        return None
    return round(100.0 * passengers / seats, 1)


def growth_pct(now, base):
    if now is None or base is None or base <= 0 or now < 0:
        return None
    return round(100.0 * (now / base - 1), 1)


def rate_pct(count, total, min_total=0):
    if count is None or total is None or total <= 0 or total < min_total or count < 0:
        return None
    return round(100.0 * count / total, 1)


def long_haul_share(routes, cutoff_miles, passenger_only=True):
    """routes: list of [distance_miles, passenger_flights, all_flights]. Share of flights at or beyond the cutoff."""
    idx = 1 if passenger_only else 2
    total = sum(r[idx] for r in routes)
    if total <= 0:
        return None
    return round(100.0 * sum(r[idx] for r in routes if r[0] >= cutoff_miles) / total, 1)


def percentiles(values):
    """values: {key: number or None}. Returns {key: 0-100 rank position} for keys that have a value.

    Rank-based, so one extreme value cannot stretch the scale. Ties share the average rank.
    """
    have = sorted((v, k) for k, v in values.items() if v is not None)
    n = len(have)
    out = {}
    i = 0
    while i < n:
        j = i
        while j + 1 < n and have[j + 1][0] == have[i][0]:
            j += 1
        pct = 100.0 * ((i + j) / 2) / (n - 1) if n > 1 else 50.0
        for t in range(i, j + 1):
            out[have[t][1]] = round(pct, 1)
        i = j + 1
    return out


def position_among(value, reference):
    """0-100 position of one value against a reference group it is not part of (used for partial-data airports).

    Share of the reference group below the value, counting ties as half.
    """
    ref = [r for r in reference if r is not None]
    if value is None or not ref:
        return None
    below = sum(1 for r in ref if r < value)
    equal = sum(1 for r in ref if r == value)
    return round(100.0 * (below + 0.5 * equal) / len(ref), 1)


def weighted_score(parts):
    """parts: list of (score 0-100 or None, weight). Returns None if ANY part is missing.

    A missing input is never treated as 0 and its weight is never shifted onto the others.
    """
    if not parts or any(s is None for s, _ in parts):
        return None
    total_weight = sum(w for _, w in parts)
    if total_weight <= 0:
        return None
    return round(sum(s * w for s, w in parts) / total_weight, 1)


def mean_available(parts):
    vals = [p for p in parts if p is not None]
    return round(sum(vals) / len(vals), 1) if vals else None


def pick_default(candidates):
    """candidates: list of (code, yearly_boardings). A default exists only if one airport clearly dominates
    (at least twice the boardings of the next one)."""
    c = sorted(candidates, key=lambda x: -(x[1] or 0))
    if not c:
        return None
    if len(c) == 1:
        return c[0][0]
    second = c[1][1] or 0
    if second == 0:
        return c[0][0]
    return c[0][0] if c[0][1] >= 2 * second else None
