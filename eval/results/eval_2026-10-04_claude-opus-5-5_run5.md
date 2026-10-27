# Evaluation run - 2026-10-04 19:21 - claude-opus-5-5

**25 of 26 questions passed.** 849 numbers appeared in the answers; 0 answers ended with a number that could not be traced to a tool result; 4 answers passed only after one automatic rewrite. Average 13.3s per question; 793,662 input and 29,019 output tokens in total.

| Id | Group | Result | Tools | Number check | Seconds |
|---|---|---|---|---|---|
| A1 | core | PASS | rank_airports | passed | 12.2 |
| A2 | core | PASS | find_airport, find_airport, compare_airports, airport_profile, airport_profile | passed | 15.3 |
| A6 | follow-up | PASS | compare_airports | passed | 11.2 |
| A3 | core | PASS | find_airport, airport_profile | passed | 10.5 |
| A7 | follow-up | PASS | airport_profile | passed | 8.0 |
| A4 | core | PASS | airport_profile | passed | 12.2 |
| A5 | follow-up | PASS | find_airport, compare_airports, airport_profile | passed | 11.6 |
| A8 | follow-up | PASS | find_airport, airport_profile | passed | 15.6 |
| B1 | filters | PASS | rank_airports | passed | 11.7 |
| B2 | filters | PASS | rank_airports | passed | 9.9 |
| B3 | filters | PASS | rank_airports, rank_airports | passed | 11.8 |
| B4 | ambiguous | PASS | find_airport, find_airport | passed | 5.9 |
| B5 | filters | PASS | rank_airports | passed | 12.0 |
| B6 | time | PASS | find_airport, airport_profile | passed | 11.0 |
| B7 | filters | PASS | rank_airports | passed | 11.9 |
| B8 | time | PASS | find_airport, airport_trend, airport_trend | rewritten | 19.1 |
| C1 | time | PASS | rank_airports | rewritten | 25.9 |
| C9 | time | PASS | rank_airports, rank_airports | passed | 14.8 |
| C10 | time | PASS | rank_airports, rank_airports | passed | 15.3 |
| C2 | out of scope | PASS | rank_airports, airport_profile, airport_profile, airport_profile, airport_profile | passed | 17.0 |
| C3 | out of scope | PASS | airport_profile | passed | 9.4 |
| C4 | out of scope | FAIL | find_airport | rewritten | 11.0 |
| C5 | out of scope | PASS | rank_airports, rank_airports | rewritten | 24.2 |
| C6 | judgment | PASS | find_airport, airport_profile | passed | 13.5 |
| C7 | out of scope | PASS | find_airport | passed | 9.8 |
| C8 | awkward data | PASS | find_airport, find_airport, find_airport, airport_profile | passed | 16.0 |

## A1 - Which airports in New England are strong candidates for terminal expansion?

*Pass when:* A ranked list from the six states, scores shown, reasons given.

*Result:* PASS

*Tool calls:* `rank_airports` {"region": "new england", "limit": 10}

Boston Logan (BOS), Burlington (BTV) and Portland, Maine (PWM) stand out in New England, with Bangor (BGR) close behind. One caveat: no public data measures how busy a terminal or its gates are. These rankings use our capacity-need score (0-100, relative to 343 airports). It shows how much added capacity would likely be filled, so it stands in for upside, not profit.

| Airport | Score | Planes full | Pax growth since 2019 | FAA pax forecast | System delay rate | Strained |
|---|---|---|---|---|---|---|
| Boston (BOS), large | 82.9 | 81.7% | 1.2% | 26.5% | 9.1% | Yes |
| Burlington (BTV), small hub | 79.2 | 83.0% | 2.3% | 22.9% | 5.5% | Yes |
| Portland (PWM), small hub | 77.4 | 82.8% | 17.2% | 21.6% | 4.6% | No |
| Bangor (BGR), nonhub | 71.8 | 80.4% | 40.8% | 24.1% | 4.7% | No |
| Hartford (BDL), medium | 65.9 | 81.3% | -2.7% | 15.7% | 4.9% | No |

- **Boston** ranks 11th of 343 nationally. Its score is driven by the flight side: it has the region's highest system delay rate. That rate counts delays that airlines code to the airport and air-traffic system, which includes ordinary weather. Boston also has by far the largest absolute prize: the FAA forecasts 5,612,088 extra boardings a year by 2035.
- **Burlington** has the fullest planes in the region, but passenger traffic has barely grown since 2019.
- **Portland and Bangor** have real recent growth: seats are up 21.6% and 48.8% since 2019. Their delays are low, though, so the case for them rests on passenger traffic, not congestion.
- **Lower down:** Worcester (ORH) and Portsmouth (PSM) each rely mostly on one airline, so their demand depends on that airline's plans. Martha's Vineyard (MVY) and Portsmouth are small enough that the FAA's forecasts for them deserve less trust.

Four airports are left out because their data is incomplete: Tweed/New Haven (HVN), Cape Cod Gateway (HYA), Block Island (BID) and Westerly (WST).

Next steps I can run: a full profile of Boston, Burlington or Portland, including a demand estimate and delay causes, or a monthly trend to check peak-season strain.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years); FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, Flight-side score, How full the planes are, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - 1 of the 10 listed airports has weaker data (PSM: small delay sample); MVY: small airport forecast; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: ORH: single_airline, MVY: small_airport_forecast, PSM: small_sample, PSM: single_airline, PSM: small_airport_forecast

## A2 - Compare LA and Santa Ana airport congestion levels.

*Pass when:* LAX vs SNA side by side, a clear verdict, Santa Ana's legal cap flagged.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "LA"}; `find_airport` {"query": "Santa Ana"}; `compare_airports` {"airport_codes": ["LAX", "SNA"]}; `airport_profile` {"airport_code": "LAX"}; `airport_profile` {"airport_code": "SNA"}

Los Angeles International (LAX) is more congested than John Wayne/Orange County in Santa Ana (SNA), but not by much. Over three years, LAX's system delay rate is 0.9 percentage points higher (about 1.23 times SNA's). Neither airport counts as "strained", which in our data means a system delay rate in the top quarter of airports.

I took "LA" to mean LAX. The metro area also has Ontario (ONT), Hollywood Burbank (BUR) and Long Beach (LGB).

| Measure | LAX | SNA | Difference |
|---|---|---|---|
| System delay rate, 3 years | 4.8% | 3.9% | +0.9 pts |
| System delay rate, latest 12 months | 5.0% | 4.3% | +0.7 pts |
| Overall delay rate (any cause), 3 years | 18.9% | 17.5% | +1.4 pts |
| System delay rank among ranked airports (0-100) | 70.9 | 47.1 | |
| System share of delayed flights | 25.7% | 22.4% | |

**What the numbers mean**
- The system delay rate is the share of arriving flights delayed by the airport or air-traffic system. Airlines assign this cause themselves, and it includes ordinary weather. So it mostly measures congestion, but not only congestion.
- At both airports, airline-caused delays (37.0% at LAX, 35.0% at SNA) and late incoming aircraft (33.4% and 39.9%) cause more delays than the system does.

**Recent months:** At both airports the latest year is a little higher than the three-year rate. The latest four months are in line with earlier periods, so this is not a recent spike or a steady worsening.

**Caveats that matter**
- **SNA's limits are legal, not just physical.** SNA has a legal cap on passengers, a cap on daily departures and a night curfew. In our units (departing passengers), the passenger cap is roughly 6.1-6.25 million. SNA had 5,590,354 passengers in the latest 12 months, so it is already close to the cap. That limits how much any added capacity could be used, whatever the delay rates say.
- **LAX has fewer seats than before.** Seats are 12.8% below 2019, so its full planes reflect airlines cutting seats, not rising demand.

I don't have gate, terminal or peak-hour data. If it would help, I can rank all five LA-area airports by system delay rate.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: How full the planes are, System delay rate; 'LA' was taken to mean LAX  
> Confidence: Medium - LAX: capacity cut; SNA: legal limit; the answer uses proxy measures (scores, system delay rate, load factor or forecasts); an airport name was resolved by default
> Warnings printed: SNA: legal_limit, LAX: capacity_cut

## A6 - And how did congestion at those two look in 2023?

*Pass when:* Uses the same two airports without being told again, and 2023 values.

*Result:* PASS

*Tool calls:* `compare_airports` {"airport_codes": ["LAX", "SNA"], "year": 2023}

In 2023 both airports were more congested than they are now, and the gap between them was wider: LAX's system delay rate was 1.4 percentage points higher than SNA's (about 1.33 times), compared with 0.9 points over the latest three years.

| Calendar 2023 | LAX | SNA | Difference |
|---|---|---|---|
| System delay rate | 5.6% | 4.2% | +1.4 pts |
| Overall delay rate (any cause) | 20.5% | 18.5% | +2.0 pts |
| Planes full (passengers / seats) | 83.9% | 83.1% | +0.8 pts |
| Arriving flights in the delay data | 195,617 | 45,732 | |

**How 2023 compares with today**
- **LAX has improved.** Its system delay rate was 5.6% in 2023, fell to 4.6% in calendar 2025, and is 5.0% over the latest 12 months. 2023 was LAX's highest year for system delays since 2019. Its overall delay rate also fell from 20.5% in 2023 to 18.7% in 2025.
- **SNA has barely moved.** Its system delay rate was 4.2% in 2023, 4.3% in 2025 and 4.3% over the latest 12 months. Its overall delay rate was 18.5% in 2023 and 18.2% in 2025.

So most of the narrowing gap comes from LAX getting better, not from SNA getting worse.

**Things to keep in mind**
- As before, the system delay category is assigned by airlines and includes ordinary weather.
- Our three-year delay window starts in August 2023, so the end of 2023 is also part of the three-year figures in my last answer.
- SNA's legal passenger and departure caps and night curfew apply in every year. They limit how much traffic, and so congestion, SNA can take on regardless of demand.

I can't give capacity-need scores for 2023, because the score exists only for the latest period. Year-by-year delay rates back to 2019 are available if you want the longer trend.

> Data period: BTS T-100 airport-month summary, calendar 2023; BTS Airline Delay Causes, calendar 2023; BTS T-100 Segment, calendar 2023  
> Assumptions: proxies, not direct measurements: How full the planes are, System delay rate  
> Confidence: Medium - LAX: capacity cut; SNA: legal limit; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: SNA: legal_limit, LAX: capacity_cut

## A3 - What is the percentage of long haul flights out of Anchorage airport?

*Pass when:* One number, the 3,000-mile definition stated, the cargo-included number next to it.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Anchorage airport"}; `airport_profile` {"airport_code": "ANC"}

At Ted Stevens Anchorage International (ANC), **2.8% of departing passenger flights were long-haul in calendar 2025**. Long-haul here means 3,000 miles or more, which is our default cutoff because there is no official definition. If you count cargo flights too, the share is **31.0%**. I took "Anchorage airport" to mean ANC. Anchorage also has Merrill Field (MRI), a much smaller airport with only partial data.

| Cutoff | Share of passenger flights | Share of all flights, cargo included |
|---|---|---|
| 2,000+ miles | 13.7% | 47.4% |
| 2,500+ miles | 9.8% | 43.2% |
| 3,000+ miles | 2.8% | 31.0% |

These are departing flights, domestic and international, all airlines, over a full 12 months of 2025. That covers 38,150 passenger flights and 87,988 flights in total.

**Why the two columns differ so much:** cargo makes up 56.6% of departing flights at ANC, and much of it flies long distances. 27,305 flights including cargo were long-haul at the 3,000-mile cutoff, against 1,061 passenger flights. On the passenger side, Anchorage is mostly a domestic airport: 98.6% of its passengers fly to US destinations. Its biggest airline is Alaska Airlines, with 61.4% of passengers.

**What this means for capacity:** cargo uses the same runways as passenger flights, but it is not in the capacity-need score. The FAA's flight forecast for ANC does include cargo. So the airport's flight-side score (75.3) partly reflects cargo traffic, not just passengers.

Background (not from our data): Anchorage is a refuelling stop for cargo flights between Asia and North America, which explains the long-haul cargo.

If you want a different long-haul cutoff, I can rerun the numbers with it.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, Passenger-side score, Flight-side score, FAA forecast passenger growth, FAA forecast flight growth; long-haul means 3,000 miles or more (our definition; adjustable); 'Anchorage airport' was taken to mean ANC; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - ANC: cargo heavy; the answer uses proxy measures (scores, system delay rate, load factor or forecasts); an airport name was resolved by default
> Warnings printed: ANC: cargo_heavy

## A7 - What if long-haul means over 2,300 miles?

*Pass when:* Recomputed at 2,300 miles for Anchorage.

*Result:* PASS

*Tool calls:* `airport_profile` {"airport_code": "ANC", "long_haul_miles": 2300}

With long-haul set at 2,300 miles, **12.6% of passenger flights leaving Anchorage (ANC) in 2025 were long-haul**: 4,820 out of 38,150. If you count cargo flights too, the share is **46.5%**: 40,947 out of 87,988.

One detail: the data counts flights of *at least* 2,300 miles, so a flight of exactly 2,300 miles is included. That is very slightly broader than "over 2,300."

| Cutoff | Share of passenger flights | Share of all flights, cargo included |
|---|---|---|
| 2,000+ miles | 13.7% | 47.4% |
| **2,300+ miles** | **12.6%** | **46.5%** |
| 2,500+ miles | 9.8% | 43.2% |
| 3,000+ miles | 2.8% | 31.0% |

**Where you set the cutoff matters a lot for passenger flights.** At 2,300 miles the share is several times what it is at 3,000. That's because many of Anchorage's longer passenger flights fall between 2,300 and 3,000 miles. Very few passenger flights go beyond 3,000. For flights including cargo, the share changes much less across the cutoffs, because a large number of cargo flights fly very long distances.

The cargo warning still applies: cargo makes up 56.6% of flights at ANC. It uses the same runways as passenger flights but isn't counted in the capacity-need score. So the cargo-included column says more about how busy the runways are than about passenger demand.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score; long-haul means 2,300 miles or more (our definition; adjustable); scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - ANC: cargo heavy; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: ANC: cargo_heavy

## A4 - What is the unmet flight demand in SFO airport and why?

*Pass when:* An estimate named as an estimate or proxy, with the why from the delay data.

*Result:* PASS

*Tool calls:* `airport_profile` {"airport_code": "SFO"}

San Francisco International (SFO) has an estimated **108,307 extra takeoffs and landings a year** in unmet flight demand by 2035. That figure is a forecast gap, not a measurement. It comes from the FAA forecast rising from 406,220 operations in fiscal 2025 to 514,527 in fiscal 2035, which is +26.7%. FAA operations count both takeoffs and landings and include cargo, and the FAA tends to over-forecast.

**Why we call it "unmet":** SFO is strained today, so its airfield is unlikely to absorb that growth.
- **System delay rate: 13.4%** over three years. This is the share of arriving flights that airlines blamed on the airport and air-traffic system. It's the highest among the 343 full-data airports (position 100 of 100).
- **Cause of delays:** the system accounts for 48.9% of delayed flights. Airline causes are 24.7%, late aircraft 23.7% and extreme weather only 2.5%. This category is coded by airlines and includes ordinary weather, so it mostly, but not purely, measures congestion.
- **Overall delay rate:** 27.4% of arrivals were 15 or more minutes late.
- Background (not from our data): SFO's parallel runways are very close together, and in fog or low cloud it often can't land on both at once. That fits a high share of system delays.

**Caveats that matter:**
- **Recent spike:** the latest 12 months show a 17.3% system delay rate. Most of that rise falls in April-July 2026, which ran at 30.0%, against 7.8% in the same months a year earlier. Treat this as a recent spike, not a steady trend. It may have a temporary cause, such as runway work, that isn't in our data.
- **Seats cut:** seats are down 5.0% since 2019 and passengers down 4.4%. Planes are 82.6% full, but that partly reflects fewer seats rather than rising demand.
- **Scheduling limits:** SFO is under FAA Level 2 schedule facilitation. Airline schedules are coordinated there, but there is no hard cap.

SFO ranks 3rd overall by capacity-need score (86.9).

**Worth checking next:** what drove the spike in April-July 2026.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; 'unmet flight demand' is an estimate from the FAA forecast, used only when the airport is strained today; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - SFO: capacity cut; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: SFO: capacity_cut

## A5 - How does that compare with Oakland?

*Pass when:* Oakland is not called unmet demand, because it is not strained.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Oakland"}; `compare_airports` {"airport_codes": ["SFO", "OAK"]}; `airport_profile` {"airport_code": "OAK"}

I took Oakland to mean Oakland San Francisco Bay (OAK). The area's other covered airport is San Jose (SJC). Unlike SFO, Oakland has **no unmet flight demand by our definition**. The FAA forecasts 30,637 extra takeoffs and landings a year by 2035, about 3.5 times fewer than SFO. But Oakland isn't strained today, so we call that figure forecast flight growth, not unmet demand. It's an estimate: FAA operations count takeoffs and landings, include cargo, and the FAA tends to over-forecast.

| | SFO | OAK |
|---|---|---|
| Capacity-need score | 86.9 (3rd of 343) | 46.0 (208th of 343) |
| Forecast extra takeoffs and landings by 2035 | 108,307 | 30,637 |
| Forecast flight growth | 26.7% | 24.8% |
| System delay rate, 3 years | 13.4% | 2.3% |
| System delay rate, latest 12 months | 17.3% | 1.7% |
| Overall delay rate | 27.4% | 18.4% |
| System's share of delayed flights | 48.9% | 12.3% |
| How full the planes are | 82.6% | 74.2% |
| Passengers vs 2019 | -4.4% | -35.5% |

**Why they differ:**
- **Delays:** SFO's system delay rate is 5.83 times Oakland's. At Oakland, most delays come from late-arriving aircraft (54.1%) and the airlines themselves (32.5%), not the airport or air-traffic system. The system category is coded by airlines and includes ordinary weather. Oakland's delays have no recent spike: its latest four months ran at 1.8%, against 1.9% a year earlier.
- **Lost traffic:** Oakland has fewer passengers than in 2019 and seats are down 31.5%. Its planes are only 74.2% full, so it has spare capacity rather than a shortage.

**Risks at Oakland:**
- Southwest carries 76.7% of its passengers, so forecast growth depends on that one airline's plans.
- Cargo makes up 17.9% of its flights. Cargo shares the runways but isn't in the score.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, How full the planes are, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; 'unmet flight demand' is an estimate from the FAA forecast, used only when the airport is strained today; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - SFO: capacity cut; OAK: capacity cut; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: SFO: capacity_cut, OAK: single_airline, OAK: capacity_cut

## A8 - Is Memphis a good candidate, given its cargo traffic?

*Pass when:* Uses the Memphis profile and the cargo share.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Memphis"}; `airport_profile` {"airport_code": "MEM"}

**Memphis (MEM) is a middling candidate for passenger capacity.** The stronger flight-side numbers are partly driven by cargo, so they say less about how many passengers would fill new capacity. It scores 59.5 out of 100 on our capacity-need score, ranking 46th of 78 FAA small-hub airports and 116th of 343 ranked airports overall.

**Why the cargo matters:** cargo makes up 65.1% of departing flights. Cargo flights use the same runways but aren't in the score. The FAA flight forecast does include them, so the forecast flight growth of 18.4% (fiscal 2035 vs 2025) probably reflects cargo growth as much as passenger growth.

Background (not from our data): Memphis is FedEx's main global sorting hub, which explains the cargo-heavy traffic.

**Passenger side is weak (score 45.4):**
- Planes are 73.4% full, in the lower third of airports. The partial 2026 figure is 70.2%.
- Passengers are up only 0.9% since 2019. Passenger flights are down 7.7% since 2019, while seats are up 6.7%.
- The FAA forecasts 25.8% passenger growth (about 609,461 extra boardings a year by 2035). That's in the top quarter, but the FAA tends to over-forecast.

**Flight side is stronger (score 73.7), with caveats:**
- The system delay rate is 4.9% over three years and 5.1% in the latest 12 months. Airlines code this category themselves, and it includes ordinary weather.
- There's no recent spike: the last four months ran at 5.5%, below 6.2% for the same months a year earlier.
- The overall delay rate is 22.7%. Most delays are caused by late-arriving aircraft (39.4%) and the airlines themselves (35.3%), not the airport system (21.4%).
- Memphis isn't classed as strained, so its 29,629 forecast extra takeoffs and landings are just forecast growth, not unmet demand.

**What to check next:** whether any upgrade would mainly serve cargo (airfield, cargo facilities) or passengers (terminal), and the cargo operators' expansion plans. Neither is in our data.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); FAA passenger boarding data CY2025, calendar 2025; BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, Passenger-side score, Flight-side score, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; 'unmet flight demand' is an estimate from the FAA forecast, used only when the airport is strained today; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - MEM: cargo heavy; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: MEM: cargo_heavy

## B1 - Score the top 3 airports that have the highest congestion in the US, only small airports.

*Pass when:* Small-hub class, sorted by the system delay rate, three airports with scores; says what 'small' means.

*Result:* PASS

*Tool calls:* `rank_airports` {"size_classes": ["small"], "sort_by": "system_delay_rate_pct", "limit": 3}

The three most congested small airports are Punta Gorda (PGD), Key West (EYW) and St. Thomas (STT). Only Punta Gorda also scores near the top for capacity need: it is #1 of all 343 ranked airports. Key West and St. Thomas are congested but land in the middle of the pack.

"Small airports" here means the FAA small-hub class (78 ranked airports). I measured "congestion" with the system delay rate over three years: arrival delays blamed on the airport and air-traffic system, divided by arriving flights. Airlines code this category themselves and it includes ordinary weather, so it mostly, but not only, reflects congestion.

| Airport | System delay rate | Capacity-need score (0-100) | Passenger side | Flight side | Rank among small hubs |
|---|---|---|---|---|---|
| Punta Gorda (PGD), FL | 8.6% | 94.9 | 93.3 | 96.5 | 1 of 78 |
| Key West (EYW), FL | 8.0% | 67.7 | 64.2 | 71.2 | 32 of 78 |
| St. Thomas, Cyril E King (STT), VI | 7.9% | 70.8 | 62.3 | 79.3 | 26 of 78 |

**Why the scores differ:**
- **Punta Gorda:** planes are 85.8% full, passengers are up 37.0% since 2019, and the FAA forecasts 30.0% more passengers and 26.8% more flights. **Caution:** Allegiant carries 99.6% of its passengers, so the demand depends on one airline's plans.
- **Key West:** passengers are up 55.9% since 2019, but planes are only 77.3% full and the FAA forecasts just 9.3% more flights.
- **St. Thomas:** planes are 77.9% full and the FAA forecasts 15.0% more flights. It is in the US Virgin Islands, a US territory. If you meant the mainland and states only, I can rerun the ranking without it.

**Things to check:**
- Tweed/New Haven (HVN) was left out because it has only partial data. I can add it.
- I haven't checked whether the latest 12 months show a rising trend or a short spike. I can pull airport profiles for that.

> Data period: BTS Airline Delay Causes, 2023-08 to 2026-07 (three years); BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: System delay rate, Capacity-need score, Passenger-side score, Flight-side score, FAA forecast passenger growth, FAA forecast flight growth; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: PGD: single_airline

## B2 - Top 5 airports in Texas by how full the planes are.

*Pass when:* Five Texas airports by load factor.

*Result:* PASS

*Tool calls:* `rank_airports` {"states": ["TX"], "sort_by": "load_factor_pct", "limit": 5}

Dallas-Fort Worth (DFW) and McAllen (MFE) have the fullest planes in Texas, tied at 82.5%. Houston Intercontinental (IAH), Abilene (ABI) and Corpus Christi (CRP) come next. I ranked all 25 Texas airports with full data, and none were left out.

"How full" here means passengers divided by seats on departing flights over the latest 12 months. It is not the official load factor, which uses passenger-miles. It is the weakest of the score's five inputs because airlines control it through pricing and the planes they fly.

| # | Airport | Size class | Planes full | Capacity-need score | Rank overall (of 343) |
|---|---|---|---|---|---|
| 1 | Dallas-Fort Worth (DFW) | large | 82.5% | 79.3 | 17 |
| 1 | McAllen (MFE) | small | 82.5% | 44.5 | 221 |
| 3 | Houston Bush Intercontinental (IAH) | large | 79.9% | 70.4 | 65 |
| 4 | Abilene (ABI) | nonhub | 79.5% | 78.1 | 26 |
| 5 | Corpus Christi (CRP) | nonhub | 76.6% | 38.0 | 246 |

**What changes the picture:**
- **Full planes alone don't mean strong upside.** McAllen and Corpus Christi have full planes but score low overall. The FAA forecasts McAllen's flights to fall by 9.8%, and Corpus Christi's to grow by only 0.3%. Both have low system delay rates (3.1% and 3.2%), meaning delays the airlines blame on the airport and air-traffic system, which includes ordinary weather.
- **DFW and IAH are flagged as strained.** Their system delay rates are 6.2% and 6.5%. At IAH, flight numbers have stayed flat while passenger numbers have risen.
- **Abilene depends on one airline.** It scores highly, but Envoy Air carries 95.8% of its passengers. If Envoy cuts service, the forecast growth may not arrive.

I can rank Texas by the overall capacity-need score instead, or look at summer-only figures, if that helps.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years); FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: How full the planes are, Capacity-need score, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: ABI: single_airline

## B3 - Which large airports have planes over 85% full?

*Pass when:* Large hubs filtered by a load factor threshold; says that none qualifies.

*Result:* PASS

*Tool calls:* `rank_airports` {"size_classes": ["large"], "sort_by": "load_factor_pct", "min_value": 85, "limit": 30}; `rank_airports` {"size_classes": ["large"], "sort_by": "load_factor_pct", "limit": 10}

**None.** None of the 30 large hubs (the FAA large-hub size class) fills planes more than 85% on average. Newark is the highest at 83.2%, and the top ten all fall between 81.2% and 83.2%.

"How full" here means passengers divided by seats on departing flights over the latest 12 months. This isn't the official load factor, which uses passenger-miles. It's also the weakest of our five inputs, because pricing and airline fleet choices affect it.

| Airport | Planes full | Capacity-need score | Passengers vs 2019 |
|---|---|---|---|
| Newark (EWR) | 83.2% | 80.7 | +1.0% |
| San Francisco (SFO) | 82.6% | 86.9 | -4.4% |
| Dallas-Fort Worth (DFW) | 82.5% | 79.3 | +14.9% |
| Atlanta (ATL) | 82.3% | 69.8 | -4.5% |
| Los Angeles (LAX) | 82.1% | 75.3 | -15.7% |
| New York JFK (JFK) | 82.0% | 84.0 | -2.1% |
| Orlando (MCO) | 81.9% | 87.8 | +14.7% |
| Seattle-Tacoma (SEA) | 81.8% | 79.8 | +1.4% |
| Boston (BOS) | 81.7% | 82.9 | +1.2% |
| Denver (DEN) | 81.2% | 76.7 | +18.8% |

**Warnings that change the picture:**
- **San Francisco and Los Angeles:** seats were cut after 2019 (-5.0% and -12.8%). Their planes are full because there are fewer seats, not because more people want to fly.
- **Newark and JFK:** legal limits cap the number of flights. Newark has an hourly cap, and JFK needs FAA slots to add flights. New gates or runways can't be used without permission for more flights.
- **Dallas-Fort Worth, Orlando and Denver** have the cleanest signals: full planes plus strong passenger growth since 2019.

At large hubs the differences in how full planes are are small, so the capacity-need score separates them better. I can also run the 85% filter for medium or small hubs, or for the summer season only.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: How full the planes are, Capacity-need score; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - the answer uses proxy measures (scores, system delay rate, load factor or forecasts); EWR: legal limit; SFO: capacity cut; LAX: capacity cut
> Warnings printed: EWR: legal_limit, JFK: legal_limit, SFO: capacity_cut, LAX: capacity_cut

## B4 - Compare Portland and Providence.

*Pass when:* Asks which Portland (Oregon or Maine), or covers both and says so.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Portland"}; `find_airport` {"query": "Providence"}

Before I compare: "Portland" could mean **Portland, Oregon (PDX)**, the larger medium-hub airport, or **Portland, Maine (PWM)**, a small-hub airport. Which one do you mean? Since Providence is in New England, it might be Maine, but I'd rather not guess.

For Providence, I'll use **Rhode Island T.F. Green International (PVD)**. Other airports in the same area are Boston Logan (BOS) and Manchester-Boston Regional (MHT), if you'd like either of those instead.

> Data period: no data was used in this reply  
> Assumptions: none  
> Confidence: n/a - no data figures were used in this reply

## B5 - Which airports are the best candidates overall? Only count the ones with complete data.

*Pass when:* National ranking shown per size class.

*Result:* PASS

*Tool calls:* `rank_airports` {"sort_by": "total_score", "limit": 5}

Among the 343 airports with complete data, the top candidates are **Punta Gorda (PGD)** at 94.9, ranked first nationally, and **Orlando International (MCO)** at 87.8, the best-scoring large hub. The score measures upside: how much added capacity would likely be filled. It doesn't measure profit. Because size isn't part of the score, here are the leaders in each FAA size class:

| Size class | Top airports (capacity-need score) | Extra boardings per year by 2035 (FAA forecast, #1) |
|---|---|---|
| Large | Orlando (MCO) 87.8, San Francisco (SFO) 86.9, Chicago O'Hare (ORD) 84.6, New York JFK (JFK) 84.0, Miami (MIA) 83.0 | 7,766,513 |
| Medium | Southwest Florida (RSW) 81.7, Charleston (CHS) 78.8, Jacksonville (JAX) 75.8, San Juan (SJU) 75.4, Raleigh-Durham (RDU) 73.1 | 1,461,612 |
| Small hub | Punta Gorda (PGD) 94.9, Northwest Arkansas (XNA) 85.5, Orlando Sanford (SFB) 85.2, St Pete-Clearwater (PIE) 84.1, Provo (PVU) 80.2 | 329,582 |
| Nonhub | Rickenbacker (LCK) 85.7, Traverse City (TVC) 78.8, Abilene (ABI) 78.1, Scott/MidAmerica (BLV) 77.8, Aguadilla (BQN) 77.7 | 51,970 |

**Warnings that change the picture:**
- **Legal caps:** JFK's flights are limited by FAA slot rules, so added runway or gate space can't be used without more slots. O'Hare has a temporary summer 2026 cap on flights.
- **Seats were cut:** At San Francisco, seats are down 5.0% from 2019 and passengers are down 4.4%. Its full planes reflect fewer seats, not rising demand. The same is true at Aguadilla.
- **One airline:** Allegiant carries over 98% of passengers at Punta Gorda, Orlando Sanford, St Pete-Clearwater, Rickenbacker and Scott/MidAmerica. If Allegiant cuts service, the forecast growth may not arrive.
- **Heavy cargo:** Cargo is 44.2% of flights at Rickenbacker and 42.8% at Aguadilla. Cargo isn't in the score, but it uses the same runways.

Large hubs with no warnings and high data confidence: Orlando, Miami. Mid-sized: Southwest Florida (RSW), Charleston (CHS).

Next, I can profile any of these in detail, including the flight-demand estimate and delay causes.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years); FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, How full the planes are, FAA forecast passenger growth, FAA forecast flight growth; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - SFO: capacity cut; ORD: legal limit; JFK: legal limit; LCK: cargo heavy
> Warnings printed: ORD: legal_limit, JFK: legal_limit, SFO: capacity_cut, PGD: single_airline, SFB: single_airline, PIE: single_airline, LCK: cargo_heavy, LCK: single_airline, ABI: single_airline, BLV: single_airline, BQN: cargo_heavy, BQN: capacity_cut

## B6 - How has passenger traffic at Boston changed since 2019? Give me the year by year picture.

*Pass when:* Year by year values for Boston, with 2026 marked partial.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Boston"}; `airport_profile` {"airport_code": "BOS"}

Boston Logan (BOS) is back to its 2019 passenger level but no higher. It recovered steadily from 2020 to 2024, and 2025 came in a little below 2024. Passengers in the latest 12 months (2025-05 to 2026-04) are up 1.2% on calendar 2019.

I took "Boston" to mean Logan. The other airports nearby are Manchester-Boston Regional (MHT) in New Hampshire and Providence (PVD) in Rhode Island.

| Year | Passengers | Planes full (%) |
|---|---|---|
| 2019 | 20,742,138 | 81.9 |
| 2020 | 6,050,302 | 52.0 |
| 2021 | 10,938,231 | 75.1 |
| 2022 | 17,472,973 | 78.5 |
| 2023 | 19,991,297 | 83.3 |
| 2024 | 21,280,480 | 83.1 |
| 2025 | 21,105,980 | 81.6 |
| 2026 (Jan-Apr only) | 6,139,216 | 78.2 |

"Passengers" counts people on departing flights. Someone on a connecting flight is counted on each leg, so these numbers can be higher than the FAA's official boarding count. "Planes full" is passengers divided by seats. The 2026 row covers only four months, so don't compare it with the full years.

**What sits behind the numbers:**
- **Bigger planes, slightly fewer flights:** Seats are up 1.4% on 2019 and passenger flights are down 3.1% (2025 vs 2019). Passengers per flight went from 106.4 to 111.9.
- **Demand pressure:** Planes were 81.7% full in the latest 12 months, which puts Boston in the top sixth of ranked airports. The FAA forecasts 26.5% passenger growth by fiscal 2035, about 5.6 million more boardings a year. The FAA tends to over-forecast.
- **Congestion:** The system delay rate is 9.1% over three years (10.9% in the latest 12 months), which ranks near the top of all airports. Airlines assign this delay category themselves, and it includes ordinary weather. The newest months show no recent spike.

In short, traffic stopped growing after 2024 while delays stayed high.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); FAA passenger boarding data CY2025, calendar 2025; BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: How full the planes are, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; 'Boston' was taken to mean BOS  
> Confidence: Medium - the answer uses proxy measures (scores, system delay rate, load factor or forecasts); an airport name was resolved by default

## B7 - Show me medium-size airports in the West with the fastest forecast passenger growth.

*Pass when:* West region, medium hubs, sorted by forecast passenger growth.

*Result:* PASS

*Tool calls:* `rank_airports` {"region": "west", "size_classes": ["medium"], "sort_by": "forecast_passenger_growth_pct", "limit": 10}

Portland (PDX) has the fastest FAA-forecast passenger growth among the West's medium-hub airports, at +33.2%. Oakland (OAK), San Jose (SJC) and Boise (BOI) are close behind, each near +29-30%. The figure compares FAA forecast boardings in fiscal 2035 with fiscal 2025. Use it to rank airports against each other, not as a prediction, because the FAA tends to forecast too high.

"Medium" here means the FAA medium-hub class. The West has 11 of them, all with full data. Here are the top 10:

| # | Airport | Forecast pax growth | Extra boardings by 2035 | Pax vs 2019 | Planes full | Score |
|---|---|---|---|---|---|---|
| 1 | Portland (PDX) | 33.2% | 2,989,548 | -6.4% | 82.0% | 72.3 |
| 2 | Oakland (OAK) | 29.9% | 1,402,276 | -35.5% | 74.2% | 46.0 |
| 3 | San Jose (SJC) | 29.6% | 1,620,865 | -35.0% | 73.9% | 44.7 |
| 4 | Boise (BOI) | 28.6% | 735,328 | +24.8% | 78.7% | 66.7 |
| 5 | Sacramento (SMF) | 24.7% | 1,682,362 | +3.8% | 76.5% | 52.0 |
| 6 | Anchorage (ANC) | 24.6% | 660,937 | +0.8% | 72.8% | 59.1 |
| 7 | Ontario (ONT) | 22.9% | 799,528 | +26.5% | 74.1% | 52.0 |
| 8 | Kahului (OGG) | 21.9% | 753,173 | -9.4% | 77.7% | 48.1 |
| 9 | Orange County (SNA) | 19.4% | 1,059,150 | +7.2% | 80.4% | 62.0 |
| 10 | Burbank (BUR) | 16.0% | 531,720 | -0.7% | 72.3% | 44.0 |

**Caveats that change the picture:**
- **Oakland and San Jose:** traffic is still about 35% below 2019 and seats were cut by about 31-32%. Much of their forecast growth would be recovering lost traffic, not new demand. Southwest carries 76.7% of Oakland's passengers, and San Jose has a night noise curfew.
- **Portland and Kahului:** seats were also cut, so full planes partly reflect fewer seats.
- **Boise:** it's the only airport near the top with both real growth since 2019 and no warnings, so it's the cleanest case. Portland has the highest capacity-need score.
- **Orange County:** a legal cap on passengers and departures limits how much added capacity could be used.
- **Anchorage and Ontario:** they're cargo-heavy (cargo is 56.6% and 36.2% of flights), and cargo competes for the same runways.

> Data period: FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: FAA forecast passenger growth, Capacity-need score, How full the planes are, FAA forecast flight growth; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - PDX: capacity cut; OAK: capacity cut; SJC: capacity cut, legal limit; ANC: cargo heavy
> Warnings printed: SJC: legal_limit, SNA: legal_limit, PDX: capacity_cut, OAK: single_airline, OAK: capacity_cut, SJC: capacity_cut, ANC: cargo_heavy, ONT: cargo_heavy, OGG: capacity_cut

## B8 - What's the busiest month at Burlington, Vermont, and how full are the planes then?

*Pass when:* The busiest month and its load factor.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Burlington, Vermont"}; `airport_trend` {"airport_code": "BTV", "metric": "passengers"}; `airport_trend` {"airport_code": "BTV", "metric": "load_factor_pct"}

**October is the busiest month at Patrick Leahy Burlington International (BTV), and planes are about 85% full then.** Over the last three Octobers (2023-2025), the airport averaged 73,848 passengers a month, with 84.9% of seats filled.

The most recent October (2025) was the busiest single month in the 36-month series: 79,157 passengers, with planes 86.9% full.

**How the busiest months compare**

| Month (3-year average) | Passengers | Share of seats filled |
|---|---|---|
| October | 73,848 | 84.9% |
| August | 70,578 | 85.5% |
| July | 67,585 | 86.7% |
| September | 63,462 | 79.8% |
| January (quietest) | 45,791 | 80.1% |

**What this means**
- **October isn't when planes are fullest.** July is, at 86.7%. That suggests airlines add more seats for the October rush, so the planes fill up a bit less than in midsummer.
- **The busy season runs July-October.** Every other month is clearly quieter, with June the busiest of the rest at 58,314 passengers.
- **The year-round average is 83.0%** for the latest 12 months, so October is only somewhat above normal.
- **How full the planes were has varied over time.** Planes were very full from mid-2023 to early 2024, peaking at 91.0% in July 2023. They were noticeably emptier for most of the following year, with a low of 71.8% in September 2024, then filled up again from mid-2025.

"Passengers" here means people on departing flights. "Share of seats filled" is passengers divided by seats, not the official load factor (which is based on miles flown). It depends partly on airline pricing and aircraft choices, so treat it as a rough sign of demand.

Background (not from our data): Vermont's autumn foliage season usually draws a lot of tourists, which likely explains the October peak.

> Data period: BTS T-100 airport-month summary, 2023-05 to 2026-04  
> Assumptions: proxies, not direct measurements: How full the planes are  
> Confidence: Medium - the answer uses proxy measures (scores, system delay rate, load factor or forecasts)

## C1 - Score the top 3 airports that have the highest congestion in August in the US.

*Pass when:* Ranks by the August system delay rate and says scores do not exist by month.

*Result:* PASS

*Tool calls:* `rank_airports` {"sort_by": "system_delay_rate_pct", "month": 8, "limit": 3}

Using the system delay rate for August as the measure of congestion, the three most congested ranked airports are Newark (EWR), Orlando (MCO) and San Juan (SJU). All three score high on capacity need. Orlando scores highest, at 87.8.

| Airport | August system delay rate | Capacity-need score | Passenger side | Flight side | National rank (of 343) |
|---|---|---|---|---|---|
| Newark Liberty (EWR), large hub | 10.9% | 80.7 | 72.7 | 88.6 | 13 |
| Orlando International (MCO), large hub | 10.3% | 87.8 | 81.5 | 94.0 | 2 |
| San Juan Luis Munoz Marin (SJU), medium hub | 9.8% | 75.4 | 77.6 | 73.3 | 41 |

**What the numbers mean**
- **August system delay rate:** the share of arriving flights delayed by causes in the airport and air-traffic system, for August 2023, 2024 and 2025 added together. Airlines code this category themselves, and it includes ordinary weather, so it mostly measures congestion but not only congestion.
- **Capacity-need score (0-100):** estimates how much added capacity would be filled, over the latest 12 months. It doesn't measure profit. The data marks all three airports as strained today.

**Things that change the picture**
- **Newark has a legal flight cap:** 36 arrivals and 36 departures an hour. Its high delay rate and flight-side score may not turn into added flights while the cap stays.
- **San Juan is tied for third:** at least one other airport also has 9.8%, so third place isn't clear-cut. It is also in a US territory. If you want US states only, I can give you the next airport instead.
- **Orlando looks strongest on growth:** passengers are up 14.7% since 2019, and the FAA forecasts growth of 28.2% in passengers and 26.4% in flights.
- **Some airports aren't in the ranking:** 59 airports with partial data were left out, and so were 104 with too few August arrivals for a reliable rate.

Next, I could re-rank by the overall August delay rate or leave out the US territories.

> Data period: BTS Airline Delay Causes, August of 2023, 2024, 2025 (summed); BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: System delay rate, Capacity-need score, Passenger-side score, Flight-side score, FAA forecast passenger growth, FAA forecast flight growth; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - EWR: legal limit; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: EWR: legal_limit

## C9 - Which large airports are most congested in summer?

*Pass when:* Ranks large hubs by the summer (June to August) system delay rate, using the season filter; Newark leads.

*Result:* PASS

*Tool calls:* `rank_airports` {"size_classes": ["large"], "sort_by": "system_delay_rate_pct", "season": "summer", "limit": 10}; `rank_airports` {"size_classes": ["large"], "sort_by": "total_delay_rate_pct", "season": "summer", "limit": 10}

Over the summers of 2023-2025, Newark (EWR) is the most congested large hub. Next come Orlando (MCO), New York JFK, Boston (BOS) and Denver (DEN). If you count delays from every cause, Orlando ranks first and Florida airports fill four of the top five places.

I'm measuring congestion two ways, using June-August of 2023, 2024 and 2025 combined. All 30 FAA large hubs were ranked.
- **System delay rate:** the share of arriving flights delayed by the airport and air-traffic system. Airlines assign this cause themselves, and it includes ordinary weather.
- **Overall delay rate:** the share of arrivals 15 or more minutes late for any reason.

| Airport | Summer system delay % | Summer overall delay % |
|---|---|---|
| Newark (EWR) | 13.2 | 27.5 |
| Orlando (MCO) | 10.6 | 32.1 |
| New York JFK (JFK) | 10.1 | 27.1 |
| Boston (BOS) | 9.9 | 28.5 |
| Denver (DEN) | 9.7 | 27.0 |
| New York LaGuardia (LGA) | 9.5 | not in top 10 |
| Fort Lauderdale (FLL) | 9.0 | 30.1 |
| Chicago O'Hare (ORD) | 8.7 | not in top 10 |
| Miami (MIA) | 8.7 | 28.9 |
| Washington Reagan (DCA) | 8.2 | not in top 10 |

Tampa (TPA, 30.3%), Philadelphia (PHL, 27.4%) and Dallas-Fort Worth (DFW, 26.8%) also make the top 10 for overall delays, but not for system delays.

Background (not from our data): Florida's summer afternoon thunderstorms probably explain much of its high overall delay rates.

**Caveats that change the investment reading:**
- **Legal limits on flights:** Newark, JFK, LaGuardia, O'Hare (a temporary summer 2026 cap) and Reagan all have caps or slot limits. Added runway or gate capacity there can't be used without more flights being allowed. At LaGuardia and Reagan, the FAA's flight forecast already assumes the limits.
- **Capacity cuts:** Fort Lauderdale and Philadelphia have fewer seats than in 2019, so full planes there reflect cut capacity rather than rising demand.
- **No legal limit or capacity-cut warning:** Orlando, Boston, Denver and Miami are strained without either problem, and Orlando ranks first for capacity need among large hubs.

I can profile any of these to break down delay causes and show whether delays are rising.

> Data period: BTS Airline Delay Causes, summer (June, July, August) of 2023, 2024, 2025 (summed) / 2023-08 to 2026-07 (three years); BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: System delay rate, How full the planes are, FAA forecast passenger growth, FAA forecast flight growth  
> Confidence: Medium - EWR: legal limit; JFK: legal limit; LGA: forecast constrained, legal limit; FLL: capacity cut
> Warnings printed: EWR: legal_limit, JFK: legal_limit, LGA: legal_limit, ORD: legal_limit, DCA: legal_limit, LGA: forecast_constrained, FLL: capacity_cut, DCA: forecast_constrained, PHL: capacity_cut

## C10 - And is it the same ones in winter?

*Pass when:* A follow-up: ranks the same group for winter (December to February); San Francisco leads, so the answer is no.

*Result:* PASS

*Tool calls:* `rank_airports` {"size_classes": ["large"], "sort_by": "system_delay_rate_pct", "season": "winter", "limit": 10}; `rank_airports` {"size_classes": ["large"], "sort_by": "total_delay_rate_pct", "season": "winter", "limit": 10}

Mostly, yes, but the order changes. San Francisco (SFO) moves to the top in winter, while Boston, Denver and Chicago O'Hare drop out of the top 10 for system delays. Seven airports are in the top 10 in both seasons: Newark, LaGuardia, Fort Lauderdale, Miami, Reagan, Orlando and JFK. Delay rates are also generally lower in winter. The worst winter overall delay rate (25.5%) is well below the worst summer one (32.1% at Orlando).

"Winter" here means December, January and February of 2023, 2024 and 2025, with each December counted in the same calendar year as that January and February. I used the same two measures as before, ranked across all 30 large hubs.

| Airport | Winter system delay % | Winter overall delay % | In summer top 10 for system delays? |
|---|---|---|---|
| San Francisco (SFO) | 11.6 | 25.5 | No |
| Fort Lauderdale (FLL) | 9.7 | 25.5 | Yes |
| Newark (EWR) | 9.1 | not in top 10 | Yes (1st) |
| LaGuardia (LGA) | 9.0 | 21.7 | Yes |
| Miami (MIA) | 8.9 | 22.7 | Yes |
| Reagan (DCA) | 8.5 | 22.4 | Yes |
| Orlando (MCO) | 7.8 | 23.0 | Yes |
| JFK | 7.4 | 21.8 | Yes |
| Tampa (TPA) | 7.3 | 22.5 | No |
| Las Vegas (LAS) | 7.1 | not in top 10 | No |

San Diego (SAN, 22.1%) and Boston (BOS, 21.5%) also make the top 10 for overall delays in winter.

**What this means for investment:**
- The Florida hubs and the New York-area airports are congested in both seasons, so their strain lasts all year rather than peaking in one season.
- **San Francisco:** it ranks first in winter, but seats there are down 5.0% since 2019 because capacity was cut. Its full planes reflect fewer seats more than rising demand.
- **Legal limits on flights:** the slot or cap limits at Newark, JFK, LaGuardia and Reagan still apply. San Diego has a night curfew.
- **Delay coding:** airlines decide when a delay counts as a "system" delay, and that category includes ordinary weather. Some of the winter pattern may be weather rather than lack of capacity.

> Data period: BTS Airline Delay Causes, winter (December, January, February) of 2023, 2024, 2025 (summed) / 2023-08 to 2026-07 (three years); BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: System delay rate, How full the planes are  
> Confidence: Medium - SFO: capacity cut; FLL: capacity cut; EWR: legal limit; LGA: forecast constrained, legal limit
> Warnings printed: EWR: legal_limit, LGA: legal_limit, DCA: legal_limit, JFK: legal_limit, SAN: legal_limit, SFO: capacity_cut, FLL: capacity_cut, LGA: forecast_constrained, DCA: forecast_constrained

## C2 - Where is Delta the dominant airline?

*Pass when:* Says airline-network questions are not supported; may offer the biggest-airline share per airport.

*Result:* PASS

*Tool calls:* `rank_airports` {"sort_by": "top_airline_share_pct", "limit": 30, "size_classes": ["large", "medium"]}; `airport_profile` {"airport_code": "ATL"}; `airport_profile` {"airport_code": "MSP"}; `airport_profile` {"airport_code": "DTW"}; `airport_profile` {"airport_code": "SLC"}

I can confirm four airports where Delta is the biggest airline: Atlanta (ATL), Minneapolis-St Paul (MSP), Salt Lake City (SLC) and Detroit (DTW). This is a partial list, because my data can't filter by airline. For each airport it records only the biggest airline and that airline's share of passengers. So I ranked large and medium hubs by that share, then looked up these four one at a time.

| Airport | Delta's share of passengers (2025) | Capacity-need score (0-100) | How full the planes are | Passengers vs 2019 |
|---|---|---|---|---|
| Atlanta (ATL) | 74.7% | 69.8 | 82.3% | -4.5% |
| Minneapolis-St Paul (MSP) | 58.0% | 64.8 | 81.0% | -10.0% |
| Salt Lake City (SLC) | 57.5% | 60.9 | 80.1% | +4.7% |
| Detroit (DTW) | 54.8% | 60.6 | 79.2% | -10.1% |

What this means for capacity:
- **Atlanta** is the strongest Delta case. Its planes are among the fullest of any airport, and the FAA forecasts 11,460,085 more passengers boarding a year by 2035. But Atlanta relies on Delta more than almost any other large hub, so its growth largely depends on Delta's plans.
- **Minneapolis and Detroit** both have fewer seats than in 2019, and passengers fell faster. Their fairly full planes reflect those seat cuts rather than rising demand.
- **Salt Lake City** is the only one of the four with more passengers than in 2019. It has low congestion: a system delay rate of 2.8%, the share of arrivals delayed by the airport and air-traffic system. That category is coded by airlines and includes ordinary weather.

This list may be missing airports:
- I didn't check small hubs or nonhubs.
- I didn't check other large airports where Delta may be the biggest airline without a majority share.

I can look up any specific airports you have in mind and tell you which airline is biggest at each.

> Data period: BTS T-100 Segment, calendar 2025; BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, How full the planes are, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - DAL: legal limit; OAK: capacity cut; ANC: cargo heavy; EWR: legal limit
> Warnings printed: DAL: legal_limit, EWR: legal_limit, SJC: legal_limit, DAL: single_airline, HOU: single_airline, MDW: single_airline, OAK: single_airline, OAK: capacity_cut, ANC: cargo_heavy, MSP: capacity_cut, SJC: capacity_cut, DTW: capacity_cut, : more

## C3 - How many flights go from JFK to London?

*Pass when:* Declines: route-level questions are not supported.

*Result:* PASS

*Tool calls:* `airport_profile` {"airport_code": "JFK"}

I can't give you a count for JFK to London. This version has no route or destination data, so it can't count flights between two cities. The closest thing it has is the long-haul share of departures from John F Kennedy International (JFK), and London flights are part of that.

**Long-haul departures from JFK, calendar 2025** (domestic and international, all airlines; these cutoffs are our own, since there's no official definition of long-haul):

| Cutoff | Passenger flights | Share of passenger flights |
|---|---|---|
| 2,000+ miles | 96,455 | 45.4% |
| 2,500+ miles | 60,217 | 28.4% |
| 3,000+ miles | 49,841 | 23.5% |

That's out of 212,394 departing passenger flights in 2025. 45.6% of JFK's departing passengers fly to US destinations.

Background (not from our data): London is more than 3,000 miles from New York, so JFK-London flights are inside the 3,000+ mile group. That group also includes many other European, Asian and West Coast routes, so it can't stand in for London alone.

**For investment purposes:** JFK has a capacity-need score of 84.0. That ranks it 4th of 30 large hubs and 9th of 343 airports overall. Note that JFK is slot-controlled by FAA order. Extra runway or gate capacity can't be used unless more slots are granted, which limits how much added capacity could be filled.

For the actual JFK-London flight count, you'd need a route-level source such as the BTS T-100 Segment data filtered by origin and destination. I can also show JFK's delays, how full its planes are, or how it compares with Newark (EWR) and LaGuardia (LGA).

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); FAA passenger boarding data CY2025, calendar 2025; BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, How full the planes are; long-haul means 3,000 miles or more (our definition; adjustable); scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - JFK: legal limit; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: JFK: legal_limit

## C4 - What's the congestion level at Teterboro?

*Pass when:* Says Teterboro is outside the covered airports; no invented number.

*Result:* FAIL - failed: says /not covered|outside|isn't covered|is not covered|not in|isn't in|not among|not one of|don't have|no data/

*Tool calls:* `find_airport` {"query": "Teterboro"}

I can't give a congestion figure for Teterboro, because it isn't one of the 402 FAA primary airports in our dataset. Our dataset only covers primary airports, the ones with enough scheduled passenger boardings to get that FAA status.

Background (not from our data): Teterboro is mainly a private-jet and business-aviation airport. It has almost no scheduled airline service, so the airline delay data we use to measure congestion doesn't exist for it.

**What I can do instead:** I can show congestion at the nearby New York-area airports in our dataset, such as Newark (EWR), LaGuardia (LGA) and JFK (JFK). For each one I'd give:
- **System delay rate:** over three years and over the latest 12 months. Airlines code these delays themselves, and the category includes ordinary weather.
- **Overall delay rate:** all delays, whatever the cause.
- **Delay causes:** what's behind the delays.

Do you want that comparison, or a closer look at one of them?

> Data period: no data was used in this reply  
> Assumptions: none  
> Confidence: n/a - no data figures were used in this reply

## C5 - Which airports were the top expansion candidates in 2021?

*Pass when:* Says the score exists for the latest period only; offers raw 2021 metrics.

*Result:* PASS

*Tool calls:* `rank_airports` {"year": 2021, "sort_by": "load_factor_pct", "limit": 5}; `rank_airports` {"year": 2021, "sort_by": "system_delay_rate_pct", "limit": 5}

I can't rank 2021 expansion candidates, because the capacity-need score only exists for the latest period. What I can show is the 2021 raw numbers for the two measures behind the score that have yearly history. The ranked lists include only the 343 airports with full data.

**Fullest planes in 2021** (passengers divided by seats on departing flights)

| Airport | 2021 | Score today |
|---|---|---|
| McAllen (MFE) | 84.4% | 44.5 |
| Wilkes-Barre/Scranton (AVP) | 84.3% | 71.3 |
| Aguadilla (BQN), Puerto Rico | 83.8% | 77.7 |
| Ponce (PSE), Puerto Rico | 82.3% | 75.5 |
| Hartford Bradley (BDL) | 82.2% | 65.9 |

**Highest system delay rate in 2021** (share of arriving flights delayed for reasons airlines put in the "system" category, which includes ordinary weather)

| Airport | 2021 | Score today |
|---|---|---|
| Key West (EYW) | 11.5% | 67.7 |
| Punta Gorda (PGD) | 10.0% | 94.9 (ranked 1st of 343) |
| Newark (EWR) | 8.8% | 80.7 |
| Dallas Love Field (DAL) | 8.4% | 42.8 |
| Aguadilla (BQN) | 8.4% | 77.7 |

**Caveats that change the reading:**
- **Legal caps:** Newark is limited to 36 arrivals and 36 departures an hour. Dallas Love Field is limited by federal law to 20 gates. Both limits restrict expansion.
- **Seat cuts:** Wilkes-Barre/Scranton, Aguadilla and Ponce still have fewer seats than in 2019. Their full planes partly reflect seat cuts rather than rising demand.
- **Other:** Cargo is 42.8% of flights at Aguadilla. Ponce's delay data is thin, too thin to rank it on delays for 2021. One airline carries almost all passengers at Punta Gorda (Allegiant) and at Dallas Love Field (Southwest).

2021 doesn't point the same way as today: McAllen and Dallas Love Field topped a 2021 list but now have some of the lowest scores here (44.5 and 42.8).

Background (not from our data): 2021 was a pandemic recovery year with reduced schedules, so full planes and delays then may not show lasting demand.

I can run the same lists for other years, or split them by airport size.

> Data period: BTS T-100 airport-month summary, calendar 2021 / 2025-05 to 2026-04 (latest 12 complete months); BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / calendar 2021  
> Assumptions: proxies, not direct measurements: How full the planes are, Capacity-need score, System delay rate; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - 1 of the 5 listed airports has weaker data (PSE: small delay sample); AVP: capacity cut; BQN: capacity cut, cargo heavy; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: EWR: legal_limit, DAL: legal_limit, AVP: capacity_cut, BQN: cargo_heavy, BQN: capacity_cut, PSE: small_sample, PSE: capacity_cut, PSE: small_airport_forecast, PGD: single_airline, DAL: single_airline

## C6 - Should we invest in expanding LaGuardia?

*Pass when:* Gives the evidence and the slot limit; leaves the decision to the analyst.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "LaGuardia"}; `airport_profile` {"airport_code": "LGA"}

That decision is yours, but the data shows mixed evidence. LaGuardia (LGA) is very congested, yet a legal cap on flights limits how much added capacity airlines could actually use. It ranks 19th of 30 large hubs on our capacity-need score (67.8 out of 100), and 76th of 343 airports overall.

**The case for:**
- **Congestion:** 8.4% of arriving flights had system delays over three years, and 10.4% in the latest 12 months. Only about 2% of airports score worse. Airlines assign this delay category, and it includes ordinary weather. Overall, 21.5% of arrivals were at least 15 minutes late. System delays are the largest single cause, at 39.3% of delayed flights. The recent level is not a short-term spike.
- **Full planes:** 80.8% of seats were filled, and 85.4% in the peak month (August 2025).
- **Estimated unmet flight demand:** the FAA forecasts 33,029 more takeoffs and landings a year by 2035 (+9.3%). This is a forecast, not a measurement.

**The case against:**
- **Legal limits:** an FAA order caps flight slots, and nonstop flights are limited to 1,500 miles (Saturdays exempt). The FAA forecast already assumes the cap, so more airfield capacity may not mean more flights.
- **Growth comes from bigger planes, not more flights:** departing passenger flights are down 4.8% since 2019, while passengers per flight rose from 85.3 to 94.7. Passengers are up only 4.7% since 2019, and the FAA forecasts +18.4% by 2035. Both are about average among airports.

**What to check next:** whether the slot rules could change, gate and terminal use (not in our data), and comparisons with New York JFK (JFK) and Newark (EWR). I can run that comparison.

Background (not from our data): LaGuardia's terminals were recently rebuilt at large scale, so the room for more terminal work may be small.

I don't have cost or return figures. The score only measures how much added capacity would likely be filled.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); FAA passenger boarding data CY2025, calendar 2025; BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, How full the planes are, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; 'unmet flight demand' is an estimate from the FAA forecast, used only when the airport is strained today; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - LGA: forecast constrained, legal limit; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: LGA: legal_limit, LGA: forecast_constrained

## C7 - What will a new terminal at Denver cost, and what return would we get?

*Pass when:* Declines cost and return; offers the capacity-need evidence.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Denver"}

I can't estimate what a new terminal at Denver International (DEN) would cost or what it would return. Our data has no construction costs, revenue, gate counts or terminal sizes. What I can show is the upside: how much added capacity would likely be filled. Denver scores well on that.

**Capacity-need score for Denver (DEN):** 76.7 out of 100. That ranks it 12th of 30 large hubs and 33rd of the 343 airports with full data. The score compares Denver with other airports and stands in for profit potential. It doesn't measure profit.

| Metric | Value | What it measures |
|---|---|---|
| Load factor | 81.2% | Share of seats filled, May 2025 - April 2026 |
| Passenger growth since 2019 | 18.8% | Passengers now vs 2019 |
| Seat change since 2019 | 26.1% | Airlines have added capacity, not cut it |
| FAA forecast passenger growth | 23.7% | Fiscal 2035 vs 2025 |
| FAA forecast extra boardings | 9,475,223 | Added yearly boardings by fiscal 2035 |
| System delay rate | 6.6% | Three-year rate, August 2023 - July 2026 |
| FAA forecast flight growth | 14.7% | Fiscal 2035 vs 2025 |
| Boardings 2025 | 39,976,695 | Size (not part of the score) |

The data flags Denver as strained today. Planes are fairly full, demand has grown and is forecast to keep growing, and airlines have kept adding seats. One caution on the delay figure: airlines assign delays to the "system" category themselves, and it includes ordinary weather.

**Next steps you could take:**
- Run the full Denver profile, including the flight-demand estimate and what is causing the delays.
- Compare Denver with other large hubs.

For cost and return, you would need Denver's capital plan and the airport's financial statements, which are outside this dataset.

> Data period: see the tool trace  
> Assumptions: proxies, not direct measurements: Capacity-need score; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - the answer uses proxy measures (scores, system delay rate, load factor or forecasts)

## C8 - What is the delay rate at Glacier Park airport in Kalispell, and can I trust it?

*Pass when:* Resolves Glacier Park to FCA, gives the rate and the sample size.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Glacier Park, Kalispell"}; `find_airport` {"query": "FCA"}; `find_airport` {"query": "Kalispell"}; `airport_profile` {"airport_code": "FCA"}

Over the last three years, 4.0% of arriving flights at Glacier Park International in Kalispell (FCA; its FAA code is GPI) had a system delay, and 16.6% arrived 15 or more minutes late for any reason. The figures rest on a solid sample and full data, so you can rely on them, as long as you keep in mind what they measure.

| Measure | Value |
|---|---|
| System delay rate, 3 years (2023-08 to 2026-07) | 4.0% |
| System delay rate, latest 12 months | 4.7% |
| Overall delay rate (15+ min, any cause), 3 years | 16.6% |
| Arriving flights in the sample | 15,601 |
| Rank on system delay among the 343 fully ranked airports (0-100) | 49.1, about the middle |

**Why you can trust it:**
- The rate is based on 15,601 arriving flights, so it isn't a small sample.
- The airport has full data and no data warnings.
- The yearly figures are consistent: 3.1% in 2023, 3.9% in 2024 and 3.9% in 2025.

**Limits to keep in mind:**
- **Airlines report the causes.** The "system" category covers delays put down to the airport and air-traffic system, and it includes ordinary weather. So it mostly reflects congestion, but not only congestion.
- **Coverage is partial.** It counts only domestic flights by the larger airlines that report delays.
- **Most delays aren't the airport's fault.** Of flights delayed 15+ minutes, 42.9% were put down to the airline and 28.5% to a late incoming aircraft. Only 24.1% were system delays and 4.4% extreme weather.
- **There's a slight recent rise, not a spike.** April-July 2026 ran at 5.3%, against 3.3% in the same months a year earlier. The data doesn't count this as a spike concentrated in recent months, so treat it as a modest drift to watch rather than a clear trend.

In short, Kalispell's congestion is moderate. Its high capacity-need score (76.3) comes mainly from the passenger side, not from delays.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, Passenger-side score, System delay rate; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
