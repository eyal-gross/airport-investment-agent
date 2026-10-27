# Evaluation run - 2026-10-04 19:27 - claude-opus-5-5

**25 of 26 questions passed.** 802 numbers appeared in the answers; 0 answers ended with a number that could not be traced to a tool result; 2 answers passed only after one automatic rewrite. Average 12.2s per question; 737,660 input and 26,435 output tokens in total.

| Id | Group | Result | Tools | Number check | Seconds |
|---|---|---|---|---|---|
| A1 | core | PASS | rank_airports | passed | 13.7 |
| A2 | core | PASS | find_airport, find_airport, compare_airports | passed | 12.1 |
| A6 | follow-up | PASS | compare_airports | passed | 9.4 |
| A3 | core | PASS | find_airport, airport_profile | passed | 9.2 |
| A7 | follow-up | PASS | airport_profile | passed | 7.8 |
| A4 | core | PASS | airport_profile | passed | 10.2 |
| A5 | follow-up | PASS | find_airport, compare_airports, airport_profile | passed | 12.6 |
| A8 | follow-up | PASS | find_airport, airport_profile | passed | 15.6 |
| B1 | filters | PASS | rank_airports | rewritten | 18.2 |
| B2 | filters | PASS | rank_airports | passed | 10.9 |
| B3 | filters | PASS | rank_airports, rank_airports | passed | 12.0 |
| B4 | ambiguous | PASS | find_airport, find_airport | passed | 5.7 |
| B5 | filters | PASS | rank_airports | passed | 10.9 |
| B6 | time | PASS | find_airport, airport_profile | passed | 11.9 |
| B7 | filters | PASS | rank_airports | passed | 11.2 |
| B8 | time | PASS | find_airport, airport_trend, airport_trend, airport_profile | rewritten | 18.9 |
| C1 | time | PASS | rank_airports | passed | 12.7 |
| C9 | time | PASS | rank_airports, rank_airports | passed | 13.8 |
| C10 | time | PASS | rank_airports, rank_airports | passed | 12.6 |
| C2 | out of scope | PASS | rank_airports, airport_profile, airport_profile, airport_profile, airport_profile | passed | 16.0 |
| C3 | out of scope | PASS | airport_profile | passed | 10.8 |
| C4 | out of scope | PASS | find_airport | passed | 6.4 |
| C5 | out of scope | PASS | rank_airports, rank_airports | passed | 14.1 |
| C6 | judgment | FAIL | find_airport, airport_profile | passed | 14.9 |
| C7 | out of scope | PASS | find_airport | passed | 10.2 |
| C8 | awkward data | PASS | find_airport, find_airport, airport_profile | passed | 14.8 |

## A1 - Which airports in New England are strong candidates for terminal expansion?

*Pass when:* A ranked list from the six states, scores shown, reasons given.

*Result:* PASS

*Tool calls:* `rank_airports` {"region": "new england", "limit": 10}

**The strongest New England candidates are Boston Logan (BOS), Burlington (BTV), Portland, Maine (PWM) and Bangor (BGR).** They rank 1-4 of the region's 12 airports with full data. For a terminal specifically, PWM and BGR have the strongest passenger-side evidence. BOS ranks first mainly because of airfield delays, which a terminal alone may not fix.

| Airport | Size class | Score | Passenger side | Flight side | Planes full | Passengers vs 2019 | FAA forecast passengers |
|---|---|---|---|---|---|---|---|
| Boston (BOS) | large | 82.9 | 72.2 | 93.6 | 81.7% | +1.2% | +26.5% |
| Burlington (BTV) | small | 79.2 | 73.7 | 84.8 | 83.0% | +2.3% | +22.9% |
| Portland (PWM) | small | 77.4 | 79.2 | 75.6 | 82.8% | +17.2% | +21.6% |
| Bangor (BGR) | nonhub | 71.8 | 78.0 | 65.5 | 80.4% | +40.8% | +24.1% |
| Hartford (BDL) | medium | 65.9 | 60.8 | 71.0 | 81.3% | -2.7% | +15.7% |

- **BOS:** Its 9.1% system delay rate points to a strained airfield more than a crowded terminal. Passenger numbers are almost flat since 2019. Its forecast gain is the largest in absolute terms: 5,612,088 extra yearly boardings by 2035.
- **PWM:** Real growth, and seats are up 21.6% since 2019. It is also flagged as having flat flight counts while passengers rise, which suggests demand is being absorbed by fuller or larger planes.
- **BGR:** The fastest growth, with seats up 48.8%. It is small, though: 437,108 boardings in 2025.
- **BTV:** Planes are the fullest in the region, but growth since 2019 is modest. It is flagged as strained.

**Caveats:**
- No public data measures terminal or gate use, so "terminal need" here is inferred from how full the planes are, passenger growth and the FAA forecast.
- The system delay category is coded by airlines and includes ordinary weather.
- The score measures upside, not cost or return.
- Four airports have only partial data and are left out of the ranking: Tweed-New Haven (HVN), Cape Cod Gateway (HYA), Block Island (BID) and Westerly (WST).

I can pull full profiles or a side-by-side comparison of PWM, BGR and BTV next.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years); FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, Passenger-side score, Flight-side score, How full the planes are, FAA forecast passenger growth, System delay rate; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - 1 of the 10 listed airports has weaker data (PSM: small delay sample); MVY: small airport forecast; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: ORH: single_airline, MVY: small_airport_forecast, PSM: small_sample, PSM: single_airline, PSM: small_airport_forecast

## A2 - Compare LA and Santa Ana airport congestion levels.

*Pass when:* LAX vs SNA side by side, a clear verdict, Santa Ana's legal cap flagged.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "LA"}; `find_airport` {"query": "Santa Ana"}; `compare_airports` {"airport_codes": ["LAX", "SNA"]}

Los Angeles International (LAX) is more congested than John Wayne/Orange County in Santa Ana (SNA), but only slightly. On every delay measure, LAX is a little higher. By "LA" I assumed LAX. The metro area also has Ontario (ONT), Hollywood Burbank (BUR) and Long Beach (LGB).

| Measure | LAX | SNA | Difference |
|---|---|---|---|
| System delay rate, three years (2023-08 to 2026-07) | 4.8% | 3.9% | +0.9 pts (1.23x) |
| System delay rate, latest 12 months | 5.0% | 4.3% | +0.7 pts (1.16x) |
| Overall delay rate (15+ min late, any cause) | 18.9% | 17.5% | +1.4 pts (1.08x) |
| Delays blamed on the system | 25.7% | 22.4% | - |
| Delays from a late incoming plane | 33.4% | 39.9% | - |

**What these measure:** The system delay rate is the share of arriving flights delayed by the airport and air-traffic system. It's our best proxy for airfield congestion, but airlines assign the delay cause and the category includes ordinary weather, so it's mostly congestion rather than purely congestion. At both airports, most delays come from airline operations and late incoming planes, not the system.

**Recent year:** Both airports' latest 12-month system delay rates are above their three-year averages. I haven't checked whether that's a short spike or a lasting change, so don't read it as "getting worse" yet.

**Warnings that change the conclusion:**
- **SNA has a legal cap:** about 6.1-6.25 million departing passengers a year, a daily departure limit and a night curfew. Its latest 12 months are 5,590,354 passengers, so it's already close to the cap. Low delays there may partly reflect the cap rather than spare room.
- **LAX cut capacity:** seats are down 12.8% since 2019 and passengers down 15.7%, so its full planes don't mean demand is rising.

Neither airport is flagged as strained today.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: How full the planes are, System delay rate; 'LA' was taken to mean LAX  
> Confidence: Medium - LAX: capacity cut; SNA: legal limit; the answer uses proxy measures (scores, system delay rate, load factor or forecasts); an airport name was resolved by default
> Warnings printed: SNA: legal_limit, LAX: capacity_cut

## A6 - And how did congestion at those two look in 2023?

*Pass when:* Uses the same two airports without being told again, and 2023 values.

*Result:* PASS

*Tool calls:* `compare_airports` {"airport_codes": ["LAX", "SNA"], "year": 2023}

In calendar 2023, LAX was again more congested than SNA, and the gap was a bit wider than it is now. Both airports had higher delay rates in 2023 than in the latest 12 months.

| Calendar 2023 | LAX | SNA | Difference |
|---|---|---|---|
| System delay rate | 5.6% | 4.2% | +1.4 pts (1.33x) |
| Overall delay rate (15+ min late, any cause) | 20.5% | 18.5% | +2.0 pts (1.11x) |
| Arriving flights in the delay data | 195,617 | 45,732 | - |

**Compared with now:**
- LAX's system delay rate went from 5.6% in 2023 to 5.0% in the latest 12 months (2025-08 to 2026-07). SNA's went from 4.2% to 4.3%, about flat.
- Overall delay rates were also higher in 2023: LAX 20.5% and SNA 18.5%, against 18.9% and 17.5% over the latest three years.
- So the latest-12-month figures I flagged earlier don't show a rise from 2023 levels. LAX has eased and SNA has held steady.

**Things to keep in mind:**
- The system delay category is assigned by airlines and includes ordinary weather. It's a proxy for congestion, not a pure measure of it.
- It only covers domestic flights on the larger reporting airlines.
- The three-year window used for the score starts in August 2023, so it overlaps 2023 by five months.
- Scores only exist for the latest period, so I can't give a 2023 capacity-need score. These are raw rates only.

If you want, I can pull the month-by-month system delay series for either airport to show when the drop happened.

> Data period: BTS T-100 airport-month summary, calendar 2023; BTS Airline Delay Causes, calendar 2023; BTS T-100 Segment, calendar 2023  
> Assumptions: proxies, not direct measurements: System delay rate  
> Confidence: Medium - LAX: capacity cut; SNA: legal limit; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: SNA: legal_limit, LAX: capacity_cut

## A3 - What is the percentage of long haul flights out of Anchorage airport?

*Pass when:* One number, the 3,000-mile definition stated, the cargo-included number next to it.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Anchorage airport"}; `airport_profile` {"airport_code": "ANC"}

At Ted Stevens Anchorage International (ANC), **2.8% of departing passenger flights were long-haul in 2025**, using our default cutoff of 3,000 miles or more. If you count cargo flights too, the share is **31.0%**. The gap is large because ANC is a major cargo hub.

I assumed you meant ANC. The only other covered airport in Anchorage is Merrill Field (MRI), a much smaller non-hub airport with only partial data.

There's no official definition of long-haul, so here are the shares at three cutoffs. They count departing flights in calendar 2025, domestic and international, across all airlines:

| Cutoff | Passenger flights | All flights incl. cargo |
|---|---|---|
| 2,000+ miles | 13.7% (5,239 flights) | 47.4% (41,732 flights) |
| 2,500+ miles | 9.8% (3,723 flights) | 43.2% (37,969 flights) |
| 3,000+ miles | 2.8% (1,061 flights) | 31.0% (27,305 flights) |

The totals behind these shares are 38,150 passenger departures and 87,988 departures including cargo.

**Why this matters:** Cargo makes up 56.6% of departing flights at ANC. Cargo flights use the same runways as passenger flights but aren't in the capacity-need score. Passenger traffic is mostly domestic (98.6% of passengers).

Background (not from our data): Anchorage is a common refuelling and transfer stop for cargo flights between Asia and North America. That explains why so many of its long-haul flights carry freight rather than passengers.

I can also show ANC's capacity-need score and delay picture, or rank other airports by long-haul share.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); FAA passenger boarding data CY2025, calendar 2025; BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score; long-haul means 3,000 miles or more (our definition; adjustable); 'Anchorage airport' was taken to mean ANC; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - ANC: cargo heavy; the answer uses proxy measures (scores, system delay rate, load factor or forecasts); an airport name was resolved by default
> Warnings printed: ANC: cargo_heavy

## A7 - What if long-haul means over 2,300 miles?

*Pass when:* Recomputed at 2,300 miles for Anchorage.

*Result:* PASS

*Tool calls:* `airport_profile` {"airport_code": "ANC", "long_haul_miles": 2300}

If long-haul means 2,300 miles or more, **12.6% of passenger flights leaving Anchorage (ANC) in 2025 were long-haul (4,820 flights)**. Counting cargo flights too, the share is **46.5% (40,947 flights)**.

The tool counts flights of at least the cutoff distance, so a flight of exactly 2,300 miles is included. That's very unlikely to change the result.

| Cutoff | Passenger flights | All flights incl. cargo |
|---|---|---|
| 2,000+ miles | 13.7% | 47.4% |
| **2,300+ miles** | **12.6%** | **46.5%** |
| 2,500+ miles | 9.8% | 43.2% |
| 3,000+ miles | 2.8% | 31.0% |

**What this shows:**
- **The 3,000-mile cutoff is where the passenger share drops sharply.** At 2,300 miles the share is close to the 2,000-mile figure. Above 3,000 miles it falls to 2.8%. So many of ANC's longer passenger flights are between about 2,300 and 3,000 miles.
- **Cargo dominates long-haul traffic at every cutoff.** Cargo makes up 56.6% of departing flights, and at 2,300 miles it accounts for most of the long-haul flights.

Background (not from our data): Many of ANC's longer passenger flights probably go to the Lower 48 states, which are mostly at this kind of distance from Anchorage. Our data doesn't include routes or destinations, so I can't confirm which ones.

I can rank other airports by long-haul share for comparison. That ranking uses our default 3,000-mile cutoff.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); BTS T-100 Segment, calendar 2025  
> Assumptions: long-haul means 2,300 miles or more (our definition; adjustable)  
> Confidence: Medium - ANC: cargo heavy
> Warnings printed: ANC: cargo_heavy

## A4 - What is the unmet flight demand in SFO airport and why?

*Pass when:* An estimate named as an estimate or proxy, with the why from the delay data.

*Result:* PASS

*Tool calls:* `airport_profile` {"airport_code": "SFO"}

San Francisco International (SFO) has an estimated **108,307 extra takeoffs and landings a year** of unmet flight demand by fiscal 2035. That is the FAA forecast rising from 406,220 to 514,527 operations, or +26.7%. We call it "unmet" only because SFO is already strained today. Its system delay rate is the highest among the 343 full-data airports, so the airport is unlikely to absorb that growth as it is. This is an estimate, not a measurement. The figures count takeoffs plus landings and include cargo, and the FAA tends to over-forecast.

**Why it counts as unmet**
- **System delay rate: 13.4%** of arriving flights over three years. These are delays the airlines attribute to the airport and air-traffic system. Airlines code this category themselves, and it includes ordinary weather, so it mostly measures congestion but not only congestion.
- **System causes are the biggest share of delays:** 48.9% of delayed flights, against 24.7% for airline causes, 23.7% for late aircraft and 2.5% for extreme weather.
- **Overall delay rate: 27.4%** of arrivals were 15 or more minutes late, from any cause.

**What to watch**
- **The latest-year system delay rate (17.3%) is driven by a recent spike, not a steady trend.** From 2026-04 to 2026-07 it was 30.0%, against 7.8% in the same months a year earlier and 10.3% in the other months of the latest year. The cause could be temporary, and our data doesn't show it.
- **Capacity was cut.** Seats are down 5.0% since 2019 and passenger flights down 11.0%. Planes are 82.6% full, but that partly reflects fewer seats rather than rising demand.
- **There is no hard legal cap.** SFO is under FAA Level 2 schedule facilitation, which means schedules are coordinated but not capped.

Background (not from our data): SFO's closely spaced parallel runways lose capacity in low clouds and fog, which helps explain why system delays are so high there.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: FAA forecast passenger growth, System delay rate, FAA forecast flight growth; 'unmet flight demand' is an estimate from the FAA forecast, used only when the airport is strained today  
> Confidence: Medium - SFO: capacity cut; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: SFO: capacity_cut

## A5 - How does that compare with Oakland?

*Pass when:* Oakland is not called unmet demand, because it is not strained.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Oakland"}; `compare_airports` {"airport_codes": ["SFO", "OAK"]}; `airport_profile` {"airport_code": "OAK"}

I took Oakland to mean Oakland San Francisco Bay (OAK). The same metro area also has San Jose (SJC), as well as SFO.

**Oakland doesn't count as having unmet flight demand.** The FAA forecasts 30,637 more takeoffs and landings a year there by 2035 (+24.8%), but we call that "forecast flight growth", not unmet demand, because Oakland isn't strained today. SFO has 3.54 times as much forecast growth (108,307), and it is strained.

| | SFO | OAK |
|---|---|---|
| Capacity-need score | 86.9 (rank 3 of 343) | 46.0 (rank 208 of 343) |
| Flight-side score | 97.1 | 49.7 |
| System delay rate, 3 years | 13.4% | 2.3% |
| System delay rate, latest 12 months | 17.3% | 1.7% |
| Overall delay rate | 27.4% | 18.4% |
| System causes' share of delays | 48.9% | 12.3% |
| How full the planes are | 82.6% | 74.2% |
| Passenger growth since 2019 | -4.4% | -35.5% |
| FAA forecast flight growth | 26.7% | 24.8% |

**Why the two differ**
- **Oakland's delays aren't about airport capacity.** Most of its delays are blamed on late-arriving aircraft (54.1%) and the airlines themselves (32.5%), not on the airport and air-traffic system. Its system delay rate is steady, with no recent spike.
- **Oakland has spare room because it shrank.** Seats are down 31.5% since 2019 and passenger flights down 32.2%. So its forecast growth could likely use the space it already has.

**Risks specific to Oakland**
- **One airline dominates.** Southwest carries 76.7% of passengers, so the forecast growth depends on that one airline's plans.
- **Cargo is a big share of traffic.** 17.9% of departing flights are cargo, against 1.2% at SFO. Cargo uses the runways but isn't in the score.

Background (not from our data): Oakland and SFO share the Bay Area's airspace, so traffic that can't fit at SFO could in principle shift to Oakland.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, Flight-side score, How full the planes are, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; 'unmet flight demand' is an estimate from the FAA forecast, used only when the airport is strained today; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - SFO: capacity cut; OAK: capacity cut; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: SFO: capacity_cut, OAK: single_airline, OAK: capacity_cut

## A8 - Is Memphis a good candidate, given its cargo traffic?

*Pass when:* Uses the Memphis profile and the cargo share.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Memphis"}; `airport_profile` {"airport_code": "MEM"}

**Memphis (MEM) is a middling candidate for passenger capacity, and its cargo traffic makes it look better than it is.** Its capacity-need score is 59.5. That ranks 46th of 78 small hubs (the FAA "small hub" size class) and 116th of 343 ranked airports. The score comes almost entirely from the flight side. Cargo is 65.1% of departing flights, and the FAA flight forecast counts those cargo flights.

**Flight side: strong, but driven by cargo (73.7)**
- The FAA forecasts 18.4% more takeoffs and landings by 2035, about 29,629 extra a year. Cargo is included in that number.
- 4.9% of arriving flights had system delays over three years (5.1% in the latest 12 months). Airlines code this delay category themselves, and it includes ordinary weather. The rate is not high enough to count as "strained," so the forecast growth is not unmet demand.
- Only 21.4% of delayed flights blame the airport and air-traffic system. Late aircraft (39.4%) and airline causes (35.3%) are bigger. So delays point to airline operations more than a shortage of airfield space.
- The overall delay rate is 22.7%, and there is no recent spike.

**Passenger side: weak (45.4)**
- Planes are 73.4% full, which puts Memphis in the bottom third. That's down from 77.6% in 2019 and 70.2% so far in 2026.
- Passengers are up just 0.9% since 2019, while seats are up 6.7%. Seats are growing faster than passengers.
- The FAA forecasts 25.8% passenger growth (about 609,000 more boardings a year), which is one bright spot. The FAA tends to over-forecast, though.

Background (not from our data): Memphis is FedEx's main global hub, so any extra airfield capacity would mostly serve one cargo operator.

**What to check next:** how much of the forecast flight growth is cargo, and how much of any project is airfield work versus terminal work. Gate use and project costs aren't in our data. I can also compare Memphis with small hubs that score higher on passenger demand if that would help.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); FAA passenger boarding data CY2025, calendar 2025; BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, Passenger-side score, Flight-side score, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; 'unmet flight demand' is an estimate from the FAA forecast, used only when the airport is strained today; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - MEM: cargo heavy; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: MEM: cargo_heavy

## B1 - Score the top 3 airports that have the highest congestion in the US, only small airports.

*Pass when:* Small-hub class, sorted by the system delay rate, three airports with scores; says what 'small' means.

*Result:* PASS

*Tool calls:* `rank_airports` {"size_classes": ["small"], "sort_by": "system_delay_rate_pct", "limit": 3}

Among FAA small-hub airports, the three most congested are Punta Gorda (PGD), Key West (EYW) and St. Thomas (STT). Punta Gorda is far ahead on capacity-need score: 94.9, the highest of all 343 ranked airports.

Here, congestion means the **system delay rate**. That's the share of arriving flights delayed by the airport and air-traffic system, measured over three years (2023-08 to 2026-07). Airlines decide which delays go in this category, and it includes ordinary weather, so it mostly reflects congestion but not only that.

| Rank | Airport | System delay rate | Capacity-need score (0-100) | Passenger side | Flight side | Rank among small hubs (of 78) |
|---|---|---|---|---|---|---|
| 1 | Punta Gorda (PGD), FL | 8.6% | 94.9 | 93.3 | 96.5 | 1 |
| 2 | Key West International (EYW), FL | 8.0% | 67.7 | 64.2 | 71.2 | 32 |
| 3 | Cyril E King (STT), St. Thomas, VI | 7.9% | 70.8 | 62.3 | 79.3 | 26 |

**What stands out:**
- **Punta Gorda** scores high on every input. Planes are 85.8% full (passengers divided by seats). Passengers are up 37.0% since 2019, and the FAA forecasts growth of 30.0% in passengers and 26.8% in flights by 2035. **Warning:** Allegiant Air carries 99.6% of its passengers, so future demand depends on one airline's plans.
- **Key West** has the most passenger growth since 2019 (55.9%), but planes are less full (77.3%) and the FAA forecasts only 9.3% flight growth. That holds its score down.
- **St. Thomas** is in a US territory. If you meant US states only, it would drop out and the next airport would move up. I can pull that list.

One small hub, Tweed/New Haven (HVN), was left out because its data is incomplete.

If you want to go further, I can check whether delays at these airports are rising in the latest 12 months or whether that's a recent spike.

> Data period: BTS Airline Delay Causes, 2023-08 to 2026-07 (three years); BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: System delay rate, Capacity-need score, Passenger-side score, Flight-side score, FAA forecast passenger growth, FAA forecast flight growth; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: PGD: single_airline

## B2 - Top 5 airports in Texas by how full the planes are.

*Pass when:* Five Texas airports by load factor.

*Result:* PASS

*Tool calls:* `rank_airports` {"states": ["TX"], "sort_by": "load_factor_pct", "limit": 5}

Dallas-Fort Worth (DFW) and McAllen (MFE) have the fullest planes in Texas. Both fill 82.5% of seats, followed by Houston Bush (IAH), Abilene (ABI) and Corpus Christi (CRP). This compares all 25 Texas airports with full data, and none were left out.

"How full" here means passengers divided by seats on departing flights over the latest 12 months. It's not the official load factor, which uses passenger-miles. It's also the weakest of the five scored metrics, because airline pricing and choice of aircraft affect it.

| # | Airport | Size class | Seats filled | Capacity-need score | Rank among all 343 ranked airports |
|---|---|---|---|---|---|
| 1 (tie) | Dallas-Fort Worth (DFW) | large | 82.5% | 79.3 | 17 |
| 1 (tie) | McAllen (MFE) | small | 82.5% | 44.5 | 221 |
| 3 | Houston Bush (IAH) | large | 79.9% | 70.4 | 65 |
| 4 | Abilene (ABI) | nonhub | 79.5% | 78.1 | 26 |
| 5 | Corpus Christi (CRP) | nonhub | 76.6% | 38.0 | 246 |

**What changes the picture:**
- **Full planes don't always mean a high score.** McAllen and Corpus Christi have full planes but low overall scores. The FAA forecasts flat or falling flight numbers there (-9.8% at MFE, 0.3% at CRP), and their system delay rates are low (about 3%).
- **DFW and IAH are both strained.** Their planes are full, they have the highest system delay rates of the five (6.2% and 6.5%), and their forecast growth is solid. At IAH the number of flights has stayed flat while passengers grew.
- **Abilene depends on one airline.** Envoy Air carries 95.8% of its passengers, so if that airline cuts service, the forecast growth may not arrive. It's also small, with 105,976 boardings in 2025.

The system delay rate counts arrival delays that airlines blame on the airport and air-traffic system. Airlines assign that category themselves, and it includes ordinary weather.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years); FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: How full the planes are, Capacity-need score, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: ABI: single_airline

## B3 - Which large airports have planes over 85% full?

*Pass when:* Large hubs filtered by a load factor threshold; says that none qualifies.

*Result:* PASS

*Tool calls:* `rank_airports` {"size_classes": ["large"], "sort_by": "load_factor_pct", "min_value": 85, "limit": 30}; `rank_airports` {"size_classes": ["large"], "sort_by": "load_factor_pct", "limit": 10}

**None of the 30 large-hub airports has planes over 85% full.** The highest is Newark Liberty (EWR) at 83.2%. The top ten are all between 81% and 84%.

"How full the planes are" means passengers divided by seats on departing flights over the latest 12 months. It's our own measure, not the official load factor, and it's the weakest of the five scored inputs because airline pricing and aircraft choice drive it.

| Airport | Planes full | Capacity-need score | Note |
|---|---|---|---|
| Newark (EWR) | 83.2% | 80.7 | Legal flight cap |
| San Francisco (SFO) | 82.6% | 86.9 | Seats were cut |
| Dallas-Fort Worth (DFW) | 82.5% | 79.3 | |
| Atlanta (ATL) | 82.3% | 69.8 | |
| Los Angeles (LAX) | 82.1% | 75.3 | Seats were cut |
| New York JFK (JFK) | 82.0% | 84.0 | Slot-controlled |
| Orlando (MCO) | 81.9% | 87.8 | |
| Seattle-Tacoma (SEA) | 81.8% | 79.8 | |
| Boston Logan (BOS) | 81.7% | 82.9 | |
| Denver (DEN) | 81.2% | 76.7 | |

**Warnings that affect what these numbers mean:**
- **Seats cut at SFO and LAX:** Both have fewer seats than in 2019 (-5.0% and -12.8%). Their full planes come from reduced capacity, not rising demand.
- **Legal limits at EWR and JFK:** Newark has a cap of 36 arrivals and 36 departures an hour, and JFK is slot-controlled. New runways or gates there couldn't be used without more slots.
- **Strongest full-plane cases without a warning:** DFW, Orlando and Denver. Their planes are about as full as the others, and passengers are up since 2019 (+14.9%, +14.7% and +18.8%).

If it helps, I can lower the cutoff (for example to 82%), run the same 85% check for medium or small hubs, or look at peak-season fullness, such as summer.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: How full the planes are, Capacity-need score; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - the answer uses proxy measures (scores, system delay rate, load factor or forecasts); EWR: legal limit; SFO: capacity cut; LAX: capacity cut
> Warnings printed: EWR: legal_limit, JFK: legal_limit, SFO: capacity_cut, LAX: capacity_cut

## B4 - Compare Portland and Providence.

*Pass when:* Asks which Portland (Oregon or Maine), or covers both and says so.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Portland"}; `find_airport` {"query": "Providence"}

Which Portland do you mean: Portland, Oregon (PDX) or Portland, Maine (PWM)?

For Providence, I'll use Rhode Island T.F. Green International (PVD). The same metro area also includes Boston Logan (BOS) and Manchester-Boston Regional (MHT), if you'd rather use one of those.

Both Portlands are in the same FAA small-hub class as PVD, so either one works as a direct comparison. Portland, Maine (PWM) is the closer regional peer. I can also compare all three.

> Data period: no data was used in this reply  
> Assumptions: none  
> Confidence: n/a - no data figures were used in this reply

## B5 - Which airports are the best candidates overall? Only count the ones with complete data.

*Pass when:* National ranking shown per size class.

*Result:* PASS

*Tool calls:* `rank_airports` {"sort_by": "total_score"}

Among the 343 airports with complete data, the top candidates are **Orlando International (MCO)** among large hubs, **Southwest Florida International (RSW)** among medium hubs, **Punta Gorda (PGD)** among small hubs (it is also #1 nationally) and **Rickenbacker (LCK)** among nonhubs. I've ranked them within FAA size classes because size isn't part of the score. Without that split, small leisure airports fill the top of the national list.

The score runs from 0 to 100. It estimates how much added capacity would be filled, so it points to upside. It doesn't measure profit.

| Class | Top 5 (score) |
|---|---|
| Large | MCO 87.8, San Francisco (SFO) 86.9, O'Hare (ORD) 84.6, JFK 84.0, Miami (MIA) 83.0 |
| Medium | RSW 81.7, Charleston (CHS) 78.8, Jacksonville (JAX) 75.8, San Juan (SJU) 75.4, Raleigh-Durham (RDU) 73.1 |
| Small hub | PGD 94.9, Northwest Arkansas (XNA) 85.5, Orlando Sanford (SFB) 85.2, St Pete-Clearwater (PIE) 84.1, Provo (PVU) 80.2 |
| Nonhub | LCK 85.7, Traverse City (TVC) 78.8, Abilene (ABI) 78.1, MidAmerica St Louis (BLV) 77.8, Aguadilla (BQN) 77.7 |

**Caveats that change the picture:**
- **Legal limits:** JFK's flight slots are capped by FAA order, and O'Hare has a temporary flight cap for summer 2026. New runways or gates there can't be fully used unless those limits change.
- **SFO and BQN cut capacity:** seats are down since 2019 (SFO -5.0%, BQN -10.2%). Their planes are full because there are fewer seats, not because demand is rising.
- **One airline:** at PGD, SFB, PIE, LCK and BLV, Allegiant carries over 98% of passengers, and at ABI Envoy carries 95.8%. Their growth depends on one airline's plans.
- **Cargo-heavy:** cargo makes up 44.2% of flights at LCK and 42.8% at BQN. Cargo isn't in the score but shares the runways.
- The delay part of the score uses the system delay category, which airlines code themselves and which includes ordinary weather.

On the large-hub list, **MCO and MIA** have high-confidence data and none of these warnings. Among medium hubs, **RSW and CHS** are the clean leaders.

I can profile any of these in more detail, or compare a few side by side.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); BTS Airline Delay Causes, 2023-08 to 2026-07 (three years); FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, System delay rate; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - SFO: capacity cut; ORD: legal limit; JFK: legal limit; LCK: cargo heavy
> Warnings printed: ORD: legal_limit, JFK: legal_limit, SFO: capacity_cut, PGD: single_airline, SFB: single_airline, PIE: single_airline, LCK: cargo_heavy, LCK: single_airline, ABI: single_airline, BLV: single_airline, BQN: cargo_heavy, BQN: capacity_cut

## B6 - How has passenger traffic at Boston changed since 2019? Give me the year by year picture.

*Pass when:* Year by year values for Boston, with 2026 marked partial.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Boston"}; `airport_profile` {"airport_code": "BOS"}

Boston Logan (BOS) is back to its 2019 passenger level but has barely grown past it. The latest 12 months (2025-05 to 2026-04) had 20,983,745 passengers, which is 1.2% above 2019. Traffic peaked in 2024 and dipped slightly in 2025. I took "Boston" to mean Logan. The area also has Manchester-Boston Regional (MHT) and Providence (PVD).

| Year | Passengers | How full the planes were |
|---|---|---|
| 2019 | 20,742,138 | 81.9% |
| 2020 | 6,050,302 | 52.0% |
| 2021 | 10,938,231 | 75.1% |
| 2022 | 17,472,973 | 78.5% |
| 2023 | 19,991,297 | 83.3% |
| 2024 | 21,280,480 | 83.1% |
| 2025 | 21,105,980 | 81.6% |
| 2026 (Jan-Apr only) | 6,139,216 | 78.2% |

These are passengers on departing flights (BTS). Someone who changes planes at Logan is counted on each flight they take. "How full" means passengers divided by seats.

**What's behind the numbers:**
- **Seats and flights:** Seats are up 1.4% on 2019, roughly in step with passengers. Passenger flights in 2025 were down 3.1% from 2019, but each flight carried more people (111.9 per flight, against 106.4 in 2019). So the growth came from bigger or fuller planes, not more departures.
- **2026:** Only four months of data so far, so don't compare it with full years.
- **Delays:** Delays caused by the airport and air-traffic system rose from 9.2% of arriving flights in 2019 to 11.0% in 2025. Airlines assign this category themselves, and it includes ordinary weather. The rate for the latest four months is in line with a year earlier, so this isn't a recent spike.
- **Forecast:** The FAA expects passenger boardings to grow 26.5% by fiscal 2035, about 5.6 million more a year. The FAA tends to forecast too high.

I can also break this down month by month, for example to show the summer peak (July 2025 was the busiest month, with 2,026,031 passengers).

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); FAA passenger boarding data CY2025, calendar 2025; BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: How full the planes are, FAA forecast passenger growth, FAA forecast flight growth; 'Boston' was taken to mean BOS  
> Confidence: Medium - the answer uses proxy measures (scores, system delay rate, load factor or forecasts); an airport name was resolved by default

## B7 - Show me medium-size airports in the West with the fastest forecast passenger growth.

*Pass when:* West region, medium hubs, sorted by forecast passenger growth.

*Result:* PASS

*Tool calls:* `rank_airports` {"region": "west", "size_classes": ["medium"], "sort_by": "forecast_passenger_growth_pct", "limit": 10}

Portland (PDX) has the fastest FAA forecast passenger growth of the West's medium-hub airports, at 33.2% (fiscal 2035 vs 2025). Oakland (OAK), San Jose (SJC) and Boise (BOI) follow, each close to 30%. The forecast is best used to compare airports with each other, not as a prediction, because the FAA tends to forecast too high. There are 11 medium hubs in the West, and the top 10 are shown below.

| # | Airport | Forecast pax growth | Extra boardings by 2035 | Growth since 2019 | Score (0-100) |
|---|---|---|---|---|---|
| 1 | Portland (PDX) | 33.2% | 2,989,548 | -6.4% | 72.3 |
| 2 | Oakland (OAK) | 29.9% | 1,402,276 | -35.5% | 46.0 |
| 3 | San Jose (SJC) | 29.6% | 1,620,865 | -35.0% | 44.7 |
| 4 | Boise (BOI) | 28.6% | 735,328 | 24.8% | 66.7 |
| 5 | Sacramento (SMF) | 24.7% | 1,682,362 | 3.8% | 52.0 |
| 6 | Anchorage (ANC) | 24.6% | 660,937 | 0.8% | 59.1 |
| 7 | Ontario (ONT) | 22.9% | 799,528 | 26.5% | 52.0 |
| 8 | Kahului (OGG) | 21.9% | 753,173 | -9.4% | 48.1 |
| 9 | John Wayne/Orange County (SNA) | 19.4% | 1,059,150 | 7.2% | 62.0 |
| 10 | Hollywood Burbank (BUR) | 16.0% | 531,720 | -0.7% | 44.0 |

**What changes the picture:**
- **Oakland and San Jose** are still about 35% below 2019 passenger levels, and airlines have cut seats by about a third. Their high forecasts are mostly a recovery story, and both score low overall. One airline, Southwest, carries 76.7% of Oakland's passengers. San Jose has a night noise curfew.
- **Portland** has the highest overall score (72.3) and the largest absolute gain. However, seats there were also cut since 2019, so how full its planes are (82.0%) partly reflects fewer seats rather than more demand.
- **Boise** is the cleanest growth case: passengers are up 24.8% since 2019, there are no data warnings, and its data confidence is high.
- **John Wayne (SNA)** has a legal passenger cap and a curfew. **Anchorage** (56.6% of flights are cargo) and **Ontario** (36.2%) are cargo-heavy.

I can profile Portland or Boise in more depth if that would help.

> Data period: FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: FAA forecast passenger growth, Capacity-need score, How full the planes are, FAA forecast flight growth; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - PDX: capacity cut; OAK: capacity cut; SJC: capacity cut, legal limit; ANC: cargo heavy
> Warnings printed: SJC: legal_limit, SNA: legal_limit, PDX: capacity_cut, OAK: single_airline, OAK: capacity_cut, SJC: capacity_cut, ANC: cargo_heavy, ONT: cargo_heavy, OGG: capacity_cut

## B8 - What's the busiest month at Burlington, Vermont, and how full are the planes then?

*Pass when:* The busiest month and its load factor.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Burlington, Vermont"}; `airport_trend` {"airport_code": "BTV", "metric": "passengers"}; `airport_trend` {"airport_code": "BTV", "metric": "load_factor_pct"}; `airport_profile` {"airport_code": "BTV"}

October is the busiest month at Patrick Leahy Burlington International (BTV), and planes are about 85-87% full then. That's a bit fuller than the airport's yearly average of 83.0%.

| | Passengers on departing flights | How full the planes are |
|---|---|---|
| October 2025 (busiest single month in the data) | 79,157 | 86.9% |
| October, average of the last 3 years | 73,848 | 84.9% |
| Latest 12 months (2025-05 to 2026-04) | 702,627 | 83.0% |

"How full the planes are" means passengers divided by seats on departing flights. It's not the official load factor, which uses passenger-miles. It reflects airline pricing and choice of aircraft, so it's only a rough stand-in for unmet demand.

**The busiest month isn't the fullest one.** Measured as a three-year average, July has the fullest planes (86.7%), with August and February next (both 85.5%). Summer is the other big peak in passengers: August averages 70,578 and July 67,585.

**The seasons are uneven.** October averages well over half again as many passengers as January (45,791), the quietest month. Anything built for the peak would sit partly empty in winter and spring.

**Why this matters for capacity:**
- Seats are almost unchanged since 2019 (+0.1%).
- Passenger flights fell 18.0% between 2019 and 2025, while passengers per flight rose from 58.1 to 73.2. Airlines are flying bigger planes rather than more flights.
- BTV ranks 6th of 78 small-hub airports on our capacity-need score, at 79.2.

Background (not from our data): October in Vermont is fall-foliage season, which likely explains the peak.

> Data period: BTS T-100 airport-month summary, 2023-05 to 2026-04 / 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; FAA passenger boarding data CY2025, calendar 2025; BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: How full the planes are, Capacity-need score, FAA forecast flight growth; 'unmet flight demand' is an estimate from the FAA forecast, used only when the airport is strained today; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - the answer uses proxy measures (scores, system delay rate, load factor or forecasts)

## C1 - Score the top 3 airports that have the highest congestion in August in the US.

*Pass when:* Ranks by the August system delay rate and says scores do not exist by month.

*Result:* PASS

*Tool calls:* `rank_airports` {"sort_by": "system_delay_rate_pct", "month": 8, "limit": 3}

Newark (EWR), Orlando (MCO) and San Juan (SJU) had the most August congestion. All three also score high on capacity need, and Orlando scores highest of the three. SJU shares third place with another airport at the same August rate, which the ranking didn't name.

"Congestion" here means the **system delay rate**: arrival delays blamed on the airport and air-traffic system, divided by arriving flights. It covers August 2023, 2024 and 2025 added together. Airlines assign this delay category, and it includes ordinary weather, so it mostly measures congestion but not only congestion. The capacity-need score (0-100) only exists for the latest period, so the scores below are the current ones, not August ones.

| Airport | Aug system delay rate | Capacity-need score | Passenger side | Flight side | National rank |
|---|---|---|---|---|---|
| Newark Liberty (EWR) | 10.9% | 80.7 | 72.7 | 88.6 | 13 of 343 |
| Orlando International (MCO) | 10.3% | 87.8 | 81.5 | 94.0 | 2 of 343 |
| San Juan Luis Munoz Marin (SJU) | 9.8% (tied) | 75.4 | 77.6 | 73.3 | 41 of 343 |

**What stands out:**
- **Newark has a legal flight cap**: 36 arrivals and 36 departures an hour under an FAA order. Its high flight-side score reflects delays, but the cap limits how much added runway or flight capacity could actually be used. Its passenger growth since 2019 is only 1.0%, so terminal or passenger-side upgrades may be the more relevant angle.
- **Orlando is the strongest case**: 14.7% passenger growth since 2019, a 28.2% FAA forecast for passenger growth and 26.4% for flight growth. The FAA tends to over-forecast, so treat those forecasts as a way to rank airports, not as predictions.
- **San Juan is a medium hub in a US territory.** Planes are the fullest of the three (84.6% of seats filled) and passengers are up 45.1% since 2019. But its forecast growth is low (8.5% passengers, 11.1% flights).

All three count as strained today. The ranking only included airports with full data and enough August flights to trust a delay rate.

> Data period: BTS Airline Delay Causes, August of 2023, 2024, 2025 (summed); BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: System delay rate, Capacity-need score, Passenger-side score, Flight-side score, FAA forecast passenger growth, FAA forecast flight growth; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - EWR: legal limit; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: EWR: legal_limit

## C9 - Which large airports are most congested in summer?

*Pass when:* Ranks large hubs by the summer (June to August) system delay rate, using the season filter; Newark leads.

*Result:* PASS

*Tool calls:* `rank_airports` {"size_classes": ["large"], "sort_by": "system_delay_rate_pct", "season": "summer", "limit": 10}; `rank_airports` {"size_classes": ["large"], "sort_by": "total_delay_rate_pct", "season": "summer", "limit": 10}

Newark (EWR) is the most congested large hub in summer, with a system delay rate of 13.2%. Orlando (MCO), New York JFK (JFK) and Boston (BOS) follow. Orlando also has the highest overall delay rate in summer, at 32.1%.

"Summer" here means June to August of 2023, 2024 and 2025 combined. "Large" means the FAA large-hub class (30 airports). The system delay rate counts arrivals delayed for airport or air-traffic reasons. Airlines code this category themselves, and it includes ordinary weather, so it mostly reflects congestion but not only that.

| Large hub | Summer system delay rate | Summer overall delay rate |
|---|---|---|
| Newark (EWR) | 13.2% | 27.5% |
| Orlando (MCO) | 10.6% | 32.1% |
| New York JFK (JFK) | 10.1% | 27.1% |
| Boston Logan (BOS) | 9.9% | 28.5% |
| Denver (DEN) | 9.7% | 27.0% |
| New York LaGuardia (LGA) | 9.5% | not in top 10 |
| Fort Lauderdale (FLL) | 9.0% | 30.1% |
| Chicago O'Hare (ORD) | 8.7% (tie) | not in top 10 |
| Miami (MIA) | 8.7% (tie) | 28.9% |

**Overall delay rate (any cause):** Florida airports lead this measure: Orlando, Tampa (TPA) at 30.3%, Fort Lauderdale and Miami. Tampa does not make the system-delay top 10, so a larger share of its delays comes from other causes.

**Warnings that change the picture:**
- **Legal limits on flights:** Newark (hourly cap), JFK and LaGuardia (FAA slot limits) and O'Hare (a temporary summer 2026 cap) have legal limits on flights. Added runway or gate capacity can't be used there without more slots or a looser cap. Reagan National (DCA) is 10th at 8.2% and has the same problem.
- **Fewer seats:** Fort Lauderdale has fewer seats than in 2019, so its full planes reflect cuts, not rising demand.
- **No legal limit flagged:** Orlando, Boston, Denver and Miami have no legal-limit warning, so for expansion they're the clearest congested candidates. Note that the legal-limits list is hand-made and may be incomplete.

I can show the month-by-month delay pattern for any of these airports, or compare a few of them side by side.

> Data period: BTS Airline Delay Causes, summer (June, July, August) of 2023, 2024, 2025 (summed) / 2023-08 to 2026-07 (three years); BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: System delay rate, How full the planes are  
> Confidence: Medium - EWR: legal limit; JFK: legal limit; LGA: forecast constrained, legal limit; FLL: capacity cut
> Warnings printed: EWR: legal_limit, JFK: legal_limit, LGA: legal_limit, ORD: legal_limit, DCA: legal_limit, LGA: forecast_constrained, FLL: capacity_cut, DCA: forecast_constrained, PHL: capacity_cut

## C10 - And is it the same ones in winter?

*Pass when:* A follow-up: ranks the same group for winter (December to February); San Francisco leads, so the answer is no.

*Result:* PASS

*Tool calls:* `rank_airports` {"size_classes": ["large"], "sort_by": "system_delay_rate_pct", "season": "winter", "limit": 10}; `rank_airports` {"size_classes": ["large"], "sort_by": "total_delay_rate_pct", "season": "winter", "limit": 10}

Mostly, with one big change: San Francisco (SFO) leads in winter, with a system delay rate of 11.6%, but it isn't in the summer top 10. Newark (EWR), Fort Lauderdale (FLL), LaGuardia (LGA), Miami (MIA), Orlando (MCO) and JFK (JFK) are in the top 10 in both seasons. Denver (DEN), Boston (BOS) and O'Hare (ORD) drop out of the winter top 10 for system delays. Delay rates are generally lower in winter than in summer.

| Large hub | Winter system delay rate | Winter overall delay rate |
|---|---|---|
| San Francisco (SFO) | 11.6% | 25.5% (tie) |
| Fort Lauderdale (FLL) | 9.7% | 25.5% (tie) |
| Newark (EWR) | 9.1% | not in top 10 |
| LaGuardia (LGA) | 9.0% | 21.7% |
| Miami (MIA) | 8.9% | 22.7% |
| Reagan National (DCA) | 8.5% | 22.4% |
| Orlando (MCO) | 7.8% | 23.0% |
| JFK (JFK) | 7.4% | 21.8% |
| Tampa (TPA) | 7.3% | 22.5% |
| Las Vegas (LAS) | 7.1% (tie) | not in top 10 |

**Notes:**
- **How "winter" is counted:** Winter means December, January and February. The tool takes those months from 2023, 2024 and 2025 together, so each winter mixes a December with the January and February of the same calendar year.
- **Overall delays:** Florida hubs still rank high on overall delays (Orlando, Miami, Tampa). San Diego (SAN) at 22.1% and Boston at 21.5% also make that top 10.
- **San Francisco:** Its seats are below 2019 levels (capacity was cut), so its full planes partly reflect fewer seats. Also, the system delay category is coded by airlines and includes ordinary weather. Background (not from our data): fog and low clouds in winter often cut SFO's arrival rate because its runways are close together.
- **Legal limits:** Newark, JFK, LaGuardia, Reagan National and San Diego (night curfew) all have legal limits, so congestion there may not turn into usable added capacity.

**Across both seasons:** Orlando and Miami are in the top 10 in both seasons, on both delay measures, and have no legal-limit flag.

> Data period: BTS Airline Delay Causes, winter (December, January, February) of 2023, 2024, 2025 (summed) / 2023-08 to 2026-07 (three years); BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: System delay rate, How full the planes are  
> Confidence: Medium - SFO: capacity cut; FLL: capacity cut; EWR: legal limit; LGA: forecast constrained, legal limit
> Warnings printed: EWR: legal_limit, LGA: legal_limit, DCA: legal_limit, JFK: legal_limit, SAN: legal_limit, SFO: capacity_cut, FLL: capacity_cut, LGA: forecast_constrained, DCA: forecast_constrained

## C2 - Where is Delta the dominant airline?

*Pass when:* Says airline-network questions are not supported; may offer the biggest-airline share per airport.

*Result:* PASS

*Tool calls:* `rank_airports` {"sort_by": "top_airline_share_pct", "size_classes": ["large", "medium"], "limit": 30}; `airport_profile` {"airport_code": "ATL"}; `airport_profile` {"airport_code": "MSP"}; `airport_profile` {"airport_code": "DTW"}; `airport_profile` {"airport_code": "SLC"}

Our data confirms four large hubs where Delta Air Lines is the biggest airline: Atlanta (ATL), Minneapolis-St Paul (MSP), Salt Lake City (SLC) and Detroit (DTW). Delta carries more than half of all passengers at each one, and about three-quarters at Atlanta.

| Airport | Delta share of passengers (2025) | Capacity-need score | How full the planes are | Note |
|---|---|---|---|---|
| Atlanta (ATL) | 74.7% | 69.8 | 82.3% | - |
| Minneapolis-St Paul (MSP) | 58.0% | 64.8 | 81.0% | Seats were cut since 2019 |
| Salt Lake City (SLC) | 57.5% | 60.9 | 80.1% | - |
| Detroit (DTW) | 54.8% | 60.6 | 79.2% | Seats were cut since 2019 |

**How I found these:** I can't search by airline. The data only records each airport's biggest airline and its share of passengers. So I ranked the large and medium hubs by that share and checked the profiles of the four that looked like Delta hubs. The list may not be complete:
- I only checked the top 30 of the 64 ranked large and medium hubs. Airports further down weren't checked, including Seattle (SEA) at 42.6%, where I didn't look up which airline is the biggest.
- I didn't look at small hubs or nonhubs.

**What this means for investment:** depending on one airline is a risk the score doesn't capture. Forecast growth at these airports depends partly on Delta's plans. At Minneapolis-St Paul and Detroit, passengers are still about 10% below 2019 and seats were cut. That means the full planes there reflect fewer seats more than rising demand.

I can check the biggest airline at other specific airports, or go through the small hubs, if you'd like.

> Data period: BTS T-100 Segment, calendar 2025; BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, How full the planes are, FAA forecast passenger growth, FAA forecast flight growth; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - DAL: legal limit; OAK: capacity cut; ANC: cargo heavy; EWR: legal limit
> Warnings printed: DAL: legal_limit, EWR: legal_limit, SJC: legal_limit, DAL: single_airline, HOU: single_airline, MDW: single_airline, OAK: single_airline, OAK: capacity_cut, ANC: cargo_heavy, MSP: capacity_cut, SJC: capacity_cut, DTW: capacity_cut, : more

## C3 - How many flights go from JFK to London?

*Pass when:* Declines: route-level questions are not supported.

*Result:* PASS

*Tool calls:* `airport_profile` {"airport_code": "JFK"}

I can't tell you how many flights go from JFK to London. The dataset has no route, destination or city-pair counts. The closest thing I have is how many of John F Kennedy International's (JFK) flights are long-haul.

**JFK departing passenger flights, calendar 2025** (212,394 in total, all destinations and airlines):

| Long-haul cutoff (our definition) | Long-haul passenger flights | Share of passenger flights |
|---|---|---|
| 2,000+ miles | 96,455 | 45.4% |
| 2,500+ miles | 60,217 | 28.4% |
| 3,000+ miles (our default) | 49,841 | 23.5% |

Background (not from our data): London is more than 3,000 miles from New York, so JFK-London flights are inside the 3,000+ mile group. That group also includes flights to the rest of Europe, Asia and other long-haul destinations, so it gives an upper limit, not a London count.

**Other context that may help:**
- 45.6% of JFK's passengers fly to US destinations, so most of its traffic is international.
- Its biggest airline is Delta, with 24.8% of passengers.

**Warning:** JFK's flight slots are capped by FAA order (it's a Level 3 slot-controlled airport). Even if long-haul demand is strong, added runway or gate capacity can't be used without more slots.

For the London count itself, you'd need a route-level source such as the BTS T-100 segment data filtered to JFK-London airports. I can also show JFK's long-haul share at a different mileage cutoff, or compare it with Newark (EWR).

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); BTS T-100 Segment, calendar 2025  
> Assumptions: long-haul means 3,000 miles or more (our definition; adjustable)  
> Confidence: Medium - JFK: legal limit
> Warnings printed: JFK: legal_limit

## C4 - What's the congestion level at Teterboro?

*Pass when:* Says Teterboro is outside the covered airports; no invented number.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Teterboro"}

I don't have congestion data for Teterboro. It isn't one of the 402 FAA "primary" airports this dataset covers, which are commercial-service airports with more than 10,000 passenger boardings a year.

Background (not from our data): Teterboro is mainly a business and private jet airport. It has almost no scheduled airline service, so it isn't in the BTS airline delay and passenger data that our congestion measures come from.

Here's what I can do instead: show congestion at the commercial airports in the New York-New Jersey area, such as Newark (EWR), LaGuardia (LGA) and JFK. For each one I'd give:
- **System delay rate:** the share of flights delayed for reasons in the air traffic system. Airlines code these delays themselves, and the category includes ordinary weather. I'd give it over three years and for the latest 12 months.
- **Overall delay rate:** the share of flights delayed for any reason.

Do you want me to compare those three, or rank every airport in the New York metro area?

> Data period: no data was used in this reply  
> Assumptions: none  
> Confidence: n/a - no data figures were used in this reply

## C5 - Which airports were the top expansion candidates in 2021?

*Pass when:* Says the score exists for the latest period only; offers raw 2021 metrics.

*Result:* PASS

*Tool calls:* `rank_airports` {"year": 2021, "sort_by": "load_factor_pct", "limit": 5}; `rank_airports` {"year": 2021, "sort_by": "system_delay_rate_pct", "limit": 5}

I can't rank 2021 expansion candidates. The capacity-need score only exists for the latest period, so there's no 2021 version of it. What I can show is the raw 2021 numbers for the two most important parts of the score.

**Fullest planes, calendar 2021** (passengers divided by seats on departing flights)

| Airport | 2021 |
|---|---|
| McAllen (MFE) | 84.4% |
| Wilkes-Barre/Scranton (AVP) | 84.3% |
| Aguadilla (BQN) | 83.8% |
| Ponce (PSE) | 82.3% |
| Hartford Bradley (BDL) | 82.2% |

**Highest system delay rate, calendar 2021** (arrival delays blamed on the airport and air-traffic system, as a share of arriving flights)

| Airport | 2021 |
|---|---|
| Key West (EYW) | 11.5% |
| Punta Gorda (PGD) | 10.0% |
| Newark (EWR) | 8.8% |
| Dallas Love Field (DAL) | 8.4% |
| Aguadilla (BQN) | 8.4% |

**Caveats that change how to read these:**
- 2021 was still a pandemic-recovery year, so these numbers may not reflect normal demand.
- Airlines code the system-delay category themselves, and it includes ordinary weather.
- How full the planes are is the weakest signal in the score. It depends on airline pricing and fleet choices, not just demand.
- Today, AVP, BQN and PSE have full planes partly because seats were cut, not because demand grew.
- Newark has an FAA cap of 36 arrivals and 36 departures an hour. Dallas Love Field is capped at 20 gates by federal law.
- Cargo makes up 42.8% of BQN's flights.
- Almost all of Punta Gorda's passengers fly one airline (Allegiant). Dallas Love Field is the same with Southwest.

Looking at the current period instead, Punta Gorda ranks first overall of 343 airports on the capacity-need score.

I can also rank 2021 by passenger numbers or by share of long-haul flights. Or I can show how any of these airports changed year by year from 2019 to today.

> Data period: BTS T-100 airport-month summary, calendar 2021 / 2025-05 to 2026-04 (latest 12 complete months); BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / calendar 2021  
> Assumptions: proxies, not direct measurements: How full the planes are, Capacity-need score, System delay rate; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - 1 of the 5 listed airports has weaker data (PSE: small delay sample); AVP: capacity cut; BQN: capacity cut, cargo heavy; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: EWR: legal_limit, DAL: legal_limit, AVP: capacity_cut, BQN: cargo_heavy, BQN: capacity_cut, PSE: small_sample, PSE: capacity_cut, PSE: small_airport_forecast, PGD: single_airline, DAL: single_airline

## C6 - Should we invest in expanding LaGuardia?

*Pass when:* Gives the evidence and the slot limit; leaves the decision to the analyst.

*Result:* FAIL - failed: says /slot/

*Tool calls:* `find_airport` {"query": "LaGuardia"}; `airport_profile` {"airport_code": "LGA"}

I can't make the investment call for you, and I have no cost or return data. What the data shows is a mixed case. LaGuardia (LGA) is one of the most congested airports we cover, but a federal cap on flights limits how much new capacity could actually be used.

**Overall position:** LaGuardia's capacity-need score is 67.8 out of 100. That ranks it 19th of 30 large hubs and 76th of all 343 ranked airports. The score measures upside, meaning how much added capacity would likely be filled. It's a stand-in for profit, not a measure of it.

| Measure | LGA | Position among peers (0-100) |
|---|---|---|
| How full the planes are | 80.8% | 78.9 |
| Passenger growth since 2019 | 4.7% | 49.0 |
| FAA forecast passenger growth (2025-2035) | 18.4% | 47.2 |
| System delay rate (3 years) | 8.4% | 98.1 |
| FAA forecast flight growth (2025-2035) | 9.3% | 45.9 |

**Congestion is real.** "System" delays are those airlines attribute to the airport and air-traffic system; airlines code these themselves, and the category includes ordinary weather. They are 8.4% of arrivals over three years and 10.4% in the latest 12 months, with no sudden recent spike. Arrivals late for any reason are 21.5%, and system causes account for 39.3% of those delays. Because LGA is strained, the FAA's forecast of 33,029 extra takeoffs and landings by 2035 counts as an *estimate* of unmet flight demand. The FAA tends to over-forecast.

**Why that demand may not be capturable:**
- **Legal limits:** an FAA order caps the number of flights, and nonstop flights are limited to 1,500 miles (Saturdays exempt). The FAA's flight forecast already assumes the cap, so it isn't a measure of unconstrained demand.
- **Growth comes from bigger planes, not more flights:** passenger flights are down 4.8% since 2019, while passengers per flight rose from 85.3 to 94.7.
- **Passenger growth is middling:** both past and forecast growth sit near the middle of the pack.

Background (not from our data): LaGuardia's terminals were recently rebuilt on a large scale. Our score doesn't account for capacity that's already been built or is under construction.

**What to check next:**
- Whether the flight cap or distance limit could realistically change.
- How busy the terminal is at peak hours, which isn't in our data.
- A side-by-side comparison with JFK and Newark (EWR) in the same metro area. I can run that if you want.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); FAA passenger boarding data CY2025, calendar 2025; BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, How full the planes are, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; 'unmet flight demand' is an estimate from the FAA forecast, used only when the airport is strained today; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - LGA: forecast constrained, legal limit; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: LGA: legal_limit, LGA: forecast_constrained

## C7 - What will a new terminal at Denver cost, and what return would we get?

*Pass when:* Declines cost and return; offers the capacity-need evidence.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Denver"}

I can't tell you what a new terminal at Denver International (DEN) would cost or what return it would earn. Our data has no construction costs, revenue or other financial figures, and no gate counts or terminal sizes. What I can show is how much added capacity would likely be filled. That's our proxy for upside, and Denver scores well on it.

**Denver (DEN), capacity-need score 76.7 out of 100**
The score compares each airport with the 343 airports that have full data. Denver ranks 12th of 30 large hubs and 33rd overall.

| Measure | Value | What it shows |
|---|---|---|
| Passenger-side score | 76.7 | Demand from passengers |
| Flight-side score | 76.7 | Pressure on flights |
| Load factor | 81.2% | How full the planes are, latest 12 months |
| Passenger growth since 2019 | 18.8% | Growth so far |
| Seat change since 2019 | 26.1% | Airlines have added seats, not cut them |
| FAA forecast passenger growth | 23.7% | Fiscal 2035 vs 2025 |
| FAA forecast extra boardings | about 9.5 million | Forecast added boardings per year by fiscal 2035 |
| FAA forecast flight growth | 14.7% | Fiscal 2035 vs 2025 |
| System delay rate | 6.6% | Three-year rate. Airlines code these delays, and they include ordinary weather |
| Boardings, 2025 | about 40.0 million | Size (not part of the score) |

Our data flags Denver as strained today. That means demand is pressing on current capacity: planes are full, passenger numbers keep growing and the FAA expects more growth.

**What would help next:**
- I can pull Denver's full profile: the flight-demand estimate, delay causes, and whether delays are rising or just spiked recently.
- I can compare Denver with other large hubs to see whether the upside is stronger somewhere else.

You'd need to get cost and return figures from the airport's own capital plan or a feasibility study.

> Data period: see the tool trace  
> Assumptions: proxies, not direct measurements: Capacity-need score, Passenger-side score, Flight-side score; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - the answer uses proxy measures (scores, system delay rate, load factor or forecasts)

## C8 - What is the delay rate at Glacier Park airport in Kalispell, and can I trust it?

*Pass when:* Resolves Glacier Park to FCA, gives the rate and the sample size.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Glacier Park, Kalispell"}; `find_airport` {"query": "FCA"}; `airport_profile` {"airport_code": "FCA"}

Glacier Park International (FCA) in Kalispell, Montana has a **system delay rate of 4.0%** and an **overall delay rate of 16.6%** over three years (Aug 2023 - Jul 2026). The figure is reasonably reliable: the data is complete and covers 15,601 arriving flights. But it measures something narrower than "congestion," so read it with the caveats below.

(The name search didn't find it, so I looked it up by its code, FCA. The FAA's own code for it is GPI.)

| Measure | Value |
|---|---|
| System delay rate, 3 years | 4.0% |
| System delay rate, latest 12 months | 4.7% |
| Overall delay rate (15+ min late, any cause), 3 years | 16.6% |
| Rank on system delay among full-data airports (0-100) | 49.1, mid-pack |

**What the system delay rate measures:** arrival delays the airline blamed on the airport and air-traffic system, divided by all arrivals. It's our stand-in for congestion.

**Why you can mostly trust it:**
- The data is complete and has no data warnings, so its confidence label is "high."
- The three-year sample is large.
- The rate has been stable year to year: 3.1% (2023), 3.9% (2024), 3.9% (2025).
- The latest months show no unusual spike.

**Why to be careful:**
- **Airlines choose the delay category, and it includes ordinary weather.** It's mostly congestion, not purely congestion.
- **Coverage:** it only counts domestic flights of the larger airlines that report delays.
- **Most delays have other causes.** Of flights delayed 15+ minutes, 42.9% were blamed on the airline and 28.5% on a late incoming plane. Only 24.1% were system delays.

**Bottom line:** Kalispell isn't strained. Its interest as an investment comes from the passenger side: planes are 85.7% full, and passengers are up 57.0% since 2019.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Passenger-side score, System delay rate  
> Confidence: Medium - the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
