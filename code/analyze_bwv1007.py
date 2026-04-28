#!/usr/bin/env python3
"""
Análisis ultramétrico del Preludio BWV 1007 (Suite No. 1 en Sol mayor).
- Parsing MIDI monofónico → secuencia de eventos (tiempo, pitch class S^1, tensión tonal).
- Torre de particiones A_n con distancia d_n (p-ádica), clustering por umbral δ.
- Métrica armónica extra: tensión tonal (distancia en circle of fifths al centro Sol mayor).
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path

import numpy as np

try:
    from mido import MidiFile
except ImportError:
    raise SystemExit("Instala mido: pip install mido")

# --- Circle of fifths: orden (C=0, G=1, D=2, A=3, E=4, B=5, F#=6, C#=7, G#=8, D#=9, A#=10, F=11)
# Sol mayor = G major → centro tonal = pitch class 7 (G)
CIRCLE_OF_FIFTHS = [0, 7, 2, 9, 4, 11, 6, 1, 8, 3, 10, 5]  # C, G, D, A, E, B, F#, C#, ...
PC_TO_FIFTH_INDEX = {pc: i for i, pc in enumerate(CIRCLE_OF_FIFTHS)}
TONIC_G = 7  # pitch class G


def pitch_class(note: int) -> int:
    return note % 12


def circle_of_fifths_distance(pc: int, center: int = TONIC_G) -> float:
    """Distancia mínima en el circle of fifths desde pc hasta center (en pasos de quinta)."""
    i = PC_TO_FIFTH_INDEX.get(pc, 0)
    j = PC_TO_FIFTH_INDEX.get(center, 0)
    d = abs(i - j)
    return min(d, 12 - d)


def tonal_tension(pc: int, center: int = TONIC_G, sigma: float = 2.0) -> float:
    """Tensión tonal: peso gaussiano por distancia en circle of fifths (0 = máximo reposo)."""
    d = circle_of_fifths_distance(pc, center)
    return 1.0 - math.exp(-(d ** 2) / (2 * sigma ** 2))


def load_midi_sequence(path: str):
    """Extrae secuencia monofónica: (t_abs, pitch_class, tension)."""
    mid = MidiFile(path)
    ticks_per_beat = mid.ticks_per_beat
    t_ticks = 0
    events = []
    for track in mid.tracks:
        t_ticks = 0
        for msg in track:
            t_ticks += msg.time
            if not getattr(msg, "type", "").startswith("note_"):
                continue
            if msg.type == "note_on" and msg.velocity == 0:
                continue
            if msg.type == "note_off":
                continue
            if msg.type != "note_on":
                continue
            pc = pitch_class(msg.note)
            tension = tonal_tension(pc)
            events.append((t_ticks, pc, tension))
    events.sort(key=lambda x: x[0])
    return events, ticks_per_beat


def to_continuous_time(events, ticks_per_beat: int, tempo: int = 500_000):
    """Convierte ticks a tiempo en segundos (default 120 BPM si no hay meta tempo)."""
    # 500000 µs/beat = 120 BPM
    sec_per_beat = tempo / 1e6
    sec_per_tick = sec_per_beat / ticks_per_beat
    return [(t_ticks * sec_per_tick, pc, tension) for t_ticks, pc, tension in events]


def embed_s1(pc: int) -> tuple[float, float]:
    """Pitch class a S^1: (cos(2π pc/12), sin(2π pc/12))."""
    x = 2 * math.pi * pc / 12
    return (math.cos(x), math.sin(x))


def build_X(events_sec):
    """Matriz X: cada fila = (cos, sin, tension) para cada evento."""
    rows = []
    for _, pc, tension in events_sec:
        c, s = embed_s1(pc)
        rows.append([c, s, tension])
    return np.array(rows, dtype=float)


def cluster_count_at_n(X: np.ndarray, n: int, p: int, delta: float) -> int:
    """
    Torre ultramétrica: a nivel n, el espacio de índices se particiona en bloques
    de tamaño p^n (índices i con mismo i // p^n). Dentro de cada bloque A_n,
    dos puntos están en el mismo cluster si d(i,j) <= delta (distancia euclídea en X).
    #clusters = suma sobre bloques de (componentes conexas por delta dentro del bloque).
    """
    N = len(X)
    if n <= 0:
        return 1
    pn = p ** n
    if pn > N:
        return N
    num_blocks = (N + pn - 1) // pn
    total_clusters = 0
    for b in range(num_blocks):
        start, end = b * pn, min((b + 1) * pn, N)
        indices = list(range(start, end))
        if not indices:
            continue
        sub = X[indices]
        n_sub = len(indices)
        parent = list(range(n_sub))

        def find(u):
            if parent[u] != u:
                parent[u] = find(parent[u])
            return parent[u]

        def union(u, v):
            pu, pv = find(u), find(v)
            if pu != pv and np.linalg.norm(sub[u] - sub[v]) <= delta:
                parent[pu] = pv

        for i in range(n_sub):
            for j in range(i + 1, n_sub):
                if np.linalg.norm(sub[i] - sub[j]) <= delta:
                    union(i, j)
        total_clusters += sum(1 for i in range(n_sub) if find(i) == i)
    return total_clusters


def main():
    parser = argparse.ArgumentParser(description="Torre ultramétrica BWV 1007 Prelude")
    parser.add_argument("midi", nargs="?", default="bwv1007_prelude.mid", help="Archivo MIDI")
    parser.add_argument("--delta", type=float, default=0.3, help="Umbral de distancia (0.2–0.4)")
    parser.add_argument("--deltas", type=str, default="", help="Varios deltas separados por coma (ej: 0.2,0.3,0.4)")
    parser.add_argument("--p", type=int, default=2, help="Base p-ádica (2 o 3)")
    parser.add_argument("--n-max", type=int, default=7, help="Máximo nivel n")
    parser.add_argument("--list-n", type=str, default="2,3,4,5,6,7", help="Niveles n a reportar (ej: 2,3,4,5,6,7)")
    args = parser.parse_args()

    path = Path(args.midi)
    if not path.exists():
        path = Path("cs1-1pre.mid")
    if not path.exists():
        raise SystemExit(f"No se encontró archivo MIDI: {args.midi} ni cs1-1pre.mid")

    events, tpb = load_midi_sequence(str(path))
    events_sec = to_continuous_time(events, tpb)
    X = build_X(events_sec)
    N = len(X)
    n_levels = [int(x) for x in args.list_n.replace(",", " ").split()]

    deltas = [args.delta]
    if args.deltas:
        deltas = [float(x.strip()) for x in args.deltas.split(",")]

    print(f"Archivo: {path.name}")
    print(f"Eventos (notas): {N}")
    for delta in deltas:
        print(f"\n--- Delta = {delta}, p = {args.p} ---")
        print(f"{'n':>4}  {'#clusters':>10}")
        print("-" * 16)
        for n in n_levels:
            if n < 1:
                continue
            k = cluster_count_at_n(X, n, args.p, delta)
            print(f"{n:>4}  {k:>10}")
    print("\n--- fin ---")


if __name__ == "__main__":
    main()
