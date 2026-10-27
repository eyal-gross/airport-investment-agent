"""The sources that are a single file at a stable address."""
from pathlib import Path

from .common import get, is_zip, save_checked

BTS_SUMMARY_API = "https://data.bts.gov/resource/r495-tyji.csv"  # Socrata API: T-100 airport-month summary
BTS_SUMMARY_EXPORT = "https://data.bts.gov/api/views/r495-tyji/rows.csv?accessType=DOWNLOAD"
OURAIRPORTS = "https://davidmegginson.github.io/ourairports-data/airports.csv"


def fetch_bts_summary(dest: Path) -> Path:
    """BTS T-100 airport-month summary, 2014 onward, through the data.bts.gov public API export."""
    ok = lambda p: p.stat().st_size > 5_000_000 and b"Origin Airport Code" in p.open("rb").readline()
    return save_checked(dest, lambda: get(BTS_SUMMARY_EXPORT, timeout=600), check=ok)


def fetch_faa_forecast(url: str, dest: Path) -> Path:
    return save_checked(dest, lambda: get(url, timeout=600), check=is_zip)


def fetch_faa_boardings(url: str, dest: Path) -> Path:
    return save_checked(dest, lambda: get(url), check=is_zip)  # an .xlsx file is a zip


def fetch_ourairports(dest: Path) -> Path:
    ok = lambda p: b"iata_code" in p.open("rb").readline()
    return save_checked(dest, lambda: get(OURAIRPORTS), check=ok)
