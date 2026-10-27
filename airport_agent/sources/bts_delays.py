"""BTS Airline Delay Causes (airport-month, pre-aggregated). About 17 seconds per year.

The download form passes its filter in a query parameter with a letter-rotation encoding. It is undocumented,
so it could break; the format check below rejects anything that is not the expected zip.
"""
import string
from pathlib import Path

from .common import get, is_zip, save_checked

URL = "https://www.transtats.bts.gov/OT_Delay/ot_delaycause1_DL.aspx"
_ALPHABET = string.ascii_uppercase + string.ascii_lowercase + string.digits


def _encode(text: str) -> str:
    return "".join(_ALPHABET[(_ALPHABET.index(c) + 13) % 62] if c in _ALPHABET else c for c in text)


def fetch(year_from: int, month_from: int, year_to: int, month_to: int, dest: Path) -> Path:
    query = _encode(f"where yearmonth between {year_from * 12 + month_from} AND {year_to * 12 + month_to}")
    return save_checked(dest, lambda: get(URL, params={"8n4": query}), check=is_zip)
