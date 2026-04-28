#!/usr/bin/env bash
# ============================================================================
# exact_commands.sh
#
# End-to-end commands to regenerate every CSV summarised in repro/results/
# from the MIDIs in repro/data/midi/ using the code in repro/code/.
#
# Conservative wall-time on a 2024 MacBook Pro (Apple M3 Pro, 18 GB):
#   - Single piece, 1 prime, 5 levels, 3 k-values, 3 configs: ~5–15 min
#   - Full Phase-I suite (12 pieces × 4 primes × 5 levels × 3 k × 3 configs):
#                                                                ~5–10 hours
#   - Profinite audit + coherence:                              ~30–60 min
# ============================================================================

set -euo pipefail
cd "$(dirname "$0")/.."   # work from repro/

OUT="results_local"
mkdir -p "$OUT"

# ---------------------------------------------------------------------------
# 1. Phase I: per-piece beta_0 across primes p = 2, 3, 5, 7
# ---------------------------------------------------------------------------
PIECES=(
  "bwv1007-1.mid:bwv1007_pre"
  "bwv1007-2.mid:bwv1007_all"
  "bwv1007-3.mid:bwv1007_cou"
  "bwv1007-4.mid:bwv1007_sar"
  "bwv1007-5.mid:bwv1007_men"
  "bwv1007-6.mid:bwv1007_gig"
  "cs1-1pre.mid:cs1_1pre"
  "cs1-3cou.mid:cs1_3cou"
  "cs1-4sar.mid:cs1_4sar"
  "toy_binary.mid:toy_binary"
  "toy_ternary.mid:toy_ternary"
)

for entry in "${PIECES[@]}"; do
  midi="${entry%%:*}"
  name="${entry##*:}"
  python code/profinite_echo_midi.py \
      --midi "data/midi/$midi" \
      --piece "$name" \
      --primes 2 3 5 7 \
      --levels 1 2 3 4 5 \
      --kvalues 8 10 12 \
      --configs A B C \
      --cap 300 \
      --out "$OUT/$name"
done

# ---------------------------------------------------------------------------
# 2. Aggregate Phase I outputs into the SUMMARY_TABLE_p2357.csv shape
# ---------------------------------------------------------------------------
python code/job_list_generator.py --aggregate "$OUT" --out "$OUT/summary"

# ---------------------------------------------------------------------------
# 3. Phase I sensitivity: "next+" and "next++" window-length variants
# ---------------------------------------------------------------------------
for variant in nextplus nextpp; do
  python code/job_list_generator.py \
      --variant "$variant" \
      --base "$OUT" \
      --out "$OUT/${variant}_summary"
done

# ---------------------------------------------------------------------------
# 4. Profinite-map coherence audit (Coh_pi, Coh_grid)
# ---------------------------------------------------------------------------
python code/analyze_bwv1007.py \
    --bundle "$OUT" \
    --audit \
    --out "$OUT/audit_summary"

# ---------------------------------------------------------------------------
# 5. Null-model (random-permutation) controls
# ---------------------------------------------------------------------------
python code/job_list_generator.py \
    --null-model \
    --n-perms 100 \
    --base "$OUT" \
    --out "$OUT/nullmodel_summary"

echo ""
echo "=== Done. Summary tables in: $OUT/{summary,nextplus_summary,nextpp_summary,audit_summary,nullmodel_summary} ==="
echo "Compare against the bundled tables in repro/results/ for verification."
