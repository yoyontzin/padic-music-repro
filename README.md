# Reproducibility bundle — Profinite/$p$-adic multiscale diagnostics on symbolic music

**Companion repository for the manuscripts:**

- *Prime-power indexed multiscale graph diagnostics for symbolic temporal data: methodological exploration and delimitation via BWV 1007.* Submitted to *Journal of Mathematics and Music* (Taylor & Francis).
- *Profinite hierarchical patterns and prime-indexed multiscale invariants in symbolic music.* Submitted to *Computational and Applied Mathematics* (Springer).

**Author:** J. Rogelio Pérez-Buendía · CIMAT–Mérida · ORCID [0000-0002-7739-4779](https://orcid.org/0000-0002-7739-4779).

**Funding:** SECIHTI (Mexico), grant CF~2019/217367.

---

## What is in this bundle

```
repro/
├── README.md                    ← this file
├── LICENSE                      ← MIT for code, CC-BY 4.0 for data/results
├── CITATION.cff                 ← citation metadata (Zenodo-ingested)
├── requirements.txt             ← Python dependencies (pinned)
├── code/                        ← pipeline & analysis scripts
│   ├── profinite_echo_midi.py   ← main pipeline (~65 KB, ~1.7k LOC)
│   ├── analyze_bwv1007.py       ← BWV 1007 specific driver
│   ├── continuous_patterns.py   ← seconds-axis continuous-pattern analysis
│   ├── get_mutopia_midis.py     ← Mutopia downloader (CC-licensed MIDIs)
│   ├── job_list_generator.py    ← batch-job manifest generator
│   └── run_one_piece.py         ← single-piece convenience driver
├── data/
│   └── midi/                    ← 26 MIDI files (CC / public-domain)
├── results/                     ← summary tables and pipeline reports
│   ├── SUMMARY_TABLE.csv                    ← full benchmark suite, p∈{2,3}
│   ├── SUMMARY_TABLE_p2357.csv              ← extended suite with control primes p∈{5,7}
│   ├── SUMMARY_REPORT.txt                   ← top-line aggregates
│   ├── CONTROL_PRIMES_REPORT.txt            ← control-primes diagnostics
│   ├── audit_table.csv, audit_by_piece.csv  ← profinite-coherence audit (Coh_pi, Coh_grid)
│   ├── PIPELINE_NOTES.md, SUMMARY.md        ← human-readable pipeline notes
│   ├── SUMMARY_TABLE_p2357_nextplus.csv     ← Phase I sensitivity (next++ window)
│   ├── SUMMARY_TABLE_p2357_nextpp.csv       ← Phase I sensitivity (next++ pp window)
│   ├── CONTROL_PRIMES_REPORT_nextplus.txt
│   ├── CONTROL_PRIMES_REPORT_nextpp.txt
│   ├── SUMMARY_TABLE_nullmodel_p2357.csv    ← null-model (random permutation) results
│   └── NULLMODEL_REPORT.txt
└── reproducibility/
    ├── git_head.txt             ← exact commit hash of the source repo
    ├── environment.txt          ← Python version + pip freeze
    ├── exact_commands.sh        ← end-to-end commands to regenerate everything
    └── MANIFEST.txt             ← SHA-256 hashes of every bundled file
```

> **Note.** The full pipeline output across all configurations is ~5.3 GB (6,400+ CSVs). This bundle ships **only the aggregated summary tables and audit reports** required to verify all numerical claims in both manuscripts. Anyone wishing to regenerate the full output can do so with the commands in `reproducibility/exact_commands.sh`.

---

## Quick start

```bash
# 1. Set up a fresh environment (Python 3.13.3 used by the author)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Reproduce a single piece (≈ 5–15 min depending on hardware):
python code/profinite_echo_midi.py \
    --midi data/midi/bwv1007-1.mid \
    --piece bwv1007_pre \
    --primes 2 3 \
    --levels 1 2 3 4 5 \
    --kvalues 8 10 12 \
    --configs A B C \
    --cap 300 \
    --out results_local/bwv1007_pre

# 3. Reproduce the full benchmark suite (~5–10 h on a laptop):
bash reproducibility/exact_commands.sh
```

After (2), compare your `results_local/bwv1007_pre/SUMMARY.csv` against the corresponding rows in `results/SUMMARY_TABLE.csv`. Numerical values should match within floating-point tolerance.

---

## How the bundle relates to the papers

| Paper claim / table / figure | Backing artefact in this bundle |
|---|---|
| **Long paper §5.1** Benchmark across full suite | `results/SUMMARY_TABLE.csv` + `results/SUMMARY_REPORT.txt` |
| **Long paper §5.2** Control-prime diagnostics ($p\in\{5,7\}$) | `results/SUMMARY_TABLE_p2357.csv` + `results/CONTROL_PRIMES_REPORT.txt` |
| **Long paper §5.3** Profinite-map coherence ($\mathrm{Coh}_{\pi},\mathrm{Coh}_{\mathrm{grid}}$) | `results/audit_table.csv` + `results/audit_by_piece.csv` |
| **Long paper §5.4** Phase-I sensitivity (window length) | `results/SUMMARY_TABLE_p2357_nextplus.csv`, `results/SUMMARY_TABLE_p2357_nextpp.csv` |
| **Long paper §5.5** Null-model controls (random permutations) | `results/SUMMARY_TABLE_nullmodel_p2357.csv` + `results/NULLMODEL_REPORT.txt` |
| **Long paper supplement §D.1** Full-suite summary | `results/SUMMARY_TABLE.csv` (aggregated by piece × axis × config) |
| **Long paper supplement §D.2** Phase-I control primes | `results/SUMMARY_TABLE_p2357.csv` (filtered to $p\in\{5,7\}$) |
| **Long paper supplement §D.3** Profinite-map coherence | `results/audit_table.csv` (columns `coh_pi_*`, `coh_grid_*`) |
| **Short paper §3** BWV 1007 single-piece diagnostics | `results/audit_by_piece.csv` (rows `bwv1007_*`) |
| **Short paper Appendix A** Reproducibility manifest | `reproducibility/git_head.txt`, `MANIFEST.txt`, `exact_commands.sh` |

---

## MIDI sources and licensing

All MIDI files in `data/midi/` are either in the public domain or distributed under permissive Creative Commons licenses:

| File pattern | Source | License |
|---|---|---|
| `bwv1007-*.mid`, `bwv1008-*.mid`, `cellosuite3-*.mid` | [Mutopia Project](https://www.mutopiaproject.org/) | CC-BY 4.0 / CC-BY-SA 3.0 |
| `cs1-*.mid` | Dave's J.S. Bach MIDI page (1997) | Public domain (US — work from before 1929) |
| `bwv1007_prelude.mid` | Author's own quantization | CC0 |
| `toy_binary.mid`, `toy_ternary.mid` | Author-generated synthetic toys | CC0 |

Per-file attribution is listed in `data/midi/README.md`.

---

## License

- **Code (`code/`)**: MIT License (see `LICENSE`).
- **Data (`data/`)** and **results (`results/`)**: CC-BY 4.0.
- **Per-MIDI provenance and licenses**: see `data/midi/README.md`.

---

## Cite this bundle

If you use this code or data, please cite both the relevant manuscript(s) and this bundle. A `CITATION.cff` is provided so that GitHub and Zenodo render the citation correctly. The Zenodo DOI for this bundle is:

> **DOI:** [10.5281/zenodo.19837174](https://doi.org/10.5281/zenodo.19837174)

---

## Contact

Issues and questions: open a GitHub issue or email `<contact email withheld for double-blind submission; available from the corresponding author upon request>`.
