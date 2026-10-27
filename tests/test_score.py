"""Scoring rules on a small made-up table: same input -> same score, missing is never 0, weights never shift."""
import pandas as pd

from airport_agent.pipeline import score

CFG = dict(strained_percentile=75, flights_flat_max_pct=2, passengers_up_min_pct=5, seats_cut_max_pct=-5, passengers_flat_max_pct=2)
WEIGHTS = {"load_factor_pct": ("passenger", 0.25), "passenger_growth_since_2019_pct": ("passenger", 0.125),
           "forecast_passenger_growth_pct": ("passenger", 0.125), "system_delay_rate_pct": ("flight", 0.25),
           "forecast_flight_growth_pct": ("flight", 0.25)}


def table():
    rows = [
        # code, load factor, growth, forecast pax, delay rate, forecast flights
        ("AAA", 90.0, 30.0, 40.0, 12.0, 30.0),   # top on everything
        ("BBB", 80.0, 10.0, 20.0, 6.0, 15.0),
        ("CCC", 70.0, -5.0, 10.0, 3.0, 5.0),     # bottom on everything
        ("NOD", 85.0, 20.0, 30.0, None, 20.0),   # no delay rate -> partial
        ("NEW", 82.0, None, 25.0, 5.0, 10.0),    # no 2019 base -> the stated exception
        ("THN", None, None, 12.0, 4.0, 8.0),     # no passenger data -> too thin
    ]
    df = pd.DataFrame(rows, columns=["airport_code"] + score.SCORED)
    df["size_class"] = "small"
    return df


def scored():
    return score.add_scores(table(), WEIGHTS, CFG).set_index("airport_code")


def test_scoring_is_deterministic():
    assert score.add_scores(table(), WEIGHTS, CFG).equals(score.add_scores(table(), WEIGHTS, CFG))


def test_best_and_worst():
    s = scored()
    assert s.at["AAA", "total_score"] == 100.0
    assert s.at["CCC", "total_score"] == 0.0
    assert s.at["AAA", "rank_overall"] == 1


def test_tiers():
    s = scored()
    assert s.at["AAA", "data_tier"] == "full"
    assert s.at["NOD", "data_tier"] == "partial"
    assert s.at["THN", "data_tier"] == "too_thin"


def test_missing_delay_rate_gives_passenger_score_only():
    s = scored()
    assert pd.notna(s.at["NOD", "passenger_score"])
    assert pd.isna(s.at["NOD", "flight_score"])      # not built from the forecast alone
    assert pd.isna(s.at["NOD", "total_score"])       # no total, no re-weighting
    assert pd.isna(s.at["NOD", "rank_overall"])


def test_too_thin_has_no_scores():
    s = scored()
    assert pd.isna(s.at["THN", "passenger_score"]) and pd.isna(s.at["THN", "total_score"])


def test_no_2019_base_exception():
    s = scored()
    r = s.loc["NEW"]
    assert r["no_2019_base"] and r["data_tier"] == "full"
    # the demand half rests on the forecast alone: half load factor, half forecast growth
    expected = round((r["load_factor_score"] * 0.25 + r["forecast_passenger_growth_score"] * 0.25) / 0.5, 1)
    assert r["passenger_score"] == expected
    assert pd.notna(r["total_score"])


def test_total_is_the_average_of_the_two_sides():
    r = scored().loc["BBB"]
    assert r["total_score"] == round((r["passenger_score"] + r["flight_score"]) / 2, 1)


def test_strained_means_top_quarter_delay_rate():
    s = scored()
    assert s.at["AAA", "is_strained"]
    assert not s.at["CCC", "is_strained"]
    assert not s.at["NOD", "is_strained"]


def test_capacity_cut_flag():
    df = pd.DataFrame(dict(passenger_growth_since_2019_pct=[0.0, 20.0, 10.0], seats_change_since_2019_pct=[-8.0, -8.0, 15.0],
                           passenger_flights_change_since_2019_pct=[-10.0, -10.0, 12.0]))
    out = score.add_flags(df, CFG)
    assert list(out["flag_capacity_cut"]) == [True, False, False]            # seats down AND passengers flat
    assert list(out["flag_flights_flat_passengers_up"]) == [False, True, False]
