"""One command for the whole write path: fetch -> clean -> score -> check -> write the serving tables.

    python -m airport_agent.pipeline.build             build from the raw files already downloaded (fetch what is missing)
    python -m airport_agent.pipeline.build --refresh   re-pull every source from the public APIs and endpoints first

If a data check fails the build stops and the previous serving tables stay in place.
"""
import argparse
import json
import sys
from datetime import datetime, timezone

import pandas as pd

from ..paths import SERVING, settings
from . import checks, clean, fetch, score


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--refresh", action="store_true", help="re-download every source (about 15 minutes)")
    args = ap.parse_args(argv)
    cfg = settings()

    print("1. fetch")
    report = fetch.fetch_all(refresh=args.refresh)
    missing = [e["file"] for e in report if e["status"] == "failed, no file"]
    if missing:
        print(f"STOPPED: could not download {missing} and no earlier copy exists.")
        return 1
    print("2. clean")
    cleaned = clean.run(cfg)
    print("3. score")
    tables = score.run(cleaned, cfg)
    again = score.run(cleaned, cfg)
    deterministic = all(tables[k].equals(again[k]) for k in tables if isinstance(tables[k], pd.DataFrame))
    print("4. check")
    results = checks.run(tables, cleaned, cfg)
    results.append(dict(check="scoring twice gives identical tables (deterministic)", ok=deterministic, detail=""))
    if not checks.summarize(results):
        print("STOPPED: a data check failed. The previous serving tables were left untouched.")
        return 1

    print("5. write serving tables")
    SERVING.mkdir(parents=True, exist_ok=True)
    built_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    periods = tables.pop("periods")
    tables["airport_metrics"]["built_at"] = built_at
    for name, df in tables.items():
        df.to_parquet(SERVING / f"{name}.parquet", index=False)
        print(f"  {name}: {len(df):,} rows")
    m = tables["airport_metrics"]
    manifest = dict(built_at=built_at, score_version=str(cfg["score_version"]), periods=periods, sources=report,
                    rows={k: len(v) for k, v in tables.items()}, checks_passed=f"{len(results)} of {len(results)}",
                    checks=results,
                    summary=dict(airports=len(m), data_tiers=m["data_tier"].value_counts().to_dict(),
                                 confidence=m["confidence"].value_counts().to_dict()))
    (SERVING / "fetch_manifest.json").write_text(json.dumps(manifest, indent=1, default=str), encoding="utf-8")
    print("done:", manifest["summary"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
