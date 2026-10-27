"""Step 2 of the write path: one tidy table per source, all keyed by the same airport code (the BTS code).

Reads data/raw/, writes data/clean/. No scoring here. Rules: missing stays empty (never 0), counts are stored
and rates are derived later, cargo is kept separate from passenger flights.
"""
import io
import zipfile

import numpy as np
import pandas as pd

from ..paths import CLEAN, RAW

TERRITORIES = {"PR", "GU", "VI", "AS", "MP"}
SIZE = {"L": "large", "M": "medium", "S": "small", "N": "nonhub"}


# ---------- airports (the universe) ----------

def faa_primary_airports(cfg) -> pd.DataFrame:
    """The FAA 'primary' airports (over 10,000 boardings a year) from the FAA boardings file."""
    raw = pd.read_excel(RAW / cfg["faa_boardings_file"], header=None, engine="openpyxl")
    header_row = next(i for i, row in raw.iterrows() if "Locid" in row.values)
    df = raw.iloc[header_row + 1:].copy()
    df.columns = [str(c).strip() for c in raw.iloc[header_row]]
    df = df[df["S/L"] == "P"]
    boardings_col = f"CY {str(cfg['faa_boardings_year'])[-2:]} Enplanements"
    out = pd.DataFrame({
        "faa_code": df["Locid"].astype(str).str.strip(),
        "name": df["Airport Name"].astype(str).str.strip(),
        "city": df["City"].astype(str).str.strip(),
        "state": df["ST"].astype(str).str.strip(),
        "size_class": df["Hub"].astype(str).str.strip().map(SIZE),
        "boardings_2025": pd.to_numeric(df[boardings_col], errors="coerce").astype("Int64"),
    }).reset_index(drop=True)
    return out


def summary_months() -> pd.DataFrame:
    """BTS T-100 airport-month summary, 2019 onward. Passengers are 'on board departing flights'."""
    cols = {"Origin Airport Code": "airport_code", "Date": "date", "Total Departures": "flights",
            "Total Passengers": "passengers", "Total Seats": "seats", "Domestic Passengers": "domestic_passengers",
            "Outbound International Passengers": "international_passengers"}
    df = pd.read_csv(RAW / "t100_by_origin.csv", usecols=list(cols), dtype={"Origin Airport Code": str}).rename(columns=cols)
    df["month"] = df["date"].str.slice(0, 2).astype(int)
    df["year"] = df["date"].str.slice(6, 10).astype(int)
    df = df[df["year"] >= 2019].drop(columns="date")
    num = ["flights", "passengers", "seats", "domestic_passengers", "international_passengers"]
    df[num] = df[num].apply(pd.to_numeric, errors="coerce")
    df = df.groupby(["airport_code", "year", "month"], as_index=False)[num].sum(min_count=1)
    return df


def last_complete_month(months: pd.DataFrame) -> tuple[int, int]:
    """The newest month can be incomplete (airlines file late). A month counts as complete when it has at
    least 80% as many reporting airports as the median of the twelve months before it."""
    counts = months.groupby(["year", "month"]).size().sort_index()
    keys = list(counts.index)
    for i in range(len(keys) - 1, 11, -1):
        if counts.iloc[i] >= 0.8 * counts.iloc[i - 12:i].median():
            return keys[i]
    return keys[-1]


def window_ending(end: tuple[int, int], n: int) -> list[tuple[int, int]]:
    y, m = end
    out = []
    for _ in range(n):
        out.append((y, m))
        y, m = (y, m - 1) if m > 1 else (y - 1, 12)
    return out[::-1]


def build_airports(cfg, months: pd.DataFrame, latest12: list[tuple[int, int]]) -> pd.DataFrame:
    air = faa_primary_airports(cfg)

    # Code crosswalk FAA -> BTS. Applied when the FAA code has no passengers in the latest 12 months
    # (this also catches a stale code that only has old data), not only when the code is absent.
    key = months["year"] * 100 + months["month"]
    recent = months[key.isin([y * 100 + m for y, m in latest12])].groupby("airport_code")["passengers"].sum()
    need = [c for c in air["faa_code"] if recent.get(c, 0) <= 0]
    our = pd.read_csv(RAW / "airports.csv", usecols=["local_code", "iata_code", "iso_country"], dtype=str)
    our = our[our["iso_country"].isin(["US"] + sorted(TERRITORIES)) & our["local_code"].isin(need) & our["iata_code"].notna()]
    xw = dict(zip(our["local_code"], our["iata_code"]))
    air["airport_code"] = air["faa_code"].map(lambda c: xw.get(c, c))

    # BTS master table: permanent id, the city the airport serves, the metro area (city market), coordinates.
    z = zipfile.ZipFile(RAW / "master_cord.zip")
    name = next(n for n in z.namelist() if n.startswith("T_"))
    master = pd.read_csv(z.open(name), dtype=str, encoding="utf-8-sig")
    master = master[master["AIRPORT_IS_LATEST"] == "1"].drop_duplicates("AIRPORT")
    master = master.rename(columns={"AIRPORT": "airport_code", "AIRPORT_ID": "bts_airport_id",
                                    "DISPLAY_AIRPORT_CITY_NAME_FULL": "served_city", "CITY_MARKET_ID": "metro_id",
                                    "LATITUDE": "latitude", "LONGITUDE": "longitude"})
    air = air.merge(master[["airport_code", "bts_airport_id", "served_city", "metro_id", "latitude", "longitude"]],
                    on="airport_code", how="left")
    air["latitude"] = pd.to_numeric(air["latitude"], errors="coerce")
    air["longitude"] = pd.to_numeric(air["longitude"], errors="coerce")
    air["is_territory"] = air["state"].isin(TERRITORIES)

    # A metro area is named after the city served by its biggest airport; airports alone in their market
    # simply carry their own served city.
    air["metro_airport_count"] = air.groupby("metro_id")["airport_code"].transform("count").where(air["metro_id"].notna(), 1)
    biggest = air.sort_values("boardings_2025", ascending=False).drop_duplicates("metro_id").set_index("metro_id")["served_city"]
    air["metro_name"] = air["metro_id"].map(biggest)
    air.loc[air["metro_airport_count"] > 1, "metro_name"] = air["metro_name"] + " metro area"
    air["metro_airport_count"] = air["metro_airport_count"].astype(int)
    cols = ["airport_code", "bts_airport_id", "faa_code", "name", "city", "served_city", "state", "is_territory",
            "metro_id", "metro_name", "metro_airport_count", "size_class", "boardings_2025", "latitude", "longitude"]
    return air[cols].sort_values("airport_code").reset_index(drop=True)


# ---------- delays ----------

def build_delays(codes: set[str]) -> pd.DataFrame:
    """BTS Airline Delay Causes: arriving flights of reporting airlines, by arrival airport and month."""
    frames = []
    for path in sorted(RAW.glob("dc_*.zip")):
        z = zipfile.ZipFile(path)
        frames.append(pd.read_csv(z.open("Airline_Delay_Cause.csv"), encoding="utf-8-sig",
                                  usecols=["year", "month", "carrier", "airport", "arr_flights", "arr_del15", "carrier_ct",
                                           "weather_ct", "nas_ct", "security_ct", "late_aircraft_ct", "arr_cancelled"]))
    df = pd.concat(frames, ignore_index=True).drop_duplicates(["year", "month", "carrier", "airport"])
    df = df[df["airport"].isin(codes)]
    ren = {"airport": "airport_code", "arr_flights": "arriving_flights", "arr_del15": "delayed_flights",
           "nas_ct": "system_delays", "carrier_ct": "airline_delays", "late_aircraft_ct": "late_aircraft_delays",
           "weather_ct": "weather_delays", "security_ct": "security_delays", "arr_cancelled": "cancelled_flights"}
    df = df.rename(columns=ren)
    num = [c for c in ren.values() if c != "airport_code"]
    return df.groupby(["airport_code", "year", "month"], as_index=False)[num].sum(min_count=1)


# ---------- routes and airlines ----------

def build_routes(cfg, codes: set[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    """BTS T-100 Segment, all carriers, domestic and international. A passenger flight has seats and a
    passenger service class (F scheduled, L non-scheduled); everything else is cargo."""
    routes, airlines = [], []
    use = ["DEPARTURES_PERFORMED", "SEATS", "PASSENGERS", "DISTANCE", "UNIQUE_CARRIER_NAME", "ORIGIN", "DEST", "MONTH", "CLASS"]
    for year in cfg["route_years"]:
        path = RAW / f"t100_{year}.zip"
        if not path.exists():
            continue
        z = zipfile.ZipFile(path)
        df = pd.read_csv(z.open("T_T100_SEGMENT_ALL_CARRIER.csv"), usecols=use, encoding="utf-8-sig",
                         dtype={"ORIGIN": str, "DEST": str, "CLASS": str, "UNIQUE_CARRIER_NAME": str})
        df = df[(df["DEPARTURES_PERFORMED"] > 0) & df["ORIGIN"].isin(codes)]
        pax = (df["SEATS"] > 0) & df["CLASS"].isin(["F", "L"])
        df["passenger_flights"] = np.where(pax, df["DEPARTURES_PERFORMED"], 0)
        df["pax"] = np.where(pax, df["PASSENGERS"], 0)
        df["pseats"] = np.where(pax, df["SEATS"], 0)
        months = int(df["MONTH"].nunique())
        r = df.groupby(["ORIGIN", "DEST"], as_index=False).agg(
            distance_miles=("DISTANCE", "max"), passenger_flights=("passenger_flights", "sum"),
            all_flights=("DEPARTURES_PERFORMED", "sum"), passengers=("pax", "sum"), seats=("pseats", "sum"))
        r.insert(1, "year", year)
        r["months_of_data"] = months
        routes.append(r.rename(columns={"ORIGIN": "airport_code", "DEST": "destination_code"}))
        a = df[pax].groupby(["ORIGIN", "UNIQUE_CARRIER_NAME"], as_index=False).agg(
            passengers=("pax", "sum"), passenger_flights=("passenger_flights", "sum"))
        a.insert(1, "year", year)
        airlines.append(a.rename(columns={"ORIGIN": "airport_code", "UNIQUE_CARRIER_NAME": "airline"}))
    return pd.concat(routes, ignore_index=True), pd.concat(airlines, ignore_index=True)


# ---------- FAA forecast ----------

def build_forecast(cfg, airports: pd.DataFrame) -> pd.DataFrame:
    """FAA Terminal Area Forecast. Scenario 0 is history, scenario 1 is the forecast. Fiscal years.
    'commercial_operations' are takeoffs PLUS landings by airlines (cargo included) - not BTS departures."""
    z = zipfile.ZipFile(RAW / cfg["faa_forecast_file"])
    faa_to_code = dict(zip(airports["faa_code"], airports["airport_code"]))

    def read(member, value_cols, out_name):
        df = pd.read_excel(io.BytesIO(z.read(member)), engine="openpyxl")
        df.columns = [str(c).strip().lower() for c in df.columns]
        df["locid"] = df["locid"].astype(str).str.strip()  # the FAA pads codes with spaces
        df = df[df["locid"].isin(faa_to_code)]
        df[out_name] = df[value_cols].apply(pd.to_numeric, errors="coerce").sum(axis=1, min_count=1)
        df["fiscal_year"] = pd.to_numeric(df["ayear"], errors="coerce").astype(int)
        df["is_forecast"] = pd.to_numeric(df["scenario"], errors="coerce") == 1
        df = df.sort_values("is_forecast").drop_duplicates(["locid", "fiscal_year"], keep="last")
        return df[["locid", "fiscal_year", "is_forecast", out_name]]

    enp = read("Enplanements.xlsx", ["aac", "commuter", "us_flag", "frgn_flag"], "boardings")
    ops = read("AirportsOperations.xlsx", ["itn_ac", "itn_at"], "commercial_operations")
    df = enp.merge(ops, on=["locid", "fiscal_year", "is_forecast"], how="outer")
    df = df[(df["fiscal_year"] >= 2019) & (df["fiscal_year"] <= 2045)]
    df.insert(0, "airport_code", df.pop("locid").map(faa_to_code))
    return df.sort_values(["airport_code", "fiscal_year"]).reset_index(drop=True)


# ---------- run ----------

def _cached(name: str, sources: list, build):
    """The two slow reads (forecast spreadsheets, route files) are rebuilt only when a raw file is newer."""
    out = CLEAN / name
    newest = max((p.stat().st_mtime for p in sources if p.exists()), default=0)
    if out.exists() and out.stat().st_mtime > newest:
        return pd.read_parquet(out)
    df = build()
    df.to_parquet(out, index=False)
    return df


def run(cfg, log=print) -> dict:
    CLEAN.mkdir(parents=True, exist_ok=True)
    months_all = summary_months()
    end = last_complete_month(months_all)
    latest12 = window_ending(end, 12)
    airports = build_airports(cfg, months_all, latest12)
    codes = set(airports["airport_code"])
    months = months_all[months_all["airport_code"].isin(codes)].copy()
    months["is_complete_month"] = (months["year"] * 100 + months["month"]) <= end[0] * 100 + end[1]
    log(f"  airports {len(airports)}, passenger months through {end[0]}-{end[1]:02d}")
    delays = build_delays(codes)
    log(f"  delay months {delays['year'].min()}-{delays['year'].max()}, airports with delay data {delays['airport_code'].nunique()}")

    route_files = [RAW / f"t100_{y}.zip" for y in cfg["route_years"]]
    def both():
        r, a = build_routes(cfg, codes)
        a.to_parquet(CLEAN / "airport_year_airlines.parquet", index=False)
        return r
    routes = _cached("airport_year_routes.parquet", route_files, both)
    airlines = pd.read_parquet(CLEAN / "airport_year_airlines.parquet")
    log(f"  routes {len(routes)} rows, years {sorted(int(y) for y in routes['year'].unique())}")
    forecast = _cached("airport_forecast.parquet", [RAW / cfg["faa_forecast_file"], RAW / cfg["faa_boardings_file"]],
                       lambda: build_forecast(cfg, airports))
    log(f"  forecast airports {forecast['airport_code'].nunique()}")

    airports.to_parquet(CLEAN / "airports.parquet", index=False)
    months.to_parquet(CLEAN / "airport_month.parquet", index=False)
    delays.to_parquet(CLEAN / "airport_month_delays.parquet", index=False)
    return dict(airports=airports, months=months, delays=delays, routes=routes, airlines=airlines, forecast=forecast,
                latest12=latest12)
