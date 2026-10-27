"""The agent: a plain tool loop. Text in, answer out - so a voice layer can wrap it without touching it.

The LLM chooses tools and writes the explanation. It cannot read files, query data or compute: every number
reaches the answer only through a tool result, and the answer is checked against those results before it is shown.
"""
import json
import logging
import time
from dataclasses import dataclass, field

from . import llm, safeguards, tools
from .paths import LOGS

MAX_ROUNDS = 8      # cap on model calls per question, so a tool loop can never run away
KEEP_DATA_TURNS = 3 # tool results of this many earlier data-fetching turns stay in the conversation; older ones become a stub
STUB = "[Older tool result removed to keep the conversation short. Call the tool again if you need these figures.]"
CHECK_PREFIX = "[Automatic check"

TOOL_SPECS = [
    {
        "name": "find_airport",
        "description": (
            "Resolve an airport name, city, nickname or code to airport codes among the covered FAA primary airports. "
            "Use it first whenever the user names an airport or city in words (for example 'LA', 'Santa Ana', 'Anchorage airport'), "
            "before calling compare_airports, airport_profile or airport_trend. It returns the candidates, the other airports in the same "
            "metro area, and a default_airport_code only when one airport clearly dominates; follow its guidance about asking the user. "
            "Do not use it for a state or a region (use rank_airports), and you can skip it when the user gives a three-letter code. "
            "It returns only identification and headline scores, not detailed metrics."),
        "input_schema": {"type": "object", "additionalProperties": False, "required": ["query"], "properties": {
            "query": {"type": "string", "description": "Airport name, city, nickname or code, e.g. 'Santa Ana', 'LA', 'Burlington, Vermont', 'SFO'."}}},
    },
    {
        "name": "rank_airports",
        "description": (
            "Rank a group of airports by the capacity-need score or by one metric, with filters. Use it for 'which airports...', 'top N...', "
            "'best candidates in <region/state>' and threshold questions ('planes over 85% full'). By default it ranks only airports with full data "
            "and names the ones it leaves out; a national ranking by score is returned per size class. Past years (year), calendar months (month) and seasons (season) "
            "rank a raw metric only, because the score exists for the latest period only. "
            "Do not use it to compare two or three named airports (use compare_airports) or to describe one airport (use airport_profile). "
            "Examples: {region:'new england'} ; {states:['TX'], sort_by:'load_factor_pct', limit:5} ; "
            "{size_classes:['small'], sort_by:'system_delay_rate_pct', limit:3} ; {sort_by:'system_delay_rate_pct', month:8, limit:3} ; "
            "{region:'northeast', sort_by:'load_factor_pct', season:'summer'}."),
        "input_schema": {"type": "object", "additionalProperties": False, "properties": {
            "region": {"type": "string", "enum": ["new england", "northeast", "midwest", "south", "west"], "description": "A named group of states."},
            "states": {"type": "array", "items": {"type": "string"}, "description": "Two-letter state codes, e.g. ['TX']."},
            "metro_of": {"type": "string", "description": "An airport code; ranks all airports in that airport's metro area."},
            "size_classes": {"type": "array", "items": {"type": "string", "enum": tools.SIZE_CLASSES},
                             "description": "FAA hub classes. 'Small airports' means 'small' (small hub); 'nonhub' is smaller still - say which you used."},
            "airport_codes": {"type": "array", "items": {"type": "string"}, "description": "Restrict to these airport codes."},
            "sort_by": {"type": "string", "enum": tools.RANK_METRICS + ["passengers"],
                        "description": "Default total_score. With year: one of " + ", ".join(tools.YEAR_METRICS) + ". With month or season: one of " + ", ".join(tools.MONTH_METRICS) + "."},
            "order": {"type": "string", "enum": ["descending", "ascending"]},
            "year": {"type": "integer", "description": "A calendar year from 2019. Raw metrics only."},
            "month": {"type": "integer", "minimum": 1, "maximum": 12, "description": "Calendar month 1-12. Without year: that month summed over the latest three years."},
            "season": {"type": "string", "enum": list(tools.SEASONS),
                       "description": "winter (Dec-Feb), spring (Mar-May), summer (Jun-Aug) or fall (Sep-Nov). Without year: summed over the latest three years that have all three months. Not together with month."},
            "min_value": {"type": "number", "description": "Keep airports whose sort_by value is at least this."},
            "max_value": {"type": "number", "description": "Keep airports whose sort_by value is at most this."},
            "limit": {"type": "integer", "minimum": 1, "maximum": 30, "description": "How many to show (default 5; per size class when grouped). 30 covers every large hub in one call."},
            "include_partial_data": {"type": "boolean", "description": "Also include airports without full data (default false). They have no total score."},
            "min_data_confidence": {"type": "string", "enum": ["high", "medium"], "description": "Keep only airports whose data confidence is at least this."},
            "group_by_size_class": {"type": "boolean", "description": "Force or disable grouping by size class."}}},
    },
    {
        "name": "compare_airports",
        "description": (
            "Compare 2 to 5 named airports side by side on the scores, the five scored metrics, delay measures, delay causes and context. "
            "It returns the differences and ratios itself, so never subtract or divide numbers yourself - quote the ones it returns. "
            "Use it for 'compare X and Y', 'X vs Y', and for follow-ups like 'how does that compare with Z'. Pass year for a past calendar year "
            "(raw metrics only). Needs airport codes: resolve names with find_airport first. "
            "Do not use it for more than 5 airports or for a whole region (use rank_airports)."),
        "input_schema": {"type": "object", "additionalProperties": False, "required": ["airport_codes"], "properties": {
            "airport_codes": {"type": "array", "items": {"type": "string"}, "minItems": 2, "maxItems": 5, "description": "Airport codes, e.g. ['LAX','SNA']. The first is the baseline 'a'."},
            "year": {"type": "integer", "description": "A calendar year from 2019, for a past-year comparison."}}},
    },
    {
        "name": "airport_profile",
        "description": (
            "Everything about one airport: scores and the five scored metrics, the flight-demand estimate (called unmet flight demand only when the "
            "airport is strained), delay rates and delay causes, the long-haul share of flights at 2,000 / 2,500 / 3,000 miles for passenger flights "
            "and for all flights including cargo, cargo share, biggest airline, busiest month, and a year-by-year history from 2019. "
            "Use it for any question about a single airport, including 'what percentage of flights are long-haul', 'unmet demand at X and why', "
            "'is X a good candidate'. Pass long_haul_miles to use a different long-haul cutoff, or year for one past year's raw values. "
            "Needs an airport code: resolve names with find_airport first. It does not return routes, destinations or per-airline detail."),
        "input_schema": {"type": "object", "additionalProperties": False, "required": ["airport_code"], "properties": {
            "airport_code": {"type": "string", "description": "Airport code, e.g. 'ANC'."},
            "year": {"type": "integer", "description": "A calendar year from 2019, for that year's raw values."},
            "long_haul_miles": {"type": "integer", "minimum": 500, "maximum": 8000, "description": "Long-haul cutoff in miles (default 3000)."}}},
    },
    {
        "name": "airport_trend",
        "description": (
            "The month-by-month series of one metric for one airport, with the highest and lowest months and a seasonal profile "
            "(each calendar month across the range). Use it for 'how did X change month by month', 'when is the peak season', "
            "'what happened in August'. Defaults to the latest 36 months; pass start_month and end_month (YYYY-MM) for another range, back to 2019-01. "
            "Needs an airport code. For year-by-year totals use airport_profile (its history_by_year) instead; for many airports in one month or season use rank_airports with month or season."),
        "input_schema": {"type": "object", "additionalProperties": False, "required": ["airport_code", "metric"], "properties": {
            "airport_code": {"type": "string"},
            "metric": {"type": "string", "enum": tools.TREND_METRICS},
            "start_month": {"type": "string", "description": "YYYY-MM"},
            "end_month": {"type": "string", "description": "YYYY-MM"}}},
    },
]


def system_prompt() -> str:
    s = tools.store()
    man = s["manifest"]
    p = man["periods"]
    tiers = man["summary"]["data_tiers"]
    return f"""You are the Airport Investment Intelligence Agent for analysts at a firm that invests in US airport modernization.

# Background
The firm wants to find airports where renovations will be most profitable through increased flight and passenger capacity. The question behind every query is: if capacity is added here, how much of it will be filled?

You work over a pre-computed, checked dataset of the {man['summary']['airports']} FAA "primary" airports (over 10,000 passenger boardings a year), built from public BTS and FAA data: {tiers.get('full', 0)} have full data and are ranked, {tiers.get('partial', 0)} have partial data, {tiers.get('too_thin', 0)} have too little.
- Passengers and seats: {p['passenger_period']}
- Delays: {p['delay_period']}
- Routes, cargo, airlines: {p['route_period']}
- Forecast: {p['forecast_edition']}

The capacity-need score (0-100, relative to other full-data airports) has two sides, one per kind of capacity:
- Passenger side (half): how full the planes are (25%), passenger growth since 2019 (12.5%), FAA forecast passenger growth (12.5%).
- Flight side (half): system delay rate over three years (25%), FAA forecast flight growth (25%).
Size is deliberately not in the score; it is shown next to it. The score ranks upside (how much added capacity would be filled). It is a proxy for profit: no public data gives renovation cost, gate counts or terminal utilization.

# How to work
Analysts act on these figures, so every number you write must come from a tool result in this conversation. Code computes; you choose the tool and explain.
- Quote numbers as the tools return them. If you need a difference, ratio or total, use one a tool returned; if no tool returned it, describe the relationship in words ("roughly a fifth higher") rather than computing a new figure.
- When the user names an airport or city in words, call find_airport first and follow its guidance. If it gives a default, use it and say what you assumed and which other airports the area has. If it says to ask, ask a short clarifying question instead of guessing.
- Lead with the answer, then the reasons. Say plainly what a number measures, including when it is a proxy. Name the definition you used when one is ours (for example the long-haul cutoff, or that "small airports" means the FAA small-hub class).
- Mention the warnings that change the conclusion (a legal cap, capacity that was cut, a small sample, cargo-heavy traffic). The interface prints all warnings, the data period and a computed confidence label under your answer, so do not write a footer, a confidence level or a data-period line yourself.
- When an airport has partial data, say so at the top and give what exists (the passenger-side score), without filling the gap.
- "Unmet flight demand" is an estimate, never a measurement: use the flight_demand block of airport_profile, keep its label (it is only called unmet demand when the airport is strained today), and explain the "why" from the delay rates and delay causes in the data.
- "Congestion" maps to the system delay rate (three-year, and latest 12 months) plus the overall delay rate. Say that the system delay category is coded by airlines and includes ordinary weather.
- Before saying delays are "getting worse" at an airport, read delays.latest_12_months_pattern in airport_profile. If rise_is_concentrated_in_recent_months is true, say the rise is a spike in those recent months, give its rates, and say a temporary cause that is not in the data is possible. Do not call it a steady trend.
- FAA forecast operations are takeoffs plus landings and include cargo; BTS flights are departures. Never compare the two directly.
- You may add background knowledge that is not in the data only when it helps explain a result, in a separate sentence that starts with "Background (not from our data):", and without any number in it.

# What this version does not do
Say so directly and offer the closest thing you can do:
- Renovation cost, return on investment, revenue or any financial figure: not available. The score is a proxy for upside only.
- Questions about one airline's network, a specific route or destination, or flight counts between two cities: not available (only an airport's biggest airline and its share).
- Rankings by score for past years: the score exists for the latest period only. Raw metrics by year (from 2019), by month and by season are available.
- Airports outside the covered set (private aviation, military, foreign, very small): not covered.
- Gate counts, terminal size, construction projects, peak-hour data, live delays: not in the data.
- Recommendations to invest: give the evidence, the caveats and what to check next; the decision is the analyst's.
If a question is ambiguous or you lack the data, saying "I don't have that" is a good answer.

# Output format
Plain, direct prose an analyst can scan: a one or two sentence answer first, then short paragraphs or a compact list or table of the supporting numbers with units. For rankings and comparisons a small markdown table is welcome. Keep it under about 250 words unless the user asks for depth. Refer to airports by name with the code in brackets on first mention. Use the plain hyphen "-" for ranges, negative numbers and asides; do not use long dashes or special minus signs.

# Examples of the three kinds of reply
- A data answer: "Boise (BOI): [the figure with its unit and period], which measures [what it measures]. [Then the reasons, and any warning that changes the conclusion.]"
- A clarifying question: "Springfield could mean Springfield, Missouri (SGF) or Springfield, Illinois (SPI). Which one do you mean?"
- A decline: "I don't have gate counts or terminal sizes - no public source gives them. What I can show is how full the planes are and how often flights are delayed there."
"""


@dataclass
class Answer:
    text: str
    trace: list = field(default_factory=list)        # [{name, input, output, is_error, ms}]
    warnings: list = field(default_factory=list)
    footer: dict = field(default_factory=dict)
    unverified: list = field(default_factory=list)   # numbers the check could not trace (after the rewrite)
    check: str = "passed"                            # passed | rewritten | fallback | no numbers
    rounds: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    seconds: float = 0.0
    model: str = ""
    error: str | None = None


def _logger():
    LOGS.mkdir(exist_ok=True)
    log = logging.getLogger("airport_agent")
    if not log.handlers:
        h = logging.FileHandler(LOGS / "agent.log", encoding="utf-8")
        h.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
        log.addHandler(h)
        log.setLevel(logging.INFO)
    return log


class Agent:
    """One conversation. `messages` holds the exact model messages; the model's own replies are never edited, and only
    the content of old tool results is replaced by a stub (see _trim). The chat screen keeps its own display records."""

    def __init__(self, model: str | None = None):
        self.model = model
        self.messages: list = []
        self.data_numbers: set = set()     # every number in the tool results still in the conversation (see _trim)
        self.last_data_trace: list = []    # tool results of the latest turn that fetched data (for follow-ups that reuse it)
        self._system = system_prompt()

    def ask(self, question: str, on_event=None) -> Answer:
        log = _logger()
        t0 = time.time()
        emit = on_event or (lambda kind, payload: None)
        self._trim()
        self.messages.append({"role": "user", "content": question})
        ans = Answer(text="")
        rewrites = 0
        log.info("QUESTION %s", json.dumps(question))
        try:
            while ans.rounds < MAX_ROUNDS:
                ans.rounds += 1
                reply = llm.complete(self.messages, self._system, TOOL_SPECS, self.model)
                ans.input_tokens += reply.input_tokens
                ans.output_tokens += reply.output_tokens
                ans.model = reply.model
                self.messages.append(llm.assistant_message(reply))

                if reply.stop_reason == "tool_use" and reply.tool_calls:
                    results = []
                    for call in reply.tool_calls:
                        emit("tool_start", call)
                        ts = time.time()
                        out = tools.call(call["name"], call["input"])
                        is_error = "error" in out
                        ms = int(1000 * (time.time() - ts))
                        ans.trace.append(dict(name=call["name"], input=call["input"], output=out, is_error=is_error, ms=ms))
                        if not is_error:
                            safeguards.numbers_in_data(out, self.data_numbers)
                        results.append(dict(id=call["id"], content=json.dumps(out, default=str), is_error=is_error))
                        log.info("TOOL %s %s error=%s %dms", call["name"], json.dumps(call["input"]), is_error, ms)
                        emit("tool_end", dict(call, is_error=is_error))
                    self.messages.append(llm.tool_results_message(results))
                    continue

                if reply.stop_reason == "refusal":
                    ans.text = "The model declined to answer this question. Try rephrasing it."
                    ans.check = "no numbers"
                    break
                text = reply.text or "(The model returned no text.)"
                if reply.stop_reason == "max_tokens":
                    text += "\n\n*(The answer was cut off at the length limit.)*"

                missing = safeguards.unverified_numbers(text, self.data_numbers, question + " " + self._system)   # the background it was given counts too
                if not missing:
                    ans.text = text
                    ans.check = "passed" if rewrites == 0 else "rewritten"
                    break
                log.info("NUMBER CHECK failed: %s", missing)
                if rewrites == 0 and ans.rounds < MAX_ROUNDS:
                    rewrites += 1
                    emit("rewrite", missing)
                    self.messages.append({"role": "user", "content": (
                        CHECK_PREFIX + ", not from the user] These numbers in your answer do not appear in any tool result: "
                        + ", ".join(missing) + ". Rewrite the answer for the user using only numbers the tools returned. "
                        "If you computed a difference, ratio or total yourself, use the one a tool returned or describe it in words. "
                        "If you need a number you do not have, call a tool. Do not mention this check.")})
                    continue
                # still failing after one rewrite: show an answer built by code, and say which numbers failed
                ans.unverified = missing
                ans.check = "fallback"
                ans.text = safeguards.fallback_answer(ans.trace) if any(not t["is_error"] for t in ans.trace) else text
                break
            else:
                ans.text = "I could not finish this within the allowed number of steps. Try a narrower question."
                ans.check = "no numbers"
                self.messages.append({"role": "assistant", "content": ans.text})   # history must not end on a tool result
        except (llm.ConfigError, llm.ModelError) as err:
            # keep the conversation usable: drop the unanswered question so history stays a valid sequence
            ans.error = str(err)
            ans.text = str(err)
            self._rollback()
        except Exception as err:
            # anything unexpected gets the same recovery, so one bad turn cannot break the rest of the conversation
            log.exception("UNEXPECTED %s", err)
            ans.error = f"{type(err).__name__}: {err}"
            ans.text = "Something went wrong while answering this question. Please try again or rephrase it."
            self._rollback()
        # A follow-up can be answered from data fetched earlier in the conversation, with no new tool call. Its figures
        # still rest on that data, so the warnings and footer are built from the latest turn that fetched some.
        basis, reused = ans.trace, False
        if safeguards.rests_on_data(ans.trace, ans.text):
            self.last_data_trace = ans.trace
        elif self.last_data_trace and not ans.error and safeguards.has_figures(ans.text):
            basis, reused = self.last_data_trace, True
        ans.warnings = safeguards.collect_warnings(basis)
        ans.footer = safeguards.footer(basis, ans.text)
        if reused:
            ans.footer["assumptions"] = "figures reuse data fetched earlier in this conversation; " + ans.footer["assumptions"]
        ans.seconds = round(time.time() - t0, 1)
        log.info("ANSWER check=%s rounds=%d tokens_in=%d tokens_out=%d seconds=%.1f tools=%s", ans.check, ans.rounds,
                 ans.input_tokens, ans.output_tokens, ans.seconds, [t["name"] for t in ans.trace])
        return ans

    def _rollback(self):
        """After a failed model call, remove the trailing messages of the unanswered turn (back to and including
        the last plain user question) so the next question starts from a valid history."""
        while self.messages:
            m = self.messages.pop()
            if _is_question(m):
                break

    def _trim(self):
        """Tool results are large (tens of thousands of characters each), so a long chat would otherwise outgrow the
        model's context. Before each new question, the results of all but the latest KEEP_DATA_TURNS data-fetching
        turns are replaced by a stub. The number check then accepts only numbers the model can still see."""
        turns = []                                   # per user question: its tool-result messages
        for m in self.messages:
            if _is_question(m):
                turns.append([])
            elif m["role"] == "user" and isinstance(m["content"], list) and turns:
                turns[-1].append(m)
        data_turns = [t for t in turns if t]
        old, kept = data_turns[:-KEEP_DATA_TURNS], data_turns[-KEEP_DATA_TURNS:]
        if not any(b["content"] != STUB for t in old for m in t for b in m["content"]):
            return
        for b in (b for t in old for m in t for b in m["content"]):
            b["content"] = STUB
        self.data_numbers = set()
        for b in (b for t in kept for m in t for b in m["content"]):
            if not b.get("is_error"):
                safeguards.numbers_in_data(json.loads(b["content"]), self.data_numbers)


def _is_question(m: dict) -> bool:
    """A plain user question, as opposed to tool results or the automatic rewrite request."""
    return m["role"] == "user" and isinstance(m["content"], str) and not m["content"].startswith(CHECK_PREFIX)
