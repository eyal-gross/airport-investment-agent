"""Formulas on made-up inputs with known answers, including the ugly edge cases.
The rule under test everywhere: when the inputs cannot support a number, the answer is None, never 0."""
from airport_agent.pipeline import formulas as F


def test_normal_values():
    assert F.load_factor(80, 100) == 80.0
    assert F.load_factor(826, 1000) == 82.6
    assert F.growth_pct(125, 100) == 25.0
    assert F.growth_pct(843, 1000) == -15.7
    assert F.rate_pct(173, 1000) == 17.3


def test_edge_cases_return_not_available():
    assert F.load_factor(50, 0) is None
    assert F.load_factor(50, None) is None
    assert F.load_factor(-5, 100) is None
    assert F.growth_pct(1000, 0) is None        # new airport: no base
    assert F.growth_pct(1000, None) is None
    assert F.growth_pct(None, 1000) is None
    assert F.rate_pct(0, 0) is None
    assert F.rate_pct(30, 87, min_total=1000) is None   # below the minimum sample
    assert F.rate_pct(100, 1000, min_total=1000) == 10.0


def test_long_haul_separates_cargo():
    routes = [[500, 800, 800], [2500, 150, 150], [3400, 50, 1050]]  # the long route is mostly cargo
    assert F.long_haul_share(routes, 3000, True) == 5.0
    assert F.long_haul_share(routes, 3000, False) == 52.5
    assert F.long_haul_share(routes, 2300, True) == 20.0
    assert F.long_haul_share([], 3000) is None
    assert F.long_haul_share([[4000, 0, 100]], 3000, True) is None   # cargo-only airport


def test_percentiles_are_rank_based():
    p = F.percentiles({"A": 10, "B": 20, "C": 30, "D": None})
    assert (p["A"], p["B"], p["C"]) == (0.0, 50.0, 100.0)
    assert "D" not in p                                   # missing is skipped, not scored as 0
    p = F.percentiles({"A": 5, "B": 5, "C": 9})
    assert p["A"] == p["B"] == 25.0                       # ties share a rank
    assert F.percentiles({"A": 7}) == {"A": 50.0}
    assert F.percentiles({"A": 1, "B": 2, "C": 3}) == F.percentiles({"C": 3, "B": 2, "A": 1})
    # one extreme outlier cannot stretch the scale
    assert F.percentiles({"A": 1, "B": 2, "C": 1400})["B"] == 50.0


def test_position_among_reference_group():
    assert F.position_among(25, [10, 20, 30, 40]) == 50.0
    assert F.position_among(5, [10, 20]) == 0.0
    assert F.position_among(None, [10, 20]) is None
    assert F.position_among(10, []) is None


def test_weighted_score_never_fills_or_shifts():
    assert F.weighted_score([(80, 0.5), (60, 0.25), (40, 0.25)]) == 65.0
    assert F.weighted_score([(80, 0.5), (None, 0.25), (40, 0.25)]) is None   # a missing input means no score
    assert F.weighted_score([]) is None
    assert F.mean_available([80, None, 40]) == 60.0
    assert F.mean_available([None, None]) is None


def test_default_airport_rule():
    assert F.pick_default([("BIG", 30_000_000), ("SML", 5_000_000)]) == "BIG"
    assert F.pick_default([("ONE", 12_000_000), ("TWO", 11_000_000)]) is None
    assert F.pick_default([("ONLY", 500_000)]) == "ONLY"
    assert F.pick_default([]) is None
