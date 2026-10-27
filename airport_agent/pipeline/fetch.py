"""Step 1 of the write path: download every public source into data/raw/.

Files already present are reused unless refresh=True. Every download goes to a temporary file and is swapped in
only after it passes its format check, so a failed fetch leaves the previous file in place.
"""
import json
from datetime import datetime, timezone

from ..paths import RAW, settings
from ..sources import bts_delays, bts_segment, simple


def _delay_files(first_year: int) -> list[tuple[str, tuple[int, int, int, int]]]:
    """One file per calendar year from first_year to this year (the current year is simply partial)."""
    this_year = datetime.now().year
    return [(f"dc_{y}.zip", (y, 1, y, 12)) for y in range(first_year, this_year + 1)]


def plan(cfg: dict) -> list[dict]:
    jobs = [
        dict(source="BTS T-100 airport-month summary (data.bts.gov API)", file="t100_by_origin.csv",
             url=simple.BTS_SUMMARY_EXPORT, run=lambda d: simple.fetch_bts_summary(d), always=True),
        dict(source="FAA Terminal Area Forecast", file=cfg["faa_forecast_file"], url=cfg["faa_forecast_url"],
             run=lambda d: simple.fetch_faa_forecast(cfg["faa_forecast_url"], d)),
        dict(source="FAA passenger boardings", file=cfg["faa_boardings_file"], url=cfg["faa_boardings_url"],
             run=lambda d: simple.fetch_faa_boardings(cfg["faa_boardings_url"], d)),
        dict(source="OurAirports (code crosswalk)", file="airports.csv", url=simple.OURAIRPORTS,
             run=lambda d: simple.fetch_ourairports(d)),
        dict(source="BTS Master Coordinate table", file="master_cord.zip", url=bts_segment.MASTER_URL,
             run=lambda d: bts_segment.fetch_master(d)),
    ]
    for name, (y1, m1, y2, m2) in _delay_files(cfg["delay_first_year"]):
        jobs.append(dict(source=f"BTS Airline Delay Causes {y1}", file=name, url=bts_delays.URL,
                         run=lambda d, a=(y1, m1, y2, m2): bts_delays.fetch(*a, d)))
    for y in cfg["route_years"]:
        jobs.append(dict(source=f"BTS T-100 Segment {y}", file=f"t100_{y}.zip", url=bts_segment.SEGMENT_URL,
                         run=lambda d, y=y: bts_segment.fetch(y, d)))
    return jobs


def fetch_all(refresh: bool = False, log=print) -> list[dict]:
    cfg = settings()
    RAW.mkdir(parents=True, exist_ok=True)
    report = []
    for job in plan(cfg):
        dest = RAW / job["file"]
        entry = dict(source=job["source"], file=job["file"], url=job["url"])
        if dest.exists() and not refresh:
            entry.update(status="reused", fetched_at=datetime.fromtimestamp(dest.stat().st_mtime, timezone.utc).isoformat(timespec="seconds"))
        else:
            try:
                log(f"fetching {job['source']} ...")
                job["run"](dest)
                entry.update(status="fetched", fetched_at=datetime.now(timezone.utc).isoformat(timespec="seconds"))
            except Exception as err:
                kept = dest.exists()
                entry.update(status="failed, previous file kept" if kept else "failed, no file", error=str(err),
                             fetched_at=datetime.fromtimestamp(dest.stat().st_mtime, timezone.utc).isoformat(timespec="seconds") if kept else None)
                log(f"  FAILED: {err}")
        report.append(entry)
    (RAW / "fetch_report.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    return report
