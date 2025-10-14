#!/usr/bin/env python3
import os
import sys
import csv
from glob import glob

# Bibliotheken aus lib/ laden
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))

# --- App-Verzeichnisse ---
APP_DIR = os.path.dirname(os.path.abspath(__file__))
LOOKUP_DIR = os.path.join(APP_DIR, "..", "lookups")
os.makedirs(LOOKUP_DIR, exist_ok=True)

# --- Dynamische Quelldateien ---
SOURCES = sorted(glob(os.path.join(LOOKUP_DIR, "regions_*.csv")))
OUTPUT = os.path.join(LOOKUP_DIR, "cloud_regions_coord.csv")

header = ["provider", "region_id", "city", "country", "lat", "lon"]
merged = []

print(f"[*] Führe {len(SOURCES)} CSV-Dateien zusammen ...")

if not SOURCES:
    print("[!] Keine regions_*.csv-Dateien im lookups-Verzeichnis gefunden.")
    sys.exit(0)

for src in SOURCES:
    try:
        with open(src, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                merged.append(row)
        print(f"[+] {os.path.basename(src)} geladen ({len(merged)} Zeilen kumuliert).")
    except Exception as e:
        print(f"[!] Fehler beim Lesen von {src}: {e}")

# --- Ergebnis schreiben ---
try:
    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(merged)
    print(f"[✓] Zusammengeführt in: {OUTPUT}")
    print(f"→ {len(merged)} Zeilen exportiert.")
except Exception as e:
    print(f"[!] Fehler beim Schreiben nach {OUTPUT}: {e}")