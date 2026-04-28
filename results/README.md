# Summary tables and pipeline reports

This folder contains the **aggregated outputs** of the pipeline, sufficient to verify all numerical claims, tables, and figures in the two companion manuscripts.

The full per-piece, per-level, per-prime, per-config CSVs (≈ 5.3 GB across ~6,400 files) are not redistributed; they can be regenerated from the code in `code/` and the inputs in `data/midi/` using `reproducibility/exact_commands.sh`.

## Files

### Phase I — main suite
- **`SUMMARY_TABLE.csv`** — full benchmark, $p \in \{2,3\}$. Columns: `piece, axis, config, k, n, beta0_p2, beta0_p3, Delta, giant_p2, giant_p3, DeltaG, V_p2, V_p3, avg_degree_p2, avg_degree_p3, k_over_V_p2, k_over_V_p3, flags`.
- **`SUMMARY_TABLE_p2357.csv`** — same suite extended with control primes $p \in \{5,7\}$. Adds `beta0_p5, beta0_p7, giant_p5, giant_p7, Delta23, Delta25, Delta27, DeltaG23, DeltaG25, DeltaG27`.
- **`SUMMARY_REPORT.txt`** — human-readable top-line aggregates: top-5 (piece, axis, config) by stable-level count, seconds-vs-beats per piece, and mean $|\Delta|$ by $k$.
- **`CONTROL_PRIMES_REPORT.txt`** — per-piece control-prime diagnostics with row counts and Delta23 / Delta25 / Delta27 ranges.

### Phase I — sensitivity
- **`SUMMARY_TABLE_p2357_nextplus.csv`** — sensitivity to window length (Phase I "next+").
- **`SUMMARY_TABLE_p2357_nextpp.csv`** — sensitivity to window length (Phase I "next++").
- **`CONTROL_PRIMES_REPORT_nextplus.txt`**, **`CONTROL_PRIMES_REPORT_nextpp.txt`** — companion human-readable reports.

### Null-model controls
- **`SUMMARY_TABLE_nullmodel_p2357.csv`** — random-permutation null model results across all pieces and primes.
- **`NULLMODEL_REPORT.txt`** — null-model diagnostics.

### Profinite-coherence audit (long paper §5.3, supplement §D.3)
- **`audit_table.csv`** — per (piece, axis, $p$, $n$): $\mathrm{Coh}_\pi$, $\mathrm{Coh}_{\mathrm{grid}}$ (recomputed and reported), $n_{\text{SC}}$, $n_{\text{AI}}$, fractions for $\pi$- and truncation-coherence, coverage.
- **`audit_by_piece.csv`** — same but aggregated by piece.
- **`PIPELINE_NOTES.md`** — author notes on the audit pipeline (how `coh_pi_recomputed` is derived from row-level $\pi$/AI counts).
- **`SUMMARY.md`** — high-level human-readable audit summary.

## Provenance

Every file in this folder was produced by the scripts in `code/` from the inputs in `data/midi/`. The exact commit hash, environment, and command sequence are recorded in `../reproducibility/`.
