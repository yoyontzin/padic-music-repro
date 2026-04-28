#!/usr/bin/env python3
"""
Patrones continuos BWV 1007: ventanas de longitud p^n, grafo de similitud L2 ≤ δ,
#clusters = componentes conexas. Usa theta (pitch class en S^1) + vel normalizada.
"""
from mido import MidiFile
import numpy as np
import networkx as nx
import itertools
from pathlib import Path

# Ruta al preludio real
MIDI_PATH = Path("bwv1007_prelude.mid")
if not MIDI_PATH.exists():
    MIDI_PATH = Path("cs1-1pre.mid")

mid = MidiFile(str(MIDI_PATH))

events = []
current_time = 0
for msg in mid:
    current_time += msg.time
    if msg.type == "note_on" and msg.velocity > 0:
        pc = msg.note % 12
        theta = 2 * np.pi * pc / 12
        vel_norm = msg.velocity / 127
        events.append({"theta": theta, "vel": vel_norm, "time": current_time})

seq = [(e["theta"], e["vel"]) for e in events]


def build_continuous_patterns(seq, p=2, max_n=6, delta=0.3):
    results = {}
    L = len(seq)
    for n in range(1, max_n + 1):
        length = p**n
        if length > L:
            results[n] = {"length": length, "num_unique": 0, "num_clusters": 0, "top_sizes": []}
            continue
        patterns = []
        step = max(1, length // 4)  # overlap para más datos
        for start in range(0, L - length + 1, step):
            window = seq[start : start + length]
            patterns.append(tuple(window))
        # dedup: usar variable distinta a 'p' (evitar shadowing del parámetro p)
        unique_patterns = list({pat for pat in patterns})

        def l2_dist(pat1, pat2):
            arr1 = np.array(pat1)
            arr2 = np.array(pat2)
            return np.mean(np.sqrt(np.sum((arr1 - arr2) ** 2, axis=1)))

        G = nx.Graph()
        G.add_nodes_from(range(len(unique_patterns)))
        for i, j in itertools.combinations(range(len(unique_patterns)), 2):
            if l2_dist(unique_patterns[i], unique_patterns[j]) <= delta:
                G.add_edge(i, j)

        components = list(nx.connected_components(G))
        results[n] = {
            "length": length,
            "num_unique": len(unique_patterns),
            "num_clusters": len(components),
            "top_sizes": sorted([len(c) for c in components], reverse=True)[:5],
        }
    return results


if __name__ == "__main__":
    print(f"Archivo: {MIDI_PATH.name}, eventos: {len(seq)}\n")
    print("p=2:", build_continuous_patterns(seq, p=2))
    print("\np=3:", build_continuous_patterns(seq, p=3))
