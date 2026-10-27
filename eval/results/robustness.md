# Robustness: how much the ranking depends on our choices

Baseline: 343 airports ranked, score version 1.0. Baseline New England top 5: BOS BTV PWM BGR BDL.
Each row re-scores every airport with one choice changed and compares the ranking with the baseline.
Rank correlation is Spearman's (1.0 = identical order).

| Scenario | Airports ranked | Rank correlation with the baseline | Top 10 per size class kept | Size classes with the same #1 | New England top 5 | Median rank move | Largest rank move |
|---|---|---|---|---|---|---|---|
| Load factor at half weight (12.5%; the rest of the passenger side shared by the two growth metrics) | 343 | 0.98 | 31 of 40 | 3 of 4 | BOS BTV PWM BGR MVY (changed) | 11 | 63 |
| Growth window changed: passenger growth since 2022 instead of 2019 | 343 | 0.982 | 33 of 40 | 3 of 4 | BOS BTV PWM BGR BDL (same order) | 9 | 77 |
| Weights shifted to the passenger side (60 / 40) | 343 | 0.992 | 37 of 40 | 4 of 4 | BOS BTV PWM BGR BDL (same order) | 6 | 58 |
| Weights shifted to the flight side (40 / 60) | 343 | 0.992 | 35 of 40 | 4 of 4 | BOS BTV PWM BGR BDL (same order) | 6 | 40 |
| Delay window of 12 months instead of 36 | 258 | 0.985 | 32 of 40 | 4 of 4 | BOS BTV PWM BGR BDL (same order) | 6 | 48 |
| All five metrics weighted equally (20% each) | 343 | 0.982 | 32 of 40 | 3 of 4 | BOS PWM BTV BGR MVY (changed) | 10 | 70 |
| FAA forecasts at half weight (18.75% together, not 37.5%; the freed weight stays on the same side) | 343 | 0.963 | 31 of 40 | 3 of 4 | BOS BTV PWM BGR BDL (same order) | 16 | 94 |
