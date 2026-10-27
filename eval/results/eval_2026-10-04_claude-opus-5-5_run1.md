# Evaluation run - 2026-10-04 15:51 - claude-opus-5-5

**23 of 24 questions passed.** 847 numbers appeared in the answers; 0 answers ended with a number that could not be traced to a tool result; 1 answers passed only after one automatic rewrite. Average 12.3s per question; 680,833 input and 23,996 output tokens in total.

| Id | Group | Result | Tools | Number check | Seconds |
|---|---|---|---|---|---|
| A1 | core | PASS | rank_airports | passed | 13.3 |
| A2 | core | PASS | find_airport, find_airport, compare_airports | passed | 14.0 |
| A6 | follow-up | PASS | compare_airports | passed | 11.8 |
| A3 | core | PASS | find_airport, airport_profile | rewritten | 16.3 |
| A7 | follow-up | PASS | airport_profile | passed | 8.1 |
| A4 | core | PASS | airport_profile | passed | 11.3 |
| A5 | follow-up | FAIL | find_airport, compare_airports, airport_profile | passed | 13.3 |
| A8 | follow-up | PASS | find_airport, airport_profile | passed | 12.0 |
| B1 | filters | PASS | rank_airports | passed | 10.9 |
| B2 | filters | PASS | rank_airports | passed | 10.1 |
| B3 | filters | PASS | rank_airports, rank_airports | passed | 13.0 |
| B4 | ambiguous | PASS | find_airport, find_airport | passed | 6.3 |
| B5 | filters | PASS | rank_airports | passed | 12.1 |
| B6 | time | PASS | find_airport, airport_profile | passed | 11.9 |
| B7 | filters | PASS | rank_airports | passed | 11.7 |
| B8 | time | PASS | find_airport, airport_trend, airport_trend | passed | 12.0 |
| C1 | time | PASS | rank_airports | passed | 11.4 |
| C2 | out of scope | PASS | rank_airports, airport_profile, airport_profile, airport_profile, airport_profile | passed | 25.3 |
| C3 | out of scope | PASS | airport_profile | passed | 11.5 |
| C4 | out of scope | PASS | find_airport | passed | 6.9 |
| C5 | out of scope | PASS | rank_airports, rank_airports | passed | 13.0 |
| C6 | judgment | PASS | find_airport, airport_profile | passed | 13.0 |
| C7 | out of scope | PASS | find_airport | passed | 10.1 |
| C8 | awkward data | PASS | find_airport, find_airport, airport_profile | passed | 15.4 |

## A1 - Which airports in New England are strong candidates for terminal expansion?

*Pass when:* A ranked list from the six states, scores shown, reasons given.

*Result:* PASS

*Tool calls:* `rank_airports` {"region": "new england", "limit": 10}

Boston Logan (BOS), Burlington (BTV) and Portland, Maine (PWM) stand out on our capacity-need score, with Bangor (BGR) close behind. Hartford's Bradley (BDL) scores lower but has the second-largest forecast passenger gain in absolute terms. For terminal expansion the passenger side matters most, but we have no data on gates or how fully terminals are used, so this is a ranking of likely upside, not a measure of terminal shortage.

| Airport | Size class | Score | Passenger side | Planes full | Passengers vs 2019 | FAA forecast passengers | Extra boardings by 2035 |
|---|---|---|---|---|---|---|---|
| Boston (BOS) | large | 82.9 | 72.2 | 81.7% | +1.2% | +26.5% | 5,612,088 |
| Burlington (BTV) | small | 79.2 | 73.7 | 83.0% | +2.3% | +22.9% | 163,754 |
| Portland ME (PWM) | small | 77.4 | 79.2 | 82.8% | +17.2% | +21.6% | 278,078 |
| Bangor (BGR) | nonhub | 71.8 | 78.0 | 80.4% | +40.8% | +24.1% | 103,055 |
| Hartford (BDL) | medium | 65.9 | 60.8 | 81.3% | −2.7% | +15.7% | 523,236 |

**Key points:**
- **BOS** is the clearest case. It is strained today, with a 9.1% system delay rate over three years. It ranks 6th of 30 large airports and has by far the biggest forecast gain in passengers.
- **BTV** is also strained (5.5% system delay rate) and ranks 6th of 78 small-hub airports. However, its passenger numbers are barely above 2019.
- **PWM** has the strongest passenger side in the region. Its flight count has stayed flat while passengers rose, which suggests airlines are using bigger or fuller planes. That points more to terminal pressure than to runway pressure.
- **BGR** has grown fastest since 2019 (+40.8%), but seats rose even more (+48.8%).

**Caveats:**
- The FAA tends to over-forecast, so its growth figures are better used to compare airports than as predictions.
- The "planes full" share is the weakest of the score's inputs.
- Four airports have only partial data and no score, so they were left out: New Haven (HVN), Cape Cod Gateway (HYA), Block Island (BID) and Westerly (WST).
- The island airports, Nantucket (ACK) and Martha's Vineyard (MVY), scored 59.1 and 57.0. Their planes are less full (63.3% and 61.0%), and MVY's forecast is less reliable because the airport is so small.

**Next checks:** gate counts, how much of each terminal is used, and existing construction plans. None of these are in our data.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years); FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, Passenger-side score, How full the planes are, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - 1 of the 10 listed airports have weaker data (PSM: small delay sample); MVY: small airport forecast; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: MVY: small_airport_forecast, PSM: small_sample, PSM: small_airport_forecast

## A2 - Compare LA and Santa Ana airport congestion levels.

*Pass when:* LAX vs SNA side by side, a clear verdict, Santa Ana's legal cap flagged.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "LA"}; `find_airport` {"query": "Santa Ana"}; `compare_airports` {"airport_codes": ["LAX", "SNA"]}

I read "LA" as Los Angeles International (LAX). The area also has Ontario (ONT), Hollywood Burbank (BUR) and Long Beach (LGB). Santa Ana is John Wayne/Orange County (SNA).

**LAX is more congested than SNA on every delay measure, but not by much.** Its three-year system delay rate is 0.9 percentage points higher (about 1.23 times SNA's rate).

| Measure | LAX | SNA | Difference |
|---|---|---|---|
| System delay rate, 3 years | 4.8% | 3.9% | +0.9 pts |
| System delay rate, latest 12 months | 5.0% | 4.3% | +0.7 pts |
| Overall delay rate, 3 years (15+ min late) | 18.9% | 17.5% | +1.4 pts |
| System share of all delays | 25.7% | 22.4% | — |
| Late-aircraft share of all delays | 33.4% | 39.9% | — |

**What these numbers mean**
- **System delay rate:** our closest measure of congestion. It counts arrival delays blamed on the airport and air-traffic system, as a share of arriving flights. Airlines code this category themselves, and it includes ordinary weather, so it is mostly congestion but not purely. It also covers only domestic flights on the larger reporting airlines.
- **Rising delays:** both airports are slightly more delayed in the latest year than over three years.
- **Neither airport counts as strained** by our measure.
- **Causes:** at both, most delays come from airline causes and late-arriving aircraft rather than the system. SNA's delays lean more toward knock-on delays from late aircraft.

**Warnings that change how to read this**
- **SNA has a legal cap.** A settlement agreement caps passengers at 12.2 or 12.5 million a year (arriving plus departing; which figure applies isn't verified). That is about 6.1–6.25 million in our departing-only counts. SNA had 5,590,354 departing passengers in the latest 12 months, which is already close to the cap. It also has a limit of 95 average daily departures and a night curfew. So low delays there may partly reflect the cap holding traffic down, not spare capacity.
- **LAX has cut capacity.** Seats are down 12.8% since 2019 and passengers are down 15.7%. Its congestion comes with fewer flights, not growing demand.

I can also compare all five LA-area airports on these measures if that would help.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: System delay rate; 'LA' was taken to mean LAX  
> Confidence: Medium - LAX: capacity cut; SNA: legal limit; the answer uses proxy measures (scores, system delay rate, load factor or forecasts); an airport name was resolved by default
> Warnings printed: SNA: legal_limit, LAX: capacity_cut

## A6 - And how did congestion at those two look in 2023?

*Pass when:* Uses the same two airports without being told again, and 2023 values.

*Result:* PASS

*Tool calls:* `compare_airports` {"airport_codes": ["LAX", "SNA"], "year": 2023}

**In 2023 both airports were more congested than they are today, and the gap between them was wider.** LAX's system delay rate was 1.4 percentage points above SNA's (about 1.33 times as high). On the latest 12 months the gap is 0.7 points.

| Calendar 2023 | LAX | SNA | Difference |
|---|---|---|---|
| System delay rate | 5.6% | 4.2% | +1.4 pts |
| Overall delay rate (15+ min late) | 20.5% | 18.5% | +2.0 pts |
| Departing passengers | 37,119,938 | 5,725,328 | — |

**How 2023 compares with now**
- **LAX:** its 2023 system delay rate of 5.6% is above its latest-12-month rate of 5.0% and its three-year rate of 4.8%. Its 2023 overall delay rate of 20.5% is also above the three-year 18.9%. LAX congestion has eased somewhat.
- **SNA:** its 2023 system delay rate of 4.2% is about the same as the latest 12 months (4.3%). Its 2023 overall delay rate of 18.5% is a little above the three-year 17.5%. SNA has been roughly flat.

**Caveats**
- **Different time windows:** the 2023 figures are for one calendar year. Today's figures cover the latest 12 months and the three years 2023-08 to 2026-07, so the windows overlap and aren't exact like-for-like comparisons.
- **Same definition as before:** the system delay category is coded by airlines, includes ordinary weather, and covers domestic flights on the larger reporting airlines only.
- **Delay causes aren't available for 2023** through this view, so I can't say whether the mix of causes changed.
- **No 2023 scores:** the capacity-need score exists only for the latest period, so only the raw numbers are shown.
- **SNA had more passengers in 2023 than now:** 5,725,328 departing passengers, against 5,590,354 in the latest 12 months. Both are near the roughly 6.1–6.25 million departing-passenger cap. That cap applies to 2026–2030; 2023 came under the earlier terms of the agreement.

I can also pull the month-by-month system delay rate for either airport from 2019 onward, to show when the easing at LAX happened.

> Data period: BTS T-100 airport-month summary, calendar 2023; BTS Airline Delay Causes, calendar 2023; BTS T-100 Segment, calendar 2023  
> Assumptions: proxies, not direct measurements: System delay rate  
> Confidence: Medium - LAX: capacity cut; SNA: legal limit; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: SNA: legal_limit, LAX: capacity_cut

## A3 - What is the percentage of long haul flights out of Anchorage airport?

*Pass when:* One number, the 3,000-mile definition stated, the cargo-included number next to it.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Anchorage airport"}; `airport_profile` {"airport_code": "ANC"}

At Ted Stevens Anchorage International (ANC), **2.8% of departing passenger flights** in 2025 flew 3,000 miles or more. If you count cargo flights too, the share rises to **31.0%**. The big gap comes from cargo, which makes up 56.6% of ANC's departing flights, and much of that cargo flies long distances.

I assumed you meant ANC. Anchorage also has Merrill Field (MRI), a much smaller nonhub airport with only partial data.

There's no official definition of "long-haul," so 3,000 miles is our default. Here is the share at other cutoffs (departing flights, domestic plus international, all airlines, calendar 2025):

| Cutoff | Passenger flights | All flights incl. cargo |
|---|---|---|
| 2,000 mi | 13.7% (5,239 flights) | 47.4% (41,732) |
| 2,500 mi | 9.8% (3,723) | 43.2% (37,969) |
| 3,000 mi | 2.8% (1,061) | 31.0% (27,305) |

The base is 38,150 passenger flights and 87,988 flights in total, of which 49,838 were cargo or other non-passenger flights.

**Why this matters for capacity:**
- **Passenger traffic is mostly domestic.** 98.6% of passengers fly to US destinations, and Alaska Airlines carries 61.4% of them.
- **Cargo isn't in the capacity-need score,** but it uses the same runways. The FAA flight forecast also includes cargo. For a runway or airfield investment at ANC, the cargo-included share is probably the more useful figure. For a passenger terminal, use the passenger-only share.

Background (not from our data): Anchorage is a major refuelling and transfer point for transpacific air cargo between Asia and North America, which explains its many long cargo flights.

I can also run the share at a different cutoff distance if you need it.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; FAA passenger boarding data CY2025, calendar 2025; BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, FAA forecast passenger growth, FAA forecast flight growth; long-haul means 3,000 miles or more (our definition; adjustable); 'Anchorage airport' was taken to mean ANC; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - ANC: cargo heavy; the answer uses proxy measures (scores, system delay rate, load factor or forecasts); an airport name was resolved by default
> Warnings printed: ANC: cargo_heavy

## A7 - What if long-haul means over 2,300 miles?

*Pass when:* Recomputed at 2,300 miles for Anchorage.

*Result:* PASS

*Tool calls:* `airport_profile` {"airport_code": "ANC", "long_haul_miles": 2300}

With a 2,300-mile cutoff, **12.6% of departing passenger flights** at Anchorage (ANC) in 2025 counted as long-haul (4,820 of 38,150). Counting cargo flights too, the share is **46.5%** (40,947 of 87,988).

One small definition point: the tool counts flights of **2,300 miles or more**, so "at least" rather than strictly "over". The difference only matters for flights of exactly 2,300 miles.

Here is how the share changes with the cutoff (departing flights, domestic plus international, all airlines, calendar 2025):

| Cutoff | Passenger flights | All flights incl. cargo |
|---|---|---|
| 2,000 mi | 13.7% | 47.4% |
| **2,300 mi** | **12.6%** | **46.5%** |
| 2,500 mi | 9.8% | 43.2% |
| 3,000 mi | 2.8% | 31.0% |

**What this shows:**
- **Most of ANC's long passenger flights are between 2,300 and 3,000 miles.** The passenger share stays near 13–14% up to 2,300 miles, then falls steeply by 3,000. So the answer depends heavily on where you put the cutoff.
- **The cargo-included share stays high at every cutoff,** because cargo is 56.6% of ANC's flights. Cargo isn't in the capacity-need score, but it uses the same runways. That makes the cargo-included figure the more relevant one for airfield capacity.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score; long-haul means 2,300 miles or more (our definition; adjustable); scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - ANC: cargo heavy; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: ANC: cargo_heavy

## A4 - What is the unmet flight demand in SFO airport and why?

*Pass when:* An estimate named as an estimate or proxy, with the why from the delay data.

*Result:* PASS

*Tool calls:* `airport_profile` {"airport_code": "SFO"}

San Francisco International (SFO) has an estimated **unmet flight demand of 108,307 extra takeoffs and landings a year by fiscal 2035**. That is a 26.7% rise in the FAA forecast, from 406,220 operations in fiscal 2025 to 514,527 in fiscal 2035. This is an estimate, not a measurement. We only call it "unmet" because SFO is strained today: its system delay rate is in the top quarter of airports with full data. Note that the FAA tends to forecast too high, and its figures count takeoffs plus landings, including cargo flights.

**Why it counts as unmet: the airfield is already congested**
- **System delay rate (three years):** 13.4%, the highest among full-data airports (position 100 of 100). It's worse over the latest 12 months: 17.3%.
- **Overall delay rate:** 27.4% of arriving flights were 15 or more minutes late.
- **Delay causes:** 48.9% of delayed flights were blamed on the airport and air-traffic system, against 24.7% on the airline, 23.7% on late-arriving aircraft and 2.5% on extreme weather. Airlines assign this "system" category themselves, and it includes ordinary weather, so it mostly reflects congestion but not only that.
- **Trend:** the system delay rate went from 3.7% in 2022 to 15.2% in 2024 and 21.5% so far in 2026 (partial year).

Background (not from our data): SFO's parallel runways sit very close together. In fog or low cloud they can't be used side by side, so the arrival rate drops, which fits the high share of system delays.

**Caveats**
- **Capacity was cut:** seats are down 5.0% since 2019 and passenger flights down 11.0%, while passengers are down 4.4%. Planes are 82.6% full partly because there are fewer seats, not only because demand is rising.
- **Schedules are coordinated:** the FAA coordinates SFO's schedules (Level 2), but this is not a hard legal cap.
- **One dominant airline:** United carries 44.8% of passengers.

SFO ranks 3rd of 343 airports overall, with a capacity-need score of 86.9 and a flight-side score of 97.1. Before acting, check how much airfield capacity the runway layout can physically add. Our data doesn't cover that.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, Flight-side score, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; 'unmet flight demand' is an estimate from the FAA forecast, used only when the airport is strained today; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - SFO: capacity cut; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: SFO: capacity_cut

## A5 - How does that compare with Oakland?

*Pass when:* Oakland is not called unmet demand, because it is not strained.

*Result:* FAIL - failed: says /not strained|isn't strained|is not strained|not called|rather than unmet|not unmet|doesn't qualify|does not qualify|forecast growth|forecast flight growth/

*Tool calls:* `find_airport` {"query": "Oakland"}; `compare_airports` {"airport_codes": ["SFO", "OAK"]}; `airport_profile` {"airport_code": "OAK"}

I took Oakland to mean Oakland San Francisco Bay (OAK). The metro area also has San Jose (SJC). Oakland has **no unmet flight demand** by our definition. The FAA still forecasts 30,637 extra takeoffs and landings a year by fiscal 2035 (+24.8%). But Oakland isn't congested, so that growth looks like something its runways can absorb. SFO's figure is 108,307 extra a year, 3.54 times Oakland's, and SFO is already strained.

| | SFO | OAK |
|---|---|---|
| Capacity-need score | 86.9 (rank 3 of 343) | 46.0 (rank 208 of 343) |
| System delay rate, 3 years | 13.4% | 2.3% |
| System delay rate, latest 12 months | 17.3% | 1.7% |
| Overall delay rate | 27.4% | 18.4% |
| Share of delays blamed on airport/air-traffic system | 48.9% | 12.3% |
| How full the planes are | 82.6% | 74.2% |
| Passenger change since 2019 | -4.4% | -35.5% |
| Seat change since 2019 | -5.0% | -31.5% |
| Cargo share of flights | 1.2% | 17.9% |
| Biggest airline's share | United 44.8% | Southwest 76.7% |

**Why the two differ:**
- **Delays at Oakland come from airlines, not the airfield.** 54.1% of its delays are from late-arriving aircraft and 32.5% are blamed on the airline. That points to delays carried over from other airports, not to Oakland's own runways or air traffic control. Airlines assign these categories themselves, and the "system" category includes ordinary weather.
- **Oakland's traffic is shrinking.** Passengers fell from 6,769,962 in 2019 to 4,561,915 in 2025, and passenger flights are down 32.2% since 2019. Airlines cut seats about as fast as passengers fell, so the planes are not unusually full.
- **The FAA's 2025 starting point looks high.** It forecasts 4,685,425 boardings for Oakland in fiscal 2025, while the latest 12 months show 4,366,089 passengers. The two figures aren't counted the same way, but this fits the FAA's tendency to forecast too high.

**Risks at Oakland:** cargo makes up almost a fifth of flights and isn't counted in the score, and three-quarters of passengers fly one airline.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); FAA passenger boarding data CY2025, calendar 2025; BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, How full the planes are, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; 'unmet flight demand' is an estimate from the FAA forecast, used only when the airport is strained today; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - SFO: capacity cut; OAK: capacity cut; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: SFO: capacity_cut, OAK: capacity_cut

## A8 - Is Memphis a good candidate, given its cargo traffic?

*Pass when:* Uses the Memphis profile and the cargo share.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Memphis"}; `airport_profile` {"airport_code": "MEM"}

**Memphis (MEM) is a middling candidate for passenger capacity.** It scores 59.5 and ranks 46th of 78 small-hub airports (116th of 343 overall). Most of that score comes from the flight side (73.7), and cargo probably drives much of it. The passenger side, which is what a terminal would serve, is weak at 45.4.

**What cargo changes**
- Cargo flights are 65.1% of departures. Cargo isn't counted in the score, but it uses the same runways.
- The FAA forecast of 18.4% more takeoffs and landings by 2035 (about 29,600 extra) includes cargo. So this figure can't tell you how much of that growth would come from passenger airlines.
- The system delay rate is 4.9% over three years and 5.1% in the latest 12 months. That places Memphis at position 74 of 100 among the ranked airports. The rate is coded by airlines, includes ordinary weather and only covers delays to passenger flights. Memphis isn't classed as "strained," so the forecast is labelled as growth, not as unmet demand.

**Passenger side**
| Metric | Value |
|---|---|
| Planes full (passengers ÷ seats) | 73.4% (77.6% in 2019) |
| Passenger growth since 2019 | 0.9% |
| Seat change since 2019 | 6.7% |
| Passenger flights vs 2019 | −7.7% |
| FAA forecast boarding growth to 2035 | 25.8% (~609,000 extra boardings a year) |

Passenger numbers are flat against 2019, while seats have grown faster, so planes are emptier than before. The FAA forecast looks strong, but the FAA tends to over-forecast. Delta is the biggest airline, with 21.7% of passengers.

**Bottom line:** the case for adding capacity is mainly about airfield and cargo, not the terminal. I don't have cost, return or gate data, so I can't judge profitability.

**Worth checking next:**
- whether delays rise during the peak cargo season (I can pull the monthly system delay trend)
- how Memphis compares with other cargo-heavy or Tennessee airports

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); FAA passenger boarding data CY2025, calendar 2025; BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, Passenger-side score, Flight-side score, How full the planes are, FAA forecast passenger growth, System delay rate; 'unmet flight demand' is an estimate from the FAA forecast, used only when the airport is strained today; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - MEM: cargo heavy; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: MEM: cargo_heavy

## B1 - Score the top 3 airports that have the highest congestion in the US, only small airports.

*Pass when:* Small-hub class, sorted by the system delay rate, three airports with scores; says what 'small' means.

*Result:* PASS

*Tool calls:* `rank_airports` {"size_classes": ["small"], "sort_by": "system_delay_rate_pct", "limit": 3}

Punta Gorda (PGD) is the most congested small airport, and it also has the highest capacity-need score of all 78 ranked small airports (94.9). Key West (EYW) and St. Thomas (STT) come next on congestion, but they score lower overall (67.7 and 70.8).

Here "small airports" means the FAA small-hub class, which has 79 airports, 78 of them with full data. "Congestion" here is the system delay rate: arrival delays that airlines blame on the airport and air-traffic system, divided by arriving flights, over three years. Airlines code this category themselves and it includes ordinary weather, so it mostly measures congestion but not only congestion.

| Airport | System delay rate | Capacity-need score | Passenger side | Flight side | Rank in class |
|---|---|---|---|---|---|
| Punta Gorda, FL (PGD) | 8.6% | 94.9 | 93.3 | 96.5 | 1 of 78 |
| Key West, FL (EYW) | 8.0% | 67.7 | 64.2 | 71.2 | 32 of 78 |
| St. Thomas, VI – Cyril E. King (STT) | 7.9% | 70.8 | 62.3 | 79.3 | 26 of 78 |

**What drives the scores:**
- **PGD** is strong on every input. Planes are 85.8% full, passengers are up 37.0% since 2019, and the FAA forecasts 30.0% passenger growth and 26.8% flight growth.
- **EYW** has the biggest growth since 2019 (passengers up 55.9%, seats up 67.8%). But its planes are less full (77.3%) and its forecast flight growth is low (9.3%), which pulls its score down.
- **STT** is in a US territory. Its forecasts are moderate: 15.6% passenger growth and 15.0% flight growth.

All three are marked as strained today, and none has had capacity cut. The FAA forecasts are used to rank airports against each other, not as predictions, because the FAA tends to over-forecast.

Tweed/New Haven (HVN) was left out because its data is partial. This ranking doesn't show the overall delay rate or the latest 12-month delay rate. I can pull those, plus delay causes, with a side-by-side comparison of these three if that would help.

> Data period: BTS Airline Delay Causes, 2023-08 to 2026-07 (three years); BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: System delay rate, Capacity-need score, Passenger-side score, Flight-side score, FAA forecast passenger growth, FAA forecast flight growth; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - the answer uses proxy measures (scores, system delay rate, load factor or forecasts)

## B2 - Top 5 airports in Texas by how full the planes are.

*Pass when:* Five Texas airports by load factor.

*Result:* PASS

*Tool calls:* `rank_airports` {"states": ["TX"], "sort_by": "load_factor_pct", "limit": 5}

Dallas-Fort Worth (DFW) and McAllen (MFE) are tied for first, with planes 82.5% full. Houston Bush (IAH), Abilene (ABI) and Corpus Christi (CRP) come next. All 25 Texas airports with full data were ranked.

| # | Airport | Size class | Planes full | Capacity-need score | Passenger growth since 2019 |
|---|---|---|---|---|---|
| 1= | Dallas-Fort Worth International (DFW) | large | 82.5% | 79.3 | 14.9% |
| 1= | McAllen International (MFE) | small | 82.5% | 44.5 | 33.5% |
| 3 | George Bush Intercontinental, Houston (IAH) | large | 79.9% | 70.4 | 6.5% |
| 4 | Abilene Regional (ABI) | nonhub | 79.5% | 78.1 | 28.8% |
| 5 | Corpus Christi International (CRP) | nonhub | 76.6% | 38.0 | 13.2% |

**What "planes full" means here:** passengers divided by seats on departing flights, May 2025 to April 2026. It isn't the official load factor, which uses passenger-miles. It's also the weakest of the five score inputs, because airline pricing and aircraft choices affect it.

**What the full score adds:**
- **DFW:** Has the strongest case overall. It's flagged as strained, with a 6.2% system delay rate, and the FAA forecasts 19.3% flight growth.
- **Abilene:** Scores almost as high (3rd of 201 nonhub airports), thanks to strong growth forecasts. It's very small, though: 105,976 boardings in 2025.
- **IAH:** Also strained. Its flight count has stayed flat while passengers have grown.
- **McAllen and Corpus Christi:** Full planes, but low scores. The FAA forecasts little or negative flight growth (−9.8% for McAllen, 0.3% for Corpus Christi), and both have low delay rates. Full planes alone don't mean capacity is short.

I can compare any of these side by side or show the monthly trend in how full the planes are.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years); FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: How full the planes are, Capacity-need score, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - the answer uses proxy measures (scores, system delay rate, load factor or forecasts)

## B3 - Which large airports have planes over 85% full?

*Pass when:* Large hubs filtered by a load factor threshold.

*Result:* PASS

*Tool calls:* `rank_airports` {"size_classes": ["large"], "sort_by": "load_factor_pct", "min_value": 85, "limit": 25}; `rank_airports` {"size_classes": ["large"], "sort_by": "load_factor_pct", "limit": 5}

**None of them.** No large airport has planes over 85% full. All 30 airports in the FAA large-hub class have full data, and the highest is Newark at 83.2%. Here "how full" means passengers divided by seats on departing flights over the latest 12 months. That is a proxy, not the official load factor, which uses passenger-miles.

These are the five fullest large airports:

| Airport | How full (%) | Seats vs 2019 (%) | Passengers vs 2019 (%) | System delay rate, 3 yrs (%) | Capacity-need score |
|---|---|---|---|---|---|
| Newark Liberty (EWR) | 83.2 | 2.2 | 1.0 | 10.4 | 80.7 |
| San Francisco (SFO) | 82.6 | -5.0 | -4.4 | 13.4 | 86.9 |
| Dallas-Fort Worth (DFW) | 82.5 | 15.8 | 14.9 | 6.2 | 79.3 |
| Atlanta (ATL) | 82.3 | -1.0 | -4.5 | 4.6 | 69.8 |
| Los Angeles (LAX) | 82.1 | -12.8 | -15.7 | 4.8 | 75.3 |

**Caveats that change how to read this:**
- **SFO and LAX had seats cut.** Both have fewer seats than in 2019, so their full planes reflect less capacity, not rising demand.
- **Newark has a legal flight cap** of 36 arrivals and 36 departures an hour. Adding terminal capacity there may not add flights.
- **Dallas-Fort Worth looks strongest on demand.** It's the only one of the five where both seats and passengers are well above 2019, so its full planes come with real growth.
- **This metric is the weakest input to the score.** It reflects airline pricing and fleet choices, and only runs from about 82% to 83% across these five.

I can rerun this with a lower cutoff (for example 80%), or check medium-hub airports, which may be fuller.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); BTS Airline Delay Causes, 2023-08 to 2026-07 (three years); FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: How full the planes are, Capacity-need score, System delay rate; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - the answer uses proxy measures (scores, system delay rate, load factor or forecasts); EWR: legal limit; SFO: capacity cut; LAX: capacity cut
> Warnings printed: EWR: legal_limit, SFO: capacity_cut, LAX: capacity_cut

## B4 - Compare Portland and Providence.

*Pass when:* Asks which Portland (Oregon or Maine), or covers both and says so.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Portland"}; `find_airport` {"query": "Providence"}

Before I compare: "Portland" could mean two airports. Which one do you mean?

- **Portland International (PDX)**, Oregon. A medium hub.
- **Portland International Jetport (PWM)**, Maine. A small hub, the same FAA size class as Providence, and also in New England.

For Providence, I've assumed you mean **Rhode Island T.F. Green International (PVD)**, the airport in the city itself. Boston Logan (BOS) and Manchester-Boston Regional (MHT) are in the same metro area, so tell me if you meant one of those.

If you'd like, I can compare all three (PDX, PWM and PVD) side by side instead.

> Data period: no data was used in this reply  
> Assumptions: none  
> Confidence: n/a - no data figures were used in this reply

## B5 - Which airports are the best candidates overall? Only count the ones with complete data.

*Pass when:* National ranking shown per size class.

*Result:* PASS

*Tool calls:* `rank_airports` {}

Ranked only among the 343 airports with complete data, the top candidates are **Orlando (MCO)** among large hubs, **Southwest Florida/Fort Myers (RSW)** among medium hubs, **Punta Gorda (PGD)** among small hubs and **Rickenbacker/Columbus (LCK)** among non-hubs. The ranking is split by FAA size class because size isn't part of the score, so a single national list would be topped by small leisure airports. The 59 airports without complete data are left out.

| Class | #1 | #2 | #3 | #4 | #5 |
|---|---|---|---|---|---|
| Large | MCO 87.8 | SFO 86.9 | ORD 84.6 | JFK 84.0 | MIA 83.0 |
| Medium | RSW 81.7 | CHS 78.8 | JAX 75.8 | SJU 75.4 | RDU 73.1 |
| Small hub | PGD 94.9 | XNA 85.5 | SFB 85.2 | PIE 84.1 | PVU 80.2 |
| Non-hub | LCK 85.7 | TVC 78.8 | ABI 78.1 | BLV 77.8 | BQN 77.7 |

Scores run from 0 to 100 and show how an airport compares with the others. They estimate how much added capacity would get used, not profit.

**What drives the leaders:**
- **MCO:** planes 81.9% full, passengers up 14.7% since 2019, system delay rate 7.5%, FAA forecasts 28.2% more passengers.
- **PGD:** has the highest score of any airport shown here. Planes are 85.8% full and passengers are up 37.0% since 2019.
- **Florida** has 8 of the 20 places.

**Caveats that change the picture:**
- **San Francisco (SFO):** airlines cut seats (-5.0% vs 2019), so full planes reflect fewer seats rather than rising demand.
- **New York JFK (JFK):** the FAA limits flights with slots, so new runways or gates can't be used without more slots.
- **Chicago O'Hare (ORD):** FAA flight limits plus a temporary cap for summer 2026.
- **LCK and Aguadilla (BQN):** cargo is about 44% and 43% of flights. Cargo isn't in the score, but it uses the same runways and is counted in the FAA flight forecast. BQN also had seats cut.
- **Delay measure:** delays are coded by airlines and include ordinary weather, so the system delay rate mostly, but not only, reflects congestion.

I can't estimate cost or return. To dig further, I can pull a full profile on any of these airports, including the flight-demand estimate and delay causes.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years); FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, How full the planes are, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - SFO: capacity cut; ORD: legal limit; JFK: legal limit; LCK: cargo heavy
> Warnings printed: ORD: legal_limit, JFK: legal_limit, SFO: capacity_cut, LCK: cargo_heavy, BQN: cargo_heavy, BQN: capacity_cut

## B6 - How has passenger traffic at Boston changed since 2019? Give me the year by year picture.

*Pass when:* Year by year values for Boston, with 2026 marked partial.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Boston"}; `airport_profile` {"airport_code": "BOS"}

Boston Logan (BOS) has recovered to just above its 2019 level, but no further. In the latest 12 months it had 20,983,745 passengers, against 20,742,138 in 2019. That is **+1.2%**. Traffic peaked in 2024 and dipped slightly in 2025. I assumed you meant Logan. The area also has Manchester-Boston Regional (MHT) and Providence (PVD).

| Year | Passengers | How full planes were | System delay rate |
|---|---|---|---|
| 2019 | 20,742,138 | 81.9% | 9.2% |
| 2020 | 6,050,302 | 52.0% | 2.7% |
| 2021 | 10,938,231 | 75.1% | 3.5% |
| 2022 | 17,472,973 | 78.5% | 6.3% |
| 2023 | 19,991,297 | 83.3% | 7.2% |
| 2024 | 21,280,480 | 83.1% | 7.9% |
| 2025 | 21,105,980 | 81.6% | 11.0% |
| 2026 (Jan–Apr only) | 6,139,216 | 78.2% | 8.8% (7 months) |

Passengers counts people on departing flights. "How full" is passengers divided by seats, not the official load factor. Don't compare the 2026 row with full years: it covers only four months, and they're the quieter early months.

**What's behind the numbers:**
- **Bigger planes, fewer flights.** Passenger flights fell 3.1% between 2019 and 2025. Passengers per flight rose from 106.4 to 111.9. Seats are up 1.4% since 2019.
- **Planes are full.** 81.7% of seats were filled in the latest 12 months, and 85.1% in the July 2025 peak.
- **Delays are rising.** The system delay rate counts delays blamed on the airport and air-traffic system. It reached 11.0% in 2025, above 2019. Airlines code this category themselves, and it includes ordinary weather.
- **Growth ahead.** The FAA forecasts 26.5% more passengers by fiscal 2035, about 5.6 million more boardings a year. The FAA tends to over-forecast.

Traffic has been flat while delays rise, which fits an airport near its limits. It doesn't prove that demand is going unmet. I can show the month-by-month passenger trend if that would help.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); FAA passenger boarding data CY2025, calendar 2025; BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: How full the planes are, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; 'unmet flight demand' is an estimate from the FAA forecast, used only when the airport is strained today; 'Boston' was taken to mean BOS  
> Confidence: Medium - the answer uses proxy measures (scores, system delay rate, load factor or forecasts); an airport name was resolved by default

## B7 - Show me medium-size airports in the West with the fastest forecast passenger growth.

*Pass when:* West region, medium hubs, sorted by forecast passenger growth.

*Result:* PASS

*Tool calls:* `rank_airports` {"region": "west", "size_classes": ["medium"], "sort_by": "forecast_passenger_growth_pct", "limit": 10}

Portland, Oregon (PDX) has the fastest FAA-forecast passenger growth of the West's medium-hub airports, at 33.2%. Oakland (OAK), San Jose (SJC) and Boise (BOI) are next, each between about 29% and 30%. Of these, Boise is the only one where the forecast is backed by real growth since 2019.

"Medium" means the FAA medium-hub class. The forecast compares fiscal 2035 with fiscal 2025, and the FAA tends to forecast too high, so use these figures to compare airports with each other, not as predictions. There are 11 airports in this group and all have full data; the top 10 are below.

| # | Airport | Forecast pax growth | Extra boardings by 2035 | Pax vs 2019 | Planes full | Score (0–100) |
|---|---|---|---|---|---|---|
| 1 | Portland (PDX) | 33.2% | 2,989,548 | -6.4% | 82.0% | 72.3 |
| 2 | Oakland (OAK) | 29.9% | 1,402,276 | -35.5% | 74.2% | 46.0 |
| 3 | San Jose (SJC) | 29.6% | 1,620,865 | -35.0% | 73.9% | 44.7 |
| 4 | Boise (BOI) | 28.6% | 735,328 | +24.8% | 78.7% | 66.7 |
| 5 | Sacramento (SMF) | 24.7% | 1,682,362 | +3.8% | 76.5% | 52.0 |
| 6 | Anchorage (ANC) | 24.6% | 660,937 | +0.8% | 72.8% | 59.1 |
| 7 | Ontario (ONT) | 22.9% | 799,528 | +26.5% | 74.1% | 52.0 |
| 8 | Kahului (OGG) | 21.9% | 753,173 | -9.4% | 77.7% | 48.1 |
| 9 | John Wayne/Orange County (SNA) | 19.4% | 1,059,150 | +7.2% | 80.4% | 62.0 |
| 10 | Hollywood Burbank (BUR) | 16.0% | 531,720 | -0.7% | 72.3% | 44.0 |

**Warnings that change the picture:**
- **Oakland and San Jose:** passengers are still about 35% below 2019 and seats were cut by about 31–32%. Much of their forecast growth may just be lost traffic coming back, which needs no new capacity. They score low (44–46). San Jose also has a night noise curfew.
- **Portland and Kahului:** seats were cut too, so full planes there partly reflect fewer seats, not rising demand.
- **Orange County (SNA):** a legal cap on passengers and departures, plus a night curfew, limits growth.
- **Anchorage and Ontario:** cargo is 56.6% and 36.2% of flights. Cargo uses the same runways but isn't in the score.

The strongest cases are Portland (highest score here and the largest extra boardings) and Boise (strong growth, no warnings).

> Data period: FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: FAA forecast passenger growth, Capacity-need score, How full the planes are, FAA forecast flight growth; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - PDX: capacity cut; OAK: capacity cut; SJC: capacity cut, legal limit; ANC: cargo heavy
> Warnings printed: SJC: legal_limit, SNA: legal_limit, PDX: capacity_cut, OAK: capacity_cut, SJC: capacity_cut, ANC: cargo_heavy, ONT: cargo_heavy, OGG: capacity_cut

## B8 - What's the busiest month at Burlington, Vermont, and how full are the planes then?

*Pass when:* The busiest month and its load factor.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Burlington, Vermont"}; `airport_trend` {"airport_code": "BTV", "metric": "passengers"}; `airport_trend` {"airport_code": "BTV", "metric": "load_factor_pct"}

October is the busiest month at Patrick Leahy Burlington International (BTV), and planes are about 85% full then. That is a bit above the airport's full-year average of 83.0%, but not its fullest month.

**Busiest month (passengers on departing flights, May 2023 to April 2026)**
- October averages 73,848 passengers across the three Octobers. It was the top month in each of the 2023, 2024 and 2025 seasons.
- The busiest single month was October 2025, with 79,157 passengers.
- August is second, averaging 70,578.

**How full the planes are in October**
| | Seat fill |
|---|---|
| Three-October average | 84.9% |
| Oct 2025 | 86.9% |
| Oct 2024 | 79.2% |
| Oct 2023 | 89.5% |
| Full year (May 2025 to Apr 2026) | 83.0% |

"How full" here means passengers divided by seats on departing flights. It is not the official load factor, which uses passenger-miles. It also reflects airline pricing and choice of aircraft as much as demand.

**The fullest month is July, not October.** July averages 86.7% full across three years, and August 85.5%. October draws the most passengers, but airlines seem to add seats to match. Summer is when seats are tightest.

**What this means for capacity:** BTV ranks 6th of 78 ranked small-hub airports, with a capacity-need score of 79.2. Its seat count is about the same as in 2019 (+0.1%), while the FAA forecasts 22.9% passenger growth. That points to the July–October peak getting tighter. Peak-hour and gate data aren't in this system, so whether the terminal itself is a bottleneck in those months would need checking separately.

> Data period: BTS T-100 airport-month summary, 2023-05 to 2026-04  
> Assumptions: proxies, not direct measurements: How full the planes are  
> Confidence: Medium - the answer uses proxy measures (scores, system delay rate, load factor or forecasts)

## C1 - Score the top 3 airports that have the highest congestion in August in the US.

*Pass when:* Ranks by the August system delay rate and says scores do not exist by month.

*Result:* PASS

*Tool calls:* `rank_airports` {"sort_by": "system_delay_rate_pct", "month": 8, "limit": 3}

Measured by the August system delay rate (Augusts 2023–2025 combined), the three most congested US airports are Newark (EWR), Orlando (MCO) and San Juan (SJU). Orlando has the highest capacity-need score of the three.

| Airport | August system delay rate | Capacity-need score | Passenger side | Flight side | Rank in size class |
|---|---|---|---|---|---|
| Newark Liberty (EWR), large | 10.9% | 80.7 | 72.7 | 88.6 | 7 of 30 |
| Orlando International (MCO), large | 10.3% | 87.8 | 81.5 | 94.0 | 1 of 30 |
| San Juan Luis Muñoz Marín (SJU), medium | 9.8% | 75.4 | 77.6 | 73.3 | 4 of 34 |

**How I measured congestion:** The system delay rate is the share of arriving flights with delays that airlines put down to the airport and air-traffic system. Airlines code this category themselves, and it includes ordinary weather, so it mostly reflects congestion but not only that. It covers domestic flights of the larger reporting airlines. Scores don't exist by month, so the scores above are the standard ones for the latest period. SJU is tied at 9.8% with another airport that the list cut off. Airports with partial data or too few flights (fewer than 300 August arrivals) were left out.

**What changes the picture:**
- **Newark has a legal cap:** an FAA order limits it to 36 arrivals and 36 departures an hour. Its delays are real, but adding capacity may not turn into more flights unless the cap changes. Its passenger growth since 2019 is also weak at 1.0%.
- **Orlando** has the strongest case for added capacity: planes 81.9% full, passengers up 14.7% since 2019, and the highest FAA forecasts of the three (28.2% passenger and 26.4% flight growth to 2035).
- **San Juan** (a US territory) has the fullest planes, at 84.6%, and passengers up 45.1% since 2019. The FAA forecasts more modest growth there: 8.5% passengers, 11.1% flights.

A useful next step would be an airport profile of each, to see the delay causes and the flight-demand estimate.

> Data period: BTS Airline Delay Causes, August of 2023, 2024, 2025 (summed); BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: System delay rate, Capacity-need score, Passenger-side score, Flight-side score, FAA forecast passenger growth, FAA forecast flight growth; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - EWR: legal limit; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: EWR: legal_limit

## C2 - Where is Delta the dominant airline?

*Pass when:* Says airline-network questions are not supported; may offer the biggest-airline share per airport.

*Result:* PASS

*Tool calls:* `rank_airports` {"sort_by": "top_airline_share_pct", "limit": 25, "group_by_size_class": true}; `airport_profile` {"airport_code": "ATL"}; `airport_profile` {"airport_code": "MSP"}; `airport_profile` {"airport_code": "DTW"}; `airport_profile` {"airport_code": "SLC"}

I can't give you a complete list of airports where Delta is the biggest airline. The data has no per-airline network view, and the ranking by top-airline share doesn't say which airline that is. The airline's name only shows up when I look at one airport at a time. I checked four likely Delta hubs, and Delta is the biggest airline at all four (share of passengers, calendar 2025):

| Airport | Delta share | Capacity-need score | Rank in size class |
|---|---|---|---|
| Atlanta (ATL) | 74.7% | 69.8 | 18 of 30 large |
| Minneapolis-St Paul (MSP) | 58.0% | 64.8 | 23 of 30 large |
| Salt Lake City (SLC) | 57.5% | 60.9 | 25 of 30 large |
| Detroit (DTW) | 54.8% | 60.6 | 26 of 30 large |

**What this means for investment:**
- **Reliance on one airline is a risk.** ATL has the highest biggest-airline share of any large airport in the dataset. Growth at all four depends heavily on Delta's own plans.
- **Seats were cut at MSP and DTW.** Seats are down 7.2% at MSP and 6.7% at DTW compared with 2019. Passenger numbers fell even more (−10.0% and −10.1%). So their full planes reflect fewer seats, not rising demand.
- **None of the four is strained today.** Their system delay rates are moderate: 4.6% at ATL, 4.2% at MSP, 3.8% at DTW and 2.8% at SLC, over three years. Airlines code this delay category, and it includes ordinary weather. So the FAA's forecast growth at these airports (19.8% to 23.5% more takeoffs and landings by 2035) is not counted as unmet demand.
- SLC is the only one of the four with more passengers than in 2019 (+4.7%).

Background (not from our data): Delta also has large operations at other airports, such as New York JFK, LaGuardia and Seattle. I haven't checked those here.

I can look up other airports one at a time to see whether Delta is the biggest airline there. Want me to check a specific list?

> Data period: BTS T-100 Segment, calendar 2025; BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, How full the planes are, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; 'unmet flight demand' is an estimate from the FAA forecast, used only when the airport is strained today; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - 25 of the 100 listed airports have weaker data (GUM: small delay sample; VLD: small delay sample; EAT: small delay sample); EWR: legal limit; MSP: capacity cut; DTW: capacity cut
> Warnings printed: EWR: legal_limit, ORD: legal_limit, SAN: legal_limit, DCA: legal_limit, DAL: legal_limit, SJC: legal_limit, SNA: legal_limit, LGB: legal_limit, HPN: legal_limit, MSP: capacity_cut, DTW: capacity_cut, PHL: capacity_cut, : more

## C3 - How many flights go from JFK to London?

*Pass when:* Declines: route-level questions are not supported.

*Result:* PASS

*Tool calls:* `airport_profile` {"airport_code": "JFK"}

I can't give you the number of JFK–London flights. This system has no route or destination data, so it can't count flights between two cities. The closest thing I have is how many of New York JFK's (JFK) departures are long-haul.

**JFK long-haul departures, calendar 2025 (all destinations, domestic plus international, all airlines)**

| Cutoff (our definition) | Passenger flights | Share of passenger flights |
|---|---|---|
| 2,000+ miles | 96,455 | 45.4% |
| 2,500+ miles | 60,217 | 28.4% |
| 3,000+ miles (our default) | 49,841 | 23.5% |

JFK had 212,394 departing passenger flights in total. Counting cargo, 24.0% of all flights were 3,000+ miles.

Background (not from our data): London is farther from New York than our default long-haul cutoff. London flights are part of the 3,000+ mile bucket, but so are many other European, Asian and South American routes. That bucket is an upper bound, not the London figure.

**Context if you're looking at JFK as a candidate:**
- Capacity-need score: 84.0. JFK ranks 4th of 30 large airports and 9th of 343 overall.
- Planes are 82.0% full, and the FAA forecasts 29.0% passenger growth by 2035.
- JFK counts as strained (its system delay rate is in the top quarter of airports): 7.5% over three years and 7.3% in the latest 12 months. Airlines assign this delay category themselves, and it includes ordinary weather.
- **Legal limit:** JFK is a Level 3 slot-controlled airport. Added runway or gate capacity can't be used unless more flight slots are approved, which matters a lot for any expansion case.

For London traffic specifically, you'd need a route-level source such as BTS T-100 segment data filtered by destination. If you want, I can show JFK's long-haul share at a different cutoff.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; long-haul means 3,000 miles or more (our definition; adjustable); scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - JFK: legal limit; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: JFK: legal_limit

## C4 - What's the congestion level at Teterboro?

*Pass when:* Says Teterboro is outside the covered airports; no invented number.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Teterboro"}

I don't have congestion data for Teterboro. It isn't one of the 402 FAA primary airports this dataset covers, so there are no delay rates or scores for it.

Background (not from our data): Teterboro is a general-aviation and business-jet airport in New Jersey with no scheduled airline service. That's why it isn't in the BTS airline delay data or the FAA primary-airport list this system is built on.

If you're looking at congestion in the New York / New Jersey area, I can:
- **Profile Newark (EWR), LaGuardia (LGA) or JFK (JFK)**, including the three-year and latest 12-month system delay rates, the overall delay rate and delay causes. The system delay category is coded by the airlines and includes ordinary weather.
- **Compare those three side by side** on congestion and the capacity-need score.
- **Rank all the airports in the metro area** by system delay rate.

Which would help most?

> Data period: no data was used in this reply  
> Assumptions: none  
> Confidence: n/a - no data figures were used in this reply

## C5 - Which airports were the top expansion candidates in 2021?

*Pass when:* Says the score exists for the latest period only; offers raw 2021 metrics.

*Result:* PASS

*Tool calls:* `rank_airports` {"year": 2021, "sort_by": "load_factor_pct", "limit": 5}; `rank_airports` {"year": 2021, "sort_by": "system_delay_rate_pct", "limit": 5}

I can't rank 2021 expansion candidates. The capacity-need score only exists for the latest period, not for past years. I can show raw 2021 metrics, though. These are the 2021 leaders on the two strongest score inputs, ranked among the 343 airports with full data:

**Fullest planes in 2021** (passengers ÷ seats on departing flights, a stand-in for unmet passenger demand)

| Airport | 2021 | Score today |
|---|---|---|
| McAllen (MFE) | 84.4% | 44.5 |
| Wilkes-Barre/Scranton (AVP) | 84.3% | 71.3 |
| Aguadilla (BQN) | 83.8% | 77.7 |
| Ponce (PSE) | 82.3% | 75.5 |
| Hartford Bradley (BDL) | 82.2% | 65.9 |

**Highest system delay rate in 2021** (a stand-in for congestion: the share of arrivals with delays airlines blamed on the airport and air-traffic system. Airlines assign this category, and it includes ordinary weather.)

| Airport | 2021 | Score today |
|---|---|---|
| Key West (EYW) | 11.5% | 67.7 |
| Punta Gorda (PGD) | 10.0% | 94.9 |
| Newark (EWR) | 8.8% | 80.7 |
| Dallas Love Field (DAL) | 8.4% | 42.8 |
| Aguadilla (BQN) | 8.4% | 77.7 |

**Caveats that change the reading:**
- **Newark** has a legal cap of 36 arrivals and 36 departures an hour.
- **Dallas Love Field** is limited to 20 gates by federal law.
- **Aguadilla, Wilkes-Barre/Scranton and Ponce:** airlines have cut seats since 2019, so full planes partly reflect fewer seats rather than rising demand.
- **Aguadilla:** 42.8% of flights are cargo.
- **Ponce:** its delay figures rest on a small number of flights. Its 2021 delay rate isn't available.

Some 2021 leaders score high today (Punta Gorda ranks first among small-hub airports). Others score low (McAllen, Love Field). Being strained in 2021 didn't reliably predict where airports stand now.

I can also run a 2021 ranking by region, size class or another metric, or show how any of these airports changed from 2019 to now.

> Data period: BTS T-100 airport-month summary, calendar 2021 / 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / calendar 2021; FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: How full the planes are, Capacity-need score, System delay rate, FAA forecast flight growth; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - 1 of the 5 listed airports have weaker data (PSE: small delay sample); AVP: capacity cut; BQN: capacity cut, cargo heavy; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: EWR: legal_limit, DAL: legal_limit, AVP: capacity_cut, BQN: cargo_heavy, BQN: capacity_cut, PSE: small_sample, PSE: capacity_cut, PSE: small_airport_forecast

## C6 - Should we invest in expanding LaGuardia?

*Pass when:* Gives the evidence and the slot limit; leaves the decision to the analyst.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "LaGuardia"}; `airport_profile` {"airport_code": "LGA"}

That's your call, but the data points to caution. LaGuardia (LGA) is one of the most congested airports we cover. However, flight slots there are capped by FAA order and nonstop flights are limited to 1,500 miles. Added capacity there wouldn't produce more flights unless those rules changed. Its overall score is above average, not top-tier.

**Score:** 67.8 out of 100 for how much added capacity would likely be filled. That puts it 19th of 30 large airports and 76th of 343 overall. The score is a stand-in for upside, not profit. I have no cost or return data.

| Measure | LGA | Rank among peers (0–100) |
|---|---|---|
| Delays caused by the airport and air-traffic system (3 yrs) | 8.4% | 98.1 |
| How full the planes are | 80.8% | 78.9 |
| Passenger growth since 2019 | 4.7% | 49.0 |
| FAA forecast passenger growth (to 2035) | 18.4% | 47.2 |
| FAA forecast flight growth (to 2035) | 9.3% | 45.9 |

**Congestion is real.** The system delay rate was 10.4% in the latest 12 months, and 21.5% of arrivals were delayed overall. Airlines blamed 39.3% of delayed flights on the airport and air-traffic system, which they code themselves and which includes ordinary weather. Only 3.6% were blamed on extreme weather.

**Growth is modest.** There were 4.8% fewer passenger flights in 2025 than in 2019. Passengers still grew because each flight carried more people (94.7 per flight, up from 85.3). The FAA forecasts 33,029 extra takeoffs and landings a year by 2035 and about 3.0 million more boardings. We call the extra flights "unmet flight demand", but that's an estimate, not a measurement. Because the slot cap is already built into that forecast, it doesn't show what demand would be without the cap.

Background (not from our data): LaGuardia has recently had a major terminal rebuild, so check what capacity is already in place before going further.

**Next steps:** confirm the slot rules and the 1,500-mile limit will stay, and check gate and terminal use, which I don't have. I could also compare LGA with JFK and Newark (EWR) if that would help.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); FAA passenger boarding data CY2025, calendar 2025; BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, How full the planes are, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; 'unmet flight demand' is an estimate from the FAA forecast, used only when the airport is strained today; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - LGA: forecast constrained, legal limit; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: LGA: legal_limit, LGA: forecast_constrained

## C7 - What will a new terminal at Denver cost, and what return would we get?

*Pass when:* Declines cost and return; offers the capacity-need evidence.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Denver"}

I can't tell you what a new terminal at Denver International (DEN) would cost or what it would return. This system has no data on construction costs, revenue or returns, and nothing on gate counts or terminal size. What I can show is how much added capacity would likely be used, which is a stand-in for profit, not a financial forecast.

**Denver (DEN)** is a large hub with 39,976,695 boardings in 2025. Its capacity-need score is **76.7 out of 100**, ranking **12th of 30** ranked large hubs. The score measures how much of any new capacity would likely be filled, compared with other airports.

| Measure | DEN |
|---|---|
| Passenger-side score | 76.7 |
| Flight-side score | 76.7 |
| Average share of seats filled (load factor) | 81.2% |
| Passenger growth since 2019 | 18.8% |
| Seat growth since 2019 | 26.1% |
| FAA forecast passenger growth (2025–2035) | 23.7% (about 9,475,223 extra boardings) |
| FAA forecast flight growth (2025–2035) | 14.7% |
| System delay rate (3 years) | 6.6% |

**What this shows:**
- **Demand is real and growing.** Planes are fairly full, and passengers have grown well since 2019.
- **The airport is under strain today.** The system delay rate counts delays that airlines put down to the air traffic system, which also includes ordinary weather.
- **Capacity has kept up.** Seats grew faster than passengers since 2019 and haven't been cut, so the growth isn't coming from a squeeze on supply.
- **The FAA forecast is solid but not the highest among large hubs.** That's why Denver ranks mid-pack rather than near the top.

**To size the opportunity, you could check:**
- Denver's full profile, including the estimate of how many more flights could be filled and what causes its delays
- A side-by-side comparison with other large hubs
- Its monthly peak-season pattern

Cost estimates and gate use would need to come from outside sources, such as the airport's own capital plan.

> Data period: no data was used in this reply  
> Assumptions: none  
> Confidence: n/a - no data figures were used in this reply

## C8 - What is the delay rate at Glacier Park airport in Kalispell, and can I trust it?

*Pass when:* Resolves Glacier Park to FCA, gives the rate and the sample size.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Glacier Park, Kalispell"}; `find_airport` {"query": "FCA"}; `airport_profile` {"airport_code": "FCA"}

Glacier Park International (FCA) in Kalispell, MT has a **system delay rate of 4.0%** over three years and an **overall delay rate of 16.6%**. The figures are reasonably reliable. The airport has full data, the sample is decent and the rate has been steady from year to year. But the system delay rate is only a rough stand-in for how congested the airport is.

The name search didn't find it, so I looked it up by its airline code, FCA. The FAA code is GPI.

**Delay figures**
| Measure | Value |
|---|---|
| System delay rate, 3 years (2023-08 to 2026-07) | 4.0% |
| System delay rate, latest 12 months | 4.7% |
| Overall delay rate (15+ min, any cause), 3 years | 16.6% |
| Arriving flights in the sample | 15,601 |
| Position among full-data airports (0–100) | 49.1 |

**Why it's fairly reliable**
- **Full data, high confidence.** All the scored measures exist for this airport.
- **Big enough sample.** About 15,600 arrivals over three years. A single year moves around more, which is why the score uses the three-year rate.
- **Steady over time.** By calendar year the system delay rate was 3.7% (2019), 3.3% (2022), 3.1% (2023), 3.9% (2024) and 3.9% (2025). So far 2026 is at 4.8%, from 7 months of data. It is drifting up but is still in the middle of the pack.

**Limits to keep in mind**
- **Airlines choose the cause.** The "system" category (airport and air-traffic system) also includes ordinary weather, so it's mostly congestion, not purely.
- **Partial coverage.** Only domestic flights of the larger airlines that report delays are counted.
- **Most delays aren't the airport's.** Of flights delayed 15+ minutes, 42.9% were blamed on the airline, 28.5% on late-arriving aircraft and only 24.1% on the system. That points to delays caused by airline operations more than an airfield running short of capacity.

Kalispell isn't counted as strained. Its pressure shows on the passenger side instead: planes are 85.7% full and passenger numbers are up 57.0% since 2019.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, Passenger-side score, System delay rate; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
