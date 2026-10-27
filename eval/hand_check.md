# Hand check against the source websites

Date: 2026-10-04. A spot check of the product's numbers against the original public websites, so the project has ground truth that did not come from its own pipeline. I opened each source website and ran the query by hand; the values below were read off the page (screenshots in `hand_check_screenshots/`). The "product says" column comes from the read-only tools in `airport_agent/tools.py`. No value in the "read on the website" column came from the pipeline.

**Result: 4 figures checked across both sources (FAA and BTS), all 4 match. 3 more values visible on the same pages also match.**

| # | Number | Product says | Read on the website | Page | Date | Match | Note |
|---|---|---|---|---|---|---|---|
| 1 | SFO FAA forecast, takeoffs and landings, fiscal 2025 | 406,220 | Air Carrier 380,290 + Air Taxi & Commuter 25,930 = 406,220 | taf.faa.gov, Query Data, Facility SFO, Detail Report (forecast issued March 2026) | 2026-10-04 | Yes | Exact. The FAA "Total" column (415,726) is higher because it adds private (GA) and military flights, which the product leaves out by design |
| 2 | SFO FAA forecast, takeoffs and landings, fiscal 2035 | 514,527 | Air Carrier 485,007 + Air Taxi & Commuter 29,520 = 514,527 | same report | 2026-10-04 | Yes | Exact. The gap, 108,307, is the product's "unmet flight demand" figure |
| 3 | SFO system delay rate, calendar 2024 | 15.2% | National Aviation System Delay 20,754 / Total Operations 136,912 = 15.16% | transtats.bts.gov/OT_Delay/OT_DelayCause1.asp, SFO, all carriers, January to December 2024, tabular version | 2026-10-04 | Yes | Rounds to 15.2%. BTS prints the same 15.16% on the page |
| 4 | LAX system delay rate, three years (August 2023 to July 2026) | 4.8% | National Aviation System Delay 28,455 / Total Operations 588,029 = 4.84% | same BTS page, LAX, all carriers, August 2023 to July 2026, tabular version | 2026-10-04 | Yes | Rounds to 4.8%. Total Operations equals the product's three-year arriving-flight count (588,029) exactly |

## Extra values on the same pages

| Value | Product says | Read on the website | Match |
|---|---|---|---|
| SFO FAA forecast boardings, fiscal 2025 | 26,106,722 | 26,106,722 (Enplanements, Total) | Yes |
| SFO FAA forecast boardings, fiscal 2035 | 34,567,301 | 34,567,301 (Enplanements, Total) | Yes |
| SFO overall delay rate, calendar 2024 | 29.5% | Five delay rows sum to 40,386 / 136,912 = 29.50% | Yes |

## Screenshots

- `hand_check_screenshots/1_faa_taf_sfo.png` - FAA Terminal Area Forecast detail report for SFO, fiscal 2025 to 2035
- `hand_check_screenshots/2_bts_delay_sfo_2024.png` - BTS delay causes, SFO, January to December 2024
- `hand_check_screenshots/3_bts_delay_lax_3yr.png` - BTS delay causes, LAX, August 2023 to July 2026

## Scope

- Covers two of the product's sources: the FAA Terminal Area Forecast and BTS Airline Delay Causes. It confirms a computed sum (two FAA columns), a one-year rate and a three-year rate built from summed counts, each from the raw counts on the page.
- Does not cover the FAA boardings file or BTS T-100 (passengers, cargo share, long-haul share). Those rest on the automated data checks and unit tests.
