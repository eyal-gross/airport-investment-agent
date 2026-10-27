"""BTS TranStats tables that have no API: the download form is replayed (load the page, post it back with the
wanted fields ticked).

- T-100 Segment, all carriers (routes, airlines, cargo): one file per year, about 3 minutes each.
- Master Coordinate table (permanent airport ids, served city, metro area, coordinates): one small file.
"""
import re
from pathlib import Path

import requests

from .common import UA, is_zip, save_checked

BASE = "https://www.transtats.bts.gov/DL_SelectFields.aspx"
SEGMENT_URL = BASE + "?gnoyr_VQ=FMG&QO_fu146_anzr=Nv4%20Pn44vr45"
MASTER_URL = BASE + "?gnoyr_VQ=FLL&QO_fu146_anzr=N8vn6v10%20f722146%20gnoyr5"
SEGMENT_FIELDS = ["YEAR", "MONTH", "UNIQUE_CARRIER", "UNIQUE_CARRIER_NAME", "ORIGIN_AIRPORT_ID", "ORIGIN",
                  "ORIGIN_CITY_NAME", "ORIGIN_STATE_ABR", "ORIGIN_COUNTRY", "DEST_AIRPORT_ID", "DEST", "DEST_CITY_NAME",
                  "DEST_STATE_ABR", "DEST_COUNTRY", "DEPARTURES_SCHEDULED", "DEPARTURES_PERFORMED", "SEATS",
                  "PASSENGERS", "FREIGHT", "DISTANCE", "AIR_TIME", "AIRCRAFT_TYPE", "CLASS", "DATA_SOURCE"]
MASTER_FIELDS = ["AIRPORT_ID", "AIRPORT", "DISPLAY_AIRPORT_NAME", "DISPLAY_AIRPORT_CITY_NAME_FULL",
                 "AIRPORT_COUNTRY_CODE_ISO", "AIRPORT_STATE_CODE", "CITY_MARKET_ID", "LATITUDE", "LONGITUDE",
                 "AIRPORT_IS_CLOSED", "AIRPORT_IS_LATEST"]


def _download(url: str, fields: list[str], year: int | None = None) -> bytes:
    s = requests.Session()
    s.headers["User-Agent"] = UA
    page = s.get(url, timeout=120).text
    form = {k: re.search(r'id="%s" value="([^"]*)"' % k, page).group(1)
            for k in ("__VIEWSTATE", "__VIEWSTATEGENERATOR", "__EVENTVALIDATION")}
    form.update({"__EVENTTARGET": "", "__EVENTARGUMENT": "", "__LASTFOCUS": "", "cboGeography": "All",
                 "cboPeriod": "All", "chkDownloadZip": "on", "btnDownload": "Download"})
    if year is not None:
        form["cboYear"] = str(year)
    form.update({f: "on" for f in fields})
    r = s.post(url, data=form, timeout=600, headers={"Referer": url})
    r.raise_for_status()
    return r.content


def fetch(year: int, dest: Path) -> Path:
    return save_checked(dest, lambda: _download(SEGMENT_URL, SEGMENT_FIELDS, year), check=is_zip, attempts=2)


def fetch_master(dest: Path) -> Path:
    return save_checked(dest, lambda: _download(MASTER_URL, MASTER_FIELDS), check=is_zip, attempts=2)
