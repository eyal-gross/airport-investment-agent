"""The agent loop's failure paths, with the model replaced by scripted replies (no API key needed):
a tool that raises, an unexpected crash, the round cap, the rewrite and the fallback, and the trimming of old tool results."""
import pandas as pd

from airport_agent import agent as A
from airport_agent import llm
from airport_agent import tools as T
from airport_agent.pipeline import clean


def tool_reply(name, **inp):
    return llm.Reply(content=[], text="", tool_calls=[dict(id="1", name=name, input=inp)], stop_reason="tool_use")


def say(text):
    return llm.Reply(content=[], text=text, stop_reason="end_turn")


def scripted(monkeypatch, replies):
    it = iter(replies)
    monkeypatch.setattr(llm, "complete", lambda *a, **k: next(it))
    return A.Agent()


def roles(ag):
    return [m["role"] for m in ag.messages]


# ---------- tool errors ----------

def test_a_bad_tool_value_comes_back_as_an_error_not_an_exception():
    out = T.call("rank_airports", {"min_value": "abc"})
    assert "error" in out and "rank_airports" in out["error"]


def test_a_failed_tool_call_does_not_break_the_conversation(monkeypatch):
    ag = scripted(monkeypatch, [tool_reply("rank_airports", min_value="abc"), say("I could not run that."), say("Hello.")])
    first = ag.ask("Rank them")
    assert first.error is None and first.trace[0]["is_error"]
    assert roles(ag) == ["user", "assistant", "user", "assistant"]      # the tool call got its result
    assert ag.ask("Hi").text == "Hello."


def test_an_unexpected_crash_rolls_the_turn_back(monkeypatch):
    ag = scripted(monkeypatch, [tool_reply("airport_profile", airport_code="SFO"), say("Hello.")])
    monkeypatch.setattr(T, "call", lambda name, arguments: 1 / 0)
    crashed = ag.ask("Tell me about SFO")
    assert crashed.error and "ZeroDivisionError" in crashed.error and "went wrong" in crashed.text
    assert ag.messages == []                                            # no tool call left without a result
    assert ag.ask("Hi").text == "Hello."


# ---------- round cap, rewrite, fallback ----------

def test_the_round_cap_stops_a_tool_loop_and_leaves_a_valid_history(monkeypatch):
    ag = scripted(monkeypatch, [tool_reply("find_airport", query="SFO")] * A.MAX_ROUNDS + [say("Hello.")])
    capped = ag.ask("Loop forever")
    assert capped.rounds == A.MAX_ROUNDS and "could not finish" in capped.text
    assert roles(ag)[-1] == "assistant"
    assert ag.ask("Hi").text == "Hello."


def test_an_invented_number_is_rewritten_once(monkeypatch):
    ag = scripted(monkeypatch, [tool_reply("airport_profile", airport_code="SFO"), say("SFO has 115 gates."), say("SFO scores 86.9.")])
    ans = ag.ask("Tell me about SFO")
    assert ans.check == "rewritten" and ans.text == "SFO scores 86.9." and not ans.unverified


def test_a_second_invented_number_gives_the_code_built_answer(monkeypatch):
    ag = scripted(monkeypatch, [tool_reply("airport_profile", airport_code="SFO"), say("SFO has 115 gates."), say("SFO has 117 gates.")])
    ans = ag.ask("Tell me about SFO")
    assert ans.check == "fallback" and ans.unverified == ["117"]
    assert "117" not in ans.text and "straight from the data" in ans.text


def test_a_number_from_an_earlier_question_is_not_a_free_pass(monkeypatch):
    ag = scripted(monkeypatch, [say("Noted."), say("It has 2,300 gates."), say("I don't have gate counts.")])
    ag.ask("Use a 2,300 mile cutoff from now on")
    assert ag.ask("How many gates does SFO have?").check == "rewritten"   # 2,300 was typed, but not in this question


def test_a_number_from_the_models_own_background_is_allowed(monkeypatch):
    ag = scripted(monkeypatch, [say("Teterboro is not covered: primary airports have over 10,000 passenger boardings a year.")])
    assert ag.ask("What about Teterboro?").check == "passed"


# ---------- trimming old tool results ----------

def test_old_tool_results_are_stubbed_and_their_numbers_stop_counting(monkeypatch):
    airports = ["ANC", "SFO", "BOS", "LAX", "MEM"]
    ag = scripted(monkeypatch, [r for code in airports for r in (tool_reply("airport_profile", airport_code=code), say("Done."))]
                  + [say("Anchorage: 56.6% of flights are cargo."), say("I would need to look Anchorage up again.")])
    for code in airports:
        ag.ask(f"Tell me about {code}")
    results = [m["content"][0]["content"] for m in ag.messages if m["role"] == "user" and isinstance(m["content"], list)]
    assert results[0] == A.STUB and results[1] != A.STUB                 # ANC is gone; the latest three and the turn before them remain
    assert len(results[0]) < 200 < len(results[-1])
    late = ag.ask("What was Anchorage's cargo share again?")             # its figures are no longer in the conversation
    assert late.check == "rewritten"
    assert [r == A.STUB for r in [m["content"][0]["content"] for m in ag.messages if m["role"] == "user" and isinstance(m["content"], list)]] \
        == [True, True, False, False, False]


# ---------- the month helpers of the cleaning step ----------

def test_window_ending_crosses_the_year_boundary():
    assert clean.window_ending((2026, 2), 4) == [(2025, 11), (2025, 12), (2026, 1), (2026, 2)]
    assert len(clean.window_ending((2026, 4), 36)) == 36 and clean.window_ending((2026, 4), 36)[0] == (2023, 5)


def test_a_thinly_reported_newest_month_is_not_the_last_complete_month():
    months = [(2025, m) for m in range(1, 13)] + [(2026, 1), (2026, 2)]
    rows = [dict(year=y, month=m, airport_code=f"A{i}") for (y, m) in months for i in range(30 if (y, m) == (2026, 2) else 100)]
    assert clean.last_complete_month(pd.DataFrame(rows)) == (2026, 1)
    full = [dict(year=y, month=m, airport_code=f"A{i}") for (y, m) in months for i in range(100)]
    assert clean.last_complete_month(pd.DataFrame(full)) == (2026, 2)
