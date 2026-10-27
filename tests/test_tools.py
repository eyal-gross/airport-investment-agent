"""The five tools against the committed serving tables: name matching, filters, the four core questions,
bad inputs, and the rules about missing data."""
import json

import pytest

from airport_agent import tools as T


def find(q):
    return T.find_airport(q)["result"]


def codes(result):
    return [c["airport_code"] for c in result["candidates"]]


# ---------- name matching (regressions seen in other solutions) ----------

def test_asheville_is_not_nashville():
    assert codes(find("Asheville")) == ["AVL"]
    assert codes(find("Nashville")) == ["BNA"]


def test_la_means_los_angeles_not_louisiana():
    r = find("LA")
    assert r["default_airport_code"] == "LAX"
    assert "SNA" in [a["airport_code"] for a in r["same_metro_area"]]
    assert "error" in T.find_airport("Louisiana")          # a state, pointed to the rank tool


def test_portland_in_two_states_asks():
    r = find("Portland")
    assert r["default_airport_code"] is None and set(codes(r)) == {"PDX", "PWM"}
    assert find("Portland, Maine")["default_airport_code"] == "PWM"


def test_served_city_and_nicknames():
    assert find("Providence")["default_airport_code"] == "PVD"      # filed under Warwick
    assert find("Glacier Park")["default_airport_code"] == "FCA"
    assert find("Santa Ana")["default_airport_code"] == "SNA"
    assert find("Boston Logan airport")["default_airport_code"] == "BOS"
    assert find("Burlington, Vermont")["default_airport_code"] == "BTV"


def test_dominant_airport_is_default_and_similar_ones_are_not():
    assert find("Dallas")["default_airport_code"] == "DFW"
    assert find("New York")["default_airport_code"] is None


def test_uncovered_airport():
    r = find("Teterboro")
    assert r["match_type"] == "none" and r["candidates"] == []


def test_faa_code_resolves_to_bts_code():
    assert T.airport_profile("IWA")["result"]["airport"]["airport_code"] == "AZA"


# ---------- the four core questions ----------

def test_q1_new_england_ranking():
    r = T.rank_airports(region="new england")
    states = {a["state"] for a in r["result"]["ranking"]}
    assert states <= {"CT", "ME", "MA", "NH", "RI", "VT"}
    scores = [a["total_score"] for a in r["result"]["ranking"]]
    assert scores == sorted(scores, reverse=True) and all(s is not None for s in scores)
    excluded = json.dumps(r["result"]["excluded"])
    assert "HVN" in excluded                                 # New Haven has no delay data: named, not ranked


def test_q2_lax_vs_sna_has_differences_and_the_legal_cap():
    r = T.compare_airports(["LAX", "SNA"])
    c = next(x for x in r["result"]["comparisons"] if x["metric"] == "system_delay_rate_pct")
    assert c["difference_a_minus_b"] == round(c["a_value"] - c["b_value"], 1) and "ratio_a_to_b" in c
    legal = [w for w in r["warnings"] if w["type"] == "legal_limit"]
    assert legal and legal[0]["airport_code"] == "SNA" and "million" in legal[0]["message"]


def test_q3_anchorage_long_haul_showcase():
    lh = T.airport_profile("ANC")["result"]["long_haul"]
    assert lh["headline_cutoff_miles"] == 3000
    assert lh["headline_share_of_passenger_flights_pct"] == 2.8
    assert lh["headline_share_of_all_flights_including_cargo_pct"] == 31.0
    assert [x["cutoff_miles"] for x in lh["by_cutoff"]] == [2000, 2500, 3000]


def test_q3_custom_cutoff_updates_the_headline():
    lh = T.airport_profile("ANC", long_haul_miles=2300)["result"]["long_haul"]
    assert lh["headline_cutoff_miles"] == 2300
    row = next(x for x in lh["by_cutoff"] if x["cutoff_miles"] == 2300)
    assert lh["headline_share_of_passenger_flights_pct"] == row["share_of_passenger_flights_pct"]


def test_q4_unmet_demand_only_when_strained():
    sfo = T.airport_profile("SFO")["result"]["flight_demand"]
    assert sfo["is_strained"] and sfo["label"].startswith("unmet flight demand")
    assert sfo["forecast_extra_operations"] == sfo["forecast_operations_2035"] - sfo["forecast_operations_2025"]
    oak = T.airport_profile("OAK")["result"]["flight_demand"]
    assert not oak["is_strained"] and "NOT called unmet demand" in oak["label"]


def test_recent_delay_spike_is_flagged_only_when_the_newest_months_stand_out():
    cfg = T.store()["cfg"]
    flagged = 0
    for code in ["SFO", "LAX", "BOS", "EWR", "ANC", "BTV"]:
        p = T.airport_profile(code)["result"]["delays"]["latest_12_months_pattern"]
        recent, ago, rest = (p["recent_months_system_delay_rate_pct"], p["same_months_a_year_earlier_system_delay_rate_pct"],
                             p["other_months_system_delay_rate_pct"])
        expected = recent >= cfg["recent_spike_ratio"] * ago and recent >= cfg["recent_spike_ratio"] * rest
        assert p["rise_is_concentrated_in_recent_months"] == expected
        assert ("as a recent spike" in p["note"]) == expected
        flagged += expected
    assert T.airport_profile("SFO")["result"]["delays"]["latest_12_months_pattern"]["rise_is_concentrated_in_recent_months"]
    assert flagged < 6      # the flag separates airports; it is not always on


# ---------- rules ----------

def test_every_result_has_the_uniform_shape():
    for r in [T.find_airport("SFO"), T.rank_airports(states=["TX"]), T.compare_airports(["BOS", "PVD"]),
              T.airport_profile("MEM"), T.airport_trend("BTV", "passengers")]:
        assert {"result", "definitions", "warnings", "data_quality", "notes", "meta"} <= set(r)
        for d in r["definitions"].values():
            assert d["unit"] and d["source"] and d["period"]     # no bare numbers


def test_partial_airport_gets_passenger_score_only():
    a = T.airport_profile("HVN")
    assert a["result"]["airport"]["data_tier"] == "partial"
    assert a["result"]["airport"]["total_score"] is None and a["result"]["airport"]["passenger_score"] is not None
    assert any(w["severity"] == "blocking" for w in a["warnings"])


def test_ranking_by_score_is_not_available_for_past_years():
    r = T.rank_airports(sort_by="total_score", year=2021)
    assert "error" in r and "sort_by_with_year" in r["valid_options"]


def test_year_view_keeps_warnings_and_states_its_period():
    r = T.compare_airports(["LAX", "SNA"], year=2023)
    assert r["result"]["period"].startswith("calendar 2023")
    assert any(w["type"] == "legal_limit" for w in r["warnings"])
    assert r["definitions"]["system_delay_rate_pct"]["period"].startswith("calendar 2023")


def test_partial_year_is_marked():
    r = T.airport_profile("SFO", year=2026)
    assert "PARTIAL" in r["result"]["period"]


def test_national_ranking_is_grouped_by_size_class():
    r = T.rank_airports()
    assert set(r["result"]["ranking"]) == {"large", "medium", "small", "nonhub"}


def test_month_ranking():
    r = T.rank_airports(sort_by="system_delay_rate_pct", month=8, limit=3)
    assert len(r["result"]["ranking"]) == 3 and "August" in r["definitions"]["system_delay_rate_pct"]["period"]


def test_season_ranking_equals_its_three_months_added_up():
    r = T.rank_airports(sort_by="system_delay_rate_pct", season="summer", size_classes=["large"], limit=30)
    period = r["definitions"]["system_delay_rate_pct"]["period"]
    assert "summer (June, July, August)" in period and "summed" in period
    years = [int(y) for y in period.split(" of ")[1].split(" (")[0].split(", ")]
    mt = T.store()["airport_month"]
    for row in (r["result"]["ranking"][0], r["result"]["ranking"][-1]):
        g = mt[(mt["airport_code"] == row["airport_code"]) & mt["month"].isin([6, 7, 8]) & mt["year"].isin(years)]
        assert len(g) == 9      # three complete summers, never a half season
        assert row["sort_value"] == round(100 * g["system_delays"].sum() / g["arriving_flights"].sum(), 1)
    values = [a["sort_value"] for a in r["result"]["ranking"]]
    assert values == sorted(values, reverse=True)
    one_year = T.rank_airports(sort_by="passengers", season="winter", year=2024, airport_codes=["BOS"])
    g = mt[(mt["airport_code"] == "BOS") & mt["month"].isin([12, 1, 2]) & (mt["year"] == 2024)]
    assert one_year["result"]["ranking"][0]["sort_value"] == int(g["passengers"].sum())
    assert T.rank_airports(season="autumn", sort_by="passengers")["result"]["ranking"]      # 'autumn' is accepted as fall


@pytest.mark.parametrize("kwargs", [dict(season="monsoon", sort_by="passengers"), dict(season="summer", month=7, sort_by="passengers"),
                                    dict(season="summer"), dict(season="summer", sort_by="passengers", year=1999)])
def test_season_bad_inputs_are_errors_not_exceptions(kwargs):
    assert T.call("rank_airports", kwargs).get("error")


def test_filters():
    r = T.rank_airports(size_classes=["large"], sort_by="load_factor_pct", min_value=85)
    assert all(a["size_class"] == "large" and a["load_factor_pct"] >= 85 for a in r["result"]["ranking"])
    r = T.rank_airports(states=["Texas"], sort_by="load_factor_pct", limit=5)
    assert all(a["state"] == "TX" for a in r["result"]["ranking"])
    r = T.rank_airports(region="west", min_data_confidence="high")
    assert all(a["data_confidence"] == "high" for a in r["result"]["ranking"])


@pytest.mark.parametrize("bad", [
    lambda: T.rank_airports(region="europe"),
    lambda: T.rank_airports(size_classes=["huge"]),
    lambda: T.rank_airports(sort_by="vibes"),
    lambda: T.compare_airports(["LAX"]),
    lambda: T.airport_profile("TEB"),
    lambda: T.airport_trend("SFO", "gates"),
    lambda: T.call("rank_airports", {"regoin": "west"}),
    lambda: T.call("run_sql", {"q": "select 1"}),
])
def test_bad_inputs_return_an_error_with_options_not_an_exception(bad):
    assert "error" in bad()


def test_trend_series():
    r = T.airport_trend("BTV", "passengers", "2024-01", "2025-12")["result"]
    assert r["months_in_series"] == 24 and r["highest"]["value"] >= r["lowest"]["value"]
