# Evaluation run - 2026-10-04 18:16 - claude-opus-5-5

**26 of 26 questions passed.** 933 numbers appeared in the answers; 0 answers ended with a number that could not be traced to a tool result; 3 answers passed only after one automatic rewrite. Average 12.8s per question; 799,572 input and 28,917 output tokens in total.

| Id | Group | Result | Tools | Number check | Seconds |
|---|---|---|---|---|---|
| A1 | core | PASS | rank_airports | passed | 12.7 |
| A2 | core | PASS | find_airport, find_airport, compare_airports, airport_profile, airport_profile | passed | 13.3 |
| A6 | follow-up | PASS | compare_airports | passed | 10.6 |
| A3 | core | PASS | find_airport, airport_profile | passed | 10.1 |
| A7 | follow-up | PASS | airport_profile | passed | 7.7 |
| A4 | core | PASS | airport_profile | passed | 11.7 |
| A5 | follow-up | PASS | find_airport, compare_airports, airport_profile | passed | 12.1 |
| A8 | follow-up | PASS | find_airport, airport_profile | passed | 14.4 |
| B1 | filters | PASS | rank_airports | rewritten | 16.8 |
| B2 | filters | PASS | rank_airports | passed | 10.1 |
| B3 | filters | PASS | rank_airports, rank_airports | passed | 10.8 |
| B4 | ambiguous | PASS | find_airport, find_airport | passed | 6.9 |
| B5 | filters | PASS | rank_airports | passed | 13.1 |
| B6 | time | PASS | find_airport, airport_profile | passed | 13.1 |
| B7 | filters | PASS | rank_airports | passed | 11.7 |
| B8 | time | PASS | find_airport, airport_trend, airport_trend | passed | 11.7 |
| C1 | time | PASS | rank_airports, rank_airports | rewritten | 22.4 |
| C9 | time | PASS | rank_airports, rank_airports | passed | 13.8 |
| C10 | time | PASS | rank_airports, rank_airports | passed | 14.2 |
| C2 | out of scope | PASS | rank_airports, airport_profile, airport_profile, airport_profile, airport_profile | passed | 16.5 |
| C3 | out of scope | PASS | airport_profile | passed | 9.6 |
| C4 | out of scope | PASS | find_airport | passed | 5.6 |
| C5 | out of scope | PASS | rank_airports, rank_airports | passed | 15.9 |
| C6 | judgment | PASS | find_airport, airport_profile | passed | 15.1 |
| C7 | out of scope | PASS | find_airport | passed | 10.2 |
| C8 | awkward data | PASS | find_airport, find_airport, airport_profile | rewritten | 22.2 |

## A1 - Which airports in New England are strong candidates for terminal expansion?

*Pass when:* A ranked list from the six states, scores shown, reasons given.

*Result:* PASS

*Tool calls:* `rank_airports` {"region": "new england", "limit": 10}

Four airports stand out on our capacity-need score: Boston Logan (BOS), Burlington (BTV), Portland, Maine (PWM) and Bangor (BGR). No data measures terminal or gate use directly. For terminals, the passenger-side score is probably the more useful signal. It is built from how full the planes are, passenger growth since 2019 and the FAA's passenger forecast.

| Airport | Size class | Total score | Passenger side | Flight side | Planes full | Passenger growth since 2019 | FAA forecast passenger growth | Forecast extra boardings by 2035 |
|---|---|---|---|---|---|---|---|---|
| BOS | large | 82.9 | 72.2 | 93.6 | 81.7% | 1.2% | 26.5% | 5,612,088 |
| BTV | small | 79.2 | 73.7 | 84.8 | 83.0% | 2.3% | 22.9% | 163,754 |
| PWM | small | 77.4 | 79.2 | 75.6 | 82.8% | 17.2% | 21.6% | 278,078 |
| BGR | nonhub | 71.8 | 78.0 | 65.5 | 80.4% | 40.8% | 24.1% | 103,055 |

**What each case rests on:**
- **BOS** ranks 11th of 343 airports nationally and is flagged as strained. Its strength is the flight side: a 9.1% system delay rate over three years. That rate is the share of arrivals delayed by causes airlines code to the airport and air-traffic system, which includes ordinary weather. Passenger growth since 2019 is nearly flat, so the case relies on how full the planes are and on the forecast.
- **BTV** is also strained, with the fullest planes in the group. But passengers have barely grown since 2019.
- **PWM** has the strongest passenger side. Passengers are up 17.2% since 2019 while flight counts stayed flat, so the growth went into bigger or fuller planes.
- **BGR** has the fastest growth since 2019 (40.8%), but a weaker flight side.

**Further down:** Hartford (BDL, 65.9) and Providence (PVD, 59.8) are larger airports but score as mid-pack. JetBlue carries 83.5% of passengers at Worcester (ORH), and Allegiant carries 81.2% at Portsmouth (PSM), so their demand depends on one airline. PSM's data confidence is also low.

**Not ranked (partial data):** New Haven (HVN), Cape Cod (HYA), Block Island (BID) and Westerly (WST).

The score shows how much added capacity would likely be filled. It is not a measure of profit, and I have no cost data. To go further, I can profile any of these airports, including delay causes and the estimated flight demand.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years); FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, Passenger-side score, Flight-side score, How full the planes are, FAA forecast passenger growth, System delay rate; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - 1 of the 10 listed airports has weaker data (PSM: small delay sample); MVY: small airport forecast; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: ORH: single_airline, MVY: small_airport_forecast, PSM: small_sample, PSM: single_airline, PSM: small_airport_forecast

## A2 - Compare LA and Santa Ana airport congestion levels.

*Pass when:* LAX vs SNA side by side, a clear verdict, Santa Ana's legal cap flagged.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "LA"}; `find_airport` {"query": "Santa Ana"}; `compare_airports` {"airport_codes": ["LAX", "SNA"]}; `airport_profile` {"airport_code": "LAX"}; `airport_profile` {"airport_code": "SNA"}

Los Angeles International (LAX) is more congested than John Wayne/Orange County in Santa Ana (SNA) on every delay measure, but the gap is small. Neither airport is "strained" by our definition, which means a system delay rate in the top quarter of airports. I took "LA" to mean LAX. The metro area also has Ontario (ONT), Hollywood Burbank (BUR) and Long Beach (LGB).

| Measure | LAX | SNA | Difference |
|---|---|---|---|
| System delay rate, 3 years | 4.8% | 3.9% | +0.9 pts |
| System delay rate, latest 12 months | 5.0% | 4.3% | +0.7 pts |
| Overall delay rate (15+ min, any cause) | 18.9% | 17.5% | +1.4 pts |
| Where its system delay rate ranks (0-100, higher = more delays) | 70.9 | 47.1 | |
| Flight-side score | 80.5 | 58.7 | +21.8 |

**What the numbers mean:** The system delay rate is the share of arriving flights that airlines blamed on the airport and air-traffic system. It mostly reflects congestion, but it also includes ordinary weather, and only larger airlines report it.

**Causes of delays:** At both airports, most delays come from the airlines themselves and from late-arriving aircraft. System delays are 25.7% of delayed flights at LAX and 22.4% at SNA.

**Recent trend:** Both are a little higher in the latest 12 months than over three years. That is not a recent spike: the newest four months look like the rest of the year and the same months a year earlier.

**Warnings that change the picture:**
- **SNA has a legal limit.** It is capped at roughly 6.1-6.25 million passengers a year in our units, limited to 95 average daily departures in the regulated class, and closed at night. It carried 5,590,354 passengers in the latest 12 months. Its lower delays partly reflect traffic held down by these rules, so the cap limits expansion more than delays do.
- **LAX cut capacity.** Seats are down 12.8% since 2019 and passengers down 15.7%, so its congestion comes with less traffic than in 2019, not more.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, Flight-side score, System delay rate; 'LA' was taken to mean LAX; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - LAX: capacity cut; SNA: legal limit; the answer uses proxy measures (scores, system delay rate, load factor or forecasts); an airport name was resolved by default
> Warnings printed: SNA: legal_limit, LAX: capacity_cut

## A6 - And how did congestion at those two look in 2023?

*Pass when:* Uses the same two airports without being told again, and 2023 values.

*Result:* PASS

*Tool calls:* `compare_airports` {"airport_codes": ["LAX", "SNA"], "year": 2023}

In 2023 both airports were more congested than they are now, and LAX was further ahead of SNA. LAX's system delay rate was a third higher than SNA's that year. In the latest 12 months the gap is about a sixth.

**Calendar 2023**

| Measure | LAX | SNA | Difference |
|---|---|---|---|
| System delay rate | 5.6% | 4.2% | +1.4 pts (1.33x) |
| Overall delay rate (15+ min, any cause) | 20.5% | 18.5% | +2.0 pts (1.11x) |
| Arriving flights in the delay data | 195,617 | 45,732 | |
| Passengers on departing flights | 37,119,938 | 5,725,328 | |

**Comparison with other years (from the yearly history):**
- **LAX:** 2023 was its most congested year since 2019, when the system delay rate was 6.3%. The rate then fell to 4.9% in 2024 and 4.6% in 2025, and is 5.0% so far in 2026, which covers 7 months of delay data.
- **SNA:** The rate has stayed in a narrow band: 4.2% in 2023, 3.7% in 2024, 4.3% in 2025 and 4.1% so far in 2026.

So the gap has narrowed since 2023 mainly because LAX improved, not because SNA got worse. The 2023 passenger counts were also higher than now at both airports. At LAX, congestion eased as traffic dropped below its 2023 level.

The system delay rate is coded by airlines and includes ordinary weather, so it measures congestion mostly, not purely. The capacity-need score exists only for the latest period, so I can't show 2023 scores. If you want to see when the 2023 congestion at LAX was worst, I can pull a month-by-month view.

> Data period: BTS T-100 airport-month summary, calendar 2023; BTS Airline Delay Causes, calendar 2023; BTS T-100 Segment, calendar 2023  
> Assumptions: proxies, not direct measurements: System delay rate  
> Confidence: Medium - LAX: capacity cut; SNA: legal limit; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: SNA: legal_limit, LAX: capacity_cut

## A3 - What is the percentage of long haul flights out of Anchorage airport?

*Pass when:* One number, the 3,000-mile definition stated, the cargo-included number next to it.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Anchorage airport"}; `airport_profile` {"airport_code": "ANC"}

At Ted Stevens Anchorage International (ANC), **2.8% of departing passenger flights fly 3,000 miles or more**. If you count cargo flights too, the share jumps to **31.0%**, because ANC is a major cargo hub.

I took "Anchorage airport" to mean ANC. The area's only other covered airport is Merrill Field (MRI), a much smaller non-hub airport with partial data.

**How I defined long-haul:** There's no official definition. My default is a departing flight of at least 3,000 miles, domestic plus international, all airlines, for calendar 2025. The share changes a lot depending on the cutoff:

| Cutoff | Share of passenger flights | Share of all flights incl. cargo |
|---|---|---|
| 2,000 mi | 13.7% (5,239 flights) | 47.4% (41,732 flights) |
| 2,500 mi | 9.8% (3,723 flights) | 43.2% (37,969 flights) |
| 3,000 mi | 2.8% (1,061 flights) | 31.0% (27,305 flights) |

That's out of 38,150 passenger departures and 87,988 departures in total in 2025.

**Why the two shares are so different:** Cargo makes up 56.6% of ANC's departures (49,838 cargo and other non-passenger flights). Passenger service is mostly domestic: 98.6% of passengers fly to US destinations, and Alaska Airlines carries 61.4% of them. So most of the long-haul flying here is cargo.

Background (not from our data): Anchorage is a common refuelling and transfer stop for cargo flights between Asia and North America, which explains its high share of long-haul cargo flights.

**Why this matters for investment:** Cargo uses the same runways but isn't in the capacity-need score. The FAA's flight forecast does include cargo. I can rerun the shares at any other cutoff if you need one.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; FAA passenger boarding data CY2025, calendar 2025; BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, FAA forecast passenger growth, FAA forecast flight growth; long-haul means 3,000 miles or more (our definition; adjustable); 'Anchorage airport' was taken to mean ANC; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - ANC: cargo heavy; the answer uses proxy measures (scores, system delay rate, load factor or forecasts); an airport name was resolved by default
> Warnings printed: ANC: cargo_heavy

## A7 - What if long-haul means over 2,300 miles?

*Pass when:* Recomputed at 2,300 miles for Anchorage.

*Result:* PASS

*Tool calls:* `airport_profile` {"airport_code": "ANC", "long_haul_miles": 2300}

With long-haul set at 2,300 miles, **12.6% of departing passenger flights at Anchorage (ANC) are long-haul** (4,820 of 38,150 in calendar 2025). If you count cargo flights too, the share is **46.5%** (40,947 of 87,988 departures).

One small detail: the tool counts flights of *at least* 2,300 miles, not strictly over it. That only matters for flights of exactly 2,300 miles.

Here is how 2,300 compares with the other cutoffs:

| Cutoff | Share of passenger flights | Share of all flights incl. cargo |
|---|---|---|
| 2,000 mi | 13.7% | 47.4% |
| **2,300 mi** | **12.6%** | **46.5%** |
| 2,500 mi | 9.8% | 43.2% |
| 3,000 mi | 2.8% | 31.0% |

The share barely moves between 2,000 and 2,300 miles. It falls a bit by 2,500 miles and drops sharply by 3,000 miles. So most of ANC's longer passenger flights are between about 2,500 and 3,000 miles. Because the result swings so much in that range, the cutoff you choose matters a lot here. It's worth deciding on one before comparing ANC with other airports.

The gap between the two columns is still about cargo: 56.6% of ANC's departures are cargo or other non-passenger flights. Cargo uses the same runways but isn't counted in the capacity-need score.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score; long-haul means 2,300 miles or more (our definition; adjustable); scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - ANC: cargo heavy; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: ANC: cargo_heavy

## A4 - What is the unmet flight demand in SFO airport and why?

*Pass when:* An estimate named as an estimate or proxy, with the why from the delay data.

*Result:* PASS

*Tool calls:* `airport_profile` {"airport_code": "SFO"}

**San Francisco International (SFO)** has an estimated **108,307 extra takeoffs and landings a year of unmet flight demand by fiscal 2035**. The main reason is that the airfield is already the most congested in our data, so it has little room to absorb that growth. This figure is an estimate, not a measurement. It is the FAA's forecast growth in commercial operations, from 406,220 in fiscal 2025 to 514,527 in fiscal 2035 (+26.7%). FAA operations include cargo, and the FAA tends to over-forecast. We only call the gap "unmet" because SFO counts as strained today.

**Why it's considered unmet:**
- **System delay rate: 13.4%** of arriving flights over three years. That's the highest of all full-data airports (position 100 of 100). Airlines assign delays to this category, and it includes ordinary weather, so it's mostly congestion but not only congestion.
- **System delays are the main cause.** They account for 48.9% of delayed flights, compared with 24.7% for airline causes, 23.7% for late aircraft and 2.5% for extreme weather. Overall, 27.4% of arrivals are 15+ minutes late.
- **Recent spike, not a steady trend:** the latest-12-month system delay rate is 17.3%, but most of that comes from 2026-04 to 2026-07, which ran at 30.0%. The same months a year earlier ran at 7.8%, and the other recent months ran at 10.3%. A temporary cause that isn't in our data is possible.
- **Strong forecast:** flight growth of 26.7% puts SFO at position 94.2 of 100.

**Caveats:**
- **Airlines have cut capacity.** Seats are down 5.0% and passengers down 4.4% compared with 2019, so full planes (82.6% load factor) reflect fewer seats rather than rising demand.
- **No hard cap.** SFO is under FAA Level 2 schedule facilitation, which coordinates schedules but doesn't impose a limit.

Background (not from our data): SFO's closely spaced parallel runways lose arrival capacity in low visibility, which helps explain why system delays are so high there.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: How full the planes are, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; 'unmet flight demand' is an estimate from the FAA forecast, used only when the airport is strained today  
> Confidence: Medium - SFO: capacity cut; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: SFO: capacity_cut

## A5 - How does that compare with Oakland?

*Pass when:* Oakland is not called unmet demand, because it is not strained.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Oakland"}; `compare_airports` {"airport_codes": ["SFO", "OAK"]}; `airport_profile` {"airport_code": "OAK"}

I took "Oakland" to mean **Oakland San Francisco Bay (OAK)**. The metro area also has San Jose (SJC). Unlike San Francisco (SFO), Oakland **has no unmet flight demand by our definition**. The FAA forecasts 30,637 extra takeoffs and landings a year by fiscal 2035, but that is just **forecast flight growth**. Oakland's airfield isn't strained today, so nothing suggests that growth would go unserved.

| Metric | SFO | OAK |
|---|---|---|
| Capacity-need score | 86.9 (#3 of 343) | 46.0 (#208 of 343) |
| Flight-side score | 97.1 | 49.7 |
| Forecast extra operations by 2035 | 108,307 | 30,637 |
| Forecast flight growth | 26.7% | 24.8% |
| System delay rate (3 yr) | 13.4% | 2.3% |
| System delay rate (latest 12 mo) | 17.3% | 1.7% |
| Overall delay rate | 27.4% | 18.4% |
| System share of delays | 48.9% | 12.3% |
| How full the planes are | 82.6% | 74.2% |
| Passengers vs 2019 | -4.4% | -35.5% |

**Why they differ:** Both airports have strong FAA growth forecasts. The difference is congestion. SFO's system delay rate is 5.83 times Oakland's. Most of Oakland's delays come from the airlines themselves: late-arriving aircraft cause 54.1% and airline causes 32.5%. The airport and air-traffic system cause only 12.3%. Oakland's delay rates have also stayed flat, with no recent spike. (The system delay category is assigned by airlines and includes ordinary weather.)

**Caveats for Oakland:**
- **Lost traffic:** seats are down 31.5% and passengers down 35.5% since 2019. The airport has lost traffic, so the forecast growth is partly about recovering it.
- **One airline:** Southwest carries 76.7% of passengers, so the growth depends on that airline's plans.
- **Cargo:** 17.9% of departing flights are cargo (1.2% at SFO). Cargo uses the same runways but isn't in the score.

Taken together, Oakland has spare capacity, while SFO is short of it.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, Flight-side score, How full the planes are, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; 'unmet flight demand' is an estimate from the FAA forecast, used only when the airport is strained today; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - SFO: capacity cut; OAK: capacity cut; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: SFO: capacity_cut, OAK: single_airline, OAK: capacity_cut

## A8 - Is Memphis a good candidate, given its cargo traffic?

*Pass when:* Uses the Memphis profile and the cargo share.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Memphis"}; `airport_profile` {"airport_code": "MEM"}

Memphis (MEM) is a middling candidate overall, and the cargo is the reason to be careful. Its stronger side, flights, depends partly on cargo, while its passenger side is weak. It scores 59.5 out of 100 on capacity need, ranking 46th of 78 small-hub airports and 116th of 343 overall.

**Passenger side is weak (score 45.4):**
- Planes are 73.4% full (passengers divided by seats). That is the weakest of the five inputs.
- Passengers grew only 0.9% since 2019, while seats grew 6.7%. Supply has grown faster than demand.
- The FAA forecasts 25.8% passenger growth by 2035, or about 609,461 extra boardings a year. The FAA tends to over-forecast.

**Flight side is stronger (score 73.7), but cargo drives part of it:**
- Cargo is 65.1% of departing flights. The score leaves cargo out, but cargo uses the same runways.
- The FAA's 18.4% forecast flight growth (29,629 extra takeoffs and landings by 2035) includes cargo, so it is not purely passenger demand.
- The system delay rate is 4.9% over three years and 5.1% in the latest 12 months, with no recent spike. Airlines assign this delay category themselves, and it includes ordinary weather. The rate covers only domestic flights of the larger reporting airlines, so cargo flights' own delays are not measured.
- The airport is not classed as strained. So the forecast growth is not called unmet demand.
- Of delayed flights, 21.4% were blamed on the airport and air-traffic system. Most were airline-related (35.3%) or caused by a late incoming aircraft (39.4%).

**Context:** Passenger flights are down 7.7% since 2019. Delta is the biggest airline with 21.7% of passengers. No passenger flights go 3,000 miles or more (0.0%), but 5.9% of all flights do once cargo is counted.

Background (not from our data): Memphis is FedEx's global hub, so airfield growth there likely depends on cargo plans more than passenger demand.

**Worth checking next:** cargo operators' expansion plans, and whether any proposed project is mainly for the passenger terminal or for the airfield.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); FAA passenger boarding data CY2025, calendar 2025; BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, Passenger-side score, Flight-side score, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; 'unmet flight demand' is an estimate from the FAA forecast, used only when the airport is strained today; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - MEM: cargo heavy; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: MEM: cargo_heavy

## B1 - Score the top 3 airports that have the highest congestion in the US, only small airports.

*Pass when:* Small-hub class, sorted by the system delay rate, three airports with scores; says what 'small' means.

*Result:* PASS

*Tool calls:* `rank_airports` {"size_classes": ["small"], "sort_by": "system_delay_rate_pct", "limit": 3}

Among small airports (the FAA "small hub" class), the three most congested are Punta Gorda (PGD), Key West (EYW) and St. Thomas (STT). Punta Gorda is the clear standout: its capacity-need score of 94.9 ranks it #1 of all 343 ranked airports, not just among small ones.

"Congestion" here means the system delay rate: the share of arriving flights delayed by the airport or air-traffic system, over the three years 2023-08 to 2026-07. Airlines code this category themselves, and it includes ordinary weather, so it mostly reflects congestion but not entirely.

| Airport | System delay rate | Total score | Passenger side | Flight side | Rank (small / overall) |
|---|---|---|---|---|---|
| Punta Gorda (PGD), FL | 8.6% | 94.9 | 93.3 | 96.5 | 1 of 78 / 1 of 343 |
| Key West International (EYW), FL | 8.0% | 67.7 | 64.2 | 71.2 | 32 / 77 |
| Cyril E. King, St. Thomas (STT), VI | 7.9% | 70.8 | 62.3 | 79.3 | 26 / 64 |

**What drives the scores**
- **PGD:** Planes are 85.8% full, passengers are up 37.0% since 2019, and the FAA forecasts flight growth of 26.8% by 2035. **Caveat:** Allegiant Air carries 99.6% of its passengers, so the growth depends on one airline's plans.
- **EYW:** Passengers are up 55.9% since 2019, but the FAA forecasts only 9.3% flight growth. That holds back its flight-side score even though its delays are high.
- **STT:** Planes are 77.9% full and the FAA forecasts 15.0% flight growth. It's in a US territory, so leave it out if you meant US states only. In that case the next airport down the delay ranking would be third, and I can pull it.

All three are flagged as strained today. Tweed/New Haven (HVN) is left out of the ranking because it has only partial data.

> Data period: BTS Airline Delay Causes, 2023-08 to 2026-07 (three years); BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: System delay rate, Capacity-need score, Passenger-side score, Flight-side score, FAA forecast passenger growth, FAA forecast flight growth; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: PGD: single_airline

## B2 - Top 5 airports in Texas by how full the planes are.

*Pass when:* Five Texas airports by load factor.

*Result:* PASS

*Tool calls:* `rank_airports` {"states": ["TX"], "sort_by": "load_factor_pct", "limit": 5}

Dallas-Fort Worth (DFW) and McAllen (MFE) are tied for the fullest planes in Texas, at 82.5%. Houston Intercontinental (IAH), Abilene (ABI) and Corpus Christi (CRP) come next. All 25 Texas airports with full data were ranked, and none were left out.

"How full" here means passengers divided by seats on departing flights over the latest 12 months. This is not the official load factor, which uses passenger-miles. It's also the weakest of the five scored inputs, because airlines' pricing and choice of aircraft shape it.

| # | Airport | Size class | Planes full | Capacity-need score | Passenger growth since 2019 | System delay rate |
|---|---|---|---|---|---|---|
| 1= | Dallas-Fort Worth (DFW) | large | 82.5% | 79.3 | 14.9% | 6.2% |
| 1= | McAllen (MFE) | small | 82.5% | 44.5 | 33.5% | 3.1% |
| 3 | Houston Intercontinental (IAH) | large | 79.9% | 70.4 | 6.5% | 6.5% |
| 4 | Abilene (ABI) | nonhub | 79.5% | 78.1 | 28.8% | 4.4% |
| 5 | Corpus Christi (CRP) | nonhub | 76.6% | 38.0 | 13.2% | 3.2% |

**What changes the picture:**
- **Full planes don't always mean a high score.** McAllen ties for the fullest planes, but the FAA forecasts its flights to fall by 9.8%. That puts its overall rank at 221 of 343. Corpus Christi's flight forecast is about flat (0.3%).
- **DFW and IAH are the strongest large-hub cases.** Both are flagged as strained and have the highest system delay rates on this list. That rate counts delays airlines put down to the airport and air-traffic system, and it includes ordinary weather. At IAH, flights have stayed flat while passengers grew.
- **Abilene depends on one airline.** It scores well (rank 26 overall), but Envoy Air carries 95.8% of its passengers. If Envoy cuts service, the forecast growth may not arrive.

I can also rank Texas by the full capacity-need score, or show these figures for the summer only.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years); FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: How full the planes are, Capacity-need score, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: ABI: single_airline

## B3 - Which large airports have planes over 85% full?

*Pass when:* Large hubs filtered by a load factor threshold.

*Result:* PASS

*Tool calls:* `rank_airports` {"size_classes": ["large"], "sort_by": "load_factor_pct", "min_value": 85, "limit": 30}; `rank_airports` {"size_classes": ["large"], "sort_by": "load_factor_pct", "limit": 5}

None of the 30 large hubs fills more than 85% of its seats. The highest is Newark (EWR) at 83.2%. "How full" here means passengers divided by seats on departing flights over the latest 12 months. That's not the official load factor, which uses passenger-miles and seat-miles.

These are the five fullest large hubs:

| Airport | How full | Seats vs 2019 | Passengers vs 2019 | Capacity-need score |
|---|---|---|---|---|
| Newark (EWR) | 83.2% | +2.2% | +1.0% | 80.7 |
| San Francisco (SFO) | 82.6% | -5.0% | -4.4% | 86.9 |
| Dallas-Fort Worth (DFW) | 82.5% | +15.8% | +14.9% | 79.3 |
| Atlanta (ATL) | 82.3% | -1.0% | -4.5% | 69.8 |
| Los Angeles (LAX) | 82.1% | -12.8% | -15.7% | 75.3 |

Points that affect how to read this:
- **SFO and LAX are flagged as "capacity was cut."** Both have fewer seats and fewer passengers than in 2019. Their full planes reflect fewer seats, not rising demand.
- **Newark has a legal flight cap** of 36 arrivals and 36 departures an hour. That limits how many more flights could be added, whatever the demand.
- **Dallas-Fort Worth is the strongest case for real demand.** Passengers are up 14.9% since 2019 and seats are up 15.8%, so its planes are full even with more seats.
- **This is the weakest of the five score inputs.** How full planes are depends on airline pricing and fleet choices, so it's only a rough proxy for unmet demand.

I can lower the cutoff (for example to 80%), check smaller airport classes for the 85% mark, or rank large hubs by the full capacity-need score.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: How full the planes are, Capacity-need score, FAA forecast flight growth; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - the answer uses proxy measures (scores, system delay rate, load factor or forecasts); EWR: legal limit; SFO: capacity cut; LAX: capacity cut
> Warnings printed: EWR: legal_limit, SFO: capacity_cut, LAX: capacity_cut

## B4 - Compare Portland and Providence.

*Pass when:* Asks which Portland (Oregon or Maine), or covers both and says so.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Portland"}; `find_airport` {"query": "Providence"}

Before I compare, which Portland do you mean: Portland, Oregon (PDX) or Portland, Maine (PWM)?

For Providence I'll use Rhode Island T.F. Green International (PVD). The same metro area also has Boston Logan (BOS) and Manchester-Boston Regional (MHT).

Portland, Maine is a small-hub airport like PVD, so it's the closer match by size. Portland, Oregon is a medium hub. If it helps, I can compare all three in one table.

> Data period: no data was used in this reply  
> Assumptions: none  
> Confidence: n/a - no data figures were used in this reply

## B5 - Which airports are the best candidates overall? Only count the ones with complete data.

*Pass when:* National ranking shown per size class.

*Result:* PASS

*Tool calls:* `rank_airports` {"sort_by": "total_score", "limit": 5}

Among the 343 airports with complete data, the top scorer by size class is **Orlando (MCO)** for large hubs, **Southwest Florida/Fort Myers (RSW)** for medium hubs, **Punta Gorda (PGD)** for small hubs (also #1 nationally) and **Rickenbacker (LCK)** for nonhubs. Florida takes 8 of the 20 places shown below.

The ranking is by size class because size isn't part of the score. Without that split, small leisure airports fill the top of a national list.

| Class | Airport | Score | National rank | Watch-outs |
|---|---|---|---|---|
| Large | Orlando (MCO) | 87.8 | 2 | None |
| Large | San Francisco (SFO) | 86.9 | 3 | Seats were cut, so full planes partly reflect fewer seats |
| Large | Chicago O'Hare (ORD) | 84.6 | 7 | Temporary summer 2026 flight cap |
| Large | New York JFK (JFK) | 84.0 | 9 | Slot-controlled: new capacity needs more slots |
| Large | Miami (MIA) | 83.0 | 10 | None |
| Medium | Fort Myers (RSW) | 81.7 | 12 | None |
| Medium | Charleston (CHS) | 78.8 | 22 | None |
| Medium | Jacksonville (JAX) | 75.8 | 38 | None |
| Small | Punta Gorda (PGD) | 94.9 | 1 | Allegiant carries 99.6% of passengers |
| Small | Northwest Arkansas (XNA) | 85.5 | 5 | None |
| Small | Orlando Sanford (SFB) | 85.2 | 6 | Allegiant carries 99.5% |
| Small | St Pete-Clearwater (PIE) | 84.1 | 8 | Allegiant carries 98.4% |
| Nonhub | Rickenbacker (LCK) | 85.7 | 4 | 44.2% of flights are cargo; Allegiant carries 99.7% |
| Nonhub | Traverse City (TVC) | 78.8 | 22 | None |

**Cleanest leads:** Orlando, Miami, Fort Myers, Charleston and Northwest Arkansas score high and have no warnings. Orlando also has a large FAA-forecast gain: 7,766,513 extra boardings a year by 2035.

**Read with care:**
- **JFK and O'Hare:** flight limits may stop added capacity from being used.
- **SFO:** the high score partly comes from cut seats rather than rising demand.
- **Allegiant airports:** most of the top small airports depend on one airline. If it pulls back, the forecast growth may not arrive.

The score (0-100) ranks how much added capacity would likely be filled, compared with other airports. It's a proxy for profit, not a return estimate: I have no cost data.

I can profile any of these airports, or rank a specific region or state.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, How full the planes are, FAA forecast passenger growth, FAA forecast flight growth; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - SFO: capacity cut; ORD: legal limit; JFK: legal limit; LCK: cargo heavy
> Warnings printed: ORD: legal_limit, JFK: legal_limit, SFO: capacity_cut, PGD: single_airline, SFB: single_airline, PIE: single_airline, LCK: cargo_heavy, LCK: single_airline, ABI: single_airline, BLV: single_airline, BQN: cargo_heavy, BQN: capacity_cut

## B6 - How has passenger traffic at Boston changed since 2019? Give me the year by year picture.

*Pass when:* Year by year values for Boston, with 2026 marked partial.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Boston"}; `airport_profile` {"airport_code": "BOS"}

Boston Logan (BOS) passenger traffic is back to about where it was in 2019, and no higher. Passengers in the latest 12 months (May 2025 - April 2026) were 1.2% above calendar 2019. Traffic peaked in 2024 and was slightly lower in 2025.

I took "Boston" to mean Logan. The area also has Manchester-Boston Regional (MHT) in New Hampshire and Providence's T.F. Green (PVD) in Rhode Island.

| Year | Passengers (departing flights) | How full the planes were |
|---|---|---|
| 2019 | 20,742,138 | 81.9% |
| 2020 | 6,050,302 | 52.0% |
| 2021 | 10,938,231 | 75.1% |
| 2022 | 17,472,973 | 78.5% |
| 2023 | 19,991,297 | 83.3% |
| 2024 | 21,280,480 | 83.1% |
| 2025 | 21,105,980 | 81.6% |
| 2026 (Jan-Apr only) | 6,139,216 | 78.2% |

What stands out:
- **Recovery took four years.** 2020 traffic was well under a third of 2019. Logan passed its 2019 level only in 2024.
- **Since 2024, traffic has been flat, not growing.** 2025 came in a little below 2024. The 2026 figure covers only four months, so don't compare it with the full years.
- **Fewer flights, bigger planes.** Passenger flights in 2025 were 3.1% below 2019, while passengers per flight rose from 106.4 to 111.9. Seats are up 1.4% on 2019, about the same as passengers.
- **"How full" is passengers divided by seats.** It isn't the official load factor. It's at 81.7% for the latest 12 months, below the 2023-24 highs.

For the investment question: Logan's flat passenger numbers count against it (it sits at the 40th percentile on growth since 2019). Strain does more to drive its high score: a 9.1% system delay rate puts it at the 99th percentile. Separately, the FAA forecasts 26.5% more boardings by 2035.

I can also break this down month by month to show the seasonal peaks. July 2025 was the busiest month, with 2,026,031 passengers.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); FAA passenger boarding data CY2025, calendar 2025; BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, How full the planes are, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; 'Boston' was taken to mean BOS; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - the answer uses proxy measures (scores, system delay rate, load factor or forecasts); an airport name was resolved by default

## B7 - Show me medium-size airports in the West with the fastest forecast passenger growth.

*Pass when:* West region, medium hubs, sorted by forecast passenger growth.

*Result:* PASS

*Tool calls:* `rank_airports` {"region": "west", "size_classes": ["medium"], "sort_by": "forecast_passenger_growth_pct", "limit": 10}

Portland (PDX) has the fastest FAA-forecast passenger growth among the West's medium-hub airports, at 33.2%. Oakland (OAK), San Jose (SJC) and Boise (BOI) come next. Of the top four, only Boise also has rising traffic today. These are the top 10 of 11 medium-hub airports in the West, all with full data.

| # | Airport | Forecast pax growth 2025-2035 | Extra boardings by 2035 | Pax growth since 2019 | Planes full | Score |
|---|---|---|---|---|---|---|
| 1 | Portland (PDX) | 33.2% | 2,989,548 | -6.4% | 82.0% | 72.3 |
| 2 | Oakland (OAK) | 29.9% | 1,402,276 | -35.5% | 74.2% | 46.0 |
| 3 | San Jose (SJC) | 29.6% | 1,620,865 | -35.0% | 73.9% | 44.7 |
| 4 | Boise (BOI) | 28.6% | 735,328 | 24.8% | 78.7% | 66.7 |
| 5 | Sacramento (SMF) | 24.7% | 1,682,362 | 3.8% | 76.5% | 52.0 |
| 6 | Anchorage (ANC) | 24.6% | 660,937 | 0.8% | 72.8% | 59.1 |
| 7 | Ontario (ONT) | 22.9% | 799,528 | 26.5% | 74.1% | 52.0 |
| 8 | Kahului (OGG) | 21.9% | 753,173 | -9.4% | 77.7% | 48.1 |
| 9 | Santa Ana (SNA) | 19.4% | 1,059,150 | 7.2% | 80.4% | 62.0 |
| 10 | Burbank (BUR) | 16.0% | 531,720 | -0.7% | 72.3% | 44.0 |

**Caveats that change the reading:**
- **The forecast is for ranking, not a prediction.** The FAA tends to forecast too high.
- **Oakland and San Jose are still about 35% below 2019 traffic.** Airlines cut seats there by about as much, so their forecasts partly describe a recovery, not demand for new space. Southwest carries 76.7% of Oakland's passengers. San Jose has a night noise curfew.
- **Portland and Kahului also have fewer seats than in 2019.** So Portland's full planes partly reflect cut capacity, not only rising demand.
- **Anchorage and Ontario carry a lot of cargo** (cargo is 56.6% and 36.2% of flights). Cargo shares the runways but isn't in the score.
- **Santa Ana has a legal cap** on passengers and departures, plus a night curfew.

Boise stands out as the cleanest case: strong forecast, real growth since 2019 and no data warnings. Portland has the highest total score and the most extra boardings forecast.

> Data period: FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: FAA forecast passenger growth, Capacity-need score, How full the planes are, FAA forecast flight growth; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - PDX: capacity cut; OAK: capacity cut; SJC: capacity cut, legal limit; ANC: cargo heavy
> Warnings printed: SJC: legal_limit, SNA: legal_limit, PDX: capacity_cut, OAK: single_airline, OAK: capacity_cut, SJC: capacity_cut, ANC: cargo_heavy, ONT: cargo_heavy, OGG: capacity_cut

## B8 - What's the busiest month at Burlington, Vermont, and how full are the planes then?

*Pass when:* The busiest month and its load factor.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Burlington, Vermont"}; `airport_trend` {"airport_code": "BTV", "metric": "load_factor_pct"}; `airport_trend` {"airport_code": "BTV", "metric": "passengers"}

At Burlington International (BTV) in Vermont, **October is the busiest month**. Planes are about **85% full** then: 84.9% across the last three Octobers and 86.9% in October 2025. So the busiest month is also one of the fullest.

**October in detail** (passengers on departing flights):
- Average October over 2023-2025: 73,848 passengers.
- October 2025: 79,157 passengers, the highest month in the last 36.
- October 2024: 74,742 passengers. October 2023: 67,645 passengers.

**How October compares with the rest of the year** (averaged over the last three years):

| Month | Passengers (avg) | Seats filled |
|---|---|---|
| July | 67,585 | 86.7% (fullest) |
| August | 70,578 | 85.5% |
| October | 73,848 | 84.9% |
| January | 45,791 | 80.1% (quietest) |
| Last 12 months, all months | - | 83.0% |

A few things to keep in mind:
- **July-October is BTV's peak season.** Traffic is highest in late summer and October, and planes are fullest in July. November drops off sharply.
- **What "seats filled" measures:** passengers divided by seats on departing flights. This is our proxy for unmet passenger demand, not the official load factor. It also depends on airline pricing and aircraft choice, which makes it the weakest input to our score.
- **The pattern is uneven from year to year.** Planes were fuller in 2023 than in 2024, then got fuller again in 2025. For example, October was 89.5% full in 2023, 79.2% in 2024 and 86.9% in 2025.

Background (not from our data): Vermont's fall-foliage season probably explains the October peak.

Overall, BTV ranks 6th of 78 small-hub airports on our capacity-need score (79.2). That score estimates how much added capacity would be filled, not profit.

> Data period: BTS T-100 airport-month summary, 2023-05 to 2026-04  
> Assumptions: proxies, not direct measurements: How full the planes are  
> Confidence: Medium - the answer uses proxy measures (scores, system delay rate, load factor or forecasts)

## C1 - Score the top 3 airports that have the highest congestion in August in the US.

*Pass when:* Ranks by the August system delay rate and says scores do not exist by month.

*Result:* PASS

*Tool calls:* `rank_airports` {"sort_by": "system_delay_rate_pct", "month": 8, "limit": 3}; `rank_airports` {"sort_by": "system_delay_rate_pct", "month": 8, "limit": 5}

Newark (EWR), Orlando (MCO) and San Juan (SJU) have the most August congestion. Their capacity-need scores are 80.7, 87.8 and 75.4. Two things matter for the third spot: San Juan ties with Aguadilla (BQN), and both are in Puerto Rico. If you leave out US territories, Boston (BOS) is third.

Here "congestion" means the system delay rate. That's the share of arriving flights delayed for reasons airlines code to the airport and air-traffic system, which includes ordinary weather. These figures are August only, with 2023, 2024 and 2025 added together. The capacity-need score runs from 0 to 100 and covers the latest period only, not August.

| Airport | Aug. system delay | Score (rank of 343) | Passenger side | Flight side | Planes full | Size class |
|---|---|---|---|---|---|---|
| Newark (EWR) | 10.9% | 80.7 (#13) | 72.7 | 88.6 | 83.2% | large |
| Orlando (MCO) | 10.3% | 87.8 (#2) | 81.5 | 94.0 | 81.9% | large |
| San Juan (SJU) | 9.8% | 75.4 (#41) | 77.6 | 73.3 | 84.6% | medium |
| Aguadilla (BQN), tied 3rd | 9.8% | 77.7 (#29) | 68.7 | 86.7 | 85.7% | nonhub |
| Boston (BOS), top non-territory after these | 9.3% | 82.9 (#11) | 72.2 | 93.6 | 81.7% | large |

**Caveats that change the reading:**
- **Newark:** the FAA caps it at 36 arrivals and 36 departures an hour. Adding terminal or runway capacity may not add flights unless that legal limit changes. Passengers are up only 1.0% since 2019.
- **Orlando:** the strongest case of the five. It ranks #2 nationally and has the highest FAA forecast growth here (28.2% for passengers, 26.4% for flights).
- **San Juan:** strong growth since 2019 (45.1% more passengers), but the FAA forecast is low (8.5% passenger growth).
- **Aguadilla:** cargo is 42.8% of its flights, and its seats were cut. Its full planes reflect fewer seats, not rising demand.

The ranking leaves out 59 airports with partial data and 104 with too few August flights to give a reliable delay rate.

> Data period: BTS Airline Delay Causes, August of 2023, 2024, 2025 (summed); BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: System delay rate, Capacity-need score, Passenger-side score, Flight-side score, How full the planes are, FAA forecast passenger growth; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - EWR: legal limit; the answer uses proxy measures (scores, system delay rate, load factor or forecasts); BQN: capacity cut, cargo heavy
> Warnings printed: EWR: legal_limit, BQN: cargo_heavy, BQN: capacity_cut

## C9 - Which large airports are most congested in summer?

*Pass when:* Ranks large hubs by the summer (June to August) system delay rate, using the season filter; Newark leads.

*Result:* PASS

*Tool calls:* `rank_airports` {"size_classes": ["large"], "sort_by": "system_delay_rate_pct", "season": "summer", "limit": 10}; `rank_airports` {"size_classes": ["large"], "sort_by": "total_delay_rate_pct", "season": "summer", "limit": 10}

Newark (EWR) is the most congested large airport in summer, with Orlando (MCO), New York JFK, Boston (BOS) and Denver (DEN) next. I measured congestion by the summer system delay rate: arrival delays that airlines blame on the airport and air-traffic system, divided by arriving flights. Airlines code this category themselves, and it includes ordinary weather. "Summer" means June-August of 2023, 2024 and 2025 combined. "Large" is the FAA large-hub class (30 airports).

| Rank | Airport | Summer system delay | Summer overall delay | Capacity-need score |
|---|---|---|---|---|
| 1 | Newark (EWR) | 13.2% | 27.5% | 80.7 |
| 2 | Orlando (MCO) | 10.6% | 32.1% | 87.8 |
| 3 | New York JFK (JFK) | 10.1% | 27.1% | 84.0 |
| 4 | Boston Logan (BOS) | 9.9% | 28.5% | 82.9 |
| 5 | Denver (DEN) | 9.7% | 27.0% | 76.7 |
| 6 | New York LaGuardia (LGA) | 9.5% | not in top 10 | 67.8 |
| 7 | Fort Lauderdale (FLL) | 9.0% | 30.1% | 80.5 |
| 8= | Chicago O'Hare (ORD) | 8.7% | not in top 10 | 84.6 |
| 8= | Miami (MIA) | 8.7% | 28.9% | 83.0 |
| 10 | Washington Reagan (DCA) | 8.2% | not in top 10 | 52.2 |

The overall delay rate counts arrivals 15 or more minutes late from any cause. On that measure Florida leads: Orlando 32.1%, Tampa (TPA) 30.3%, Fort Lauderdale 30.1%. Philadelphia (PHL) at 27.4% and Dallas-Fort Worth (DFW) at 26.8% also make that top 10.

**Warnings that change the investment picture:**
- **Legal limits on flights:** EWR, JFK, LGA and DCA have legal caps or slot limits, and ORD has a temporary cap for summer 2026. At these airports, new runway or gate capacity can't be used without more slots. At LGA and DCA the FAA flight forecast already assumes the slot limits.
- **Seats were cut:** FLL and PHL have fewer seats than in 2019, so their full planes reflect the cuts rather than rising demand.
- **Strongest candidates:** MCO, BOS, MIA and DEN combine heavy summer congestion with no flagged legal cap.

Next, I can show the summer peak month by month for any of these airports.

> Data period: BTS Airline Delay Causes, summer (June, July, August) of 2023, 2024, 2025 (summed) / 2023-08 to 2026-07 (three years); BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: System delay rate, Capacity-need score, How full the planes are, FAA forecast passenger growth, FAA forecast flight growth; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - EWR: legal limit; JFK: legal limit; LGA: forecast constrained, legal limit; FLL: capacity cut
> Warnings printed: EWR: legal_limit, JFK: legal_limit, LGA: legal_limit, ORD: legal_limit, DCA: legal_limit, LGA: forecast_constrained, FLL: capacity_cut, DCA: forecast_constrained, PHL: capacity_cut

## C10 - And is it the same ones in winter?

*Pass when:* A follow-up: ranks the same group for winter (December to February); San Francisco leads, so the answer is no.

*Result:* PASS

*Tool calls:* `rank_airports` {"size_classes": ["large"], "sort_by": "system_delay_rate_pct", "season": "winter", "limit": 10}; `rank_airports` {"size_classes": ["large"], "sort_by": "total_delay_rate_pct", "season": "winter", "limit": 10}

Mostly, but not entirely: 7 of the summer top 10 also make the winter top 10. The big change is San Francisco (SFO), which tops the winter list but wasn't in the summer top 10. As before, I ranked by the system delay rate, which counts delays airlines blame on the airport and air-traffic system and includes ordinary weather. "Winter" means December-February of 2023, 2024 and 2025 combined, across the 30 large hubs.

| Winter rank | Airport | Winter system delay | Winter overall delay | Summer system rank |
|---|---|---|---|---|
| 1 | San Francisco (SFO) | 11.6% | 25.5% | not in top 10 |
| 2 | Fort Lauderdale (FLL) | 9.7% | 25.5% | 7 |
| 3 | Newark (EWR) | 9.1% | not in top 10 | 1 |
| 4 | LaGuardia (LGA) | 9.0% | 21.7% | 6 |
| 5 | Miami (MIA) | 8.9% | 22.7% | 8= |
| 6 | Washington Reagan (DCA) | 8.5% | 22.4% | 10 |
| 7 | Orlando (MCO) | 7.8% | 23.0% | 2 |
| 8 | JFK | 7.4% | 21.8% | 3 |
| 9 | Tampa (TPA) | 7.3% | 22.5% | not in top 10 |
| 10= | Las Vegas (LAS) | 7.1% | not in top 10 | not in top 10 |

**What changes:**
- **Dropped out:** Boston (BOS), Denver (DEN) and Chicago O'Hare (ORD) are summer-only problems by this measure. Boston still has the 10th-highest winter overall delay rate (21.5%).
- **New:** SFO, Tampa and Las Vegas. San Diego (SAN) makes the winter overall-delay top 10 (22.1%) and has a night curfew.
- **Severity:** Winter is milder. The highest winter overall delay rate is 25.5%, against Orlando's 32.1% in summer.

**Takeaway:** Newark, Orlando, JFK, LaGuardia, Fort Lauderdale, Miami and Reagan are congested in both seasons. Of these, only Orlando and Miami have no flagged legal limit or seat cut.

SFO has the highest three-year system delay rate in either list (13.4%), but its seats are down 5.0% since 2019, so its full planes reflect fewer seats rather than rising demand.

Background (not from our data): SFO's winter delays are often linked to low cloud and fog limiting use of its closely spaced parallel runways.

> Data period: BTS Airline Delay Causes, winter (December, January, February) of 2023, 2024, 2025 (summed) / 2023-08 to 2026-07 (three years); BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: System delay rate, How full the planes are  
> Confidence: Medium - SFO: capacity cut; FLL: capacity cut; EWR: legal limit; LGA: forecast constrained, legal limit
> Warnings printed: EWR: legal_limit, LGA: legal_limit, DCA: legal_limit, JFK: legal_limit, SAN: legal_limit, SFO: capacity_cut, FLL: capacity_cut, LGA: forecast_constrained, DCA: forecast_constrained

## C2 - Where is Delta the dominant airline?

*Pass when:* Says airline-network questions are not supported; may offer the biggest-airline share per airport.

*Result:* PASS

*Tool calls:* `rank_airports` {"sort_by": "top_airline_share_pct", "size_classes": ["large", "medium"], "limit": 30}; `airport_profile` {"airport_code": "ATL"}; `airport_profile` {"airport_code": "MSP"}; `airport_profile` {"airport_code": "DTW"}; `airport_profile` {"airport_code": "SLC"}

I can confirm Delta is the biggest airline at four large hubs: Atlanta (ATL), Minneapolis-St Paul (MSP), Detroit (DTW) and Salt Lake City (SLC). This list isn't complete. Our data can't search or filter by airline. Each airport record only names its single biggest airline and that airline's share of passengers. So I picked these four from background knowledge and checked each one's profile.

| Airport | Delta's share of passengers (2025) | Capacity-need score | Rank among 30 large hubs |
|---|---|---|---|
| Atlanta (ATL) | 74.7% | 69.8 | 18 |
| Minneapolis-St Paul (MSP) | 58.0% | 64.8 | 23 |
| Salt Lake City (SLC) | 57.5% | 60.9 | 25 |
| Detroit (DTW) | 54.8% | 60.6 | 26 |

**What this means for capacity investment:**
- **Relying on one airline is a risk.** At all four, growth depends heavily on Delta's plans. Atlanta is the most concentrated: only Southwest's airports Dallas Love Field, Houston Hobby and Chicago Midway, plus Oakland, have a higher top-airline share among large and medium hubs.
- **Seats were cut at MSP and DTW.** Both have fewer seats than in 2019 (-7.2% and -6.7%), so their full planes partly reflect that cut rather than rising demand.
- **None of the four is strained.** Their system delay rates over three years are 2.8-4.6% (a delay category the airlines code themselves, which includes ordinary weather). So the FAA's forecast flight growth there is not called unmet demand.

I can't see who is biggest at other airports without checking each one. Other airports could also have Delta on top, such as New York JFK, LaGuardia, Boston, Seattle or smaller airports. Seattle (SEA), for example, has a top-airline share of 42.6%, but the ranking doesn't say which airline that is. I can check any of these one by one if you'd like.

> Data period: BTS T-100 Segment, calendar 2025; BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, How full the planes are, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; 'unmet flight demand' is an estimate from the FAA forecast, used only when the airport is strained today; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - DAL: legal limit; OAK: capacity cut; ANC: cargo heavy; EWR: legal limit
> Warnings printed: DAL: legal_limit, EWR: legal_limit, SJC: legal_limit, DAL: single_airline, HOU: single_airline, MDW: single_airline, OAK: single_airline, OAK: capacity_cut, ANC: cargo_heavy, MSP: capacity_cut, SJC: capacity_cut, DTW: capacity_cut, : more

## C3 - How many flights go from JFK to London?

*Pass when:* Declines: route-level questions are not supported.

*Result:* PASS

*Tool calls:* `airport_profile` {"airport_code": "JFK"}

I can't tell you how many JFK flights go to London. This system has no route or destination data. The closest figure I have is JFK's long-haul flights in total, without a breakdown by destination.

**John F Kennedy International (JFK), calendar 2025, departing flights:**

| Cutoff (our definition) | Long-haul passenger flights | Share of passenger flights |
|---|---|---|
| 2,000+ miles | 96,455 | 45.4% |
| 2,500+ miles | 60,217 | 28.4% |
| 3,000+ miles | 49,841 | 23.5% |

JFK had 212,394 departing passenger flights in 2025. These counts include both domestic and international flights on all airlines. Domestic flights carried 45.6% of departing passengers.

Background (not from our data): London is more than 3,000 miles from New York, so JFK-London flights fall in the 3,000+ mile bucket. That bucket also includes many other long-haul routes, so it doesn't tell you the London count.

**Why this matters for capacity:** Using the 3,000-mile cutoff, almost a quarter of JFK's passenger flights are long-haul. JFK's capacity-need score is 84.0, ranking it 4th of 30 large hubs. However, the FAA limits flight slots at JFK, so more runway or gate space can't be used unless more slots are granted.

To get London flight counts, you'd need route-level data such as BTS T-100 Segment filtered by destination. I can't query that here. I can show JFK's long-haul share at a different cutoff, or compare it with Newark (EWR) or LaGuardia (LGA).

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA passenger boarding data CY2025, calendar 2025; BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score; long-haul means 3,000 miles or more (our definition; adjustable); scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - JFK: legal limit; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: JFK: legal_limit

## C4 - What's the congestion level at Teterboro?

*Pass when:* Says Teterboro is outside the covered airports; no invented number.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Teterboro"}

I don't have congestion data for Teterboro. It isn't one of the 402 FAA primary airports this dataset covers, so I have no delay rates or scores for it.

Background (not from our data): Teterboro is mainly a private and business jet airport. It has almost no scheduled airline service, and the delay data I use only covers scheduled airline flights.

Here is what I can do instead:
- **Compare the New York-area primary airports on congestion:** Newark (EWR), LaGuardia (LGA) and JFK. Congestion here means the three-year system delay rate, the system delay rate for the latest 12 months and the overall delay rate. The system delay category is coded by the airlines and includes ordinary weather.
- **Give a full profile of one of those airports:** delay causes, how full the planes are, the FAA growth forecast and its capacity-need score.

Should I compare those three?

> Data period: no data was used in this reply  
> Assumptions: none  
> Confidence: n/a - no data figures were used in this reply

## C5 - Which airports were the top expansion candidates in 2021?

*Pass when:* Says the score exists for the latest period only; offers raw 2021 metrics.

*Result:* PASS

*Tool calls:* `rank_airports` {"year": 2021, "sort_by": "load_factor_pct", "limit": 5}; `rank_airports` {"year": 2021, "sort_by": "system_delay_rate_pct", "limit": 5}

I can't rank 2021 expansion candidates. The capacity-need score only exists for the latest period, so there's no 2021 score. What I can show is the two main raw signals for calendar 2021: how full the planes were and the system delay rate.

**Fullest planes in 2021** (passengers divided by seats on departing flights)

| Airport | 2021 | Latest 12 months | Score today |
|---|---|---|---|
| McAllen (MFE) | 84.4% | 82.5% | 44.5 |
| Wilkes-Barre/Scranton (AVP) | 84.3% | 82.1% | 71.3 |
| Aguadilla (BQN) | 83.8% | 85.7% | 77.7 |
| Ponce (PSE) | 82.3% | 83.8% | 75.5 |
| Hartford Bradley (BDL) | 82.2% | 81.3% | 65.9 |

**Highest system delay rate in 2021** (delays airlines blamed on the airport and air-traffic system, per arriving flight)

| Airport | 2021 | Last three years | Score today |
|---|---|---|---|
| Key West (EYW) | 11.5% | 8.0% | 67.7 |
| Punta Gorda (PGD) | 10.0% | 8.6% | 94.9 (#1 overall) |
| Newark (EWR) | 8.8% | 10.4% | 80.7 |
| Dallas Love Field (DAL) | 8.4% | 4.9% | 42.8 |
| Aguadilla (BQN) | 8.4% | 6.6% | 77.7 |

**Caveats that change the reading**
- **Full planes partly reflect seat cuts:** At AVP, BQN and PSE, airlines cut seats compared with 2019, so planes look full because there are fewer seats, not because demand rose.
- **Legal caps:** Newark has a flight cap (36 arrivals and 36 departures an hour). Love Field is limited to 20 gates by federal law.
- **One airline dominates:** Allegiant carries 99.6% of passengers at Punta Gorda and Southwest 96.8% at Love Field.
- **Other warnings:** BQN is cargo-heavy (42.8% of flights). PSE's delay figures rest on a small sample.
- **Weather counts too:** The system delay category is coded by airlines and includes ordinary weather.

I can also rank 2021 by passenger numbers or overall delay rate, by size class or region, or compare any of these airports' year-by-year history since 2019.

> Data period: BTS T-100 airport-month summary, calendar 2021 / 2025-05 to 2026-04 (latest 12 complete months); BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / calendar 2021; FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: How full the planes are, Capacity-need score, System delay rate; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - 1 of the 5 listed airports has weaker data (PSE: small delay sample); AVP: capacity cut; BQN: capacity cut, cargo heavy; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: EWR: legal_limit, DAL: legal_limit, AVP: capacity_cut, BQN: cargo_heavy, BQN: capacity_cut, PSE: small_sample, PSE: capacity_cut, PSE: small_airport_forecast, PGD: single_airline, DAL: single_airline

## C6 - Should we invest in expanding LaGuardia?

*Pass when:* Gives the evidence and the slot limit; leaves the decision to the analyst.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "LaGuardia"}; `airport_profile` {"airport_code": "LGA"}

I can't make the investment decision for you, and I have no cost or return data. Based on the data I do have, LaGuardia (LGA) has one of the worst congestion levels in the country, but its legal limits mean extra space would probably not lead to many more flights. Its overall score is mid-pack: **67.8, ranking 19th of 30 large hubs** (76th of 343 overall).

**What makes the case:**
- **Congestion is severe:** 8.4% of arriving flights had a system delay over three years, which beats about 98% of airports. The rate was 10.4% in the latest 12 months, and that is not a recent spike. Airlines code this delay type themselves, and it includes ordinary weather. Overall, 21.5% of arrivals were 15 or more minutes late.
- **System delays are the biggest delay cause**, at 39.3% of delayed flights.
- **Planes are fairly full:** about 80.8% of seats are filled, which beats about 79% of airports.
- **The FAA forecasts about 3.0 million more boardings a year by 2035.** That is 18.4% growth, close to the middle of the pack.

**What weakens it:**
- **Legal limits:** the FAA caps flights at LGA with slots, and nonstop flights are limited to 1,500 miles. The FAA forecast already assumes these limits, so the 9.3% forecast growth in flights is not a measure of true demand.
- **Growth has come from bigger planes, not more flights:** passenger flights are down 4.8% since 2019, while passengers per flight rose from 85.3 to 94.7. Passengers have grown only 4.7% since 2019.
- **The biggest airline is Delta**, with 23.8% of passengers.

The "unmet flight demand" of 33,029 extra takeoffs and landings by 2035 is an FAA-based estimate, not a measurement, and the FAA tends to over-forecast.

Background (not from our data): LaGuardia's terminals were recently rebuilt. The score doesn't know about capacity that has already been built.

**What to check next:** whether the slot rules or distance limit are likely to change, how full the gates and terminals are, and how LGA compares with JFK and Newark (EWR). I can run that comparison if you want.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); FAA passenger boarding data CY2025, calendar 2025; BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, How full the planes are, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; 'unmet flight demand' is an estimate from the FAA forecast, used only when the airport is strained today; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - LGA: forecast constrained, legal limit; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: LGA: legal_limit, LGA: forecast_constrained

## C7 - What will a new terminal at Denver cost, and what return would we get?

*Pass when:* Declines cost and return; offers the capacity-need evidence.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Denver"}

I can't tell you what a new terminal at Denver International (DEN) would cost or return. There's no cost, revenue or return data in this system. What I can show is how much of any added capacity would likely be used, which our capacity-need score is built to measure. It's only a stand-in for profit, not a financial estimate.

**Denver (DEN), large hub**

| Measure | Value |
|---|---|
| Capacity-need score (0-100) | 76.7 (12th of 30 large hubs, 33rd of 343 ranked airports) |
| Passenger-side / flight-side score | 76.7 / 76.7 |
| Load factor (share of seats filled) | 81.2% |
| Passenger growth since 2019 | 18.8% |
| Seats added since 2019 | 26.1% |
| FAA forecast passenger growth, 2025-2035 | 23.7% (about 9.5 million extra boardings a year) |
| FAA forecast flight growth, 2025-2035 | 14.7% |
| System delay rate (3 years) | 6.6% |
| Boardings, 2025 | 39,976,695 |

**What this means:** Denver is rated as strained today. Its planes are fairly full, passenger numbers have grown well since 2019 even as airlines added seats, and the FAA expects strong further growth. The system delay rate is a category that airlines code themselves, and it includes ordinary weather, so it only roughly measures congestion. There's also no evidence that airlines cut capacity here. Overall, the data suggests added capacity would be well used. Whether a terminal would pay off depends on cost and financing, which aren't in our data.

**Worth checking outside this system:** the airport's capital plan and current construction, gate and terminal use, and airline agreements. We don't have those either.

I can pull Denver's full profile (delay causes, the trend in the latest 12 months, flight-demand estimate) or compare it with other large hubs if that would help.

> Data period: see the tool trace  
> Assumptions: proxies, not direct measurements: Capacity-need score, Passenger-side score, Flight-side score; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - the answer uses proxy measures (scores, system delay rate, load factor or forecasts)

## C8 - What is the delay rate at Glacier Park airport in Kalispell, and can I trust it?

*Pass when:* Resolves Glacier Park to FCA, gives the rate and the sample size.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Glacier Park, Kalispell"}; `find_airport` {"query": "FCA"}; `airport_profile` {"airport_code": "FCA"}

Glacier Park International (FCA) has a **system delay rate of 4.0%** and an **overall delay rate of 16.6%**. Both cover August 2023 to July 2026. You can rely on them as a fair three-year picture, but read them with the limits below.

The name search didn't find "Glacier Park, Kalispell", but the code FCA did. The FAA code for the same airport is GPI.

| Measure | Value |
|---|---|
| System delay rate, 3 years | 4.0% |
| System delay rate, latest 12 months | 4.7% |
| Overall delay rate (15+ min late, any cause), 3 years | 16.6% |
| Arriving flights behind these rates | 15,601 |
| Position among the 343 ranked airports (0-100) | 49.1, about the middle |

**Why the numbers are reasonably solid**
- The airport has full data and no data warnings.
- The rates rest on 15,601 arriving flights, so a few bad days don't move them much.
- The yearly system delay rate has been steady: 3.1% (2023), 3.9% (2024), 3.9% (2025).

**What to keep in mind**
- **Who is counted:** only domestic flights of the larger airlines that report delays, not every flight at FCA.
- **Airlines choose the cause:** the "system" category is coded by the airlines and includes ordinary weather. It mostly reflects congestion, but not only. In the overall delay rate, most delays are blamed on the airline itself (42.9%) or on late incoming aircraft (28.5%). Airport and air-traffic system causes account for 24.1%.
- **Latest year:** 4.7% is above the three-year 4.0%. The data doesn't flag it as a recent spike, but one year varies a lot, which is why the score uses the three-year rate.

So FCA is not congested by this measure. Its high capacity-need score (76.3) comes mostly from the passenger side: planes are 85.7% full and passengers are up 57.0% since 2019.

I can also show the delay rate month by month to check for seasonal patterns.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, Passenger-side score, System delay rate; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
