#!/usr/bin/env python3
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
import requests
from bs4 import BeautifulSoup
import csv
import time
import unicodedata

# --- App Paths ---
APP_DIR = os.path.dirname(os.path.abspath(__file__))
LOOKUP_DIR = os.path.join(APP_DIR, "..", "lookups")
os.makedirs(LOOKUP_DIR, exist_ok=True)

# --- Provider spezifisch ---
PROVIDER = "Google"
OUTPUT = os.path.join(LOOKUP_DIR, f"regions_{PROVIDER.lower()}.csv")
URL = "https://cloud.google.com/compute/docs/gpus/gpu-regions-zones"
GEOCODE_API = "https://nominatim.openstreetmap.org/search"

def normalize_text(text):
    if not text:
        return ""
    return unicodedata.normalize("NFKC", text).encode("utf-8", "ignore").decode("utf-8")

def geocode(city, country):
    query = f"{city}, {country}"
    try:
        params = {"q": query, "format": "json", "limit": 1}
        headers = {"User-Agent": "vhc-cloudmapper"}
        r = requests.get(GEOCODE_API, params=params, headers=headers, timeout=10)
        if r.status_code == 200 and r.json():
            data = r.json()[0]
            return data["lat"], data["lon"]
    except:
        pass
    return None, None

print("[*] Lade GCP GPU Regions & Zones Seite ...")
resp = requests.get(URL)
resp.encoding = "utf-8"
soup = BeautifulSoup(resp.text, "html.parser")

table = soup.find("table")
regions = []

for tr in table.find_all("tr")[1:]:
    cols = [td.get_text(strip=True) for td in tr.find_all("td")]
    if len(cols) < 2:
        continue
    region_id = normalize_text(cols[0].split()[0].strip())
    parts = [p.strip() for p in cols[1].split(",")]
    city = parts[0] if parts else ""
    country = parts[1] if len(parts) > 1 else ""
    if region_id and city and country:
        regions.append((region_id, city, country))

print(f"[*] {len(regions)} Regionen gefunden")

with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["provider", "region_id", "city", "country", "lat", "lon"])
    for region_id, city, country in regions:
        lat, lon = geocode(city, country)
        writer.writerow([PROVIDER, region_id, city, country, lat or "", lon or ""])
        time.sleep(1.0)

print(f"[✓] {OUTPUT} erstellt.")