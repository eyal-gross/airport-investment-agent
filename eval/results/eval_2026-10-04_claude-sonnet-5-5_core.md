# Evaluation run - 2026-10-04 15:53 - claude-sonnet-5-5

**7 of 7 questions passed.** 223 numbers appeared in the answers; 0 answers ended with a number that could not be traced to a tool result; 1 answers passed only after one automatic rewrite. Average 7.6s per question; 205,404 input and 5,374 output tokens in total.

| Id | Group | Result | Tools | Number check | Seconds |
|---|---|---|---|---|---|
| A1 | core | PASS | rank_airports | passed | 8.5 |
| A2 | core | PASS | find_airport, find_airport, compare_airports | passed | 8.7 |
| A6 | follow-up | PASS | compare_airports | passed | 7.0 |
| A3 | core | PASS | airport_profile | passed | 4.9 |
| A7 | follow-up | PASS | airport_profile | rewritten | 8.6 |
| A4 | core | PASS | airport_profile | passed | 7.2 |
| A5 | follow-up | PASS | find_airport, compare_airports | passed | 8.5 |

## A1 - Which airports in New England are strong candidates for terminal expansion?

*Pass when:* A ranked list from the six states, scores shown, reasons given.

*Result:* PASS

*Tool calls:* `rank_airports` {"region": "new england"}

**The strongest New England candidates are Boston (BOS), Burlington (BTV) and Portland, Maine (PWM).** Bangor (BGR) and Hartford (BDL) follow. The score is a proxy for how much added capacity would be filled. It is not a measure of terminal need or return, and there is no cost data.

| Airport | Score | Planes full | Passenger growth since 2019 | System delay | FAA forecast passenger growth | FAA forecast flight growth |
|---|---|---|---|---|---|---|
| Boston (BOS), large | 82.9 | 81.7% | 1.2% | 9.1% | 26.5% | 23.8% |
| Burlington (BTV), small hub | 79.2 | 83.0% | 2.3% | 5.5% | 22.9% | 23.0% |
| Portland (PWM), small hub | 77.4 | 82.8% | 17.2% | 4.6% | 21.6% | 23.3% |
| Bangor (BGR), nonhub | 71.8 | 80.4% | 40.8% | 4.7% | 24.1% | 15.2% |
| Hartford (BDL), medium | 65.9 | 81.3% | -2.7% | 4.9% | 15.7% | 16.5% |

- **Boston:** It has the highest system delay rate in the group, and it is flagged as strained. It also has the largest absolute FAA-forecast gain, about 5.6 million extra boardings a year by 2035.
- **Burlington:** Its planes are the fullest in the region. It is flagged as strained. Passenger growth has been modest, and the FAA forecasts about 164,000 extra boardings.
- **Portland:** Passengers are up 17.2% since 2019, with seats up 21.6%, so airlines have already added capacity. It is not flagged as strained. The FAA forecasts about 278,000 extra boardings.
- **Bangor:** Passenger growth has been strong, but the flight-side forecast is weaker than at the three above.

Four airports are not ranked because their data is partial or thin: New Haven (HVN), Cape Cod Gateway (HYA), Block Island (BID) and Westerly (WST). I have not scored them.

Caveats:
- System delay includes ordinary weather and is coded by airlines.
- FAA forecasts tend to run high.
- Load factor here is passengers divided by seats, not the official measure.

Gate counts, terminal utilization and construction plans are not in the data, so check those next. I can pull a detailed profile or monthly seasonality for any of these airports.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years); FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, Flight-side score, How full the planes are, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - the answer uses proxy measures (scores, system delay rate, load factor or forecasts)

## A2 - Compare LA and Santa Ana airport congestion levels.

*Pass when:* LAX vs SNA side by side, a clear verdict, Santa Ana's legal cap flagged.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "LA"}; `find_airport` {"query": "Santa Ana"}; `compare_airports` {"airport_codes": ["LAX", "SNA"]}

Los Angeles International (LAX) is somewhat more congested than John Wayne/Orange County (SNA), but the gap is modest. I assumed "LA" means LAX. The same metro area also has Ontario (ONT), Burbank (BUR) and Long Beach (LGB). "Santa Ana" is SNA.

| Measure | LAX | SNA |
|---|---|---|
| System delay rate, 3 years | 4.8% | 3.9% |
| System delay rate, latest 12 months | 5.0% | 4.3% |
| Overall delay rate (any cause, 15+ min late) | 18.9% | 17.5% |
| Share of delays coded "system" | 25.7% | 22.4% |
| Load factor | 82.1% | 80.4% |

The system delay rate is our congestion measure. Airlines code that category, and it includes ordinary weather, so it is mostly but not purely congestion. LAX is higher on all three delay rates, by about 1 percentage point or less. Neither airport is flagged as strained.

For both, most delays come from airline causes and late-arriving aircraft rather than the system category. At SNA, late aircraft account for 39.9% of delays. At LAX they account for 33.4%.

Two warnings:
- **LAX:** Capacity was cut. Seats are down 12.8% against 2019 and passengers are down 15.7%. The full planes reflect fewer seats, not rising demand.
- **SNA:** It has a legal cap, a departure limit and a night curfew. The cap is 12.2 or 12.5 million annual passengers counting arrivals and departures. In our departing-only units that is roughly 6.1 to 6.25 million. SNA had 5.59 million passengers in the latest 12 months. Which cap figure applies is not verified, and the legal-limits list is partial. Added capacity at SNA may be constrained regardless of delays.

The capacity-need scores are 75.3 for LAX and 62.0 for SNA. The score is a proxy for upside only and says nothing about cost or return.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, How full the planes are, System delay rate; 'LA' was taken to mean LAX; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - LAX: capacity cut; SNA: legal limit; the answer uses proxy measures (scores, system delay rate, load factor or forecasts); an airport name was resolved by default
> Warnings printed: SNA: legal_limit, LAX: capacity_cut

## A6 - And how did congestion at those two look in 2023?

*Pass when:* Uses the same two airports without being told again, and 2023 values.

*Result:* PASS

*Tool calls:* `compare_airports` {"airport_codes": ["LAX", "SNA"], "year": 2023}

Congestion was higher at both airports in 2023 than in the latest period, and LAX was still the more congested of the two. The tool reports 12 months of delay data for calendar 2023 for both airports.

| Measure (calendar 2023) | LAX | SNA |
|---|---|---|
| System delay rate | 5.6% | 4.2% |
| Overall delay rate | 20.5% | 18.5% |
| Load factor | 83.9% | 83.1% |

**Change against the figures I gave earlier** (earlier figures are 3-year, 2023-08 to 2026-07, and latest 12 months, 2025-08 to 2026-07):
- **LAX:** The system delay rate was 5.6% in 2023, against 5.0% in the latest 12 months. The 3-year figure is 4.8%.
- **SNA:** The system delay rate was 4.2% in 2023, against 4.3% in the latest 12 months. The 3-year figure is 3.9%. This is essentially flat.

The gap between the two was wider in 2023 (1.4 percentage points on system delays) than it is now (0.7 points in the latest 12 months). Most of the gap closing comes from LAX improving.

Load factor fell at both airports from 2023 to the latest period. LAX went from 83.9% to 82.1% and SNA from 83.1% to 80.4%.

The system delay category is coded by airlines and includes ordinary weather, so it is mostly but not purely congestion. The capacity cut at LAX and the legal cap at SNA that I flagged earlier still apply.

> Data period: BTS T-100 airport-month summary, calendar 2023; BTS Airline Delay Causes, calendar 2023; BTS T-100 Segment, calendar 2023  
> Assumptions: proxies, not direct measurements: How full the planes are, System delay rate  
> Confidence: Medium - LAX: capacity cut; SNA: legal limit; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: SNA: legal_limit, LAX: capacity_cut

## A3 - What is the percentage of long haul flights out of Anchorage airport?

*Pass when:* One number, the 3,000-mile definition stated, the cargo-included number next to it.

*Result:* PASS

*Tool calls:* `airport_profile` {"airport_code": "ANC"}

**Anchorage (ANC): 2.8% of departing passenger flights are long-haul.** That uses our default cutoff of 3,000 miles or more, in calendar 2025. It is 1,061 of 38,150 passenger departures. There is no official definition of long-haul, so the cutoff is ours.

If you count cargo flights too, the share is 31.0% (27,305 of 87,988 departures). Cargo and other non-passenger flights are 56.6% of all departures here, and many of them are long international legs. That is why the two figures differ so much.

The share is sensitive to the cutoff:

| Cutoff | Passenger flights | All flights incl. cargo |
|---|---|---|
| 2,000 miles | 13.7% | 47.4% |
| 2,500 miles | 9.8% | 43.2% |
| 3,000 miles | 2.8% | 31.0% |

For passenger service, ANC is mostly domestic, at 98.6% of passengers. Alaska Airlines is the biggest carrier, with 61.4% of passengers. The cargo-heavy traffic also lowers our data confidence for this airport.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); BTS T-100 Segment, calendar 2025  
> Assumptions: long-haul means 3,000 miles or more (our definition; adjustable)  
> Confidence: Medium - ANC: cargo heavy
> Warnings printed: ANC: cargo_heavy

## A7 - What if long-haul means over 2,300 miles?

*Pass when:* Recomputed at 2,300 miles for Anchorage.

*Result:* PASS

*Tool calls:* `airport_profile` {"airport_code": "ANC", "long_haul_miles": 2300}

With a 2,300-mile cutoff, **12.6% of Anchorage (ANC) departing passenger flights are long-haul.** That is 4,820 of 38,150 flights in calendar 2025.

If you include cargo flights, the share is 46.5% (40,947 of 87,988 departures).

The tool counts flights flying at least the cutoff distance, so "2,300 miles or more" is what was measured, not strictly "over 2,300".

The 2,300-mile figure sits between the 2,000-mile and 2,500-mile results I showed earlier:

| Cutoff | Passenger flights | All flights incl. cargo |
|---|---|---|
| 2,000 miles | 13.7% | 47.4% |
| 2,300 miles | 12.6% | 46.5% |
| 2,500 miles | 9.8% | 43.2% |
| 3,000 miles | 2.8% | 31.0% |

The passenger share falls steeply between 2,500 and 3,000 miles. Many Anchorage passenger routes are therefore between those distances, so the result is sensitive to where you set the line. The cargo-included share is dominated by cargo flights, which are 56.6% of departures.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); BTS T-100 Segment, calendar 2025  
> Assumptions: long-haul means 2,300 miles or more (our definition; adjustable)  
> Confidence: Medium - ANC: cargo heavy
> Warnings printed: ANC: cargo_heavy

## A4 - What is the unmet flight demand in SFO airport and why?

*Pass when:* An estimate named as an estimate or proxy, with the why from the delay data.

*Result:* PASS

*Tool calls:* `airport_profile` {"airport_code": "SFO"}

**Estimate: about 108,307 extra takeoffs and landings a year by 2035 at San Francisco International (SFO).** This is an estimate, not a measurement. I'm calling it unmet demand because SFO is strained today.

**How the estimate works:** It is the FAA forecast of commercial operations for fiscal 2035 (514,527) minus fiscal 2025 (406,220). That is 26.7% growth, and cargo is included. The FAA tends to over-forecast. These are takeoffs plus landings, so don't compare them with BTS departure counts.

**Why it counts as unmet (congestion):**
- SFO's three-year system delay rate is 13.4%, the highest among full-data airports (position 100 out of 100). In the latest 12 months it is 17.3%.
- The overall delay rate is 27.4%.
- About 48.9% of delayed flights are coded to the system category. That category is coded by airlines and includes ordinary weather, so it is mostly congestion but not purely.
- Airline-caused delays are 24.7%, late-arriving aircraft are 23.7%, and extreme weather is 2.5%.
- Planes are 82.6% full, which is in the top tier (position 91.2).

**Scores:** SFO's capacity-need score is 86.9, 3rd of 343 airports overall and 2nd of 30 large airports. The flight-side score is 97.1 and the passenger-side score is 76.8.

**Caveats:**
- Capacity was cut. Seats are 5.0% below 2019 and passengers are 4.4% below 2019. The full planes reflect fewer seats, not rising demand. This is why the data confidence is medium.
- The FAA forecasts 32.4% passenger growth, or 8,460,579 extra boardings.
- SFO is under FAA Level 2 schedule facilitation. Schedules are coordinated, but this is not a hard cap.
- The data has no gate, terminal or construction information, so I can't say whether capacity is already being added.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); FAA passenger boarding data CY2025, calendar 2025; BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, Passenger-side score, Flight-side score, How full the planes are, FAA forecast passenger growth, System delay rate; 'unmet flight demand' is an estimate from the FAA forecast, used only when the airport is strained today; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - SFO: capacity cut; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: SFO: capacity_cut

## A5 - How does that compare with Oakland?

*Pass when:* Oakland is not called unmet demand, because it is not strained.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Oakland"}; `compare_airports` {"airport_codes": ["SFO", "OAK"]}

**Oakland (OAK) has no unmet flight demand by our definition, and its forecast gap is much smaller than SFO's.** I assumed you meant Oakland San Francisco Bay (OAK). The same metro area also has San Francisco International (SFO) and San Jose (SJC).

OAK's FAA-forecast growth is 30,637 extra takeoffs and landings a year by 2035, against 108,307 for SFO. That is roughly a third of SFO's figure. The gap is only called unmet demand when an airport is strained today, and OAK is not strained. These are estimates, and the FAA tends to over-forecast.

| Metric | SFO | OAK |
|---|---|---|
| Capacity-need score | 86.9 (3rd of 343) | 46.0 (208th of 343) |
| System delay rate, 3 years | 13.4% | 2.3% |
| System delay rate, latest 12 months | 17.3% | 1.7% |
| Overall delay rate | 27.4% | 18.4% |
| Planes full | 82.6% | 74.2% |
| FAA forecast flight growth | 26.7% | 24.8% |
| FAA forecast passenger growth | 32.4% | 29.9% |
| Passenger growth since 2019 | -4.4% | -35.5% |

**Why they differ:** The FAA forecast growth rates are similar. What separates the two is congestion today. OAK's delays are mostly late-arriving aircraft (54.1% of delayed flights), and only 12.3% are coded to the system category. For SFO that share is 48.9%. The system category is coded by airlines and includes ordinary weather.

**Caveats:**
- Both airports cut capacity. OAK's seats are 31.5% below 2019, and its passengers are 35.5% below 2019. Its fuller planes reflect fewer seats, not rising demand.
- Cargo is 17.9% of OAK's flights, against 1.2% at SFO, and it shares the runways.
- Southwest carries 76.7% of OAK's passengers, so the airport depends heavily on one airline.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, How full the planes are, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - SFO: capacity cut; OAK: capacity cut; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: SFO: capacity_cut, OAK: capacity_cut
