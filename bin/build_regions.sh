#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# build_regions.sh
# Lädt Cloud-Region-Daten (AWS, Azure, GCP), führt sie zusammen
# und speichert sie als lookups/cloud_regions.csv
# -----------------------------------------------------------------------------
echo "=== [$(date '+%Y-%m-%d %H:%M:%S')] Cloud Regions Build gestartet ==="
exec 2>&1
set -e  # Script bricht bei Fehler ab
APP_DIR="$(dirname "$0")"
LOOKUP_DIR="${APP_DIR}/../lookups"

echo "[*] Starte Cloud Provider Regionserfassung..."

# 1️⃣ AWS
echo "[*] Lade AWS-Regionen..."
python3 "${APP_DIR}/regions_aws.py"

# 2️⃣ Azure (Microsoft)
echo "[*] Lade Azure-Regionen..."
python3 "${APP_DIR}/regions_azure.py"

# 3️⃣ Google Cloud
echo "[*] Lade GCP-Regionen..."
python3 "${APP_DIR}/regions_gcp.py"

# 4️⃣ Merge alle CSVs in lookups/cloud_regions.csv
echo "[*] Führe CSV-Dateien zusammen..."
python3 "${APP_DIR}/merge_regions.py"

# 5️⃣ Ergebnis prüfen
if [[ -f "${LOOKUP_DIR}/cloud_regions.csv" ]]; then
    echo "[✓] Erfolgreich erstellt: ${LOOKUP_DIR}/cloud_regions.csv"
else
    echo "[!] Fehler: cloud_regions.csv wurde nicht erstellt!"
    exit 1
fi

echo "[✓] Fertig."