"""Streamlit chat screen. It holds no logic about airports: it sends text to the agent and shows what comes back -
the answer, the warnings and the three footer lines built by code, the data table, and the tool trace.

Run:  streamlit run app.py
"""
import json
import re
import time
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from airport_agent import llm, tools, voice
from airport_agent.agent import Agent
from airport_agent.safeguards import footer_markdown

st.set_page_config(page_title="Airport Investment Intelligence Agent", page_icon="✈️", layout="wide")

SUGGESTED = [
    "Which airports in New England are strong candidates for terminal expansion?",
    "Compare LA and Santa Ana airport congestion levels.",
    "What is the percentage of long haul flights out of Anchorage airport?",
    "What is the unmet flight demand in SFO airport and why?",
]
SUGGESTED_ICONS = [":material/leaderboard:", ":material/compare_arrows:", ":material/public:", ":material/trending_up:"]
TOOL_LABEL = {"find_airport": "Finding the airport", "rank_airports": "Ranking airports", "compare_airports": "Comparing airports",
              "airport_profile": "Reading the airport profile", "airport_trend": "Reading the monthly trend"}
TOOL_ICON = {"find_airport": ":material/travel_explore:", "rank_airports": ":material/leaderboard:",
             "compare_airports": ":material/compare_arrows:", "airport_profile": ":material/article:",
             "airport_trend": ":material/show_chart:"}
RANK_COLUMNS = {"position": "#", "airport_code": "Code", "name": "Airport", "state": "State", "size_class": "Size class",
                "sort_value": "Sorted by", "total_score": "Score", "passenger_score": "Passenger side", "flight_score": "Flight side",
                "load_factor_pct": "Planes full %", "passenger_growth_since_2019_pct": "Growth since 2019 %",
                "forecast_passenger_growth_pct": "Forecast passengers %", "system_delay_rate_pct": "System delay %",
                "forecast_flight_growth_pct": "Forecast flights %", "boardings_2025": "Boardings 2025",
                "forecast_extra_boardings": "Extra boardings by 2035", "capacity_was_cut": "Capacity cut", "data_confidence": "Data confidence"}


# ---------- startup checks: a clear message instead of a crash ----------

try:
    manifest = tools.store()["manifest"]
except tools.DataMissing as err:
    st.error(f"{err}")
    st.stop()
except Exception as err:  # damaged tables
    st.error(f"The data tables could not be read ({err}). Rebuild them with:  python -m airport_agent.pipeline.build")
    st.stop()

key_problem = None
try:
    llm._api_key()
except llm.ConfigError as err:
    key_problem = str(err)

# Two separate stores: the agent keeps the exact model messages; `records` is only what the screen shows.
ss = st.session_state
ss.setdefault("agent", None)
ss.setdefault("records", [])
ss.setdefault("running", False)
ss.setdefault("pending", None)
ss.setdefault("speak", None)        # text to read aloud once; "" stops whatever is being read
ss.setdefault("speaking", None)     # which record is being read aloud (its Listen button shows Stop)
ss.setdefault("pending_spoken", False)
ss.setdefault("speak_in_voice_mode", False)     # the pending read-aloud belongs to voice mode (a spoken question)

# ---------- look: the theme is in .streamlit/config.toml; this only shapes the layout ----------

st.html("""<style>
.stMainBlockContainer, [data-testid="stBottomBlockContainer"] { max-width: 1080px; }
.stMainBlockContainer { padding-top: 3.25rem; }
/* top bar: product name on the left; New chat is pinned to the top right corner so it stays in view while scrolling */
.st-key-topbar { padding: 0.35rem 0 0.6rem; border-bottom: 1px solid #E8ECF3; }
.st-key-topbar p { font-size: 1.05rem; }
.st-key-new_chat { position: fixed; top: 0.65rem; right: 1.25rem; z-index: 1000000; width: auto; }
.st-key-new_chat button { background: #FFFFFF; }
/* empty state */
.st-key-hero { padding-top: 7vh; }
.st-key-hero h1, .st-key-hero p { text-align: center; }
.st-key-hero h1 { font-size: 2.1rem; padding-bottom: 0.4rem; }
[class*="st-key-sugg"] button { justify-content: flex-start; text-align: left; min-height: 4.4rem; padding: 0.85rem 1rem;
                                background: #FFFFFF; border: 1px solid #DCE2EC; transition: all 0.15s ease; }
[class*="st-key-sugg"] button > div { justify-content: flex-start; width: 100%; gap: 0.6rem; }
[class*="st-key-sugg"] button p { text-align: left; }
[class*="st-key-sugg"] button [data-testid="stIconMaterial"] { color: #2251B5; }
.st-key-hero > div:nth-child(2) p { max-width: 620px; margin: 0 auto; color: #5B6778; }
[class*="st-key-sugg"] button:hover { border-color: #2251B5; background: #F5F8FE; color: inherit;
                                      box-shadow: 0 2px 12px rgba(34, 81, 181, 0.10); }
[class*="st-key-listen"] button { color: #5B6778; }
/* the microphone in the question bar: a voice-wave mark in a dark circle, as in other assistants' voice buttons */
[data-testid="stChatInputMicButton"][aria-label="Start recording"] {
    width: 2rem; height: 2rem; border-radius: 50%; background-color: #17212F; transition: background-color 0.15s ease;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='white'%3E%3Crect x='4.6' y='10' width='1.8' height='4' rx='0.9'/%3E%3Crect x='7.9' y='7.5' width='1.8' height='9' rx='0.9'/%3E%3Crect x='11.1' y='5' width='1.8' height='14' rx='0.9'/%3E%3Crect x='14.3' y='7.5' width='1.8' height='9' rx='0.9'/%3E%3Crect x='17.6' y='10' width='1.8' height='4' rx='0.9'/%3E%3C/svg%3E");
    background-repeat: no-repeat; background-position: center; background-size: 1.35rem; }
[data-testid="stChatInputMicButton"][aria-label="Start recording"]:hover { background-color: #2251B5; }
[data-testid="stChatInputMicButton"][aria-label="Start recording"] svg { visibility: hidden; }
/* latest turn: at least a screen tall, so its question can sit at the top while the answer fills in below */
.st-key-turn_last { min-height: calc(100vh - 9rem); scroll-margin-top: 4.25rem; justify-content: flex-start; }
/* the invisible script frames (scrolling, speech) take no room, so nothing shifts when they come and go */
[data-testid="stElementContainer"]:has(> iframe), [data-testid="stElementContainer"]:has(> div > iframe) {
    position: absolute; width: 0; height: 0; overflow: hidden; }
/* live activity while the agent works */
[class*="st-key-activity"] { gap: 0.2rem; }
[class*="st-key-activity"] > div:last-child strong {
    background: linear-gradient(90deg, #17212F 0%, #17212F 35%, #9DB4E8 50%, #17212F 65%, #17212F 100%);
    background-size: 200% 100%; -webkit-background-clip: text; background-clip: text; color: transparent;
    animation: shimmer 1.8s linear infinite; }
[class*="st-key-activity"] > div:last-child [data-testid="stIconMaterial"] { animation: pulse 1.2s ease-in-out infinite; }
@keyframes shimmer { from { background-position: 100% 0; } to { background-position: -100% 0; } }
@keyframes pulse { 0%, 100% { opacity: 1; transform: scale(1); } 50% { opacity: 0.55; transform: scale(0.88); } }
/* ---- phone ---- */
@media (max-width: 640px) {
    .stMainBlockContainer { padding: 4rem 1rem 1rem; }
    [data-testid="stBottomBlockContainer"] { padding: 0.5rem 0.75rem 0.9rem; }
    /* the product name moves into the header row, between the menu arrow and New chat (icon only) */
    .st-key-topbar { position: fixed; top: 0; left: 3.4rem; right: 0; width: auto !important; height: 3.75rem; padding: 0;
                     border: none; z-index: 999991; align-items: center; pointer-events: none; }
    .st-key-topbar p { font-size: 0.98rem; white-space: nowrap; }
    .st-key-new_chat { right: 0.75rem; top: 0.6rem; pointer-events: auto; }
    .st-key-new_chat button p { display: none; }
    body:has([data-testid="stSidebar"][aria-expanded="true"]) .st-key-topbar { display: none; }
    .st-key-hero { padding-top: 1.25rem; }
    .st-key-hero h1 { font-size: 1.6rem; }
    [class*="st-key-sugg"] button { min-height: 3.6rem; padding: 0.7rem 0.9rem; }
    /* full width for the answer: no avatar column, tighter tables that scroll sideways instead of spilling out */
    [data-testid="stChatMessage"] { padding: 0.75rem 0.85rem; }
    [data-testid="stChatMessage"]:not(:has([data-testid="stChatMessageAvatarUser"])) { padding-left: 0; padding-right: 0; }
    [data-testid="stChatMessage"] > [data-testid*="ChatMessageAvatar"] { display: none; }
    [data-testid="stChatMessage"] table { display: block; max-width: 100%; overflow-x: auto; font-size: 0.86rem; }
    [data-testid="stChatMessage"] th, [data-testid="stChatMessage"] td { padding: 0.35rem 0.55rem; }
    .st-key-turn_last { min-height: calc(100vh - 8.5rem); }
    /* sidebar: the three headline numbers stay on one row */
    [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] { flex-wrap: nowrap; }
    [data-testid="stSidebar"] [data-testid="stColumn"] { min-width: 0 !important; flex: 1 1 0 !important; }
}
</style>""")

# The voice layer (voice mode and reading aloud) is loaded into the page once; a changed file replaces the old copy.
VOICE_JS = (Path(__file__).parent / "airport_agent" / "voice_mode.js").read_text(encoding="utf-8")
components.html("<script>const w = window.parent, v = " + json.dumps(str(hash(VOICE_JS))) + ";"
                "if (w.__voiceVersion !== v) { w.__voiceVersion = v; const s = w.document.createElement('script');"
                "s.textContent = " + json.dumps(VOICE_JS).replace("</", "<\\/") + "; w.document.head.appendChild(s); }</script>",
                height=0)


# ---------- rendering ----------

USER_AVATAR, AGENT_AVATAR = ":material/person:", ":material/flight_takeoff:"
CONFIDENCE_ICON = {"High": ":material/verified:", "Medium": ":material/info:", "Low": ":material/report:"}

def md(text: str) -> str:
    return text.replace("$", "\\$")     # stop Streamlit from reading dollar signs as math


def tool_detail(tool_input: dict) -> str:
    """The tool's inputs as a short plain phrase for the activity line, e.g. 'LAX, SNA'."""
    parts = []
    for v in tool_input.values():
        if isinstance(v, (list, tuple)):
            parts.append(", ".join(map(str, v)))
        elif isinstance(v, str) and v:
            parts.append(v)
    return md(" · ".join(parts))[:90].replace("[", "(").replace("]", ")")


def reveal(text: str, seconds: float = 2.5):
    """Yield the finished answer a few words at a time. A table arrives as one piece, so it never shows half-built."""
    blocks = re.split(r"(\n\s*\n)", text)
    words = sum(len(b.split()) for b in blocks if "|" not in b) or 1
    pause = min(0.03, seconds / words)
    for block in blocks:
        if "|" in block or not block.strip():
            yield block
            continue
        for piece in re.findall(r"\S+\s*", block):
            yield piece
            time.sleep(pause)


def tables_from(trace, text=""):
    out = []
    about_long_haul = "long-haul" in text.lower() or "long haul" in text.lower()
    for t in trace:
        if t["is_error"]:
            continue
        res = t["output"]["result"]
        if t["name"] == "rank_airports":
            groups = res["ranking"] if isinstance(res["ranking"], dict) else {"": res["ranking"]}
            sorted_by = t["output"].get("definitions", {}).get(res["sorted_by"], {}).get("name", res["sorted_by"])
            direction = "lowest first" if res.get("order") == "ascending" else "highest first"
            for g, rows in groups.items():
                if rows:
                    df = pd.DataFrame(rows)[[c for c in RANK_COLUMNS if c in rows[0]]].rename(columns=RANK_COLUMNS)
                    out.append((f"Ranking by {sorted_by}, {direction}" + (f" - {g}" if g else ""), df))
        elif t["name"] == "compare_airports" and res["comparisons"]:
            defs = t["output"]["definitions"]
            df = pd.DataFrame([{"Metric": defs.get(c["metric"], {}).get("name", c["metric"]), c["a"]: c["a_value"], c["b"]: c["b_value"],
                                "Difference": c["difference_a_minus_b"], "Ratio": c.get("ratio_a_to_b")} for c in res["comparisons"]])
            out.append((f"Comparison ({res['period']})", df))
        elif t["name"] == "airport_profile" and res.get("long_haul") and about_long_haul:   # only when the answer is about long-haul
            lh = res["long_haul"]
            df = pd.DataFrame(lh["by_cutoff"]).rename(columns={
                "cutoff_miles": "Cutoff (miles)", "share_of_passenger_flights_pct": "% of passenger flights",
                "share_of_all_flights_including_cargo_pct": "% of all flights incl. cargo",
                "long_haul_passenger_flights": "Long-haul passenger flights", "long_haul_flights_including_cargo": "Long-haul flights incl. cargo"})
            out.append((f"Long-haul share of departing flights, {lh['year']}", df))
        elif t["name"] == "airport_trend":
            df = pd.DataFrame(res["series"]).set_index("month")
            out.append((f"{res['airport']['name']} - {res['metric']} by month", df))
    return out


def render_answer(rec, idx):
    a = rec["answer"]
    if a.error:
        st.error(a.text)
        return
    st.markdown(md(a.text))
    if a.check == "fallback":
        st.error("Number check: these figures in the model's written answer could not be traced to the data, even after one rewrite: "
                 + ", ".join(a.unverified) + ". The answer above was built by code from the data instead.")
    for title, df in tables_from(a.trace, a.text):
        if "by month" in title:
            with st.expander(title):
                st.line_chart(df)
        else:
            st.caption(title)
            st.dataframe(df, hide_index=True, width="stretch")
    # Collapsed to keep the answer readable, but the labels still say what is inside: how many warnings and which airports
    # carry a legal limit, and the confidence level with its reason.
    if a.warnings:
        limits = list(dict.fromkeys(w["airport_code"] for w in a.warnings
                                    if (w["type"] == "legal_limit" or w["severity"] == "blocking") and w["airport_code"]))
        label = f"Warnings from the data ({len(a.warnings)})" + (f" - legal limits: {', '.join(limits)}" if limits else "")
        with st.expander(label, icon=":material/warning:"):
            st.caption("Printed by code, not by the model.")
            for w in a.warnings:
                tag = f"**{w['airport_code']}** - " if w["airport_code"] else ""
                (st.warning if w["type"] == "legal_limit" or w["severity"] == "blocking" else st.info)(md(tag + w["message"]))
    with st.expander(md(f"Confidence: {a.footer['confidence']} - {a.footer['confidence_reason']}"),
                     icon=CONFIDENCE_ICON.get(a.footer["confidence"], ":material/info:")):
        st.markdown(md(footer_markdown(a.footer)))
    if a.trace:
        check = {"passed": "every number matched against the data", "rewritten": "passed after one automatic rewrite",
                 "fallback": "failed - code-built answer shown", "no numbers": "no figures used"}[a.check]
        with st.expander(f"How this was answered: {len(a.trace)} tool call(s) - number check: {check} - {a.seconds}s - {a.model}",
                         icon=":material/account_tree:"):
            for i, t in enumerate(a.trace, 1):
                st.markdown(f"**{i}. `{t['name']}`** {'(returned an error, the model corrected itself)' if t['is_error'] else ''}")
                st.json(t["input"], expanded=True)
                with st.popover("Full tool result", icon=":material/data_object:"):
                    st.json(t["output"], expanded=False)
            st.caption(f"{a.rounds} model call(s), {a.input_tokens:,} input tokens, {a.output_tokens:,} output tokens.")
    # Any answer can be read aloud, like the speaker button in other assistants. The browser does the reading.
    reading = ss.speaking == idx
    if st.button("Stop" if reading else "Listen", key=f"listen{idx}", type="tertiary", disabled=ss.running,
                 icon=":material/stop_circle:" if reading else ":material/volume_up:",
                 help="Stop reading" if reading else "Read a short summary of this answer aloud"):
        ss.speak, ss.speaking = ("", None) if reading else (voice.spoken_summary(a.text), idx)
        st.rerun()


# ---------- sidebar: what the data covers ----------

with st.sidebar:
    st.subheader("About the data", anchor=False)
    s = manifest["summary"]
    c1, c2, c3 = st.columns(3)
    c1.metric("Airports", s["airports"], help="FAA primary airports")
    c2.metric("Ranked", s["data_tiers"].get("full", 0), help="Airports with full data. Only these are ranked.")
    c3.metric("Partial", s["data_tiers"].get("partial", 0),
              help=f"Partial data. Another {s['data_tiers'].get('too_thin', 0)} are too thin to use.")
    p = manifest["periods"]
    st.markdown("**:material/date_range: What each source covers**")
    st.markdown(f"- Passengers and seats: {p['passenger_period']}\n- Delays: {p['delay_period']}\n"
                f"- Routes, cargo, airlines: {p['route_period']}\n- Forecast: {p['forecast_edition']}\n- Size: {p['size_period']}")
    with st.expander("How the score is built", icon=":material/calculate:"):
        st.markdown("**Passenger side**: planes full 25%, growth since 2019 12.5%, forecast passengers 12.5%.\n\n"
                    "**Flight side**: system delay rate 25%, forecast flights 25%.\n\n"
                    "Size is shown next to the score, not inside it.")
    with st.expander("Sources and fetch dates", icon=":material/source:"):
        st.dataframe(pd.DataFrame([{"Source": e["source"], "Status": e["status"], "Fetched (UTC)": (e.get("fetched_at") or "")[:10]}
                                   for e in manifest["sources"]]), hide_index=True, width="stretch")
    st.caption(f"Tables built {manifest['built_at'][:16].replace('T', ' ')} UTC - score version {manifest['score_version']} - "
               f"data checks passed: {manifest['checks_passed']}.")
    st.caption(f"Model: {llm.model_name()}. The model picks a tool and explains; code computes every number.")
    can_hear = voice.available()
    if not can_hear:
        st.caption(":material/mic_off: Microphone is off: install it with `pip install -r requirements.txt`.")

# ---------- main ----------

# New chat sits top right, where other assistants put it, and stays in view while the conversation scrolls.
with st.container(key="topbar", horizontal=True, horizontal_alignment="distribute", vertical_alignment="center"):
    st.markdown(":blue[:material/flight_takeoff:] **Airport Investment Intelligence**", width="content")
    if st.button("New chat", key="new_chat", icon=":material/edit_square:", disabled=ss.running or not ss.records,
                 help="Start a new conversation"):
        ss.agent, ss.records, ss.speak, ss.speaking = None, [], "", None
        st.rerun()

if key_problem:
    st.warning(key_problem + "  Then reload this page.", icon=":material/key:")

def render_record(idx, rec):
    with st.chat_message(rec["role"], avatar=USER_AVATAR if rec["role"] == "user" else AGENT_AVATAR):
        if rec["role"] == "user":
            st.markdown(md(rec["text"]))
            if rec.get("spoken"):   # show what was heard, so a misheard question is easy to spot
                st.caption(":material/mic: Asked by voice")
        else:
            render_answer(rec, idx)


MAX_QUESTION_CHARS = 2000    # a question is a sentence or two; this caps what one message can cost


def voice_call(method, *args):
    """Call one function of the page's voice layer (airport_agent/voice_mode.js): speak, stop, heard or fail."""
    ss.voice_n = ss.get("voice_n", 0) + 1       # a changing token, so the same call can be sent twice
    components.html(f"<script>/* {ss.voice_n} */ const V = window.parent.__voice; "
                    f"if (V) V.{method}({', '.join(json.dumps(a).replace('</', '<\\/') for a in args)});</script>", height=0)


def scroll_to_turn():
    """Put the latest question at the top of the screen, so the answer is read from its start and the page does not
    chase the bottom while the answer grows. The reader scrolls down on their own."""
    ss.scroll_n = ss.get("scroll_n", 0) + 1
    components.html("<script>/* " + str(ss.scroll_n) + " */ const t = window.parent.document.querySelector('.st-key-turn_last');"
                    "if (t) { t.scrollIntoView({block: 'start'}); setTimeout(() => t.scrollIntoView({block: 'start'}), 250); }"
                    "</script>", height=0)


# The latest question and its answer sit in a block at least one screen tall (see the style above), which is what
# lets the question be scrolled to the top.
last_turn = len(ss.records) - 2 if ss.records and not ss.running else None
for idx, rec in enumerate(ss.records):
    if last_turn is not None and idx >= last_turn:
        continue
    render_record(idx, rec)
if last_turn is not None:
    with st.container(key="turn_last"):
        render_record(last_turn, ss.records[last_turn])
        render_record(last_turn + 1, ss.records[last_turn + 1])
        if ss.get("scroll_after"):
            scroll_to_turn()
            ss.scroll_after = False

hero = st.empty()   # a slot, so the welcome screen clears the moment a question is asked
if not ss.records and not ss.running:
    with hero.container(key="hero"):
        st.title("Where would added airport capacity be filled?", anchor=False)
        st.markdown(f"Ask about any of {s['airports']} US airports. Answers come from public BTS and FAA data; "
                    "every number is computed by code and checked before you see it.")
        st.space("small")
        cols = st.columns(2)
        for i, (icon, q) in enumerate(zip(SUGGESTED_ICONS, SUGGESTED)):
            if cols[i % 2].button(q, key=f"sugg{i}", icon=icon, disabled=bool(key_problem), width="stretch", wrap=True):
                ss.pending, ss.running = q, True
                st.rerun()
        # On a phone the page is taller than the screen and would open scrolled to the bottom; start at the top.
        components.html("<script>const m = window.parent.document.querySelector('.stMain'); if (m) { m.scrollTo(0, 0);"
                        "setTimeout(() => m.scrollTo(0, 0), 300); }</script>", height=0)

# One question bar for typing and speaking; a second question is blocked while one is running, since submitting
# mid-answer would corrupt the history. Voice wraps the same agent: speech -> text -> agent -> text -> speech.
if ss.running:
    hint = "Answering..."
else:
    hint = "Ask about US airports"      # short, so it is not cut off on a phone; the voice button speaks for itself
sent = st.chat_input(hint, accept_audio=can_hear, max_chars=MAX_QUESTION_CHARS, disabled=ss.running or bool(key_problem))
if sent and not ss.running:
    text, audio = (sent, None) if isinstance(sent, str) else (sent.text, sent.audio)
    text, spoken = (text or "").strip(), False
    if not text and audio is not None:
        spoken = True
        with st.spinner("Transcribing your question..."):
            try:
                text = voice.transcribe(audio.getvalue())[:MAX_QUESTION_CHARS]
            except Exception as err:
                st.error(f"Could not transcribe the recording: {err}", icon=":material/mic_off:")
                voice_call("fail", "The recording could not be transcribed. Close to see why.")
            else:
                if not text:
                    st.warning("I could not hear a question in that recording. Try again, or type it.", icon=":material/mic_off:")
                    voice_call("fail", "I did not catch a question. Try again.")
    if text:
        ss.pending, ss.running, ss.pending_spoken = text, True, spoken
        ss.speak, ss.speaking = "", None    # a new question stops whatever is being read
        st.rerun()

if ss.get("voice_failed"):
    voice_call("fail", "Something went wrong. Close to see the details.")
    ss.voice_failed = False
if ss.speak == "":
    voice_call("stop")
    ss.speak = None
elif ss.speak:
    # Read the lead of the checked answer aloud once, in the browser. Sent only on the run right after the request.
    # A spoken question is answered inside voice mode; the Listen button reads without opening it.
    voice_call("speak", ss.speak, bool(ss.speak_in_voice_mode))
    ss.speak, ss.speak_in_voice_mode = None, False

if ss.running and ss.pending:
    question = ss.pending
    with st.container(key="turn_last"):
      with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(md(question))
        if ss.pending_spoken:
            st.caption(":material/mic: Asked by voice")
            voice_call("heard", question)     # voice mode shows what was heard, so a misheard question is caught early
      scroll_to_turn()
      with st.chat_message("assistant", avatar=AGENT_AVATAR):
        # Live activity: finished steps stay listed, the current one shimmers with the icon of the tool in use.
        live, done = st.empty(), []

        def show(icon, text):
            ss.activity_n = ss.get("activity_n", 0) + 1     # each redraw needs its own key
            with live.container(key=f"activity{ss.activity_n}"):
                for line in done:
                    st.caption(f":material/check_circle: {line}")
                st.markdown(f":blue[{icon}] **{text}**")

        def on_event(kind, payload):
            if kind == "tool_start":
                show(TOOL_ICON.get(payload["name"], ":material/build:"), TOOL_LABEL.get(payload["name"], payload["name"]))
            elif kind == "tool_end":
                detail = tool_detail(payload["input"])
                done.append(TOOL_LABEL.get(payload["name"], payload["name"]) + (f" · {detail}" if detail else ""))
                show(":material/edit_note:", "Writing the answer and checking every number")
            elif kind == "rewrite":
                done.append("Number check: a figure in the draft was not found in the data")
                show(":material/restart_alt:", "Rewriting the answer")

        show(":material/psychology:", "Reading the question")
        try:
            if ss.agent is None:
                ss.agent = Agent()
            answer = ss.agent.ask(question, on_event=on_event)
        except Exception as err:  # never lose the conversation to an unexpected error
            from airport_agent.agent import Answer
            answer = Answer(text=f"Something went wrong: {err}", error=str(err))
        live.empty()
        if not answer.error and not ss.pending_spoken:
            # The answer is already complete and number-checked here; it is only revealed gradually, so it reads
            # smoothly from the top instead of snapping in. Unchecked text is never shown. (A spoken question skips
            # this: voice mode covers the chat, and the spoken answer should start without the wait.)
            st.write_stream(reveal(md(answer.text)))
    # saved before the rerun, so nothing vanishes on refresh of the run
    ss.records.append(dict(role="user", text=question, spoken=ss.pending_spoken))
    ss.records.append(dict(role="assistant", answer=answer))
    if ss.pending_spoken and not answer.error:      # a spoken question gets a spoken answer
        # shorter than the Listen button's summary: in voice mode about 20 seconds of speech is the comfortable limit
        ss.speak, ss.speaking, ss.speak_in_voice_mode = voice.spoken_summary(answer.text, 300), len(ss.records) - 1, True
    elif ss.pending_spoken:
        ss.voice_failed = True
    ss.pending, ss.running, ss.pending_spoken, ss.scroll_after = None, False, False, True
    st.rerun()
