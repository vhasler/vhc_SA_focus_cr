#!/usr/bin/env python3
import csv
import os

OUTPUT = os.path.join("..", "lookups", "cloud_regions.csv")
SOURCES = ["regions_aws.csv", "regions_azure.csv", "regions_gcp.csv"]

merged = []
header = ["provider", "region_id", "city", "country", "lat", "lon"]

print("[*] Führe CSV-Dateien zusammen ...")
for src in SOURCES:
    if not os.path.exists(src):
        print(f"[!] Datei fehlt: {src}")
        continue
    with open(src, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            merged.append(row)

with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=header)
    writer.writeheader()
    writer.writerows(merged)

print(f"[✓] Zusammengeführt in: {OUTPUT}")
print(f"→ {len(merged)} Zeilen exportiert")