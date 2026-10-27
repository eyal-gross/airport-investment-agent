"""The number check must fail both ways it can go wrong: too loose (any number passes) and too strict
(flags 'top 3', years, cutoffs the user typed). Plus the computed confidence and the code-built footer."""
from airport_agent import safeguards as S
from airport_agent import tools as T

DATA = S.numbers_in_data({"rate": 17.3, "flights": 108307, "boardings": 36497303, "share": 2.8, "note": "at least 3,000 miles", "ratio": 1.23})


def check(text, user=""):
    return S.unverified_numbers(text, DATA, user)


def test_exact_and_rounded_numbers_pass():
    assert check("The rate is 17.3% and the share is 2.8%.") == []
    assert check("About 108,000 extra flights, or 108,307 exactly.") == []
    assert check("36.5 million boardings") == []
    assert check("roughly 36 million") == []
    assert check("a ratio of 1.23") == []
    assert check("flights of 3,000 miles or more") == []       # numbers inside tool text count


def test_invented_numbers_are_flagged():
    assert check("The rate is 19.4%.") == ["19.4%"]
    assert check("About 250,000 extra flights.") == ["250,000"]
    assert check("It has 115 gates.") == ["115"]
    assert check("40 million boardings") == ["40 million"]
    assert check("The rate is 17.9%.") == ["17.9%"]            # close is not good enough


def test_a_percentage_is_not_a_free_pass():
    assert check("12%") == ["12%"]                             # small integers are only exempt as plain counts


def test_counts_years_and_scale_are_not_flagged():
    assert check("The top 3 airports in 2023, on a 0-100 scale, since 2019.") == []
    assert check("Data through 2026-04.") == []
    assert check("1. Boston\n2. Burlington") == []


def test_numbers_the_user_typed_are_allowed():
    assert check("With a 2,300 mile cutoff") == ["2,300"]
    assert check("With a 2,300 mile cutoff", user="What if long-haul means over 2,300 miles?") == []


def _trace(name, inp, out):
    return [dict(name=name, input=inp, output=out, is_error="error" in out, ms=1)]


def test_confidence_is_computed_and_varies():
    low = S.confidence(_trace("airport_profile", {}, T.airport_profile("HVN")))          # partial data
    med = S.confidence(_trace("compare_airports", {}, T.compare_airports(["LAX", "SNA"])))  # proxy + legal limit
    none = S.confidence(_trace("find_airport", {}, T.find_airport("Teterboro")))
    assert low[0] == "Low" and med[0] == "Medium" and none[0] == "n/a"
    trend = S.confidence(_trace("airport_trend", {}, T.airport_trend("BOS", "passengers")))  # direct measure, clean airport
    assert trend[0] == "High"
    assert len({low[0], med[0], trend[0]}) == 3


def test_footer_and_warnings_come_from_the_tool_result():
    trace = _trace("compare_airports", {}, T.compare_airports(["LAX", "SNA"]))
    f = S.footer(trace)
    assert "BTS" in f["data_period"] and "prox" in f["assumptions"] and f["confidence"] == "Medium"
    w = S.collect_warnings(trace)
    assert w[0]["type"] == "legal_limit" and w[0]["airport_code"] == "SNA"       # shown even if the model forgets it


def test_a_follow_up_without_a_tool_call_keeps_the_footer_of_the_data_it_reuses(monkeypatch):
    from airport_agent import agent as A, llm

    replies = iter([
        llm.Reply(content=[], text="", tool_calls=[dict(id="1", name="airport_profile", input=dict(airport_code="SFO"))], stop_reason="tool_use"),
        llm.Reply(content=[], text="SFO scores 86.9.", stop_reason="end_turn"),
        llm.Reply(content=[], text="Its system delay rate is 13.4%, and seats are down 5.0% since 2019.", stop_reason="end_turn"),
        llm.Reply(content=[], text="You're welcome.", stop_reason="end_turn"),
    ])
    monkeypatch.setattr(llm, "complete", lambda *a, **k: next(replies))
    ag = A.Agent()
    first = ag.ask("Tell me about SFO")
    follow = ag.ask("Why?")                      # answered from the first turn's data, no new tool call
    assert not follow.trace and follow.check == "passed"
    assert follow.footer["confidence"] == first.footer["confidence"] == "Medium"
    assert "Airline Delay Causes" in follow.footer["data_period"] and "earlier in this conversation" in follow.footer["assumptions"]
    assert [w["type"] for w in follow.warnings] == [w["type"] for w in first.warnings]
    thanks = ag.ask("Thanks")                    # no figures: still no data footer
    assert thanks.footer["confidence"] == "n/a" and not thanks.warnings


def test_single_airline_warning_is_a_risk_not_a_data_problem():
    r = T.rank_airports(group_by_size_class=False, limit=1)
    top = r["result"]["ranking"][0]
    assert top["airport_code"] == "PGD" and top["data_confidence"] == "high"
    assert any(w["type"] == "single_airline" and "Allegiant" in w["message"] for w in r["warnings"])
    assert not any(w["type"] == "single_airline" for w in T.airport_profile("JFK")["warnings"])


def test_fallback_answer_uses_only_tool_numbers():
    out = T.airport_profile("ANC")
    text = S.fallback_answer(_trace("airport_profile", {}, out))
    assert "2.8" in text and "31.0" in text
    assert S.unverified_numbers(text, S.numbers_in_data(out)) == []


def test_a_written_sign_must_match_the_data():
    data = S.numbers_in_data({"change": -5.0, "growth": 26.7})
    assert S.unverified_numbers("Seats are down 5.0% since 2019.", data) == []      # direction in words
    assert S.unverified_numbers("Seats changed by -5.0%.", data) == []
    assert S.unverified_numbers("Seats changed by +5.0%.", data) == ["+5.0%"]
    assert S.unverified_numbers("Growth of +26.7%.", data) == []
    assert S.unverified_numbers("Growth of -26.7%.", data) == ["-26.7%"]
    assert S.unverified_numbers("Between 5.0%-26.7%.", data) == []                  # a range, not a minus sign
