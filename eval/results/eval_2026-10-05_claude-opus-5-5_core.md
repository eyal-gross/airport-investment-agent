# Evaluation run - 2026-10-05 00:35 - claude-opus-5-5

**7 of 7 questions passed.** 231 numbers appeared in the answers; 0 answers ended with a number that could not be traced to a tool result; 0 answers passed only after one automatic rewrite. Average 10.8s per question; 218,310 input and 6,218 output tokens in total.

| Id | Group | Result | Tools | Number check | Seconds |
|---|---|---|---|---|---|
| A1 | core | PASS | rank_airports | passed | 13.4 |
| A2 | core | PASS | find_airport, find_airport, compare_airports | passed | 12.7 |
| A6 | follow-up | PASS | compare_airports | passed | 9.9 |
| A3 | core | PASS | find_airport, airport_profile | passed | 9.0 |
| A7 | follow-up | PASS | airport_profile | passed | 8.4 |
| A4 | core | PASS | airport_profile | passed | 10.0 |
| A5 | follow-up | PASS | find_airport, compare_airports, airport_profile | passed | 12.4 |

## A1 - Which airports in New England are strong candidates for terminal expansion?

*Pass when:* A ranked list from the six states, scores shown, reasons given.

*Result:* PASS

*Tool calls:* `rank_airports` {"region": "new england", "limit": 10}

Boston Logan (BOS), Burlington (BTV) and Portland, Maine (PWM) are the strongest New England candidates, with Bangor (BGR) close behind. One caveat first: no public data measures terminal or gate use, so I'm judging them by our capacity-need score. It measures how much added capacity would likely be filled. It doesn't measure profit.

| Airport | Size class | Score | Passenger side | Flight side | How full planes are | Passengers vs 2019 | FAA forecast passengers |
|---|---|---|---|---|---|---|---|
| Boston (BOS) | large | 82.9 | 72.2 | 93.6 | 81.7% | +1.2% | +26.5% |
| Burlington (BTV) | small | 79.2 | 73.7 | 84.8 | 83.0% | +2.3% | +22.9% |
| Portland (PWM) | small | 77.4 | 79.2 | 75.6 | 82.8% | +17.2% | +21.6% |
| Bangor (BGR) | nonhub | 71.8 | 78.0 | 65.5 | 80.4% | +40.8% | +24.1% |
| Hartford (BDL) | medium | 65.9 | 60.8 | 71.0 | 81.3% | -2.7% | +15.7% |

The passenger side matters most for a terminal:
- **Boston** ranks 11th of 343 nationally and is flagged as strained. It has the highest system delay rate in the region (9.1%). That category is coded by airlines and includes ordinary weather. Boston also has by far the largest forecast gain: 5,612,088 more boardings a year by 2035. Since 2019, though, its passenger numbers have barely grown.
- **Portland and Bangor** have the strongest passenger-side scores, with real growth since 2019. Seats have grown alongside passengers (+21.6% and +48.8%), so airlines are already adding capacity there.
- **Burlington** has the fullest planes in the region (83.0%) and is also flagged strained. Its growth since 2019 has been small.

"Small" here means the FAA small-hub class. FAA forecasts tend to run high, so treat them as a way to rank airports, not as predictions.

Four airports have no total score because their data is partial: New Haven (HVN), Cape Cod (HYA), Block Island (BID) and Westerly (WST). Lower down, Worcester (ORH) and Portsmouth (PSM) each rely on one airline for over 80% of passengers.

Next steps: I can pull full profiles for Boston, Burlington and Portland, or check whether Boston's delays are rising.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years); FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, Passenger-side score, Flight-side score, How full the planes are, FAA forecast passenger growth, System delay rate; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - 1 of the 10 listed airports has weaker data (PSM: small delay sample); MVY: small airport forecast; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: ORH: single_airline, MVY: small_airport_forecast, PSM: small_sample, PSM: single_airline, PSM: small_airport_forecast

## A2 - Compare LA and Santa Ana airport congestion levels.

*Pass when:* LAX vs SNA side by side, a clear verdict, Santa Ana's legal cap flagged.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "LA"}; `find_airport` {"query": "Santa Ana"}; `compare_airports` {"airport_codes": ["LAX", "SNA"]}

I've taken "LA" to mean Los Angeles International (LAX). The LA area also has Ontario (ONT), Hollywood Burbank (BUR) and Long Beach (LGB). Santa Ana is John Wayne/Orange County (SNA).

**LAX is somewhat more congested than SNA on every delay measure, but the gap is small.** The big difference is that SNA's growth is limited by a legal cap, not by its airfield.

| Measure | LAX | SNA | Gap |
|---|---|---|---|
| System delay rate, 3 years (2023-08 to 2026-07) | 4.8% | 3.9% | +0.9 pts (1.23x) |
| System delay rate, latest 12 months | 5.0% | 4.3% | +0.7 pts |
| Overall delay rate (15+ min, any cause), 3 years | 18.9% | 17.5% | +1.4 pts |
| System share of all delays | 25.7% | 22.4% | |
| Flight-side score (0-100) | 80.5 | 58.7 | +21.8 |

**What the numbers measure:** The system delay rate is the share of arriving flights delayed by the airport and air-traffic system. It's our closest measure of congestion, but airlines assign the category and it includes ordinary weather, so it isn't purely congestion. At both airports, most delays come from the airlines themselves or from late-arriving aircraft, not from the system. Neither airport is flagged as strained.

**Warnings that change the picture:**
- **SNA has a legal cap.** A settlement agreement limits its passengers and daily departures, and there is a night curfew. In our departing-passenger units the cap is roughly 6.1-6.25 million a year. SNA carried 5,590,354 in the latest 12 months, so it's already close. Its low congestion doesn't mean there's room to grow.
- **LAX's seat capacity was cut.** Seats are down 12.8% since 2019 and passengers down 15.7%. Its fairly full planes (82.1% of seats filled) reflect fewer seats, not rising demand.

The higher system delay rate in the latest 12 months at both airports is a single-year figure, so I wouldn't call it a trend. If useful, I can check the month-by-month pattern next.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, Flight-side score, How full the planes are, System delay rate; 'LA' was taken to mean LAX; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - LAX: capacity cut; SNA: legal limit; the answer uses proxy measures (scores, system delay rate, load factor or forecasts); an airport name was resolved by default
> Warnings printed: SNA: legal_limit, LAX: capacity_cut

## A6 - And how did congestion at those two look in 2023?

*Pass when:* Uses the same two airports without being told again, and 2023 values.

*Result:* PASS

*Tool calls:* `compare_airports` {"airport_codes": ["LAX", "SNA"], "year": 2023}

**In calendar 2023, LAX was again more congested than SNA, and the gap was a bit wider than it is now.**

| Calendar 2023 | LAX | SNA | Gap (LAX minus SNA) |
|---|---|---|---|
| System delay rate | 5.6% | 4.2% | +1.4 pts (1.33x) |
| Overall delay rate (15+ min, any cause) | 20.5% | 18.5% | +2.0 pts (1.11x) |
| Arriving flights in the delay data | 195,617 | 45,732 | |

The system delay rate is the share of arriving flights delayed by the airport and air-traffic system. Airlines assign that category and it includes ordinary weather, so it's mostly, not purely, a measure of congestion. Both years have a full 12 months of delay data.

**Compared with today:**
- **LAX:** Its 2023 system delay rate (5.6%) was higher than in the latest 12 months (5.0%), so it's somewhat less congested than in 2023.
- **SNA:** Its 2023 rate (4.2%) was about the same as now (4.3%).
- **The gap:** It has narrowed, mainly because LAX improved.

Two cautions:
- The current three-year delay figures cover August 2023 to July 2026, so they include the end of 2023. They aren't fully separate from this year view.
- The capacity-need score exists only for the latest period, so I can't give 2023 scores.

The present-day warnings still matter here. LAX has fewer seats than in 2019, and SNA is close to its legal passenger cap and has a night curfew. In both cases, less congestion doesn't on its own mean there's room to grow.

If useful, I can pull the month-by-month system delay series for either airport to see when the changes happened.

> Data period: BTS T-100 airport-month summary, calendar 2023; BTS Airline Delay Causes, calendar 2023; BTS T-100 Segment, calendar 2023  
> Assumptions: proxies, not direct measurements: System delay rate  
> Confidence: Medium - LAX: capacity cut; SNA: legal limit; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: SNA: legal_limit, LAX: capacity_cut

## A3 - What is the percentage of long haul flights out of Anchorage airport?

*Pass when:* One number, the 3,000-mile definition stated, the cargo-included number next to it.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Anchorage airport"}; `airport_profile` {"airport_code": "ANC"}

At Ted Stevens Anchorage International (ANC), **2.8% of departing passenger flights were long-haul in 2025**, using our default cutoff of 3,000 miles or more. If you count cargo flights too, the share rises to **31.0%**.

I took "Anchorage airport" to mean ANC. The only other airport in Anchorage in our data is Merrill Field (MRI), which is much smaller and has partial data.

There is no official definition of long-haul, so here is the share at three cutoffs. It counts departing flights in calendar 2025, domestic and international:

| Cutoff | Share of passenger flights | Share of all flights, cargo included |
|---|---|---|
| 2,000+ miles | 13.7% (5,239 flights) | 47.4% (41,732 flights) |
| 2,500+ miles | 9.8% (3,723 flights) | 43.2% (37,969 flights) |
| 3,000+ miles | 2.8% (1,061 flights) | 31.0% (27,305 flights) |

**Why the two shares differ so much:** cargo makes up 56.6% of ANC's departures (49,838 of 87,988 flights in 2025). Most of the long-haul flying is cargo, not passengers. Passenger traffic is 98.6% domestic, and Alaska Airlines carries 61.4% of passengers.

**What this means for capacity:** cargo flights use the same runways as passenger flights. They are not in the capacity-need score, but the FAA's forecast of flight growth includes them. So at ANC, the flight-side figures depend heavily on cargo, not on passenger demand. For context, ANC scores 59.1 (rank 15 of 34 medium hubs). The flight side scores well above the passenger side (75.3 vs 42.9).

I can rerun this with a different cutoff, or compare ANC's long-haul and cargo shares with other airports.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; FAA passenger boarding data CY2025, calendar 2025; BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, Passenger-side score, Flight-side score, FAA forecast passenger growth, FAA forecast flight growth; long-haul means 3,000 miles or more (our definition; adjustable); 'Anchorage airport' was taken to mean ANC; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - ANC: cargo heavy; the answer uses proxy measures (scores, system delay rate, load factor or forecasts); an airport name was resolved by default
> Warnings printed: ANC: cargo_heavy

## A7 - What if long-haul means over 2,300 miles?

*Pass when:* Recomputed at 2,300 miles for Anchorage.

*Result:* PASS

*Tool calls:* `airport_profile` {"airport_code": "ANC", "long_haul_miles": 2300}

With a 2,300-mile cutoff, **12.6% of passenger flights departing Anchorage (ANC) in 2025 were long-haul** (4,820 flights). With cargo flights included, the share is **46.5%** (40,947 flights).

The tool counts flights of *at least* the cutoff distance, so a flight of exactly 2,300 miles counts as long-haul here. That should make little or no difference to your "over 2,300 miles" definition.

| Cutoff | Share of passenger flights | Share of all flights, cargo included |
|---|---|---|
| 2,000+ miles | 13.7% | 47.4% |
| **2,300+ miles** | **12.6%** | **46.5%** |
| 2,500+ miles | 9.8% | 43.2% |
| 3,000+ miles | 2.8% | 31.0% |

**What the numbers show:**
- **The share hardly moves between 2,000 and 2,300 miles.** Very few ANC passenger flights fall in that distance band.
- **The big drop comes between 2,500 and 3,000 miles.** Many passenger flights fall in that band, so where you set the cutoff around there changes the answer a lot.
- **Cargo dominates long-haul at ANC.** Cargo is 56.6% of all departures, and the share with cargo included stays far above the passenger-only share at every cutoff.

If you'd like, I can compare ANC with other airports on the long-haul measure. A ranking only uses our default 3,000-mile cutoff for passenger flights. For a few named airports, I can look up each one at 2,300 miles.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); BTS T-100 Segment, calendar 2025  
> Assumptions: long-haul means 2,300 miles or more (our definition; adjustable)  
> Confidence: Medium - ANC: cargo heavy
> Warnings printed: ANC: cargo_heavy

## A4 - What is the unmet flight demand in SFO airport and why?

*Pass when:* An estimate named as an estimate or proxy, with the why from the delay data.

*Result:* PASS

*Tool calls:* `airport_profile` {"airport_code": "SFO"}

San Francisco International (SFO) has an estimated **108,307 extra takeoffs and landings a year of unmet flight demand by 2035**. That is the FAA forecast growth from 406,220 operations in fiscal 2025 to 514,527 in fiscal 2035 (+26.7%). This is an estimate, not a measurement. It counts takeoffs plus landings, including cargo, and the FAA tends to over-forecast. We only call it "unmet" because SFO is already strained today.

**Why it counts as unmet:**
- **Most congested airport in the dataset.** SFO's system delay rate over the last three years is 13.4%, the highest among the 343 full-data airports. These are arrival delays that airlines blame on the airport and air-traffic system. Airlines code this category themselves, and it includes ordinary weather. Counting all causes, 27.4% of arrivals were late.
- **The airfield is the main cause.** 48.9% of delayed flights were blamed on the system. Airline causes were 24.7%, late-arriving aircraft 23.7%, and extreme weather only 2.5%.
- **The latest 12 months (17.3%) are a recent spike, not a steady trend.** From 2026-04 to 2026-07 the system delay rate was 30.0%, compared with 7.8% in the same months a year earlier and 10.3% in the other months. A temporary cause, such as runway work, is possible but isn't in our data.

**Warnings that change the picture:**
- **Capacity was cut.** Seats are down 5.0% since 2019 and passenger flights are down 11.0%, while passengers are down 4.4%. So the full planes (82.6% of seats filled) partly reflect fewer seats, not rising demand.
- **Schedules are coordinated.** SFO is FAA Level 2 schedule facilitation, which is not a hard cap.
- **One airline dominates.** United carries 44.8% of passengers.

Background (not from our data): SFO's closely spaced parallel runways lose arrival capacity in low clouds and fog, which helps explain why so many delays are coded to the system.

It's worth checking what caused the 2026 spike and whether any airfield projects are already planned.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: How full the planes are, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; 'unmet flight demand' is an estimate from the FAA forecast, used only when the airport is strained today  
> Confidence: Medium - SFO: capacity cut; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: SFO: capacity_cut

## A5 - How does that compare with Oakland?

*Pass when:* Oakland is not called unmet demand, because it is not strained.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Oakland"}; `compare_airports` {"airport_codes": ["SFO", "OAK"]}; `airport_profile` {"airport_code": "OAK"}

Oakland (OAK) has no unmet flight demand by our definition, because it isn't strained. The FAA forecasts 30,637 more takeoffs and landings a year there by 2035 (+24.8%), but this is only forecast growth: the airport looks able to absorb it. SFO's 108,307 counts as unmet demand because SFO is congested; that figure is 3.54 times Oakland's. I assumed you meant Oakland San Francisco Bay. The Bay Area also has San Jose (SJC).

| | SFO | OAK |
|---|---|---|
| Capacity-need score (0-100) | 86.9 (#3 of 343) | 46.0 (#208) |
| Flight-side score | 97.1 | 49.7 |
| System delay rate, 3 years | 13.4% | 2.3% |
| System delay rate, latest 12 months | 17.3% (recent spike) | 1.7% (no spike) |
| Overall delay rate | 27.4% | 18.4% |
| System share of delayed flights | 48.9% | 12.3% |
| Seats filled | 82.6% | 74.2% |
| Passengers vs 2019 | -4.4% | -35.5% |

**Why Oakland isn't strained:** its system delay rate is low, 2.3% over three years. The system category covers the airport and air-traffic system; airlines code it, and it includes ordinary weather. Most of Oakland's delays are caused by airlines themselves: 54.1% of delayed flights were waiting for a late incoming aircraft and 32.5% were airline causes.

**Warnings for Oakland:**
- **Lost traffic:** seats are down 31.5% and passengers down 35.5% since 2019, and planes are only 74.2% full.
- **One airline dominates:** Southwest carries 76.7% of passengers, so the forecast growth depends on Southwest's plans.
- **Cargo:** 17.9% of departing flights are cargo, and the FAA forecast includes cargo flights.

Background (not from our data): airlines have shifted Bay Area service toward SFO since the pandemic, which fits Oakland's drop in traffic.

I can add San Jose (SJC) to complete the Bay Area picture if that would help.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, Flight-side score, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; 'unmet flight demand' is an estimate from the FAA forecast, used only when the airport is strained today; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - SFO: capacity cut; OAK: capacity cut; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: SFO: capacity_cut, OAK: single_airline, OAK: capacity_cut
