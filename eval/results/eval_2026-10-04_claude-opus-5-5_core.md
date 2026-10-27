# Evaluation run - 2026-10-04 15:54 - claude-opus-5-5

**7 of 7 questions passed.** 241 numbers appeared in the answers; 0 answers ended with a number that could not be traced to a tool result; 0 answers passed only after one automatic rewrite. Average 10.9s per question; 207,784 input and 6,097 output tokens in total.

| Id | Group | Result | Tools | Number check | Seconds |
|---|---|---|---|---|---|
| A1 | core | PASS | rank_airports | passed | 11.8 |
| A2 | core | PASS | find_airport, find_airport, compare_airports | passed | 12.8 |
| A6 | follow-up | PASS | compare_airports | passed | 10.0 |
| A3 | core | PASS | find_airport, airport_profile | passed | 10.1 |
| A7 | follow-up | PASS | airport_profile | passed | 8.8 |
| A4 | core | PASS | airport_profile | passed | 10.1 |
| A5 | follow-up | PASS | find_airport, compare_airports, airport_profile | passed | 12.7 |

## A1 - Which airports in New England are strong candidates for terminal expansion?

*Pass when:* A ranked list from the six states, scores shown, reasons given.

*Result:* PASS

*Tool calls:* `rank_airports` {"region": "new england"}

On our capacity-need score, the strongest New England candidates are Boston Logan (BOS), Burlington (BTV) and Portland, Maine (PWM). Bangor (BGR) is a close fourth. Boston and Burlington are the only two flagged as strained today. Our data can't measure terminal or gate use directly, so I've judged "terminal expansion" from the passenger side of the score: how full the planes are, passenger growth since 2019 and the FAA forecast.

| Airport | Size class | Total score | Passenger side | Planes full | Passengers vs 2019 | FAA passenger forecast to 2035 | System delay rate (3 yr) |
|---|---|---|---|---|---|---|---|
| Boston (BOS) | large | 82.9 | 72.2 | 81.7% | +1.2% | +26.5% | 9.1% |
| Burlington (BTV) | small hub | 79.2 | 73.7 | 83.0% | +2.3% | +22.9% | 5.5% |
| Portland (PWM) | small hub | 77.4 | 79.2 | 82.8% | +17.2% | +21.6% | 4.6% |
| Bangor (BGR) | nonhub | 71.8 | 78.0 | 80.4% | +40.8% | +24.1% | 4.7% |
| Bradley, Hartford (BDL) | medium | 65.9 | 60.8 | 81.3% | -2.7% | +15.7% | 4.9% |

**What stands out:**
- **Boston** scores high mainly on congestion (flight side 93.6). The 9.1% is the system delay rate, which is coded by airlines and includes ordinary weather. Passengers are only just above 2019 levels. The FAA forecasts the biggest absolute gain: 5,612,088 extra boardings a year by 2035.
- **Portland** has the strongest passenger signal among the three leaders (passenger side 79.2). The data flags flights holding flat while passengers rise, which fits pressure on the terminal more than on the airfield. Seats are up 21.6% since 2019.
- **Bangor** has the fastest passenger growth since 2019, but seats grew even faster (+48.8%), so airlines have already added a lot of capacity.
- **Burlington** combines the fullest planes with strain, but the absolute upside is small: 163,754 extra boardings forecast.

Four airports have partial data and no total score, so they aren't ranked: Tweed/New Haven (HVN), Cape Cod Gateway (HYA), Block Island (BID) and Westerly (WST).

The score shows upside only. There's no cost, return or gate data behind it. Useful next steps are a full profile of BOS, PWM or BGR, or adding HVN's passenger-side data.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years); FAA passenger boarding data CY2025, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, Passenger-side score, Flight-side score, How full the planes are, FAA forecast passenger growth, System delay rate; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - the answer uses proxy measures (scores, system delay rate, load factor or forecasts)

## A2 - Compare LA and Santa Ana airport congestion levels.

*Pass when:* LAX vs SNA side by side, a clear verdict, Santa Ana's legal cap flagged.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "LA"}; `find_airport` {"query": "Santa Ana"}; `compare_airports` {"airport_codes": ["LAX", "SNA"]}

Los Angeles International (LAX) is somewhat more congested than John Wayne/Orange County in Santa Ana (SNA) on every delay measure, but the gap is modest. Neither airport is flagged as strained. I took "LA" to mean LAX. The metro area also has Ontario (ONT), Hollywood Burbank (BUR) and Long Beach (LGB).

| Measure | LAX | SNA | Difference |
|---|---|---|---|
| System delay rate, 3 years | 4.8% | 3.9% | +0.9 pts (1.23x) |
| System delay rate, latest 12 months | 5.0% | 4.3% | +0.7 pts (1.16x) |
| Overall delay rate (15+ min late, any cause) | 18.9% | 17.5% | +1.4 pts |
| System share of all delays | 25.7% | 22.4% | |
| Flight-side score (0-100) | 80.5 | 58.7 | +21.8 |

**What the measures mean:** The system delay rate is the closest stand-in we have for congestion. It counts delays that airlines blame on the airport and air-traffic system. Airlines code this category themselves, and it includes ordinary weather, so it is mostly congestion but not purely. At both airports most delays come from the airlines themselves and from late-arriving aircraft rather than the system. The system delay rate rose at both airports in the latest 12 months.

**What changes the picture:**
- **LAX:** Seats are down 12.8% since 2019 and passengers are down 15.7%. Its delays are happening with less traffic than before 2019, not because traffic is growing.
- **SNA:** A legal settlement caps passengers, limits regulated daily departures to an average of 95, and imposes a night curfew. In our units (departing passengers only), the cap is about 6.1-6.25 million a year. SNA carried 5,590,354 departing passengers in the latest 12 months, so it is already close to the cap. Its low congestion may mean it isn't straining the airfield, but the cap limits how much any added capacity could be used.

Next step to consider: I can pull month-by-month system delay trends for either airport, or add ONT, BUR and LGB to the comparison.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, Flight-side score, System delay rate; 'LA' was taken to mean LAX; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - LAX: capacity cut; SNA: legal limit; the answer uses proxy measures (scores, system delay rate, load factor or forecasts); an airport name was resolved by default
> Warnings printed: SNA: legal_limit, LAX: capacity_cut

## A6 - And how did congestion at those two look in 2023?

*Pass when:* Uses the same two airports without being told again, and 2023 values.

*Result:* PASS

*Tool calls:* `compare_airports` {"airport_codes": ["LAX", "SNA"], "year": 2023}

In calendar 2023, LAX was more congested than SNA, and the gap was wider than it is now. LAX had a higher system delay rate (5.6% vs 4.2%) and a higher overall delay rate (20.5% vs 18.5%).

| Measure, calendar 2023 | LAX | SNA | Difference |
|---|---|---|---|
| System delay rate | 5.6% | 4.2% | +1.4 pts (1.33x) |
| Overall delay rate (15+ min late, any cause) | 20.5% | 18.5% | +2.0 pts (1.11x) |
| Arriving flights in the delay data | 195,617 | 45,732 | |

**Compared with the latest 12 months (Aug 2025-Jul 2026):**
- **LAX** has eased: its system delay rate fell from 5.6% to 5.0%. That fits the capacity cut, since seats are still 12.8% below 2019.
- **SNA** is about where it was: 4.2% in 2023 and 4.3% now.
- **The gap** between the two has narrowed from 1.4 points in 2023 to 0.7 points now.
- **Overall delay rates:** both 2023 figures are higher than the three-year averages (18.9% at LAX, 17.5% at SNA), so 2023 was a worse delay year at both airports.

**Caveats:**
- These are raw metrics only. The capacity-need score exists only for the latest period, so I can't give 2023 scores or rankings.
- The system delay category is coded by airlines and includes ordinary weather. It also covers only domestic flights by the larger reporting airlines, which matters more at LAX because of its international traffic.
- A single year swings a lot, so I'd read the change at SNA as no real change.

I can pull the month-by-month system delay series from 2023 onward for either airport if you want to see when LAX's improvement happened.

> Data period: BTS T-100 airport-month summary, calendar 2023; BTS Airline Delay Causes, calendar 2023; BTS T-100 Segment, calendar 2023  
> Assumptions: proxies, not direct measurements: System delay rate  
> Confidence: Medium - LAX: capacity cut; SNA: legal limit; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: SNA: legal_limit, LAX: capacity_cut

## A3 - What is the percentage of long haul flights out of Anchorage airport?

*Pass when:* One number, the 3,000-mile definition stated, the cargo-included number next to it.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Anchorage airport"}; `airport_profile` {"airport_code": "ANC"}

At Ted Stevens Anchorage International (ANC), **2.8% of departing passenger flights** were long-haul in 2025, using our default cutoff of 3,000 miles or more. **If you count cargo flights too, the share is 31.0%.**

I took "Anchorage airport" to mean ANC. The only other covered airport in Anchorage is Merrill Field (MRI), a much smaller airport with partial data.

**Long-haul share at different cutoffs** (departing flights, domestic plus international, calendar 2025):

| Cutoff | Passenger flights only | All flights including cargo |
|---|---|---|
| 2,000+ miles | 13.7% (5,239 flights) | 47.4% (41,732 flights) |
| 2,500+ miles | 9.8% (3,723 flights) | 43.2% (37,969 flights) |
| 3,000+ miles | 2.8% (1,061 flights) | 31.0% (27,305 flights) |

Out of 87,988 departures in total, 38,150 were passenger flights and 49,838 were cargo or other non-passenger flights.

**Why the two shares are so different:** cargo makes up 56.6% of ANC's flights, and many cargo flights are long-haul. Passenger service is mostly shorter flights: 98.6% of passengers fly to US destinations, and Alaska Airlines carries 61.4% of them. So for passenger-terminal questions, the passenger-only share is the one to use. The cargo share matters for runway capacity, because cargo flights use the same runways.

Background (not from our data): Anchorage is a major refueling stop for cargo flights between Asia and North America, which is why it has so many long cargo flights.

There's no official definition of long-haul. 3,000 miles is our default, and I can rerun this with any cutoff you prefer.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); BTS T-100 Segment, calendar 2025  
> Assumptions: long-haul means 3,000 miles or more (our definition; adjustable); 'Anchorage airport' was taken to mean ANC  
> Confidence: Medium - ANC: cargo heavy; an airport name was resolved by default
> Warnings printed: ANC: cargo_heavy

## A7 - What if long-haul means over 2,300 miles?

*Pass when:* Recomputed at 2,300 miles for Anchorage.

*Result:* PASS

*Tool calls:* `airport_profile` {"airport_code": "ANC", "long_haul_miles": 2300}

If long-haul starts at 2,300 miles, **12.6% of Anchorage (ANC)'s departing passenger flights** count as long-haul in 2025. **Counting cargo flights too, the share is 46.5%.** The tool counts flights of 2,300 miles or more, so a flight of exactly 2,300 miles is included. That should make little difference.

| Cutoff | Passenger flights only | All flights including cargo |
|---|---|---|
| 2,000+ miles | 13.7% (5,239) | 47.4% (41,732) |
| **2,300+ miles** | **12.6% (4,820)** | **46.5% (40,947)** |
| 2,500+ miles | 9.8% (3,723) | 43.2% (37,969) |
| 3,000+ miles | 2.8% (1,061) | 31.0% (27,305) |

These shares are out of 38,150 passenger departures and 87,988 departures in total.

**What this shows:** for passenger flights, the result depends heavily on where you put the cutoff. The share drops sharply above 2,500 miles, so ANC's passenger flights cluster in the 2,000-3,000 mile range. The share including cargo stays high at every cutoff because cargo makes up 56.6% of ANC's flights, and many of them are long.

**For a passenger-capacity question,** the passenger-only share is the one to use. Cargo doesn't use the passenger terminal, but it does use the same runways. Cargo is also in the FAA flight forecast but not in our score.

The data doesn't include routes or destinations, so I can't show which routes make up the passenger long-haul flights.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, FAA forecast passenger growth, FAA forecast flight growth; long-haul means 2,300 miles or more (our definition; adjustable); scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - ANC: cargo heavy; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: ANC: cargo_heavy

## A4 - What is the unmet flight demand in SFO airport and why?

*Pass when:* An estimate named as an estimate or proxy, with the why from the delay data.

*Result:* PASS

*Tool calls:* `airport_profile` {"airport_code": "SFO"}

San Francisco International (SFO) is strained today, so its flight-demand estimate counts as **unmet flight demand: about 108,307 extra takeoffs and landings a year by fiscal 2035**. This is an estimate, not a measurement. It is the FAA forecast rising from 406,220 to 514,527 commercial operations (+26.7%, cargo included). The FAA tends to over-forecast.

**Why we call it unmet: the airfield is already congested**
- **System delay rate (three years): 13.4%** of arriving flights. That is the highest among all 343 full-data airports (position 100 of 100). Over the latest 12 months it rose to 17.3%.
- **Overall delay rate: 27.4%** of arrivals were 15 or more minutes late.
- **Delay causes:** 48.9% of delayed flights were put down to the airport and air-traffic system. Airlines caused 24.7%, late-arriving aircraft 23.7%, and extreme weather only 2.5%.
- Airlines code the "system" category themselves, and it includes ordinary weather, so it is mostly but not purely congestion.
- Background (not from our data): SFO's closely spaced parallel runways often can't be used side by side in low cloud and fog, which cuts how many planes can land. That fits a high system-delay share.

**Caveats that matter**
- **Capacity was cut.** Seats are down 5.0% and passenger flights down 11.0% since 2019, while passengers are down 4.4%. Planes are 82.6% full, but partly because there are fewer seats, not because demand is rising.
- **Schedules are coordinated.** SFO is an FAA Level 2 airport, where airline schedules are coordinated but not legally capped.
- **One airline dominates.** United carries 44.8% of passengers.

**Overall**, SFO's capacity-need score is 86.9: 3rd of 343 airports and 2nd of 30 large hubs. The flight side scores 97.1.

**To check next:** whether runway or air-traffic work is already planned or underway, and whether the 2026 delay spike continues. I can show the monthly delay trend if useful.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); FAA passenger boarding data CY2025, calendar 2025; BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, Flight-side score, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; 'unmet flight demand' is an estimate from the FAA forecast, used only when the airport is strained today; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - SFO: capacity cut; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: SFO: capacity_cut

## A5 - How does that compare with Oakland?

*Pass when:* Oakland is not called unmet demand, because it is not strained.

*Result:* PASS

*Tool calls:* `find_airport` {"query": "Oakland"}; `compare_airports` {"airport_codes": ["SFO", "OAK"]}; `airport_profile` {"airport_code": "OAK"}

I took "Oakland" to mean Oakland San Francisco Bay (OAK). The metro area also has San Jose (SJC).

Oakland has **no unmet flight demand by our definition** because it isn't strained today. The FAA forecasts about 30,637 extra takeoffs and landings a year by fiscal 2035 (+24.8%), compared with 108,307 at SFO. We label Oakland's figure "forecast flight growth," not unmet demand, because its runways appear to have spare room.

| | SFO | OAK |
|---|---|---|
| Capacity-need score | 86.9 (3rd of 343) | 46.0 (208th of 343) |
| Flight-side score | 97.1 | 49.7 |
| System delay rate, 3 yrs | 13.4% | 2.3% |
| System delay rate, latest 12 mo | 17.3% | 1.7% |
| Overall delay rate | 27.4% | 18.4% |
| System share of delayed flights | 48.9% | 12.3% |
| Planes full (load factor) | 82.6% | 74.2% |
| Passengers vs 2019 | -4.4% | -35.5% |
| Seats vs 2019 | -5.0% | -31.5% |
| Cargo share of flights | 1.2% | 17.9% |
| Biggest airline | United, 44.8% | Southwest, 76.7% |

**Why the two differ**
- **Delays come from different places.** At SFO the system delay rate is about 5.8 times Oakland's. At Oakland most delays come from late-arriving aircraft (54.1%) and the airlines themselves (32.5%), not from the airfield. That points to network knock-on effects rather than congestion. The system category is coded by airlines and includes ordinary weather.
- **Oakland lost traffic.** It is down about a third since 2019 and still falling, so planes being 74.2% full reflects seats that were cut, not demand pushing against capacity.
- **Oakland has more cargo and one dominant airline.** Cargo takes nearly a fifth of its flights and shares the runways, and Southwest carries about three-quarters of its passengers. Both add risk.

The FAA forecasts similar percentage growth at both airports. The difference is that only SFO looks unable to absorb it today.

> Data period: BTS T-100 airport-month summary, 2025-05 to 2026-04 (latest 12 complete months); FAA Terminal Area Forecast, 2025 edition (published March 2026), fiscal 2035 vs 2025; BTS Airline Delay Causes, 2023-08 to 2026-07 (three years) / 2025-08 to 2026-07 (latest 12 months); BTS T-100 Segment, calendar 2025  
> Assumptions: proxies, not direct measurements: Capacity-need score, Flight-side score, How full the planes are, FAA forecast passenger growth, System delay rate, FAA forecast flight growth; 'unmet flight demand' is an estimate from the FAA forecast, used only when the airport is strained today; scores are relative (position among full-data airports) and rank upside, not return - no cost data exists  
> Confidence: Medium - SFO: capacity cut; OAK: capacity cut; the answer uses proxy measures (scores, system delay rate, load factor or forecasts)
> Warnings printed: SFO: capacity_cut, OAK: capacity_cut
