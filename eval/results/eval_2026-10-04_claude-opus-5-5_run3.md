# Evaluation run - 2026-10-04 18:01 - claude-opus-5-5

**24 of 24 questions passed.** 747 numbers appeared in the answers; 0 answers ended with a number that could not be traced to a tool result; 3 answers passed only after one automatic rewrite. Average 13.4s per question; 702,927 input and 25,947 output tokens in total.

| Id | Group | Result | Tools | Number check | Seconds |
|---|---|---|---|---|---|
| A1 | core | PASS | rank_airports | passed | 12.4 |
| A2 | core | PASS | find_airport, find_airport, compare_airports, airport_profile, airport_profile | passed | 16.5 |
| A6 | follow-up | PASS | compare_airports | passed | 9.7 |
| A3 | core | PASS | find_airport, airport_profile | passed | 9.9 |
| A7 | follow-up | PASS | airport_profile | passed | 8.6 |
| A4 | core | PASS | airport_profile | passed | 11.1 |
| A5 | follow-up | PASS | find_airport, compare_airports, airport_profile | passed | 11.5 |
| A8 | follow-up | PASS | find_airport, airport_profile | passed | 15.4 |
| B1 | filters | PASS | rank_airports | rewritten | 18.0 |
| B2 | filters | PASS | rank_airports | passed | 10.0 |
| B3 | filters | PASS | rank_airports, rank_airports | passed | 12.2 |
| B4 | ambiguous | PASS | find_airport, find_airport | passed | 12.4 |
| B5 | filters | PASS | rank_airports | rewritten | 21.1 |
| B6 | time | PASS | find_airport, airport_profile | passed | 11.4 |
| B7 | filters | PASS | rank_airports | passed | 14.3 |
| B8 | time | PASS | find_airport, airport_trend, airport_trend | passed | 12.5 |
| C1 | time | PASS | rank_airports, rank_airports | passed | 15.2 |
| C2 | out of scope | PASS | rank_airports, airport_profile, airport_profile, airport_profile, airport_profile | passed | 18.3 |
| C3 | out of scope | PASS | airport_profile | passed | 12.2 |
| C4 | out of scope | PASS | find_airport | rewritten | 12.6 |
| C5 | out of scope | PASS | rank_airports, rank_airports | passed | 13.3 |
| C6 | judgment | PASS | find_airport, airport_profile | passed | 13.2 |
| C7 | out of scope | PASS | find_airport | passed | 11.4 |
| C8 | awkward data | PASS | find_airport, find_airport, find_airport, airport_profile | passed | 17.4 |

## A1 - Which airports in New England are strong candidates for terminal expansion?

*Pass when:* A ranked list from the six states, scores shown, reasons given.

*Result:* PASS

*Tool calls:* `rank_airports` {"region": "new england"}

By our capacity-need score, Boston Logan (BOS), Burlington (BTV) and Portland, Maine (PWM) are New England's strongest candidates. Bangor (BGR) and Bradley/Hartford (BDL) come next. One limit up front: no public data measures terminal or gate use. "Terminal expansion" is judged here on how full the planes are, passenger growth and FAA forecasts. The **passenger-side score** fits a terminal question best.

| Airport | Size class | Total score | Passenger score | Planes full (%) | Passenger growth since 2019 (%) | FAA forecast passenger growth (%) | Forecast extra boardings by 2035 |
|---|---|---|---|---|---|---|---|
| Boston Logan (BOS) | large | 82.9 | 72.2 | 81.7 | 1.2 | 26.5 | 5,612,088 |
| Burlington (BTV) | small | 79.2 | 73.7 | 83.0 | 2.3 | 22.9 | 163,754 |
| Portland, ME (PWM) | small | 77.4 | 79.2 | 82.8 | 17.2 | 21.6 | 278,078 |
| Bangor (BGR) | nonhub | 71.8 | 78.0 | 80.4 | 40.8 | 24.1 | 103,055 |
| Bradley (BDL) | medium | 65.9 | 60.8 | 81.3 | -2.7 | 15.7 | 523,236 |

**What the numbers show:**
- **Boston (BOS)** has by far the largest forecast gain in passengers. It is flagged as strained, mainly on the flight side: a 9.1% system delay rate, which is mostly congestion but is coded by airlines and includes ordinary weather. Its passenger numbers are flat since 2019.
- **Portland (PWM) and Bangor (BGR)** have the strongest passenger-side scores, backed by real growth: 17.2% and 40.8%. At Portland, the number of flights stayed flat while passengers rose, so the growth is coming through fuller or larger planes. That fits a terminal-side constraint more than an airfield one.
- **Burlington (BTV)** scores high mostly on full planes and the FAA forecast, not on growth so far.
- **Bradley (BDL)** carries fewer passengers than in 2019.

FAA forecasts are used to compare airports, not as predictions; the FAA tends to over-forecast. Four airports have only partial data and are not ranked: Tweed/New Haven (HVN), Cape Cod Gateway (HYA), Block Island (BID) and Westerly (WST).

To check next: gate counts and terminal use, any projects already planned, and cost. None of these are in our data. I can pull a full profile of any of these airports.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years); FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, Passenger-side score, Flight-side score, How full the planes are, FAA forecast passenger growth, System delay rate; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - the answer uses proxy measures (scores, system delay rate, load factor or forecasts)

## A2 - Compare LA and Santa Ana airport congestion levels.

*Pass when:* LAX vs SNA side by side, a clear verdict, Santa Ana's legal cap flagged.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "LA"}; `find_airport` {"query": "Santa Ana"}; `compare_airports` {"airport_codes": ["LAX", "SNA"]}; `airport_profile` {"airport_code": "LAX"}; `airport_profile` {"airport_code": "SNA"}

LAX is more congested than Santa Ana (SNA), but only modestly. Neither airport counts as "strained" in our data, which would mean a system delay rate in the top quarter of the 343 ranked airports.

I took "LA" to mean Los Angeles International (LAX). The LA metro area also has Ontario (ONT), Hollywood Burbank (BUR) and Long Beach (LGB). Santa Ana is John Wayne/Orange County (SNA).

| Measure | LAX | SNA |
|---|---|---|
| System delay rate, 3 years | 4.8% | 3.9% |
| System delay rate, latest 12 months | 5.0% | 4.3% |
| Overall delay rate (15+ min, any cause) | 18.9% | 17.5% |
| Rank on system delay (0-100 among peers) | 70.9 | 47.1 |
| System share of delayed flights | 25.7% | 22.4% |
| Flight-side score | 80.5 | 58.7 |

**What the numbers mean:** The system delay rate is our measure of congestion. It counts arrivals delayed by the airport and air-traffic system. Airlines assign that cause, and it includes ordinary weather, so it's mostly, but not purely, congestion. LAX's three-year rate is 1.23 times SNA's. At both airports, most delays come from the airlines or from late-arriving aircraft, not the system.

**Trend:** Both airports' latest-12-month rates are a bit above their three-year averages. Our check finds no recent spike at either, so this isn't a sharp new deterioration. LAX's system delay rate was higher in 2019 (6.3%), when it had more flights. Its passenger flights are down 17.4% since then.

**Warnings that change the picture:**
- **SNA has a legal cap:** passengers, average daily departures and a night curfew. In our units (departing passengers) the cap is roughly 6.1-6.25 million a year. SNA carried 5,590,354 in the latest 12 months, so the cap may limit growth more than congestion does.
- **LAX has cut capacity:** seats are down 12.8% since 2019. Its full planes reflect fewer seats, not rising demand.

I don't have gate, terminal or peak-hour data, so this covers airfield delays only.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, Flight-side score, How full the planes are, System delay rate; 'LA' was taken to mean LAX; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - LAX: capacity cut; SNA: legal limit; the answer uses proxy measures (scores, system delay rate, load factor or forecasts); an airport name was resolved by default
> Warnings printed: SNA: legal_limit, LAX: capacity_cut

## A6 - And how did congestion at those two look in 2023?

*Pass when:* Uses the same two airports without being told again, and 2023 values.

*Result:* PASS

*Tool calls:* `compare_airports` {"airport_codes": ["LAX", "SNA"], "year": 2023}

In 2023 LAX was again more congested than SNA, and the gap was wider than it is now. LAX's system delay rate was 1.33 times SNA's, compared with 1.23 times over the latest three years.

| Calendar 2023 | LAX | SNA | Difference |
|---|---|---|---|
| System delay rate | 5.6% | 4.2% | 1.4 points |
| Overall delay rate (15+ min, any cause) | 20.5% | 18.5% | 2.0 points |
| Arriving flights in delay data | 195,617 | 45,732 | - |
| Passengers (departing) | 37,119,938 | 5,725,328 | - |

**How 2023 compares with later years:**
- **LAX:** 2023 was a high year for system delays. The rate was 5.6% in 2023, 4.9% in 2024 and 4.6% in 2025, and it is 5.0% so far in 2026 (7 months of delay data). Its overall delay rate also peaked in 2023 at 20.5%.
- **SNA:** steadier. The system delay rate was 4.2% in 2023, 3.7% in 2024 and 4.3% in 2025, and it is 4.1% so far in 2026.

**Notes:**
- The system delay category is coded by airlines and includes ordinary weather, so it's mostly, but not purely, congestion. It covers only domestic flights of the larger reporting airlines.
- For past years I can show only raw metrics like these. The capacity-need score and peer rankings exist for the latest period only, so I can't tell you whether either airport counted as "strained" in 2023.
- The current warnings still apply. SNA has a legal cap on passengers and departures, plus a night curfew. LAX's full planes reflect seats cut since 2019 more than rising demand.

If you want to see which months drove LAX's 2023 rate, I can pull the month-by-month series.

> Data period: BTS T-100 airport-month summary, calendar 2023; BTS Airline Delay Causes, calendar 2023; BTS T-100 Segment, calendar 2023  
> Assumptions: proxies, not direct measurements: How full the planes are, System delay rate  
> Confidence: Medium - LAX: capacity cut; SNA: legal limit; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: SNA: legal_limit, LAX: capacity_cut

## A3 - What is the percentage of long haul flights out of Anchorage airport?

*Pass when:* One number, the 3,000-mile definition stated, the cargo-included number next to it.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Anchorage airport"}; `airport_profile` {"airport_code": "ANC"}

At Ted Stevens Anchorage International (ANC), **2.8% of departing passenger flights are long-haul**, meaning they fly 3,000 miles or more. If you count cargo flights too, the share rises to **31.0%**. I assumed you meant ANC. The only other covered airport in Anchorage is Merrill Field (MRI), a much smaller airport with partial data.

The two numbers differ because cargo makes up 56.6% of ANC's departing flights, and many of those cargo flights are long-distance. Of 87,988 departing flights in calendar 2025, 38,150 were passenger flights and 49,838 were cargo or other non-passenger flights.

"Long-haul" has no official definition. We use 3,000 miles by default, and the share changes a lot with the cutoff:

| Cutoff | Passenger flights | All flights incl. cargo |
|---|---|---|
| 2,000+ miles | 13.7% (5,239 flights) | 47.4% (41,732) |
| 2,500+ miles | 9.8% (3,723) | 43.2% (37,969) |
| 3,000+ miles | 2.8% (1,061) | 31.0% (27,305) |

These shares count departing flights, both domestic and international, across all airlines. Passenger traffic at ANC is 98.6% domestic, and its biggest airline is Alaska Airlines, with 61.4% of passengers.

**Why this matters for capacity:** cargo flights use the same runways as passenger flights but aren't counted in the capacity-need score. However, the FAA's flight forecast, which feeds the score, does include cargo. So read ANC's flight-side figures with its cargo traffic in mind.

I can rerun the shares at a different cutoff if you want.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, Flight-side score, FAA forecast passenger growth, FAA forecast flight growth; long-haul means 3,000 miles or more (our definition; adjustable); 'Anchorage airport' was taken to mean ANC; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - ANC: cargo heavy; the answer uses proxy measures (scores, system delay rate, load factor or forecasts); an airport name was resolved by default
> Warnings printed: ANC: cargo_heavy

## A7 - What if long-haul means over 2,300 miles?

*Pass when:* Recomputed at 2,300 miles for Anchorage.

*Result:* PASS

*Tool calls:* `airport_profile` {"airport_code": "ANC", "long_haul_miles": 2300}

With a 2,300-mile cutoff, **12.6% of passenger flights departing Anchorage (ANC) count as long-haul** (4,820 flights). Counting cargo flights too, the share is **46.5%** (40,947 flights). Both figures are for calendar 2025 and include domestic and international flights. Note that the tool counts flights of 2,300 miles or more, so a flight of exactly 2,300 miles is included.

| Cutoff | Passenger flights | All flights incl. cargo |
|---|---|---|
| 2,000+ miles | 13.7% | 47.4% |
| **2,300+ miles** | **12.6%** | **46.5%** |
| 2,500+ miles | 9.8% | 43.2% |
| 3,000+ miles | 2.8% | 31.0% |

**What this shows:**
- **Passenger flights:** Moving the cutoff from 2,000 to 2,300 miles barely changes the passenger share. The big drops come above 2,300 miles: the share falls to 9.8% at 2,500 and to 2.8% at 3,000. So many of ANC's longer passenger flights are between about 2,300 and 3,000 miles, which means the passenger figure depends heavily on which cutoff you pick.
- **Cargo:** With cargo included, almost half of all departures are 2,300 miles or more. That's because cargo makes up 56.6% of ANC's flights. Cargo uses the same runways as passenger flights but isn't counted in the capacity-need score.

I can run the same cutoff on other airports to compare.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score; long-haul means 2,300 miles or more (our definition; adjustable); scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - ANC: cargo heavy; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: ANC: cargo_heavy

## A4 - What is the unmet flight demand in SFO airport and why?

*Pass when:* An estimate named as an estimate or proxy, with the why from the delay data.

*Result:* PASS

*Tool calls:* `airport_profile` {"airport_code": "SFO"}

San Francisco International (SFO) has an estimated **unmet flight demand of about 108,307 extra takeoffs and landings a year** by fiscal 2035. That is an estimate, not a measurement. It is the FAA forecast rising from 406,220 commercial operations (FY2025) to 514,527 (FY2035), which is +26.7%. FAA operations count takeoffs plus landings and include cargo, though cargo is only 1.2% of SFO flights. The FAA tends to over-forecast.

**Why it counts as "unmet":** we only use that label when an airport is strained today, and SFO is.

- **System delay rate: 13.4%** of arriving flights over three years. That is the highest among full-data airports (position 100 of 100). This category is coded by airlines and covers airport and air-traffic system delays, including ordinary weather.
- **Delay causes:** system delays make up 48.9% of delayed flights. Airline causes are 24.7%, late aircraft 23.7% and extreme weather only 2.5%. Most delays trace to the airfield and airspace, not the carriers.
- **Overall delay rate:** 27.4% of arrivals were 15+ minutes late.
- **Flight-side score:** 97.1. SFO ranks 3rd of 343 overall and 2nd of 30 large hubs.

**Caveats that matter:**
- **Recent spike, not a steady trend:** the latest-12-month system delay rate of 17.3% comes mostly from April-July 2026, which ran at 30.0%. The same months a year earlier ran at 7.8%, and the rest of the year at 10.3%. A temporary cause that isn't in our data is possible.
- **Capacity was cut:** seats are down 5.0% and passenger flights down 11.0% since 2019. So the full planes (82.6% of seats filled) partly reflect fewer seats, not only rising demand.
- **Scheduling limit:** SFO is under FAA Level 2 schedule facilitation. Schedules are coordinated, but there is no hard cap.

Background (not from our data): SFO's closely spaced parallel runways lose capacity when low clouds or fog prevent paired approaches. This is a common explanation for its high system delays.

**Worth checking next:** the cause of the 2026 spike and any airfield projects already planned.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); FAA passenger boarding data CY2025, calendar 2025; BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, Flight-side score, How full the planes are, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; 'unmet flight demand' is an estimate from the FAA forecast, used only when the airport is strained today; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - SFO: capacity cut; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: SFO: capacity_cut

## A5 - How does that compare with Oakland?

*Pass when:* Oakland is not called unmet demand, because it is not strained.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Oakland"}; `compare_airports` {"airport_codes": ["SFO", "OAK"]}; `airport_profile` {"airport_code": "OAK"}

Oakland San Francisco Bay (OAK) has **no unmet flight demand by our definition**. The FAA forecasts +30,637 takeoffs and landings by fiscal 2035 (+24.8%), but OAK isn't strained, so that number is only forecast growth. SFO's forecast gap is about 3.5 times larger (108,307) and does count as unmet, because SFO is the most delay-constrained airport in the dataset. I took "Oakland" to mean OAK. The Bay Area also has San Jose (SJC).

| | SFO | OAK |
|---|---|---|
| Capacity-need score | 86.9 (3rd of 343) | 46.0 (208th of 343) |
| Flight-side score | 97.1 | 49.7 |
| Forecast extra operations by 2035 | 108,307 | 30,637 |
| System delay rate, 3 years | 13.4% | 2.3% |
| System delay rate, latest 12 months | 17.3% | 1.7% |
| Overall delay rate | 27.4% | 18.4% |
| System share of delays | 48.9% | 12.3% |
| Planes full (passengers / seats) | 82.6% | 74.2% |
| Passengers vs 2019 | -4.4% | -35.5% |

**Why OAK isn't constrained:** its system delay rate (delays airlines blame on the airport and air-traffic system, ordinary weather included) is low and steady. There is no recent spike. Most OAK delays come from late-arriving aircraft (54.1%) and airline causes (32.5%), which point to airline operations rather than a lack of airfield capacity.

**Warnings for OAK:**
- **Traffic has shrunk, not grown:** seats are down 31.5% and passenger flights down 32.2% since 2019. The airport has room it isn't using.
- **One airline dominates:** Southwest carries 76.7% of passengers. If it cuts service, the forecast growth may not arrive.
- **Cargo is significant:** 17.9% of departing flights are cargo, which shares the runways but isn't in the score.

In short, SFO shows strain today plus forecast growth. OAK shows forecast growth on top of a shrinking base.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, Flight-side score, How full the planes are, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; 'unmet flight demand' is an estimate from the FAA forecast, used only when the airport is strained today; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - SFO: capacity cut; OAK: capacity cut; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: SFO: capacity_cut, OAK: single_airline, OAK: capacity_cut

## A8 - Is Memphis a good candidate, given its cargo traffic?

*Pass when:* Uses the Memphis profile and the cargo share.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Memphis"}; `airport_profile` {"airport_code": "MEM"}

**Memphis (MEM) looks like a mixed case for passenger capacity.** Its capacity-need score is 59.5, which ranks it 46th of 78 small-hub airports and 116th of 343 overall. Most of that score comes from the flight side, and cargo probably drives much of the flight side.

**Why cargo matters here:** 65.1% of departing flights are cargo. Cargo isn't in the score, but it does count in the FAA's flight forecast, so the forecast 18.4% growth in operations (29,629 extra takeoffs and landings by fiscal 2035) is likely mostly cargo.

Background (not from our data): Memphis is FedEx's main global hub, which explains the cargo share.

| Measure | MEM | Position among peers (0-100) |
|---|---|---|
| Flight-side score | 73.7 | - |
| Passenger-side score | 45.4 | - |
| How full the planes are | 73.4% | 33.6 |
| Passenger growth since 2019 | 0.9% | 39.5 |
| FAA forecast passenger growth | 25.8% | 75.0 |
| System delay rate (3 years) | 4.9% | 74.0 |
| FAA forecast flight growth | 18.4% | 73.4 |

**The passenger evidence is weak:**
- Passenger numbers are flat compared with 2019.
- Seats are up 6.7% over the same period, so seat supply is growing faster than demand.
- Planes are less full than in 2019 (77.6% then).
- Passenger flights are down 7.7% since 2019.

The FAA expects about 609,000 more boardings a year by 2035. The FAA tends to over-forecast, though, and the trend so far doesn't support that growth.

**Congestion is moderate.** The system delay rate is 4.9% over three years and 5.1% in the latest 12 months, with no recent spike. Airlines code this category, and it includes ordinary weather. The airport and air-traffic system caused only 21.4% of delayed flights; late aircraft (39.4%) and airline causes (35.3%) caused more. MEM isn't classed as strained, so the forecast growth is not called unmet demand. Also, the delay data covers passenger airlines only, so it doesn't measure cargo congestion.

**What to check next:** the cargo operator's expansion plans, how much of the forecast growth is cargo, and runway and apron use. None of these is in our data.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); FAA passenger boarding data CY2025, calendar 2025; BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, Passenger-side score, Flight-side score, How full the planes are, FAA forecast passenger growth, System delay rate; 'unmet flight demand' is an estimate from the FAA forecast, used only when the airport is strained today; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - MEM: cargo heavy; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: MEM: cargo_heavy

## B1 - Score the top 3 airports that have the highest congestion in the US, only small airports.

*Pass when:* Small-hub class, sorted by the system delay rate, three airports with scores; says what 'small' means.

*Result:* PASS

*Tool calls:* `rank_airports` {"size_classes": ["small"], "sort_by": "system_delay_rate_pct", "limit": 3}

Among FAA small-hub airports, the 3 most congested are Punta Gorda (PGD), Key West (EYW) and St. Thomas (STT). Only Punta Gorda also has a top capacity-need score: it ranks 1st of 78 small hubs. Key West ranks 32nd and St. Thomas 26th.

Here, "congestion" means the system delay rate. That's arrival delays blamed on the airport and air-traffic system, divided by arriving flights, over 3 years. Airlines decide which delays go in this category, and it includes ordinary weather, so it mostly, but not only, reflects congestion. "Small airports" means the FAA small-hub class.

| Airport | System delay rate | Capacity-need score | Passenger side | Flight side | Planes full | Passenger growth since 2019 | FAA forecast flight growth |
|---|---|---|---|---|---|---|---|
| Punta Gorda (PGD), FL | 8.6% | 94.9 | 93.3 | 96.5 | 85.8% | 37.0% | 26.8% |
| Key West (EYW), FL | 8.0% | 67.7 | 64.2 | 71.2 | 77.3% | 55.9% | 9.3% |
| St. Thomas (STT), USVI | 7.9% | 70.8 | 62.3 | 79.3 | 77.9% | 41.2% | 15.0% |

**Things that change the picture:**
- **Punta Gorda:** Allegiant Air carries 99.6% of its passengers. If Allegiant cuts service, the forecast growth may not happen, and the score doesn't account for this.
- **St. Thomas:** It's in a US territory (the US Virgin Islands). If you meant US states only, the next airport on the list would take its place, and I can pull it.
- **All three:** The data marks all three as strained today.
- **Left out:** Tweed/New Haven (HVN) wasn't ranked because its data is incomplete.

Key West and St. Thomas are congested, but their scores are only mid-range. That's mostly because the FAA forecasts less flight growth there. A next step could be to compare the 3 side by side on delay causes, or to check whether the delays are rising in recent months.

> Data period: BTS Airline Delay Causes, 2023-08 to 2026-07 (three years); BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: System delay rate, Capacity-need score, Passenger-side score, Flight-side score, How full the planes are, FAA forecast passenger growth; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: PGD: single_airline

## B2 - Top 5 airports in Texas by how full the planes are.

*Pass when:* Five Texas airports by load factor.

*Result:* PASS

*Tool calls:* `rank_airports` {"states": ["TX"], "sort_by": "load_factor_pct", "limit": 5}

Dallas-Fort Worth (DFW) and McAllen (MFE) are tied for the fullest planes in Texas, at 82.5% of seats filled. Houston Bush (IAH), Abilene (ABI) and Corpus Christi (CRP) come next. All 25 Texas airports with full data were ranked, and none were left out.

"How full" means passengers divided by seats on departing flights over the latest 12 months. It isn't the official load factor, which is based on miles flown. It's also the weakest of the five scored inputs, because it depends partly on how airlines set fares and choose aircraft.

| # | Airport | Size class | Planes full | Capacity-need score | Strained today |
|---|---|---|---|---|---|
| 1= | Dallas-Fort Worth (DFW) | large | 82.5% | 79.3 | yes |
| 1= | McAllen (MFE) | small | 82.5% | 44.5 | no |
| 3 | Houston Bush (IAH) | large | 79.9% | 70.4 | yes |
| 4 | Abilene (ABI) | nonhub | 79.5% | 78.1 | no |
| 5 | Corpus Christi (CRP) | nonhub | 76.6% | 38.0 | no |

**What this means for capacity:**
- **DFW and IAH** have full planes and are also strained (system delay rates of 6.2% and 6.5%). Their FAA forecasts add the most passengers: about 8.5 million more boardings a year at DFW and 5.9 million at IAH by 2035. At IAH, flights have stayed flat while passenger numbers rose.
- **McAllen** has full planes and 33.5% passenger growth since 2019. However, the FAA forecasts its flights will fall by 9.8%, which pulls its overall score down.
- **Abilene** scores well on both passenger and flight measures, but it is small (about 106,000 boardings in 2025). One airline, Envoy Air, carries 95.8% of its passengers, so its future growth depends on that airline's plans.
- **Corpus Christi** has about the same number of seats as in 2019 (-0.2%) and almost no forecast flight growth (0.3%).

I can also break this down by season, for example summer peaks, or compare any of these airports in detail.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years); FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: How full the planes are, Capacity-need score, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: ABI: single_airline

## B3 - Which large airports have planes over 85% full?

*Pass when:* Large hubs filtered by a load factor threshold.

*Result:* PASS

*Tool calls:* `rank_airports` {"size_classes": ["large"], "sort_by": "load_factor_pct", "min_value": 85, "limit": 30}; `rank_airports` {"size_classes": ["large"], "sort_by": "load_factor_pct", "limit": 5}

**None of them.** No large-hub airport has planes over 85% full. All 30 large hubs have full data, and the fullest is Newark (EWR) at 83.2%.

"How full" here means passengers divided by seats on departing flights over the latest 12 months. It is not the official load factor, which is based on passenger-miles and seat-miles.

These are the five fullest large hubs:

| Airport | How full | Seats vs 2019 | Passengers vs 2019 | Capacity-need score |
|---|---|---|---|---|
| Newark (EWR) | 83.2% | 2.2% | 1.0% | 80.7 |
| San Francisco (SFO) | 82.6% | -5.0% | -4.4% | 86.9 |
| Dallas-Fort Worth (DFW) | 82.5% | 15.8% | 14.9% | 79.3 |
| Atlanta (ATL) | 82.3% | -1.0% | -4.5% | 69.8 |
| Los Angeles (LAX) | 82.1% | -12.8% | -15.7% | 75.3 |

**Warnings that change how to read this:**
- **San Francisco and Los Angeles:** both have fewer seats than in 2019. Their planes are full because seats were cut, not because demand is rising.
- **Newark:** the FAA caps it at 36 arrivals and 36 departures an hour, so how many flights can be added is limited by law, not only by demand.
- **Dallas-Fort Worth:** the cleanest signal of the five. Seats and passengers have both grown since 2019, and the data has no warnings.

How full the planes are is the weakest of the five score inputs, because it mostly reflects airline pricing and aircraft choices. The five are also tightly bunched (82.1-83.2%), so this metric barely separates them.

If you want, I can run the same 85% check on medium or small hubs, or rank the large hubs by the full capacity-need score instead.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: How full the planes are, Capacity-need score; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - the answer uses proxy measures (scores, system delay rate, load factor or forecasts); EWR: legal limit; SFO: capacity cut; LAX: capacity cut
> Warnings printed: EWR: legal_limit, SFO: capacity_cut, LAX: capacity_cut

## B4 - Compare Portland and Providence.

*Pass when:* Asks which Portland (Oregon or Maine), or covers both and says so.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Portland"}; `find_airport` {"query": "Providence"}

Portland could mean Portland, Oregon (PDX) or Portland, Maine (PWM). Which one do you mean?

For Providence, I'll use Rhode Island T.F. Green International (PVD), the only airport in the city itself. Boston Logan (BOS) and Manchester-Boston Regional (MHT) are in the same metro area, so I can add either one if you'd like.

It may help you choose:
- **Portland, Maine (PWM)** is in the same FAA size class as Providence (small hub) and the same region, so the comparison would be like-for-like.
- **Portland, Oregon (PDX)** is a medium hub, a size class up. Seat capacity there was cut compared with 2019, which affects how its full planes should be read.

I can also compare all three together.

> Data period: no data was used in this reply  
> Assumptions: none  
> Confidence: n/a - no data figures were used in this reply

## B5 - Which airports are the best candidates overall? Only count the ones with complete data.

*Pass when:* National ranking shown per size class.

*Result:* PASS

*Tool calls:* `rank_airports` {"limit": 5}

Orlando International (MCO) is the top large hub, with a score of 87.8. Across all sizes, the strongest candidates are clustered in Florida. I've ranked each FAA size class separately because size isn't part of the score, so a single national list would be topped by small leisure airports. Only the 343 airports with complete data are included; the 59 with partial or thin data are left out.

| Class | Top 5 (score 0-100) |
|---|---|
| Large hub | MCO 87.8, San Francisco (SFO) 86.9, Chicago O'Hare (ORD) 84.6, New York JFK (JFK) 84.0, Miami (MIA) 83.0 |
| Medium hub | Fort Myers (RSW) 81.7, Charleston (CHS) 78.8, Jacksonville (JAX) 75.8, San Juan (SJU) 75.4, Raleigh-Durham (RDU) 73.1 |
| Small hub | Punta Gorda (PGD) 94.9, Northwest Arkansas (XNA) 85.5, Orlando Sanford (SFB) 85.2, St Pete-Clearwater (PIE) 84.1, Provo (PVU) 80.2 |
| Nonhub | Rickenbacker (LCK) 85.7, Traverse City (TVC) 78.8, Abilene (ABI) 78.1, Belleville/MidAmerica (BLV) 77.8, Aguadilla (BQN) 77.7 |

The score measures how much added capacity would likely be filled. It's a proxy for profit, not a measure of return.

**Large hubs:** MCO and MIA have no warnings, and both have strong passenger growth since 2019 (14.7% and 23.4%).
- **SFO:** Planes are full mainly because seats were cut (-5.0% vs 2019), not because demand rose.
- **JFK:** Flights are capped by a legal slot limit, so new runway or gate capacity can't be used without more slots.
- **ORD:** Under a temporary flight cap. It still has the largest forecast gain, 11,437,065 extra boardings a year by 2035.

**Medium hubs:** RSW and CHS have no warnings. CHS has 33.2% passenger growth since 2019.

**Small hubs and nonhubs:** Most leaders depend on one airline, mainly Allegiant, which carries up to 99.9% of passengers at PGD, SFB, PIE, LCK and BLV (ABI depends on Envoy). If that airline cuts service, the forecast growth may not arrive. XNA has no such warning. Cargo is 44.2% of flights at LCK and 42.8% at BQN, and BQN's seats were also cut.

Next, I can profile any of these in detail, for example the delay causes at MCO.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years); FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, FAA forecast passenger growth, FAA forecast flight growth; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - SFO: capacity cut; ORD: legal limit; JFK: legal limit; LCK: cargo heavy
> Warnings printed: ORD: legal_limit, JFK: legal_limit, SFO: capacity_cut, PGD: single_airline, SFB: single_airline, PIE: single_airline, LCK: cargo_heavy, LCK: single_airline, ABI: single_airline, BLV: single_airline, BQN: cargo_heavy, BQN: capacity_cut

## B6 - How has passenger traffic at Boston changed since 2019? Give me the year by year picture.

*Pass when:* Year by year values for Boston, with 2026 marked partial.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Boston"}; `airport_profile` {"airport_code": "BOS"}

Boston Logan (BOS) is back to its 2019 level and has been flat for about two years. Passengers in the latest 12 months (May 2025 - April 2026) were 20,983,745, which is 1.2% above calendar 2019. Traffic peaked in 2024, and 2025 came in slightly lower. I assumed you meant Logan. The area also has Manchester-Boston Regional (MHT) and Providence (PVD).

| Year | Passengers | How full the planes are | System delay rate |
|---|---|---|---|
| 2019 | 20,742,138 | 81.9% | 9.2% |
| 2020 | 6,050,302 | 52.0% | 2.7% |
| 2021 | 10,938,231 | 75.1% | 3.5% |
| 2022 | 17,472,973 | 78.5% | 6.3% |
| 2023 | 19,991,297 | 83.3% | 7.2% |
| 2024 | 21,280,480 | 83.1% | 7.9% |
| 2025 | 21,105,980 | 81.6% | 11.0% |
| 2026 (Jan-Apr only) | 6,139,216 | 78.2% | 8.8% (Jan-Jul) |

Passengers are counted on departing flights. "How full the planes are" is passengers divided by seats. The 2026 row covers only part of the year, so don't compare it with full years.

**What's behind the numbers:**
- **More passengers per flight, fewer flights:** passenger flights in 2025 were 3.1% below 2019, while passengers per flight rose from 106.4 to 111.9. Seats are up 1.4% on 2019, so airlines have used bigger planes rather than more flights.
- **Planes are still full:** 81.7% in the latest 12 months, the 85.5th percentile among ranked airports.
- **Delays rose faster than traffic:** the system delay rate reached 11.0% in 2025. That category is coded by airlines and includes ordinary weather. The newest four months show no fresh spike.
- **Forecast:** the FAA forecasts 26.5% more passengers by fiscal 2035, but it tends to over-forecast.

The flat passenger numbers sit alongside high and rising delays. That suggests the airfield, not demand, may be what's holding growth back. I can show the month-by-month passenger series if you want to see seasonality.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: How full the planes are, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; 'Boston' was taken to mean BOS  
> Confidence: Medium - the answer uses proxy measures (scores, system delay rate, load factor or forecasts); an airport name was resolved by default

## B7 - Show me medium-size airports in the West with the fastest forecast passenger growth.

*Pass when:* West region, medium hubs, sorted by forecast passenger growth.

*Result:* PASS

*Tool calls:* `rank_airports` {"region": "west", "size_classes": ["medium"], "sort_by": "forecast_passenger_growth_pct", "limit": 10}

Portland (PDX) has the fastest FAA-forecast passenger growth among medium-hub airports in the West, at 33.2% (fiscal 2035 vs 2025). Oakland (OAK), San Jose (SJC) and Boise (BOI) are close behind. Of these, Portland and Boise also have the highest capacity-need scores.

I used the FAA "medium hub" class. The West has 11 medium hubs with full data; these are the top 10.

| # | Airport | Forecast pax growth | Extra boardings by 2035 | Score (0-100) | Pax growth since 2019 |
|---|---|---|---|---|---|
| 1 | Portland (PDX) | 33.2% | 2,989,548 | 72.3 | -6.4% |
| 2 | Oakland (OAK) | 29.9% | 1,402,276 | 46.0 | -35.5% |
| 3 | San Jose (SJC) | 29.6% | 1,620,865 | 44.7 | -35.0% |
| 4 | Boise (BOI) | 28.6% | 735,328 | 66.7 | 24.8% |
| 5 | Sacramento (SMF) | 24.7% | 1,682,362 | 52.0 | 3.8% |
| 6 | Anchorage (ANC) | 24.6% | 660,937 | 59.1 | 0.8% |
| 7 | Ontario (ONT) | 22.9% | 799,528 | 52.0 | 26.5% |
| 8 | Kahului (OGG) | 21.9% | 753,173 | 48.1 | -9.4% |
| 9 | Santa Ana (SNA) | 19.4% | 1,059,150 | 62.0 | 7.2% |
| 10 | Burbank (BUR) | 16.0% | 531,720 | 44.0 | -0.7% |

**What changes the picture:**
- **The FAA tends to over-forecast.** Use these figures to compare airports, not as predictions.
- **Some growth is a rebound.** Oakland and San Jose are still about a third below 2019 traffic, and airlines cut their seats. Oakland also depends on Southwest, which carries 76.7% of its passengers. Portland and Kahului had smaller capacity cuts.
- **Boise is the cleanest growth story.** Passengers are up 24.8% since 2019, and its data has no warnings.
- **Legal limits:** Santa Ana has a legal passenger cap of roughly 6.1-6.25 million departing passengers, plus a curfew. It already boards 5.5 million, so much of its forecast growth may not fit under the cap. San Jose has a night noise curfew.
- **Cargo:** cargo makes up 56.6% of flights at Anchorage and 36.2% at Ontario, and competes for the same runways.

I can profile Portland or Boise in more depth if that would help.

> Data period: FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: FAA forecast passenger growth, Capacity-need score, FAA forecast flight growth; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - PDX: capacity cut; OAK: capacity cut; SJC: capacity cut, legal limit; ANC: cargo heavy
> Warnings printed: SJC: legal_limit, SNA: legal_limit, PDX: capacity_cut, OAK: single_airline, OAK: capacity_cut, SJC: capacity_cut, ANC: cargo_heavy, ONT: cargo_heavy, OGG: capacity_cut

## B8 - What's the busiest month at Burlington, Vermont, and how full are the planes then?

*Pass when:* The busiest month and its load factor.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Burlington, Vermont"}; `airport_trend` {"airport_code": "BTV", "metric": "passengers"}; `airport_trend` {"airport_code": "BTV", "metric": "load_factor_pct"}

October is the busiest month at Patrick Leahy Burlington International (BTV), and planes are about 85% full then. Across the last three Octobers, BTV averaged 73,848 departing passengers, and on average 84.9% of seats were filled.

**October in each year**

| October | Passengers | Planes full |
|---|---|---|
| 2023 | 67,645 | 89.5% |
| 2024 | 74,742 | 79.2% |
| 2025 | 79,157 | 86.9% |

October 2025 was the airport's busiest single month from 2023-05 to 2026-04. Background (not from our data): this October peak fits Vermont's fall-foliage tourist season.

**Busiest month isn't the fullest month.** Planes are fullest in July (86.7% on average), with August and February next (85.5% each). October comes after them. In October, airlines seem to add seats along with the extra passengers, so planes aren't packed as tightly as in midsummer. The lowest single month was September 2024 (71.8%). August is the second-busiest month, averaging 70,578 passengers.

For comparison, planes at BTV were 83.0% full over the latest 12 months.

"Planes full" here means passengers divided by seats on departing flights. It is not the official load factor, which uses passenger-miles and seat-miles. It is a rough stand-in for unmet passenger demand, because airline pricing and choice of aircraft also affect it.

If it helps, I can check whether delays at BTV also peak in summer and fall.

> Data period: BTS T-100 airport-month summary, 2023-05 to 2026-04  
> Assumptions: proxies, not direct measurements: How full the planes are  
> Confidence: Medium - the answer uses proxy measures (scores, system delay rate, load factor or forecasts)

## C1 - Score the top 3 airports that have the highest congestion in August in the US.

*Pass when:* Ranks by the August system delay rate and says scores do not exist by month.

*Result:* PASS

*Tool calls:* `rank_airports` {"sort_by": "system_delay_rate_pct", "month": 8, "limit": 3}; `rank_airports` {"sort_by": "system_delay_rate_pct", "month": 8, "limit": 5}

The three most congested airports in August are Newark (EWR), Orlando (MCO) and San Juan (SJU). Orlando has the highest capacity-need score of the three at 87.8, and it ranks 1st of 30 large hubs. Third place is a tie: Aguadilla (BQN) has the same August delay rate as San Juan.

By "congestion" I mean the system delay rate: the share of arriving flights delayed for airport or air-traffic reasons. Airlines decide which delays go in this category, and it includes ordinary weather. The August figures add up the Augusts of 2023, 2024 and 2025. Scores aren't calculated for single months, so the scores below are for the latest period.

| Airport | Aug. system delay | Score | Passenger side | Flight side | Rank in size class |
|---|---|---|---|---|---|
| Newark (EWR) | 10.9% | 80.7 | 72.7 | 88.6 | 7 of 30 large |
| Orlando (MCO) | 10.3% | 87.8 | 81.5 | 94.0 | 1 of 30 large |
| San Juan (SJU) | 9.8% | 75.4 | 77.6 | 73.3 | 4 of 34 medium |
| Aguadilla (BQN), tied 3rd | 9.8% | 77.7 | 68.7 | 86.7 | 5 of 201 nonhub |

**What changes the picture:**
- **Newark** has a legal cap of 36 arrivals and 36 departures an hour. That limits how much any added capacity could be used. Its passenger growth since 2019 is also small (1.0%).
- **Orlando** has the strongest case: passengers are up 14.7% since 2019, and the FAA forecasts 26.4% more flights by 2035 (takeoffs plus landings, including cargo).
- **San Juan and Aguadilla** are both in Puerto Rico, a US territory. At Aguadilla, cargo is 42.8% of flights, and seats are down 10.2% since 2019. So its full planes reflect fewer seats, not rising demand.
- **If you exclude territories,** Boston (BOS) is third at 9.3%, with a score of 82.9.

To check next, I can pull full profiles, including delay causes and the flight-demand estimate, for any of these airports.

> Data period: BTS Airline Delay Causes, August of 2023, 2024, 2025 (summed); BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: System delay rate, Capacity-need score, Passenger-side score, Flight-side score, How full the planes are, FAA forecast passenger growth; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - EWR: legal limit; the answer uses proxy measures (scores, system delay rate, load factor or forecasts); BQN: capacity cut, cargo heavy
> Warnings printed: EWR: legal_limit, BQN: cargo_heavy, BQN: capacity_cut

## C2 - Where is Delta the dominant airline?

*Pass when:* Says airline-network questions are not supported; may offer the biggest-airline share per airport.

*Result:* PASS

*Tool calls:* `rank_airports` {"sort_by": "top_airline_share_pct", "size_classes": ["large"], "limit": 30, "include_partial_data": true}; `airport_profile` {"airport_code": "ATL"}; `airport_profile` {"airport_code": "MSP"}; `airport_profile` {"airport_code": "DTW"}; `airport_profile` {"airport_code": "SLC"}

**Among large-hub airports, Delta is clearly the biggest airline at four I checked: Atlanta (ATL), Minneapolis-St Paul (MSP), Salt Lake City (SLC) and Detroit (DTW).** At each one Delta carries more than half of all passengers.

This list isn't complete. Our data has only each airport's biggest airline and that airline's share of passengers (calendar 2025). It can't filter or rank by airline. So I ranked the 30 large hubs by how much of the traffic their biggest airline carries, then opened the likeliest airports one at a time to see which airline it is.

| Airport | Delta's share of passengers | Capacity-need score | Rank among 30 large hubs |
|---|---|---|---|
| Atlanta (ATL) | 74.7% (highest of all large hubs) | 69.8 | 18 |
| Minneapolis-St Paul (MSP) | 58.0% | 64.8 | 23 |
| Salt Lake City (SLC) | 57.5% | 60.9 | 25 |
| Detroit (DTW) | 54.8% | 60.6 | 26 |

**What this means for the investment question:**
- All four are in the lower half of large hubs on capacity need, and none counts as strained (where flight delays blamed on the airport and air-traffic system are in the top quarter of airports).
- **MSP and DTW: airlines cut capacity.** Seats are -7.2% and -6.7% versus 2019, and passengers are -10.0% and -10.1%. Planes there look full because there are fewer seats, not because demand is rising.
- **One airline dominates.** At all four, the airport's growth depends heavily on Delta's network plans.

**Not checked:** I didn't open any other large hub or any medium, small or nonhub airport. Delta may also be the biggest airline at other airports where it has a smaller share. I can't tell from here which airline leads at those.

Background (not from our data): Delta also runs large operations at New York JFK, LaGuardia, Boston, Seattle and Los Angeles, but it is not necessarily the biggest airline at each of them.

I can check those airports, or any medium-hub airports you name, one at a time.

> Data period: BTS T-100 Segment, calendar 2025; BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - EWR: legal limit; MSP: capacity cut; DTW: capacity cut; PHL: capacity cut
> Warnings printed: EWR: legal_limit, ORD: legal_limit, SAN: legal_limit, DCA: legal_limit, JFK: legal_limit, LGA: legal_limit, MSP: capacity_cut, DTW: capacity_cut, PHL: capacity_cut, SFO: capacity_cut, FLL: capacity_cut, DCA: forecast_constrained, : more

## C3 - How many flights go from JFK to London?

*Pass when:* Declines: route-level questions are not supported.

*Result:* PASS

*Tool calls:* `airport_profile` {"airport_code": "JFK"}

I can't tell you how many flights go from JFK to London. This version doesn't include route or destination data, so it can't count flights between two cities. The closest figure I have is how many of JFK's departing flights are long-haul, which includes transatlantic flights like London but also many other destinations.

**John F. Kennedy International (JFK), departing flights in calendar 2025 (all destinations, domestic and international, all airlines):**

| Distance (our cutoff) | Passenger flights | Share of passenger flights |
|---|---|---|
| 2,000+ miles | 96,455 | 45.4% |
| 2,500+ miles | 60,217 | 28.4% |
| 3,000+ miles (our default) | 49,841 | 23.5% |

JFK had 212,394 departing passenger flights in total. Including cargo, the 3,000-mile share is 24.0%. Cargo is only 3.5% of flights, so it barely changes the picture.

Background (not from our data): London is beyond the 3,000-mile cutoff from New York, so JFK-London flights are part of the bottom row. That row also includes other European, Asian and South American routes, so it is much bigger than the London count.

One thing matters if you're asking with capacity in mind: JFK is a slot-controlled airport, meaning the FAA legally caps how many flights it can schedule. More gates or terminal space wouldn't add flights unless the airport also got more slots.

I can also give you JFK's full capacity-need profile (it ranks 4th of 30 large hubs), or compare it with Newark (EWR) on long-haul share.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA passenger boarding data CY2025, calendar 2025; BTS T-100 Segment, calendar 2025  
> Assumptions: long-haul means 3,000 miles or more (our definition; adjustable)  
> Confidence: Medium - JFK: legal limit
> Warnings printed: JFK: legal_limit

## C4 - What's the congestion level at Teterboro?

*Pass when:* Says Teterboro is outside the covered airports; no invented number.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Teterboro"}

I can't tell you about congestion at Teterboro, because it isn't in our data. The data covers only the 402 FAA "primary" airports, which are the larger commercial airports, and Teterboro didn't match any of them.

Background (not from our data): Teterboro is a business and private jet airport with no regular airline service, so the airline delay figures we use to measure congestion don't exist for it.

Our data also doesn't include runway or ramp use, peak-hour traffic or live delays for any airport, so I can't estimate Teterboro's congestion another way.

What I can do instead:
- **Compare congestion at the nearby commercial airports.** I can put Newark (EWR), LaGuardia (LGA) and JFK (JFK) side by side. For each, I'd show the share of flights delayed by the air traffic system over three years and over the latest 12 months, the share of all flights delayed, and the causes of those delays. Note that airlines decide which delays count as air-traffic-system delays, and that category includes ordinary weather.
- **Rank the airports in the New York area or the Northeast** by that air-traffic-system delay rate.

Do you want me to run either of those?

> Data period: no data was used in this reply  
> Assumptions: none  
> Confidence: n/a - no data figures were used in this reply

## C5 - Which airports were the top expansion candidates in 2021?

*Pass when:* Says the score exists for the latest period only; offers raw 2021 metrics.

*Result:* PASS

*Tool calls:* `rank_airports` {"year": 2021, "sort_by": "load_factor_pct", "limit": 5}; `rank_airports` {"year": 2021, "sort_by": "system_delay_rate_pct", "limit": 5}

I can't rank expansion candidates for 2021. The capacity-need score only exists for the latest period, so there is no 2021 score. What I can show is how the airports ranked on two of the score's inputs in calendar 2021:

**Fullest planes in 2021** (passengers divided by seats on departing flights)

| Airport | 2021 |
|---|---|
| McAllen (MFE) | 84.4% |
| Wilkes-Barre/Scranton (AVP) | 84.3% |
| Aguadilla (BQN) | 83.8% |
| Ponce (PSE) | 82.3% |
| Hartford Bradley (BDL) | 82.2% |

**Highest system delay rate in 2021** (system-coded arrival delays divided by arriving flights)

| Airport | 2021 |
|---|---|
| Key West (EYW) | 11.5% |
| Punta Gorda (PGD) | 10.0% |
| Newark (EWR) | 8.8% |
| Dallas Love Field (DAL) | 8.4% |
| Aguadilla (BQN) | 8.4% |

Things to keep in mind:
- **2021 was a pandemic recovery year.** Airlines had cut seats, so full planes partly reflect reduced capacity rather than strong demand. AVP, BQN and PSE are all still flagged for seat cuts since 2019.
- **Airlines decide which delays count as "system" delays,** and the category includes ordinary weather.
- **Legal caps:** Newark has a cap of 36 arrivals and 36 departures an hour. Dallas Love Field is limited to 20 gates by federal law.
- **Single-airline airports:** Allegiant carries 99.6% of passengers at Punta Gorda, and Southwest carries 96.8% at Dallas Love Field.
- **Cargo:** cargo makes up 42.8% of flights at Aguadilla.
- **Small sample:** Ponce's delay rate is based on few flights.

For comparison, Punta Gorda is the top-ranked small hub on today's score (94.9). I can also pull the current national ranking by size class, or show 2021 against today for any of these airports.

> Data period: BTS T-100 airport-month summary, calendar 2021 / 2025-05 to 2026-04 (latest 12 complete months); BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / calendar 2021; FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: How full the planes are, Capacity-need score, System delay rate; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - 1 of the 5 listed airports has weaker data (PSE: small delay sample); AVP: capacity cut; BQN: capacity cut, cargo heavy; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: EWR: legal_limit, DAL: legal_limit, AVP: capacity_cut, BQN: cargo_heavy, BQN: capacity_cut, PSE: small_sample, PSE: capacity_cut, PSE: small_airport_forecast, PGD: single_airline, DAL: single_airline

## C6 - Should we invest in expanding LaGuardia?

*Pass when:* Gives the evidence and the slot limit; leaves the decision to the analyst.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "LaGuardia"}; `airport_profile` {"airport_code": "LGA"}

LaGuardia (LGA) shows real strain, but it's a weaker candidate than its congestion suggests. FAA flight slot limits cap how many flights it can add, so new capacity would mostly have to come from bigger planes rather than more flights. Whether to invest is your call. Here's the evidence.

**Score:** 67.8 out of 100. That ranks 19th of 30 large hubs and 76th of 343 airports overall. The score measures how much added capacity would likely be filled. It stands in for profit; it doesn't measure it.

| Metric | LGA | Position among peers (0-100) |
|---|---|---|
| System delay rate (3 yrs) | 8.4% | 98.1 |
| How full planes are | 80.8% | 78.9 |
| Passenger growth since 2019 | 4.7% | 49.0 |
| FAA forecast passenger growth to 2035 | 18.4% | 47.2 |
| FAA forecast flight growth to 2035 | 9.3% | 45.9 |

**Congestion:** LGA counts as strained. The system delay rate was 10.4% in the latest 12 months, and 21.5% of arrivals were late overall. The airport and air-traffic system caused 39.3% of delays. Airlines code that category, and it includes ordinary weather. The last four months show no new spike.

**Unmet flight demand (an estimate):** The FAA forecasts 33,029 more takeoffs and landings by 2035. But that forecast already assumes the slot limits, so it isn't a measure of demand without the cap.

**Why the cap matters:**
- LGA has 4.8% fewer passenger flights than in 2019, but more passengers per flight (94.7, up from 85.3). Airlines are growing by flying bigger planes.
- Nonstop flights are limited to 1,500 miles (Saturdays exempt), so long-haul growth isn't possible.
- Delta is the biggest airline, with a 23.8% share.

Background (not from our data): LaGuardia's terminals were recently rebuilt. Our data can't see construction or gate use, so check how much room is left.

**What to check next:** whether the slot rules might change, current gate and terminal use, and how LGA compares with JFK and Newark (EWR). I can't estimate costs or returns.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); FAA passenger boarding data CY2025, calendar 2025; BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, How full the planes are, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; long-haul means 3,000 miles or more (our definition; adjustable); 'unmet flight demand' is an estimate from the FAA forecast, used only when the airport is strained today; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - LGA: forecast constrained, legal limit; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: LGA: legal_limit, LGA: forecast_constrained

## C7 - What will a new terminal at Denver cost, and what return would we get?

*Pass when:* Declines cost and return; offers the capacity-need evidence.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Denver"}

I can't tell you what a new terminal at Denver International (DEN) would cost or return. There's no cost, revenue or return data in this system, and no gate counts or terminal-size data either. What I can show is how much of any added capacity would likely be used, which is our stand-in for profit potential.

**Denver's capacity-need score is 76.7 out of 100**, putting it 12th of 30 large hubs. The score compares airports with each other; it doesn't measure money.

| Measure | DEN |
|---|---|
| How full planes are (load factor) | 81.2% |
| Passenger growth since 2019 | 18.8% |
| FAA forecast passenger growth (2025-2035) | 23.7% |
| FAA forecast extra yearly boardings | 9,475,223 |
| System delay rate (three years) | 6.6% |
| FAA forecast flight growth | 14.7% |
| Seat change since 2019 | +26.1% |
| Boardings in 2025 | 39,976,695 |

**What this means:**
- **Demand is real and still growing.** Planes are fairly full, and passenger numbers are above 2019 even though airlines added seats (about a quarter more since 2019). Airlines haven't cut capacity there.
- **The airport counts as "strained" in our data.** Airlines code the system delay category themselves, and it includes ordinary weather, so it's an imperfect measure of congestion.
- **The FAA expects the most growth on the passenger side.** Its forecast for passenger growth is higher than for flight growth.

To get closer to a return estimate, you'd need cost and revenue figures from outside this system. I can pull Denver's full profile (delay causes, flight-demand estimate, year-by-year history) or compare it with other large hubs. Should I?

> Data period: see the tool trace  
> Assumptions: proxies, not direct measurements: Capacity-need score, Passenger-side score; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - the answer uses proxy measures (scores, system delay rate, load factor or forecasts)

## C8 - What is the delay rate at Glacier Park airport in Kalispell, and can I trust it?

*Pass when:* Resolves Glacier Park to FCA, gives the rate and the sample size.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Glacier Park, Kalispell"}; `find_airport` {"query": "GPI"}; `find_airport` {"query": "Kalispell, Montana"}; `airport_profile` {"airport_code": "FCA"}

At Glacier Park International in Kalispell, 16.6% of arriving flights were 15 or more minutes late over the last three years, from any cause. Delays blamed on the airport and air-traffic system (the "system delay rate") were 4.0%. You can mostly trust these figures: the airport has full, high-confidence data, and the rates are based on 15,601 arriving flights. There are a few limits on what they measure, listed below.

One note on the code: the dataset lists the airport as **FCA**, which is the code airlines use, while the FAA code is GPI. A search by name didn't find it, but searching by the code GPI did.

| Measure | Value |
|---|---|
| Overall delay rate (3 years, Aug 2023 - Jul 2026) | 16.6% |
| System delay rate (3 years) | 4.0% |
| System delay rate (latest 12 months) | 4.7% |
| System delay rate in Apr-Jul 2026 vs the same months a year earlier | 5.3% vs 3.3% |
| Arriving flights in the sample | 15,601 |

**Why you can trust it:**
- Three years of data covering about 15,600 flights is a solid sample for a small hub.
- The data checks raised no warnings.

**Limits on what it measures:**
- **Who decides the cause:** airlines assign each delay to a category. The "system" category includes ordinary bad weather, so it mostly reflects congestion, but not only congestion.
- **Which flights count:** only domestic flights of the larger airlines that report delays are included.
- **Single years swing a lot:** that's why the 3-year rate is the main figure.

**Main causes of delayed flights:** the airline itself (42.9%), a late incoming aircraft (28.5%), the airport and air-traffic system (24.1%) and extreme weather (4.4%). So most delay here is caused by airline operations rather than the airfield.

**Trend:** the system delay rate has risen gradually, from 3.1% in 2023 to 3.9% in 2024 and 2025, and 4.8% so far in 2026. The data doesn't flag the recent months as a spike. The 3-year rate of 4.0% puts the airport roughly in the middle of all full-data airports, so it doesn't count as strained.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); FAA passenger boarding data CY2025, calendar 2025; BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: System delay rate  
> Confidence: Medium - the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
