"""Run the committed question set through the REAL agent (model in the loop) and save a dated answer file.

    python eval/run_eval.py                       all 26 questions, default model
    python eval/run_eval.py --group core          only the four core questions and their follow-ups
    python eval/run_eval.py --model claude-sonnet-5-5 --group core

Each question is graded by code on the outcome, not on the exact tool sequence:
  - the expected tool was used and the expected airports appear in the tool calls (when the question has them)
  - the answer says what it must say (regular expressions from eval/questions.json)
  - the number check passed (every number in the answer matched a tool result) without falling back
  - when the answer rests on data, the code-built footer carries a computed confidence label
This is a regression check: the expected values come from this project's own tables, so it shows the agent
reads them faithfully, not that the tables are right.
Writes eval/results/eval_<date>_<model>.json and .md.
"""
import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from airport_agent import llm, safeguards  # noqa: E402
from airport_agent.agent import Agent  # noqa: E402

HERE = Path(__file__).resolve().parent
CORE_CONVERSATIONS = {"A1", "A2", "A3", "A4"}


def codes_in_trace(trace) -> set:
    found = set()
    for t in trace:
        given = [t["input"].get(k) for k in ("airport_code", "airport_codes", "metro_of")]
        found |= {str(c).upper() for g in given if g for c in (g if isinstance(g, list) else [g])}
        if isinstance(t["output"], dict):
            found |= set(t["output"].get("meta", {}).get("airports", []))
    return found


def grade(turn: dict, ans) -> dict:
    checks = {}
    names = [t["name"] for t in ans.trace]
    if turn.get("tool"):
        checks[f"used {turn['tool']}"] = turn["tool"] in names
    if turn.get("input_key"):
        checks[f"a tool call passed {turn['input_key']}"] = any(turn["input_key"] in t["input"] for t in ans.trace)
    if turn.get("codes"):
        checks[f"airports {'+'.join(turn['codes'])} in the tool calls"] = set(turn["codes"]) <= codes_in_trace(ans.trace)
    for pattern in turn.get("say_all", []):
        checks[f"says /{pattern}/"] = re.search(pattern, ans.text, re.IGNORECASE) is not None
    checks["number check passed (no fallback)"] = ans.check != "fallback" and not ans.unverified
    checks["no error"] = ans.error is None
    if safeguards.rests_on_data(ans.trace, ans.text):
        checks["footer has a computed confidence"] = ans.footer.get("confidence") in ("High", "Medium", "Low")
    return checks


def numbers_checked(text: str) -> int:
    return sum(1 for m in safeguards._NUM.finditer(text) if safeguards._parse(m))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=None)
    ap.add_argument("--group", choices=["all", "core"], default="all")
    args = ap.parse_args()
    model = args.model or llm.model_name()
    conversations = json.loads((HERE / "questions.json").read_text(encoding="utf-8"))
    if args.group == "core":
        conversations = [c for c in conversations if c["conversation"] in CORE_CONVERSATIONS]

    results, t_in, t_out, secs = [], 0, 0, 0.0
    for conv in conversations:
        agent = Agent(model=model)           # a fresh conversation; follow-ups share it
        for turn in conv["turns"]:
            ans = agent.ask(turn["question"])
            checks = grade(turn, ans)
            ok = all(checks.values())
            t_in, t_out, secs = t_in + ans.input_tokens, t_out + ans.output_tokens, secs + ans.seconds
            results.append(dict(
                id=turn["id"], group=turn["group"], conversation=conv["conversation"], question=turn["question"],
                pass_when=turn["pass_when"], passed=ok, checks=checks, answer=ans.text,
                tools=[dict(name=t["name"], input=t["input"], is_error=t["is_error"]) for t in ans.trace],
                number_check=ans.check, unverified_numbers=ans.unverified, numbers_in_answer=numbers_checked(ans.text),
                warnings=[f"{w['airport_code']}: {w['type']}" for w in ans.warnings], footer=ans.footer,
                model_calls=ans.rounds, seconds=ans.seconds, input_tokens=ans.input_tokens, output_tokens=ans.output_tokens, model=ans.model))
            failed = [k for k, v in checks.items() if not v]
            print(f"{'PASS' if ok else 'FAIL'} {turn['id']} [{ans.check}] tools={[t['name'] for t in ans.trace]} {ans.seconds}s" + (f"  failed: {failed}" if failed else ""))

    passed = sum(r["passed"] for r in results)
    summary = dict(date=datetime.now().strftime("%Y-%m-%d %H:%M"), model=model, questions=len(results), passed=passed,
                   numbers_in_answers=sum(r["numbers_in_answer"] for r in results),
                   answers_with_untraceable_numbers=sum(1 for r in results if r["unverified_numbers"]),
                   answers_rewritten_once=sum(1 for r in results if r["number_check"] == "rewritten"),
                   total_seconds=round(secs, 1), avg_seconds=round(secs / max(1, len(results)), 1),
                   input_tokens=t_in, output_tokens=t_out)
    stamp = datetime.now().strftime("%Y-%m-%d")
    base = HERE / "results" / f"eval_{stamp}_{model}{'' if args.group == 'all' else '_' + args.group}"
    base.parent.mkdir(parents=True, exist_ok=True)
    base.with_suffix(".json").write_text(json.dumps(dict(summary=summary, results=results), indent=1, default=str), encoding="utf-8")

    md = [f"# Evaluation run - {summary['date']} - {model}", "",
          f"**{passed} of {len(results)} questions passed.** {summary['numbers_in_answers']} numbers appeared in the answers; "
          f"{summary['answers_with_untraceable_numbers']} answers ended with a number that could not be traced to a tool result; "
          f"{summary['answers_rewritten_once']} answers passed only after one automatic rewrite. "
          f"Average {summary['avg_seconds']}s per question; {t_in:,} input and {t_out:,} output tokens in total.", "",
          "| Id | Group | Result | Tools | Number check | Seconds |", "|---|---|---|---|---|---|"]
    for r in results:
        md.append(f"| {r['id']} | {r['group']} | {'PASS' if r['passed'] else 'FAIL'} | {', '.join(t['name'] for t in r['tools']) or '-'} | {r['number_check']} | {r['seconds']} |")
    for r in results:
        md += ["", f"## {r['id']} - {r['question']}", "", f"*Pass when:* {r['pass_when']}", "",
               f"*Result:* {'PASS' if r['passed'] else 'FAIL'}" + ("" if r["passed"] else " - failed: " + "; ".join(k for k, v in r["checks"].items() if not v)), "",
               "*Tool calls:* " + ("; ".join(f"`{t['name']}` {json.dumps(t['input'])}" for t in r["tools"]) or "none"), "",
               r["answer"], "",
               f"> Data period: {r['footer'].get('data_period')}  ", f"> Assumptions: {r['footer'].get('assumptions')}  ",
               f"> Confidence: {r['footer'].get('confidence')} - {r['footer'].get('confidence_reason')}"]
        if r["warnings"]:
            md.append(f"> Warnings printed: {', '.join(r['warnings'])}")
    base.with_suffix(".md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=1))
    print("saved", base.with_suffix(".md"))


if __name__ == "__main__":
    try:
        main()
    except llm.ConfigError as err:
        sys.exit(str(err))
