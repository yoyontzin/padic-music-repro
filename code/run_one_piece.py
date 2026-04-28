#!/usr/bin/env python3
"""
run_one_piece.py — Wrapper CLI para un job del pipeline p-ádico.
Uso: python3 run_one_piece.py <midi> <piece_name> <axis> <p> <Nmax> [--root DIR]
Diseñado para ser llamado por SLURM array o GNU parallel.
"""
import argparse
import subprocess
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("midi",        help="Ruta al archivo MIDI (relativa a root)")
    parser.add_argument("piece",       help="Nombre de la pieza (para outputs)")
    parser.add_argument("axis",        choices=["beats", "seconds"])
    parser.add_argument("p",           type=int)
    parser.add_argument("Nmax",        type=int)
    parser.add_argument("--root",      default=".", help="Raíz del repo")
    parser.add_argument("--K",         type=int, default=16)
    parser.add_argument("--Kchild",    type=int, default=2)
    parser.add_argument("--M",         type=int, default=800)
    parser.add_argument("--step",      type=int, default=2)
    parser.add_argument("--seed",      type=int, default=42)
    parser.add_argument("--bin-beats", type=float, default=0.083333)
    parser.add_argument("--bin",       type=float, default=0.05)
    args = parser.parse_args()

    root    = Path(args.root).resolve()
    out_dir = root / "outputs" / "paper_profinite_hier" / args.piece / args.axis
    out_dir.mkdir(parents=True, exist_ok=True)

    bin_arg = ["--bin-beats", str(args.bin_beats)] if args.axis == "beats" else ["--bin", str(args.bin)]

    midi_path = Path(args.midi)
    if not midi_path.is_absolute():
        midi_path = root / midi_path

    cmd = [
        sys.executable,
        str(root / "scripts" / "build_hierarchical_maps.py"),
        str(midi_path),
        "--axis", args.axis,
        *bin_arg,
        "--p", str(args.p),
        "--Nmax", str(args.Nmax),
        "--K", str(args.K),
        "--Kchild", str(args.Kchild),
        "--M", str(args.M),
        "--step", str(args.step),
        "--seed", str(args.seed),
        "--out", str(out_dir),
    ]
    print(f"[run_one_piece] {args.piece}/{args.axis}/p{args.p} Nmax={args.Nmax}", flush=True)
    result = subprocess.run(cmd, cwd=str(root))
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
