# Pipeline Notes for SC/AI Audit

The audit distinguishes two diagnostic families:

- `*_pi`: recomputes the actual numerator of `Coh_pi`, using
  `pi(q_{n+1}(W_{p,n+1}(b)))`.
- `*_trunc`: recomputes the numerator of `Coh_grid`, using
  `q_n(trunc(W_{p,n+1}(b)))`.

This distinction is necessary because the current hierarchical pipeline assigns
level-`n+1` residues globally to child prototypes after child dictionaries have
been learned per parent. Consequently, `pi(q_{n+1}(.))` can differ from
`q_n(trunc(.))`.

Sanity checks:

- `coh_pi_recomputed == coh_pi_reported` for all audited rows.
- `coh_grid_recomputed == coh_grid_reported` for all audited rows.

Important interpretation issue:

- For `p=2` with `step=2`, coverage is exactly `valid_b / 2^{n+1} = 0.5`.
  Therefore raw `Coh_pi(2,n)` cannot exceed `0.5`; absence of super-floor
  values in raw `Coh_pi` is not evidence that (SC) is robust.
- The coverage-corrected statistic is
  `Coh_pi_valid = match / valid_b`, reported in `audit_table.csv`,
  `audit_by_piece.csv`, and `directionality_report.txt`.

Empirical outcome of the direct audit:

- In the audited `p=2`, beats-axis corpus, `AI_pi` is high while `SC_pi`
  is low.
- Aggregated over monophonic pieces, mean `frac_SC_pi = 0.0713` and mean
  `frac_AI_pi = 0.9889`.
- Aggregated over polyphonic pieces, mean `frac_SC_pi = 0.2562` and mean
  `frac_AI_pi = 0.9672`.

Thus the direct audit does **not** support the proposed thesis that (SC) is
universally robust while (AI) is the uniquely fragile condition. It supports a
different reading: the current implemented pipeline often collapses sibling
parents under `pi`, while ancestor inclusion remains mostly satisfied.
