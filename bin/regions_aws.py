#!/usr/bin/env python3
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
import requests
from bs4 import BeautifulSoup
import csv
import time

PROVIDER = "Amazon"
URL = "https://docs.aws.amazon.com/quicksuite/latest/userguide/regions.html"
OUTPUT = "regions_aws.csv"
API_URL = "https://ipinfo.io/{}/json"

def get_geo(ip):
    try:
        r = requests.get(API_URL.format(ip), timeout=5)
        if r.status_code != 200:
            return None, None, None, None
        data = r.json()
        loc = data.get("loc")
        city = data.get("city")
        country = data.get("country_name") or data.get("country")
        if loc:
            lat, lon = loc.split(",")
            return city, country, lat, lon
        return city, country, None, None
    except Exception as e:
        print(f"[!] {ip}: {e}")
        return None, None, None, None

print("[*] Lade AWS QuickSight Regions-Seite ...")
resp = requests.get(URL)
if resp.status_code != 200:
    print(f"[!] Fehler beim Laden ({resp.status_code})")
    exit(1)

resp.encoding = "utf-8"
soup = BeautifulSoup(resp.text, "html.parser")
table = soup.find("table")

regions = []
for tr in table.find_all("tr")[1:]:
    cols = [td.get_text(strip=True) for td in tr.find_all("td")]
    if len(cols) < 5:
        continue
    region_id = cols[1].strip().lower()
    ip_range = cols[4].split("/")[0].strip()
    if region_id and ip_range:
        regions.append((region_id, ip_range))

print(f"[*] {len(regions)} Regionen gefunden")

with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["provider", "region_id", "city", "country", "lat", "lon"])
    for region, ip in regions:
        city, country, lat, lon = get_geo(ip)
        writer.writerow([PROVIDER, region, city or "", country or "", lat or "", lon or ""])
        time.sleep(1.0)

print(f"[✓] {OUTPUT} erstellt.")