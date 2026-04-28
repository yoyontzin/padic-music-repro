#!/usr/bin/env python3
"""
Descarga MIDIs de Mutopia vía ZIP y los extrae al repo.
Uso: python3 get_mutopia_midis.py
"""
import urllib.request, zipfile, io, os

REPO = os.path.dirname(os.path.abspath(__file__))

# Mutopia distribuye ZIPs, no archivos individuales
ZIPS = [
    ("BWV1007", "https://www.mutopiaproject.org/ftp/BachJS/BWV1007/bwv1007/bwv1007-mids.zip"),
    ("BWV1008", "https://www.mutopiaproject.org/ftp/BachJS/BWV1008/bwv1008/bwv1008-mids.zip"),
    ("BWV1009", "https://www.mutopiaproject.org/ftp/BachJS/BWV1009/cellosuite3/cellosuite3-mids.zip"),
]

# Excluir: versiones viola y archivo concatenado completo
SKIP = ["viola", "bwv1007.mid", "cellosuite3.mid", "bwv1008.mid"]

headers = {"User-Agent": "Mozilla/5.0 (academic research; bundle: padic-music-repro)"}

print(f"Destino: {REPO}\n")
total = 0

for label, url in ZIPS:
    print(f"→ {label}: {url.split('/')[-1]}", flush=True)
    try:
        req = urllib.request.Request(url, headers=headers)
        data = urllib.request.urlopen(req, timeout=20).read()
        print(f"  ZIP descargado: {len(data)//1024} KB")
        with zipfile.ZipFile(io.BytesIO(data)) as zf:
            for name in sorted(zf.namelist()):
                if not name.lower().endswith(".mid"):
                    continue
                base = os.path.basename(name)
                if any(s in base for s in SKIP):
                    print(f"  skip: {base}")
                    continue
                dest = os.path.join(REPO, base)
                with zf.open(name) as src, open(dest, "wb") as dst:
                    dst.write(src.read())
                print(f"  OK: {base}  ({os.path.getsize(dest)} bytes)")
                total += 1
    except Exception as e:
        print(f"  FALLO: {e}")

print(f"\nTotal nuevos MIDIs: {total}")
print("\nTodos los MIDIs en repo:")
for f in sorted(f for f in os.listdir(REPO) if f.endswith(".mid")):
    print(f"  {f}")
