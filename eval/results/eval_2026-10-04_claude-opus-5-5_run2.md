# Evaluation run - 2026-10-04 15:59 - claude-opus-5-5

**24 of 24 questions passed.** 756 numbers appeared in the answers; 0 answers ended with a number that could not be traced to a tool result; 1 answers passed only after one automatic rewrite. Average 12.3s per question; 607,364 input and 22,993 output tokens in total.

| Id | Group | Result | Tools | Number check | Seconds |
|---|---|---|---|---|---|
| A1 | core | PASS | rank_airports | passed | 11.1 |
| A2 | core | PASS | find_airport, find_airport, compare_airports | passed | 12.5 |
| A6 | follow-up | PASS | compare_airports | passed | 9.5 |
| A3 | core | PASS | find_airport, airport_profile | passed | 10.1 |
| A7 | follow-up | PASS | airport_profile | passed | 7.9 |
| A4 | core | PASS | airport_profile | passed | 11.2 |
| A5 | follow-up | PASS | find_airport, compare_airports, airport_profile | passed | 12.4 |
| A8 | follow-up | PASS | find_airport, airport_profile | passed | 13.5 |
| B1 | filters | PASS | rank_airports, compare_airports | rewritten | 20.5 |
| B2 | filters | PASS | rank_airports | passed | 10.1 |
| B3 | filters | PASS | rank_airports, rank_airports | passed | 12.8 |
| B4 | ambiguous | PASS | find_airport, find_airport | passed | 5.8 |
| B5 | filters | PASS | rank_airports | passed | 13.9 |
| B6 | time | PASS | find_airport, airport_profile | passed | 11.8 |
| B7 | filters | PASS | rank_airports | passed | 13.3 |
| B8 | time | PASS | find_airport, airport_trend, airport_profile | passed | 11.7 |
| C1 | time | PASS | rank_airports, rank_airports | passed | 13.5 |
| C2 | out of scope | PASS | rank_airports, airport_profile, airport_profile, airport_profile, airport_profile | passed | 18.4 |
| C3 | out of scope | PASS | airport_profile | passed | 9.8 |
| C4 | out of scope | PASS | find_airport | passed | 7.6 |
| C5 | out of scope | PASS | - | passed | 9.3 |
| C6 | judgment | PASS | find_airport, airport_profile | passed | 16.4 |
| C7 | out of scope | PASS | find_airport | passed | 19.5 |
| C8 | awkward data | PASS | find_airport, airport_profile | passed | 13.0 |

## A1 - Which airports in New England are strong candidates for terminal expansion?

*Pass when:* A ranked list from the six states, scores shown, reasons given.

*Result:* PASS

*Tool calls:* `rank_airports` {"region": "new england", "limit": 10}

Four airports stand out on our capacity-need score: **Boston Logan (BOS)**, **Burlington (BTV)**, **Portland, Maine (PWM)** and **Bangor (BGR)**. All four score above 70 and have high data confidence. One caveat: we have no data on gates or how fully terminals are used. The score measures upside (how much added capacity would be filled), not profit or terminal crowding.

| Airport | Score | Passenger side | Flight side | Planes full | Passengers vs 2019 | FAA forecast passengers | Forecast extra boardings by 2035 |
|---|---|---|---|---|---|---|---|
| BOS (large) | 82.9 | 72.2 | 93.6 | 81.7% | +1.2% | +26.5% | 5,612,088 |
| BTV (small hub) | 79.2 | 73.7 | 84.8 | 83.0% | +2.3% | +22.9% | 163,754 |
| PWM (small hub) | 77.4 | 79.2 | 75.6 | 82.8% | +17.2% | +21.6% | 278,078 |
| BGR (nonhub) | 71.8 | 78.0 | 65.5 | 80.4% | +40.8% | +24.1% | 103,055 |
| BDL (medium) | 65.9 | 60.8 | 71.0 | 81.3% | -2.7% | +15.7% | 523,236 |

**Why they stand out:**
- **BOS:** The strongest case on both sides and by far the biggest absolute gain. Its system delay rate is 9.1%, and it is flagged as strained. This category is coded by airlines and includes ordinary weather, so it measures congestion only roughly. Passenger numbers are barely above 2019, so the case rests on the FAA forecast and on delays.
- **BTV:** Strained, with planes 83.0% full, but passenger growth since 2019 has been small.
- **PWM and BGR:** These have the best real growth since 2019 (seats are up 21.6% and 48.8%). At PWM, flights have stayed flat while passengers rose, a sign that demand is being absorbed by fuller planes.
- **Hartford (BDL):** Scores lower, but its forecast gain in boardings is larger than PWM's and BTV's combined.

Four airports have only partial data and aren't scored: New Haven (HVN), Cape Cod (HYA), Block Island (BID) and Westerly (WST).

Next steps could be a profile of BOS or PWM, or a side-by-side comparison of the top four.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years); FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, Passenger-side score, Flight-side score, How full the planes are, FAA forecast passenger growth, System delay rate; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - 1 of the 10 listed airports have weaker data (PSM: small delay sample); MVY: small airport forecast; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: MVY: small_airport_forecast, PSM: small_sample, PSM: small_airport_forecast

## A2 - Compare LA and Santa Ana airport congestion levels.

*Pass when:* LAX vs SNA side by side, a clear verdict, Santa Ana's legal cap flagged.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "LA"}; `find_airport` {"query": "Santa Ana"}; `compare_airports` {"airport_codes": ["LAX", "SNA"]}

**Los Angeles International (LAX) is somewhat more congested than John Wayne/Orange County (SNA) on every delay measure, but the gap is small.** I took "LA" to mean LAX. The metro area also has Ontario (ONT), Hollywood Burbank (BUR) and Long Beach (LGB).

| Measure | LAX | SNA | Difference |
|---|---|---|---|
| System delay rate, 3 years | 4.8% | 3.9% | +0.9 pts (ratio 1.23) |
| System delay rate, latest 12 months | 5.0% | 4.3% | +0.7 pts |
| Overall delay rate (15+ min, any cause) | 18.9% | 17.5% | +1.4 pts |
| System share of all delays | 25.7% | 22.4% | |
| Flight-side score (0-100) | 80.5 | 58.7 | +21.8 |

**What the numbers measure:** The system delay rate is the share of arriving flights delayed by the airport and air traffic system. It's our closest measure of congestion, but airlines assign the delay codes and the category includes ordinary weather. So it mostly reflects congestion, but not only congestion.

**Why delays happen:** At both airports most delays come from the airlines themselves and from late-arriving aircraft, not from the airport. That's 37.0% and 33.4% at LAX, and 35.0% and 39.9% at SNA. Neither airport is flagged as strained.

**Caveats that change the picture:**
- **SNA has a legal cap.** A settlement agreement limits passengers to roughly 6.1-6.25 million departing passengers a year in our units, with 95 average daily departures in the regulated class and a night curfew. SNA carried 5,590,354 passengers in the latest 12 months, so it is close to that ceiling. Its constraint is legal, not physical congestion.
- **LAX has fewer seats than in 2019.** Seats are down 12.8% and passengers are down 15.7%. Full planes there partly reflect fewer seats rather than rising demand.

Next, I could rank all five LA-area airports on these delay measures.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, Flight-side score, How full the planes are, System delay rate; 'LA' was taken to mean LAX; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - LAX: capacity cut; SNA: legal limit; the answer uses proxy measures (scores, system delay rate, load factor or forecasts); an airport name was resolved by default
> Warnings printed: SNA: legal_limit, LAX: capacity_cut

## A6 - And how did congestion at those two look in 2023?

*Pass when:* Uses the same two airports without being told again, and 2023 values.

*Result:* PASS

*Tool calls:* `compare_airports` {"airport_codes": ["LAX", "SNA"], "year": 2023}

**In calendar 2023 LAX was again more congested than SNA, and the gap was a bit wider than it is today.** LAX's system delay rate was 1.4 points higher than SNA's (a ratio of 1.33), compared with 0.9 points over the latest three years.

| Calendar 2023 | LAX | SNA | Difference |
|---|---|---|---|
| System delay rate | 5.6% | 4.2% | +1.4 pts (ratio 1.33) |
| Overall delay rate (15+ min, any cause) | 20.5% | 18.5% | +2.0 pts (ratio 1.11) |
| Arriving flights in delay data | 195,617 | 45,732 | |
| Passengers on departing flights | 37,119,938 | 5,725,328 | |

**Compared with now:**
- **LAX** has eased somewhat. Its system delay rate was 5.6% in 2023 and is 5.0% in the latest 12 months (August 2025 to July 2026).
- **SNA** is roughly flat, at 4.2% in 2023 and 4.3% in the latest 12 months.
- Both airports had higher overall delay rates in 2023 (20.5% and 18.5%) than their three-year averages (18.9% and 17.5%). The three-year window starts in August 2023, so it overlaps with 2023 and isn't a clean before-and-after.

**Caveats:**
- The system delay category is assigned by airlines, includes ordinary weather, and covers only domestic flights of the larger reporting airlines.
- Past years have raw metrics only. There are no 2023 capacity-need scores or delay-cause breakdowns.
- The current warnings still apply: SNA's legal passenger cap and curfew, and LAX's reduced seat capacity since 2019.

If you want to see when congestion rose or fell, I can pull the month-by-month system delay rate for either airport.

> Data period: BTS T-100 airport-month summary, calendar 2023; BTS Airline Delay Causes, calendar 2023; BTS T-100 Segment, calendar 2023  
> Assumptions: proxies, not direct measurements: System delay rate  
> Confidence: Medium - LAX: capacity cut; SNA: legal limit; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: SNA: legal_limit, LAX: capacity_cut

## A3 - What is the percentage of long haul flights out of Anchorage airport?

*Pass when:* One number, the 3,000-mile definition stated, the cargo-included number next to it.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Anchorage airport"}; `airport_profile` {"airport_code": "ANC"}

At Ted Stevens Anchorage International (ANC), **2.8% of departing passenger flights are long-haul**, using our default cutoff of 3,000 miles or more. If you count cargo flights too, the share rises to **31.0%**. Anchorage is a major cargo hub, and cargo makes up 56.6% of its departing flights.

I took "Anchorage airport" to mean ANC. The city also has Merrill Field (MRI), a much smaller nonhub airport with only partial data.

There is no official definition of long-haul, so here is the share at three cutoffs (departing flights, domestic and international, calendar 2025):

| Cutoff | Passenger flights | All flights incl. cargo |
|---|---|---|
| 2,000+ miles | 13.7% (5,239 flights) | 47.4% (41,732) |
| 2,500+ miles | 9.8% (3,723) | 43.2% (37,969) |
| 3,000+ miles | 2.8% (1,061) | 31.0% (27,305) |

Totals for 2025: 38,150 passenger departures and 87,988 departures including cargo. The two measures differ so much because 49,838 of those departures were cargo or other non-passenger flights.

**What this means for the capacity question:** Most long-haul traffic at ANC is cargo, which uses the same runways but is left out of the capacity-need score. The FAA flight forecast does include cargo, so ANC's forecast flight growth (14.8%) partly reflects freight, not passengers. Passenger traffic is 98.6% domestic, and the biggest airline is Alaska Airlines with a 61.4% share.

Background (not from our data): Anchorage sits on great-circle routes between Asia and North America, which is why freighters often stop there to refuel.

I can show the share at a different cutoff, or compare ANC with other cargo-heavy airports, if that would help.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; FAA passenger boarding data CY2025, calendar 2025; BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, FAA forecast passenger growth, FAA forecast flight growth; long-haul means 3,000 miles or more (our definition; adjustable); 'Anchorage airport' was taken to mean ANC; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - ANC: cargo heavy; the answer uses proxy measures (scores, system delay rate, load factor or forecasts); an airport name was resolved by default
> Warnings printed: ANC: cargo_heavy

## A7 - What if long-haul means over 2,300 miles?

*Pass when:* Recomputed at 2,300 miles for Anchorage.

*Result:* PASS

*Tool calls:* `airport_profile` {"airport_code": "ANC", "long_haul_miles": 2300}

If long-haul means 2,300 miles or more, **12.6% of departing passenger flights at Anchorage (ANC) are long-haul** (4,820 of 38,150 in 2025). Counting cargo flights too, the share is **46.5%** (40,947 of 87,988).

| Cutoff | Passenger flights | All flights incl. cargo |
|---|---|---|
| 2,000+ miles | 13.7% | 47.4% |
| **2,300+ miles** | **12.6%** | **46.5%** |
| 2,500+ miles | 9.8% | 43.2% |
| 3,000+ miles | 2.8% | 31.0% |

The tool counts flights of 2,300 miles or more, not strictly over 2,300. That tiny difference is unlikely to change the result.

**Why the cutoff matters so much:** The passenger share barely changes between 2,000 and 2,300 miles, then drops sharply above 2,500 and again above 3,000. So most of ANC's longer passenger flights are between about 2,000 and 3,000 miles. I don't have route data, so I can't say which destinations those are. 

Including cargo, nearly half of all departures fly 2,300 miles or more at this cutoff. That's because 56.6% of ANC's departures are cargo flights, and many are long-distance. Cargo uses the same runways but isn't part of the capacity-need score.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score; long-haul means 2,300 miles or more (our definition; adjustable); scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - ANC: cargo heavy; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: ANC: cargo_heavy

## A4 - What is the unmet flight demand in SFO airport and why?

*Pass when:* An estimate named as an estimate or proxy, with the why from the delay data.

*Result:* PASS

*Tool calls:* `airport_profile` {"airport_code": "SFO"}

San Francisco International (SFO) has an estimated **unmet flight demand of 108,307 extra takeoffs and landings a year by fiscal 2035**. That is the FAA forecast rising from 406,220 to 514,527 operations, up 26.7%. We call this gap "unmet" because SFO is already strained: its system delay rate is the highest of all full-data airports. This is an estimate, not a measurement, and the FAA tends to over-forecast.

**Why the demand looks unmet: the airfield is already congested**
- **System delay rate** (arrivals delayed by the airport and air-traffic system): 13.4% over three years, ranking 100 out of 100 among full-data airports. Over the latest 12 months it rose to 17.3%.
- **Overall delay rate** (arrivals 15+ minutes late, any cause): 27.4%.
- **Delay causes:** 48.9% of delayed flights were put down to the system, 24.7% to the airline, 23.7% to late aircraft and only 2.5% to extreme weather. Airlines code the "system" category, and it includes ordinary weather, so it mostly measures congestion but not only congestion.
- Background (not from our data): SFO's two pairs of closely spaced parallel runways lose capacity in low clouds and fog, which helps explain why so many delays fall under "system" rather than "weather."

**Caveats**
- **Capacity was cut:** seats are down 5.0% since 2019 and passengers are down 4.4%. Passenger flights are down 11.0% since 2019, while passengers per flight rose from 132.1 to 141.1. The full planes (82.6%) partly reflect fewer seats, not rising demand.
- **Delays swing a lot from year to year:** the system delay rate was 7.5% in 2023, 15.2% in 2024 and 9.9% in 2025.
- **Schedules are coordinated:** the FAA coordinates schedules at SFO (Level 2 schedule facilitation), but this is not a hard cap on flights.
- **One airline dominates:** United carries 44.8% of passengers.

SFO's flight-side score is 97.1, and it ranks 3rd of 343 airports overall. To check next: runway and airspace limits, and any capacity work already planned. Those aren't in our data.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, Flight-side score, How full the planes are, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; 'unmet flight demand' is an estimate from the FAA forecast, used only when the airport is strained today; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - SFO: capacity cut; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: SFO: capacity_cut

## A5 - How does that compare with Oakland?

*Pass when:* Oakland is not called unmet demand, because it is not strained.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Oakland"}; `compare_airports` {"airport_codes": ["SFO", "OAK"]}; `airport_profile` {"airport_code": "OAK"}

Oakland is very different from SFO. The FAA still forecasts strong growth there, but **Oakland is not strained today**, so its forecast gap of **30,637 extra takeoffs and landings by 2035 is not unmet demand**. It is labelled simply as forecast flight growth. SFO's estimated unmet demand is 3.54 times larger. (I took "Oakland" to mean Oakland San Francisco Bay (OAK). The same metro area also has San Jose (SJC).)

| | SFO | OAK |
|---|---|---|
| Capacity-need score | 86.9 (rank 3 of 343) | 46.0 (rank 208 of 343) |
| Flight-side score | 97.1 | 49.7 |
| Forecast extra takeoffs and landings by 2035 | 108,307 (unmet, estimate) | 30,637 (forecast growth only) |
| FAA forecast flight growth | 26.7% | 24.8% |
| System delay rate, 3 years | 13.4% | 2.3% |
| System delay rate, latest 12 months | 17.3% | 1.7% |
| Overall delay rate | 27.4% | 18.4% |
| System share of delayed flights | 48.9% | 12.3% |
| How full the planes are | 82.6% | 74.2% |
| Passenger growth since 2019 | -4.4% | -35.5% |

**Why the two differ**
- **Delays:** SFO's system delay rate (delays blamed on the airport and air-traffic system) is 5.83 times Oakland's. At Oakland, delays come mostly from late-arriving aircraft (54.1%) and the airline (32.5%), which points to how airlines run their schedules rather than a full airfield. Airlines code the "system" category, and it includes ordinary weather.
- **Demand has shrunk at Oakland:** seats are down 31.5% since 2019 and passengers are down 35.5%. Oakland has room to spare. Added capacity there would compete with traffic that has already left, not absorb overflow.

**Oakland-specific caveats**
- Cargo is 17.9% of departing flights, and the FAA forecast includes cargo.
- Southwest carries 76.7% of passengers, a heavy dependence on one airline.

If you want a third Bay Area option, I can add San Jose (SJC) to the comparison.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, Flight-side score, How full the planes are, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; 'unmet flight demand' is an estimate from the FAA forecast, used only when the airport is strained today; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - SFO: capacity cut; OAK: capacity cut; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: SFO: capacity_cut, OAK: capacity_cut

## A8 - Is Memphis a good candidate, given its cargo traffic?

*Pass when:* Uses the Memphis profile and the cargo share.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Memphis"}; `airport_profile` {"airport_code": "MEM"}

**Memphis (MEM) looks like a mixed candidate for passenger capacity, and its cargo traffic makes the score look better than the passenger case really is.** It scores 59.5 on capacity need, which puts it 46th of 78 small-hub airports and 116th of 343 overall. Nearly all of that comes from the flight side. Cargo is 65.1% of departing flights, so much of that flight-side strength reflects freighters rather than passengers.

| Side | Score | Inputs |
|---|---|---|
| Passenger | 45.4 | Planes 73.4% full; passengers up 0.9% since 2019; FAA forecast +25.8% |
| Flight | 73.7 | System delay rate 4.9% (5.1% latest 12 months); FAA forecast flight growth +18.4% |

**Why cargo matters here**
- **Forecast flights include cargo.** The FAA's +18.4% (29,629 extra takeoffs and landings by fiscal 2035) counts cargo, so it doesn't show how much passenger growth there will be.
- **The delay rate is a weak measure of strain here.** It only covers passenger airlines, and it suggests moderate strain, not severe. Memphis is not flagged as strained, so the forecast growth is not called unmet demand. Of flights delayed 15+ minutes, 21.4% were blamed on the airport and air-traffic system, while late aircraft (39.4%) and the airline (35.3%) were bigger causes. Airlines code the system category themselves, and it includes ordinary weather.
- **Freighters share the runways.** Cargo competes for runway capacity but isn't in the score.

**Passenger demand is soft**
- Passenger numbers are flat against 2019 and passenger flights are down 7.7%.
- Seats are up 6.7%, so airlines are adding seats faster than travellers are filling them.
- Planes have become less full: 70.2% so far in 2026, down from 82.4% in 2022.

Background (not from our data): Memphis is FedEx's main global hub, which explains why cargo dominates.

**What to check next:** whether runway or apron capacity is the real constraint (I don't have peak-hour or gate data), and how much of the 29,629 extra operations is cargo. If the investment would serve cargo infrastructure, that falls outside what this score measures.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); FAA passenger boarding data CY2025, calendar 2025; BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, Flight-side score, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; 'unmet flight demand' is an estimate from the FAA forecast, used only when the airport is strained today; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - MEM: cargo heavy; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: MEM: cargo_heavy

## B1 - Score the top 3 airports that have the highest congestion in the US, only small airports.

*Pass when:* Small-hub class, sorted by the system delay rate, three airports with scores; says what 'small' means.

*Result:* PASS

*Tool calls:* `rank_airports` {"size_classes": ["small"], "sort_by": "system_delay_rate_pct", "limit": 3}; `compare_airports` {"airport_codes": ["PGD", "EYW", "STT"]}

The three most congested small airports are Punta Gorda (PGD), Key West (EYW) and St. Thomas (STT). I ranked them by the system delay rate over three years. Punta Gorda is the clear standout: it scores 94.9, the highest of all 343 ranked airports. St. Thomas and Key West score well below it, at 70.8 and 67.7.

"Small" here means the FAA small-hub class (78 ranked airports). Tweed/New Haven (HVN) was left out because its data is incomplete.

| | Punta Gorda (PGD) | Cyril E King, St. Thomas (STT) | Key West (EYW) |
|---|---|---|---|
| System delay rate, 3 yrs | 8.6% | 7.9% | 8.0% |
| System delay rate, latest 12 mo | 7.5% | 9.6% | 7.2% |
| Overall delay rate | 24.4% | 20.2% | 19.5% |
| **Capacity-need score** (out of 100) | **94.9** | **70.8** | **67.7** |
| Rank among small airports | 1 of 78 | 26 | 32 |
| Planes full | 85.8% | 77.9% | 77.3% |
| FAA forecast flight growth | 26.8% | 15.0% | 9.3% |
| FAA forecast passenger growth | 30.0% | 15.6% | 19.7% |
| Biggest airline's share | 99.6% (Allegiant) | 33.7% (American) | 22.8% (American) |

**How to read the delay rates:** the system delay rate is our congestion measure. It counts arrival delays that airlines blame on the airport and air-traffic system. Airlines code these themselves, and the category includes ordinary weather, so it mostly, but not purely, measures congestion.

**What matters:**
- **Punta Gorda** is the strongest candidate on both halves of the score. The catch is that one airline carries 99.6% of its passengers, so its demand depends almost entirely on Allegiant's plans.
- **St. Thomas** is the only one getting worse: its latest 12 months are above its three-year rate. It is in a US territory.
- **Key West** is congested, but its FAA flight forecast is low, which holds its score down.

Next, I can show where each airport's delays come from or its monthly delay trend.

> Data period: BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; FAA passenger boarding data CY2025, calendar 2025; BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: System delay rate, Capacity-need score, How full the planes are, FAA forecast passenger growth, FAA forecast flight growth; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - the answer uses proxy measures (scores, system delay rate, load factor or forecasts)

## B2 - Top 5 airports in Texas by how full the planes are.

*Pass when:* Five Texas airports by load factor.

*Result:* PASS

*Tool calls:* `rank_airports` {"states": ["TX"], "sort_by": "load_factor_pct", "limit": 5}

Dallas-Fort Worth (DFW) and McAllen (MFE) are tied for the fullest planes in Texas at 82.5%. Houston Bush (IAH), Abilene (ABI) and Corpus Christi (CRP) come next. All 25 Texas airports with full data were ranked.

| # | Airport | Size class | How full (%) | Capacity-need score |
|---|---|---|---|---|
| 1 | Dallas-Fort Worth International (DFW) | large | 82.5 | 79.3 |
| 1 | McAllen International (MFE) | small | 82.5 | 44.5 |
| 3 | George Bush Intercontinental, Houston (IAH) | large | 79.9 | 70.4 |
| 4 | Abilene Regional (ABI) | nonhub | 79.5 | 78.1 |
| 5 | Corpus Christi International (CRP) | nonhub | 76.6 | 38.0 |

**What "how full" means:** passengers divided by seats on departing flights over the latest 12 months. It isn't the official load factor, which is based on miles flown. It's also the weakest of the five score inputs, because airline pricing and aircraft choices affect it.

**Full planes don't always mean high upside:**
- **DFW and IAH** have strong scores on the flight side too. Both are flagged as strained, with system delay rates of 6.2% and 6.5%. At IAH, flights have stayed flat while passenger numbers rose.
- **Abilene** scores high on both sides. Its FAA forecast is +31.8% for passengers and +30.5% for flights. But it's a very small airport (105,976 boardings in 2025), so the extra demand is small in absolute terms. The FAA forecasts 33,120 extra boardings a year by 2035.
- **McAllen and Corpus Christi** have full planes but weak flight-side scores. Their delay rates are low, and the FAA forecasts that McAllen's flights will shrink by 9.8%, while Corpus Christi's stay roughly flat (+0.3%). Their overall scores are low as a result.

I can rank Texas by the overall capacity-need score instead, or compare DFW, IAH and ABI side by side.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years); FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: How full the planes are, Capacity-need score, Flight-side score, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - the answer uses proxy measures (scores, system delay rate, load factor or forecasts)

## B3 - Which large airports have planes over 85% full?

*Pass when:* Large hubs filtered by a load factor threshold.

*Result:* PASS

*Tool calls:* `rank_airports` {"size_classes": ["large"], "sort_by": "load_factor_pct", "min_value": 85, "limit": 25}; `rank_airports` {"size_classes": ["large"], "sort_by": "load_factor_pct", "limit": 5}

**None of them.** Of the 30 large airports (the FAA large-hub class, all with full data), none has planes over 85% full. The highest is Newark Liberty (EWR) at 83.2%.

"How full" here means passengers divided by seats on departing flights over the latest 12 months. This is our own measure, not the official load factor, which is based on passenger-miles. It's also the weakest of the five score inputs, because airline pricing and fleet choices drive it.

The five fullest large airports:

| Airport | Planes full | Passengers vs 2019 | Seats vs 2019 | Capacity-need score |
|---|---|---|---|---|
| Newark (EWR) | 83.2% | 1.0% | 2.2% | 80.7 |
| San Francisco (SFO) | 82.6% | -4.4% | -5.0% | 86.9 |
| Dallas-Fort Worth (DFW) | 82.5% | 14.9% | 15.8% | 79.3 |
| Atlanta (ATL) | 82.3% | -4.5% | -1.0% | 69.8 |
| Los Angeles (LAX) | 82.1% | -15.7% | -12.8% | 75.3 |

The fullest planes don't all mean the same thing:
- **SFO and LAX:** both flagged for capacity cuts, so their seats are below 2019. Their full planes partly reflect fewer seats rather than rising demand.
- **Newark:** a legal flight cap of 36 arrivals and 36 departures an hour applies. This could limit how much added capacity can actually be used.
- **Dallas-Fort Worth:** the cleanest demand signal. Passengers are up 14.9% since 2019, seats grew with them and there are no warnings.

I can lower the threshold (say 80%), run the same check on medium or small hubs, or compare any of these side by side.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: How full the planes are, Capacity-need score; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - the answer uses proxy measures (scores, system delay rate, load factor or forecasts); EWR: legal limit; SFO: capacity cut; LAX: capacity cut
> Warnings printed: EWR: legal_limit, SFO: capacity_cut, LAX: capacity_cut

## B4 - Compare Portland and Providence.

*Pass when:* Asks which Portland (Oregon or Maine), or covers both and says so.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Portland"}; `find_airport` {"query": "Providence"}

Which Portland do you mean: Portland, Oregon (PDX) or Portland, Maine (PWM)?

For Providence, I'll use Rhode Island T.F. Green International (PVD) unless you say otherwise. The same metro area also has Boston Logan (BOS) and Manchester-Boston Regional (MHT).

Portland, Maine (PWM) may be the closer match for PVD, since both are in the FAA small-hub class. PDX is a medium hub. If you want, I can also compare all three: PDX, PWM and PVD.

> Data period: no data was used in this reply  
> Assumptions: none  
> Confidence: n/a - no data figures were used in this reply

## B5 - Which airports are the best candidates overall? Only count the ones with complete data.

*Pass when:* National ranking shown per size class.

*Result:* PASS

*Tool calls:* `rank_airports` {"sort_by": "total_score"}

Among the 343 airports with complete data, the strongest candidates are **Orlando (MCO)** for large airports, **Fort Myers (RSW)** for medium, **Punta Gorda (PGD)** for small and **Rickenbacker (LCK)** for nonhub. The ranking is split by FAA size class because size isn't part of the score. In a single national list, small leisure airports would crowd out the rest. I left out 59 airports with partial or thin data.

| Class | #1 | #2 | #3 | #4 | #5 |
|---|---|---|---|---|---|
| Large | MCO 87.8 | San Francisco (SFO) 86.9 | Chicago O'Hare (ORD) 84.6 | New York JFK (JFK) 84.0 | Miami (MIA) 83.0 |
| Medium | RSW 81.7 | Charleston (CHS) 78.8 | Jacksonville (JAX) 75.8 | San Juan (SJU) 75.4 | Raleigh-Durham (RDU) 73.1 |
| Small hub | PGD 94.9 | Northwest Arkansas (XNA) 85.5 | Orlando Sanford (SFB) 85.2 | St Pete-Clearwater (PIE) 84.1 | Provo (PVU) 80.2 |
| Nonhub | LCK 85.7 | Traverse City (TVC) 78.8 | Abilene (ABI) 78.1 | Scott/MidAmerica (BLV) 77.8 | Aguadilla (BQN) 77.7 |

**Cleanest cases (no warnings):**
- **MCO:** planes 81.9% full, 14.7% more passengers than in 2019 and 7,766,513 extra yearly boardings forecast by 2035.
- **MIA:** 23.4% more passengers than in 2019.
- **PGD:** planes 85.8% full and an 8.6% system delay rate.
- **RSW, CHS and XNA:** high scores with no flags.

**Warnings that change the picture:**
- **SFO:** seats were cut (-5.0% vs 2019), so its full planes reflect fewer seats, not rising demand.
- **ORD:** a temporary summer 2026 flight cap.
- **JFK:** slot-controlled, so new runways or gates can't be used without more slots.
- **LCK (44.2% cargo) and BQN (42.8%):** cargo-heavy. BQN also had seats cut.
- **PVU:** passenger growth of 383.9% since 2019 comes from a very small base.

The score is a 0-100 ranking against other full-data airports. It measures how much added capacity would likely be filled. It stands in for profit but isn't a profit measure, because there's no cost or return data. The system delay rate is coded by airlines and includes ordinary weather. I can profile any of these airports or compare a shortlist side by side.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years); FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, How full the planes are, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - SFO: capacity cut; ORD: legal limit; JFK: legal limit; LCK: cargo heavy
> Warnings printed: ORD: legal_limit, JFK: legal_limit, SFO: capacity_cut, LCK: cargo_heavy, BQN: cargo_heavy, BQN: capacity_cut

## B6 - How has passenger traffic at Boston changed since 2019? Give me the year by year picture.

*Pass when:* Year by year values for Boston, with 2026 marked partial.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Boston"}; `airport_profile` {"airport_code": "BOS"}

Passenger traffic at Boston Logan (BOS) is back to its 2019 level but has barely grown past it. The latest 12 months (May 2025 - April 2026) had 20,983,745 passengers, up 1.2% on 2019. The high point was 2024, and 2025 came in slightly below it. I assumed you meant Logan. The area's other airports are Manchester-Boston Regional (MHT) and Providence (PVD).

| Year | Passengers | How full planes were | System delay rate |
|---|---|---|---|
| 2019 | 20,742,138 | 81.9% | 9.2% |
| 2020 | 6,050,302 | 52.0% | 2.7% |
| 2021 | 10,938,231 | 75.1% | 3.5% |
| 2022 | 17,472,973 | 78.5% | 6.3% |
| 2023 | 19,991,297 | 83.3% | 7.2% |
| 2024 | 21,280,480 | 83.1% | 7.9% |
| 2025 | 21,105,980 | 81.6% | 11.0% |
| 2026 (Jan-Apr only) | 6,139,216 | 78.2% | 8.8% (Jan-Jul) |

Passengers are counted on departing flights. "How full" is passengers divided by seats. The 2026 row covers only part of the year, so it can't be compared with full years.

**What this means for capacity:**
- **Flat traffic, but not because of capacity cuts:** Seats are up 1.4% on 2019. Passenger flights in 2025 were 3.1% below 2019, but planes carried more people: 111.9 passengers per flight against 106.4.
- **Congestion is rising:** The system delay rate reached 11.0% in 2025, the highest in the series. This rate counts delays that airlines blame on the airport and air-traffic system, which includes ordinary weather. It's 9.1% over three years and 10.9% in the latest 12 months, among the highest of the 343 ranked airports. Logan counts as strained today.
- **Forecast:** The FAA expects boardings to grow 26.5% from 2025 to 2035. The FAA tends to over-forecast.

I can also show the month-by-month trend if you want to see seasonality or the recent slowdown.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); FAA passenger boarding data CY2025, calendar 2025; BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: How full the planes are, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; 'Boston' was taken to mean BOS  
> Confidence: Medium - the answer uses proxy measures (scores, system delay rate, load factor or forecasts); an airport name was resolved by default

## B7 - Show me medium-size airports in the West with the fastest forecast passenger growth.

*Pass when:* West region, medium hubs, sorted by forecast passenger growth.

*Result:* PASS

*Tool calls:* `rank_airports` {"region": "west", "size_classes": ["medium"], "sort_by": "forecast_passenger_growth_pct", "limit": 10}

Portland (PDX) has the fastest FAA forecast passenger growth among medium-hub airports in the West, at 33.2% (fiscal 2035 vs 2025). Oakland (OAK), San Jose (SJC) and Boise (BOI) are close behind. Of these, only Boise has both a strong forecast and real passenger growth since 2019.

"Medium" means the FAA medium-hub class. The West has 11 of them, all with full data, and the table shows the top 10.

| # | Airport | Forecast pax growth | Pax growth since 2019 | Planes full | Score (rank of 34 medium) |
|---|---|---|---|---|---|
| 1 | Portland (PDX) | 33.2% | -6.4% | 82.0% | 72.3 (6) |
| 2 | Oakland (OAK) | 29.9% | -35.5% | 74.2% | 46.0 (30) |
| 3 | San Jose (SJC) | 29.6% | -35.0% | 73.9% | 44.7 (31) |
| 4 | Boise (BOI) | 28.6% | 24.8% | 78.7% | 66.7 (10) |
| 5 | Sacramento (SMF) | 24.7% | 3.8% | 76.5% | 52.0 (25) |
| 6 | Anchorage (ANC) | 24.6% | 0.8% | 72.8% | 59.1 (15) |
| 7 | Ontario (ONT) | 22.9% | 26.5% | 74.1% | 52.0 (25) |
| 8 | Kahului (OGG) | 21.9% | -9.4% | 77.7% | 48.1 (29) |
| 9 | John Wayne/Orange County (SNA) | 19.4% | 7.2% | 80.4% | 62.0 (13) |
| 10 | Hollywood Burbank (BUR) | 16.0% | -0.7% | 72.3% | 44.0 (32) |

**Caveats that change the picture:**
- **Oakland and San Jose:** both still carry about a third fewer passengers than in 2019, and seats were cut by a similar amount. Their high forecasts largely describe winning back lost traffic, which explains their low overall scores. San Jose also has a night noise curfew.
- **Portland and Kahului:** both have fewer seats than in 2019, so their full planes partly reflect cut seats rather than rising demand.
- **Orange County (SNA):** a legal passenger cap of roughly 6.1-6.25 million in our units (departing passengers only) limits growth there. It boarded 5,521,729 passengers in 2025.
- **Anchorage and Ontario:** cargo makes up 56.6% and 36.2% of flights. Cargo uses the same runways but isn't in the score.

The FAA tends to over-forecast, so these figures are best used to compare airports with each other, not as predictions.

A useful next step would be a side-by-side comparison of Portland, Boise and Sacramento.

> Data period: FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: FAA forecast passenger growth, Capacity-need score, How full the planes are, FAA forecast flight growth; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - PDX: capacity cut; OAK: capacity cut; SJC: capacity cut, legal limit; ANC: cargo heavy
> Warnings printed: SJC: legal_limit, SNA: legal_limit, PDX: capacity_cut, OAK: capacity_cut, SJC: capacity_cut, ANC: cargo_heavy, ONT: cargo_heavy, OGG: capacity_cut

## B8 - What's the busiest month at Burlington, Vermont, and how full are the planes then?

*Pass when:* The busiest month and its load factor.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Burlington, Vermont"}; `airport_trend` {"airport_code": "BTV", "metric": "load_factor_pct"}; `airport_profile` {"airport_code": "BTV"}

In the latest 12 months, the busiest month at Patrick Leahy Burlington International (BTV) was **October 2025**, with **79,157 passengers** on departing flights. Planes were **86.9% full** that month, compared with 83.0% across the whole year.

**How the peak compares**
- July and August 2025 were about as full: 88.6% and 88.1%. Over the last three years, July is the fullest month on average (86.7%), with August and February next (85.5% each).
- The emptiest month in the last three years was September 2024 (71.8%).
- "How full" here means passengers divided by seats on departing flights. That isn't the official load factor, and it partly reflects airline pricing and choice of aircraft.

**Why it matters for capacity**
- BTV ranks 18th of 343 ranked airports and 6th of 78 small hubs (the FAA's small-hub class), with a capacity-need score of 79.2.
- Seats are almost unchanged since 2019 (+0.1%), while passengers are up 2.3%. Passenger flights fell 18.0% between 2019 and 2025, and each flight carries more people (73.2 per flight, up from 58.1). So airlines have been using fewer, larger planes, not adding seats.
- The airport counts as strained: its system delay rate is 5.5% over three years and 6.3% in the latest 12 months. The airlines assign this delay category themselves, and it includes ordinary weather.

**Limits**
I only have monthly totals, so I can't tell you about peak days, peak hours or how busy the gates are. If it would help, I can show the month-by-month passenger or seat series to check whether October peaks every year.

> Data period: BTS T-100 airport-month summary, 2023-05 to 2026-04 / 2025-05 to 2026-04 (latest 12 complete months); BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); FAA passenger boarding data CY2025, calendar 2025; BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: How full the planes are, Capacity-need score, System delay rate; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - the answer uses proxy measures (scores, system delay rate, load factor or forecasts)

## C1 - Score the top 3 airports that have the highest congestion in August in the US.

*Pass when:* Ranks by the August system delay rate and says scores do not exist by month.

*Result:* PASS

*Tool calls:* `rank_airports` {"sort_by": "system_delay_rate_pct", "month": 8, "limit": 3}; `rank_airports` {"sort_by": "total_delay_rate_pct", "month": 8, "limit": 3}

Ranked by August system delay rate, the three most congested airports are Newark (EWR), Orlando (MCO) and San Juan (SJU). Orlando has the highest capacity-need score of the three at 87.8, then Newark at 80.7 and San Juan at 75.4.

**How I measured congestion:** I used the system delay rate, which is the share of arriving flights delayed by causes the airport and air-traffic system are blamed for. I added up all Augusts from 2023 to 2025. Airlines decide which delays go in this category, and it includes ordinary weather, so it's mostly congestion but not only congestion.

| Airport | August system delay rate | Capacity-need score | Passenger side | Flight side | Rank in size class |
|---|---|---|---|---|---|
| Newark (EWR) | 10.9% | 80.7 | 72.7 | 88.6 | 7 of 30 large |
| Orlando (MCO) | 10.3% | 87.8 | 81.5 | 94.0 | 1 of 30 large |
| San Juan (SJU) | 9.8% | 75.4 | 77.6 | 73.3 | 4 of 34 medium |

**Caveats:**
- **Newark has a legal cap:** an FAA order limits it to 36 arrivals and 36 departures an hour. Its high delays may not turn into room for more flights, so its score needs extra care.
- **San Juan** is in a US territory. It is also tied with another airport for third place, which the tool didn't name.
- **Orlando** looks strongest: 14.7% passenger growth since 2019 and 26.4% forecast flight growth.
- **Scores are year-round.** They don't exist by month, so each score above covers the latest full period, not August.

**By overall delay rate** (delays from any cause), August's top three are different: Aguadilla (BQN) at 40.1%, San Juan (SJU) at 34.4% and Orlando Sanford (SFB) at 32.7%. Their scores are 77.7, 75.4 and 85.2. Aguadilla's score is weaker than it looks: seats there were cut since 2019, so its full planes reflect fewer seats rather than rising demand, and cargo is 42.8% of its flights.

> Data period: BTS Airline Delay Causes, August of 2023, 2024, 2025 (summed) / 2023-08 to 2026-07 (three years); BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: System delay rate, Capacity-need score, Passenger-side score, Flight-side score, How full the planes are, FAA forecast passenger growth; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - EWR: legal limit; the answer uses proxy measures (scores, system delay rate, load factor or forecasts); BQN: capacity cut, cargo heavy
> Warnings printed: EWR: legal_limit, BQN: cargo_heavy, BQN: capacity_cut

## C2 - Where is Delta the dominant airline?

*Pass when:* Says airline-network questions are not supported; may offer the biggest-airline share per airport.

*Result:* PASS

*Tool calls:* `rank_airports` {"sort_by": "top_airline_share_pct", "size_classes": ["large", "medium"], "limit": 25, "group_by_size_class": false}; `airport_profile` {"airport_code": "ATL"}; `airport_profile` {"airport_code": "MSP"}; `airport_profile` {"airport_code": "DTW"}; `airport_profile` {"airport_code": "SLC"}

I can't give you a complete list. This system can't filter airports by airline, and it has no data on any one airline's network. For each airport it only records the biggest airline and that airline's share of passengers. So I checked the four large airports most likely to be Delta strongholds. Delta is the biggest airline at all four, with more than half of passengers at each (calendar 2025):

| Airport | Delta share of passengers | Capacity-need score | Strained today? |
|---|---|---|---|
| Atlanta (ATL) | 74.7% | 69.8 | No |
| Minneapolis-St Paul (MSP) | 58.0% | 64.8 | No |
| Salt Lake City (SLC) | 57.5% | 60.9 | No |
| Detroit (DTW) | 54.8% | 54.8 | No |

What this means for capacity investment:
- **Relying on one airline is a risk.** Atlanta has the 5th-highest biggest-airline share among the 64 ranked large and medium airports. Growth at these airports depends mostly on Delta's own plans.
- **Seats were cut at Minneapolis and Detroit.** Both have fewer seats than in 2019 (-7.2% and -6.7%) and fewer passengers (-10.0% and -10.1%). Their fairly full planes reflect fewer seats, not rising demand.
- **Salt Lake City is the only one of the four with more passengers than in 2019 (+4.7%).** But its system delay rate is low (2.8% of arriving flights over three years), so it doesn't look congested.
- **None of the four is "strained"** (system delay rate in the top quarter of airports). So the FAA flight forecasts here count as forecast growth, not unmet demand.

Background (not from our data): Delta also has large operations at coastal airports such as New York JFK, Los Angeles, Seattle and Boston, where it may not be the single biggest airline.

I can check the biggest airline at any other airport you name, or rank airports by how much they rely on one airline.

> Data period: BTS T-100 Segment, calendar 2025; BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months)  
> Assumptions: proxies, not direct measurements: Capacity-need score, How full the planes are, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; 'unmet flight demand' is an estimate from the FAA forecast, used only when the airport is strained today; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - DAL: legal limit; OAK: capacity cut; ANC: cargo heavy; EWR: legal limit
> Warnings printed: DAL: legal_limit, EWR: legal_limit, SJC: legal_limit, OAK: capacity_cut, ANC: cargo_heavy, MSP: capacity_cut, SJC: capacity_cut, DTW: capacity_cut, PHL: capacity_cut, OGG: capacity_cut

## C3 - How many flights go from JFK to London?

*Pass when:* Declines: route-level questions are not supported.

*Result:* PASS

*Tool calls:* `airport_profile` {"airport_code": "JFK"}

I can't tell you how many JFK flights go to London. This system has no route, destination or city-pair data. For an airport, it only has totals and its biggest airline.

The closest thing I have is how many of John F Kennedy International's (JFK) departures fly long distances. These counts are for calendar 2025 and cover all destinations, domestic and international, not just London:

| Long-haul cutoff | Departing passenger flights | Share of passenger flights |
|---|---|---|
| 2,000+ miles | 96,455 | 45.4% |
| 2,500+ miles | 60,217 | 28.4% |
| 3,000+ miles (our default) | 49,841 | 23.5% |

JFK had 212,394 departing passenger flights in 2025. The domestic share of passengers is 45.6%, so a bit over half of passengers fly international.

Background (not from our data): London is more than 3,000 miles from New York, so JFK-London flights are part of the 3,000+ mile group above. That group also includes many other European, Asian and other long routes, so it is not a London count.

A caution for investment purposes: JFK is a slot-controlled airport, meaning the FAA caps how many flights it can have. Extra runway or gate capacity can't be used without more slots, however strong the demand. That matters even though JFK ranks 9th of 343 on the capacity-need score (84.0).

If it helps, I can give you the full JFK profile or compare its long-haul share with Newark (EWR) or other gateway airports.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score; long-haul means 3,000 miles or more (our definition; adjustable); scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - JFK: legal limit; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: JFK: legal_limit

## C4 - What's the congestion level at Teterboro?

*Pass when:* Says Teterboro is outside the covered airports; no invented number.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Teterboro"}

I don't have congestion data for Teterboro. It isn't one of the 402 FAA primary airports this dataset covers, so I have no delay rates, delay causes or other metrics for it.

Background (not from our data): Teterboro is a business and private jet airport with almost no scheduled airline service. Our congestion measures come from airline delay reports, which don't cover that kind of traffic.

Here's what I can do instead:
- **Look at nearby airline airports.** Newark (EWR), LaGuardia (LGA) and New York JFK (JFK) serve the same metro area. For each one I can give the congestion picture: the system delay rate over three years and over the latest 12 months, the overall delay rate and the delay causes. The system delay category is coded by the airlines themselves and includes ordinary weather.
- **Compare them side by side** on both congestion and the capacity-need score.

Should I pull that comparison for EWR, LGA and JFK?

> Data period: no data was used in this reply  
> Assumptions: none  
> Confidence: n/a - no data figures were used in this reply

## C5 - Which airports were the top expansion candidates in 2021?

*Pass when:* Says the score exists for the latest period only; offers raw 2021 metrics.

*Result:* PASS

*Tool calls:* none

I can't rank airports as expansion candidates for 2021. The capacity-need score only exists for the latest period, so there's no 2021 version of it.

The score combines how full planes are, passenger growth since 2019, the FAA forecast and three years of delays. Most of those inputs can't be recalculated for a single past year. For example, the FAA forecast is the 2025 edition, and the delay inputs cover 2023-08 to 2026-07.

**What I can show you for 2021:** rankings of single raw measures for that calendar year, nationally or filtered by region, state or FAA size class:
- **Load factor (%)**: how full the planes were (the share of seats filled)
- **System delay rate (%)**: a proxy for congestion. Airlines assign delays to this category, and it includes ordinary weather.
- **Total delay rate (%)**
- **Passengers**
- **Long-haul share of flights (%)** and **cargo share of flights (%)**

Keep in mind that 2021 was a recovery year after the pandemic. Many airports had unusually low traffic and unusual load factors, so a 2021 ranking may say more about how quickly each airport recovered than about lasting need.

**Other options:**
- **Today's ranking** of top candidates by the current score, which by default is split by size class
- **One airport over time**: its year-by-year history from 2019, or a month-by-month trend, to see how its 2021 position changed

Which would help most? For example, I could show the top 10 airports by 2021 load factor, or today's top candidates in a size class you choose.

> Data period: no data was used in this reply  
> Assumptions: none  
> Confidence: n/a - no data figures were used in this reply

## C6 - Should we invest in expanding LaGuardia?

*Pass when:* Gives the evidence and the slot limit; leaves the decision to the analyst.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "LaGuardia"}; `airport_profile` {"airport_code": "LGA"}

I can't make the investment decision, and I have no cost or return data. The evidence points both ways. LaGuardia (LGA) is one of the most congested airports in the country, but flight slots there are capped by FAA order. More runway or gate capacity would mostly ease delays rather than add flights, unless the cap changes.

**Why it looks strained**
- Its capacity-need score is 67.8 out of 100. That ranks it 76th of 343 airports nationally, and 19th of the 30 large airports.
- The system delay rate is 8.4% over three years and 10.4% in the latest 12 months. That puts LGA above 98% of airports. This category is coded by airlines and includes ordinary weather.
- Overall, 21.5% of arriving flights are late.
- 39.3% of delayed flights are blamed on the airport and air-traffic system, the largest single cause.
- Planes are 80.8% full on average, rising to 85.4% in August 2025.

**Why that may not turn into more flights**
- LaGuardia has a legal flight cap: slots are limited by FAA order, and nonstop flights can't go beyond 1,500 miles (Saturdays are exempt).
- The FAA's forecast of 33,029 extra takeoffs and landings by 2035 (+9.3%) already assumes the cap stays. Our data labels it "unmet flight demand (estimate)" because the airport is strained, but it is not a measure of true demand.
- Growth has come from bigger planes, not more flights. Passengers rose 4.7% since 2019 while passenger flights fell 4.8%, and passengers per flight went from 85.3 to 94.7.

**The passenger side is middling**
- The FAA forecasts 3,005,632 extra boardings by 2035 (+18.4%), about average among airports.
- Delta, the biggest airline, carries 23.8% of passengers.

Background (not from our data): LaGuardia's terminals were largely rebuilt in recent years, so near-term terminal upside may be limited.

**What to check next:** whether the slot cap might change, current terminal and gate use, and any projects already underway. Newark (EWR) and JFK are in the same metro area if you'd like a comparison.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); FAA passenger boarding data CY2025, calendar 2025; BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, Passenger-side score, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; 'unmet flight demand' is an estimate from the FAA forecast, used only when the airport is strained today; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - LGA: forecast constrained, legal limit; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: LGA: legal_limit, LGA: forecast_constrained

## C7 - What will a new terminal at Denver cost, and what return would we get?

*Pass when:* Declines cost and return; offers the capacity-need evidence.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Denver"}

I can't tell you what a new terminal at Denver International (DEN) would cost or what it would return, because this system has no cost, revenue or return data. What I can show is how much of any added capacity would likely get used. On that measure, Denver scores well.

**Capacity-need score: 76.7 out of 100.** The score compares Denver with the other airports that have full data. It ranks Denver 12th of 30 large hubs. The passenger side and the flight side each score 76.7.

| Measure | DEN |
|---|---|
| How full planes are (May 2025 - Apr 2026) | 81.2% |
| Passenger growth since 2019 | 18.8% |
| Seat growth since 2019 | 26.1% |
| FAA forecast passenger growth (fiscal 2025-2035) | 23.7% |
| FAA forecast extra boardings by 2035 | 9,475,223 |
| FAA forecast flight growth (takeoffs plus landings, includes cargo) | 14.7% |
| System delay rate (Aug 2023 - Jul 2026) | 6.6% |
| Boardings in 2025 | 39,976,695 |

**What this means:**
- The data marks Denver as strained today.
- Seats have grown faster than passengers since 2019, so the growth was not caused by cutting capacity.
- The FAA expects passenger growth to keep going over the next decade.
- The system delay rate is the measure of congestion used here. Airlines code these delays themselves, and the category includes ordinary weather. So it is a rough proxy, not a direct measure of terminal or airfield limits.

Keep in mind that the score only ranks upside (how much new capacity would get filled). It stands in for profit but is not a profit estimate.

**What to check next:** costs, Denver's own capital plan, and how full its gates and terminal are. None of these are in this data. I can also pull Denver's full profile (delay causes, flight-demand estimate, year-by-year history) or compare it with other large hubs.

> Data period: see the tool trace  
> Assumptions: proxies, not direct measurements: Capacity-need score, Passenger-side score, Flight-side score; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - the answer uses proxy measures (scores, system delay rate, load factor or forecasts)

## C8 - What is the delay rate at Glacier Park airport in Kalispell, and can I trust it?

*Pass when:* Resolves Glacier Park to FCA, gives the rate and the sample size.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Glacier Park International, Kalispell, Montana"}; `airport_profile` {"airport_code": "FCA"}

At Glacier Park International (FCA) in Kalispell, Montana, 4.0% of arriving flights were delayed by the airport and air-traffic system over the last three years (2023-08 to 2026-07). Counting every cause, 16.6% arrived 15 or more minutes late. You can trust these numbers as a broad measure, with a few limits.

**The delay figures**
| Measure | Value |
|---|---|
| System delay rate, three years | 4.0% |
| System delay rate, latest 12 months | 4.7% |
| Overall delay rate (any cause, 15+ min), three years | 16.6% |
| Arriving flights in the three-year sample | 15,601 |

**Why the numbers hold up**
- **Enough flights:** the three-year rate rests on 15,601 arriving flights. That's a reasonable sample for a small airport.
- **Stable from year to year:** the system delay rate has stayed between 2.3% and 3.9% in every full year since 2019, with 3.9% in both 2024 and 2025.
- **Full data:** FCA has complete data and the system rates its data confidence high.

**Limits to keep in mind**
- **Airlines decide the cause.** The "system" delay category is assigned by airlines and includes ordinary weather, so it mostly, but not only, measures congestion.
- **Not every flight is counted.** It covers domestic flights of the larger reporting airlines only.
- **The latest year runs higher.** The last 12 months show 4.7%, and the partial 2026 figure is 4.8%. One year can swing a lot, which is why the three-year figure drives the score. It's worth watching.
- **Congestion isn't the main cause of delays here.** Of the flights that were late, 24.1% were blamed on the airport and air-traffic system. Airline causes (42.9%) and late-arriving aircraft (28.5%) account for more.

**What it means for capacity:** FCA sits in the middle of the full-data airports on system delays (position 49.1 of 100) and is not counted as strained. So its forecast flight growth of 19.1% is not called unmet demand. FCA's strong score comes from the passenger side instead: planes are 85.7% full and passenger numbers are up 57.0% since 2019.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, Passenger-side score, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; 'unmet flight demand' is an estimate from the FAA forecast, used only when the airport is strained today; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
