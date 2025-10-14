#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# build_regions.sh
# Lädt Cloud-Region-Daten (AWS, Azure, GCP), führt sie zusammen
# und speichert sie als lookups/cloudregions.csv
# -----------------------------------------------------------------------------

set -e  # Script bricht bei Fehler ab

# -----------------------------------------------------------------------------
# App- und Verzeichnisvariablen
# -----------------------------------------------------------------------------
APP_DIR="$(dirname "$0")"
APP_NAME="vhc_SA_cloudregions"
APP_BASE="$SPLUNK_HOME/etc/apps/${APP_NAME}"
APP_VAR_DIR="${APP_BASE}/var"
LOOKUP_DIR="${APP_BASE}/lookups"

# -----------------------------------------------------------------------------
# Pfade und Dateinamen
# -----------------------------------------------------------------------------
LOCKFILE="${APP_VAR_DIR}/vhc_SA_cloudregions.lock"
LOGFILE="$SPLUNK_HOME/var/log/splunk/vhc_SA_cloudregions.log"
OUTPUT_FILE="${LOOKUP_DIR}/cloudregions.csv"

# -----------------------------------------------------------------------------
# Lockfile: verhindert parallele Ausführungen
# -----------------------------------------------------------------------------
if [ -f "$LOCKFILE" ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Script already running, exiting." >> "$LOGFILE"
    exit 0
fi
trap "rm -f \"$LOCKFILE\"" EXIT
touch "$LOCKFILE"

# -----------------------------------------------------------------------------
# Startmeldung
# -----------------------------------------------------------------------------
echo "=== [$(date '+%Y-%m-%d %H:%M:%S')] Cloud Regions Build gestartet ===" >> "$LOGFILE"

# -----------------------------------------------------------------------------
# 1️⃣ AWS
# -----------------------------------------------------------------------------
echo "[*] Lade AWS-Regionen..." >> "$LOGFILE"
"$SPLUNK_HOME/bin/splunk" cmd python3 "${APP_DIR}/regions_aws.py" >> "$LOGFILE" 2>&1

# -----------------------------------------------------------------------------
# 2️⃣ Azure
# -----------------------------------------------------------------------------
echo "[*] Lade Azure-Regionen..." >> "$LOGFILE"
"$SPLUNK_HOME/bin/splunk" cmd python3 "${APP_DIR}/regions_azure.py" >> "$LOGFILE" 2>&1

# -----------------------------------------------------------------------------
# 3️⃣ GCP
# -----------------------------------------------------------------------------
echo "[*] Lade GCP-Regionen..." >> "$LOGFILE"
"$SPLUNK_HOME/bin/splunk" cmd python3 "${APP_DIR}/regions_gcp.py" >> "$LOGFILE" 2>&1

# -----------------------------------------------------------------------------
# 4️⃣ Merge
# -----------------------------------------------------------------------------
echo "[*] Führe CSV-Dateien zusammen..." >> "$LOGFILE"
"$SPLUNK_HOME/bin/splunk" cmd python3 "${APP_DIR}/merge_regions.py" >> "$LOGFILE" 2>&1

# -----------------------------------------------------------------------------
# 5️⃣ Ergebnis prüfen
# -----------------------------------------------------------------------------
if [[ -f "$OUTPUT_FILE" ]]; then
    echo "[✓] Erfolgreich erstellt: $OUTPUT_FILE" >> "$LOGFILE"
else
    echo "[!] Fehler: $OUTPUT_FILE wurde nicht erstellt!" >> "$LOGFILE"
    exit 1
fi

# -----------------------------------------------------------------------------
# 6️⃣ Logfile ins _internal indexieren (Splunk Cloud-kompatibel)
# -----------------------------------------------------------------------------
"$SPLUNK_HOME/bin/splunk" add oneshot "$LOGFILE" \
    -index _internal \
    -sourcetype vhc:cloudregions \
    > /dev/null 2>&1 || true

# -----------------------------------------------------------------------------
# Abschlussmeldung
# -----------------------------------------------------------------------------
echo "[✓] Fertig. ($(date '+%Y-%m-%d %H:%M:%S'))" >> "$LOGFILE"
exit 0