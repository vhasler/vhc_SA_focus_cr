#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# build_regions.sh
# Lädt Cloud-Region-Daten (AWS, Azure, GCP), führt sie zusammen
# und speichert sie als lookups/cloudregions.csv
# -----------------------------------------------------------------------------

# Nicht bei erstem Fehler abbrechen – wir loggen und laufen weiter
set -u  # (kein -e)

APP_DIR="$(dirname "$0")"
APP_NAME="vhc_SA_cloudregions"
APP_BASE="$SPLUNK_HOME/etc/apps/${APP_NAME}"
LOOKUP_DIR="${APP_BASE}/lookups"

LOGFILE="$SPLUNK_HOME/var/log/splunk/${APP_NAME}.log"
TARGET_LOOKUP="${LOOKUP_DIR}/cloudregions.csv"

# Hilfsfunktion zum Ausführen + Loggen ohne Abbruch
run_step() {
  local msg="$1"; shift
  echo "[*] ${msg} ..." >> "$LOGFILE"
  if "$@"; then
    echo "[✓] ${msg} OK" >> "$LOGFILE"
  else
    local rc=$?
    echo "[!] ${msg} FAILED (rc=${rc})" >> "$LOGFILE"
  fi
}

echo "=== [$(date '+%Y-%m-%d %H:%M:%S')] Cloud Regions Build gestartet ===" >> "$LOGFILE"

# 1) AWS
run_step "Lade AWS-Regionen" \
  "$SPLUNK_HOME/bin/splunk" cmd python3 "${APP_DIR}/regions_aws.py" >> "$LOGFILE" 2>&1

# 2) Azure
run_step "Lade Azure-Regionen" \
  "$SPLUNK_HOME/bin/splunk" cmd python3 "${APP_DIR}/regions_azure.py" >> "$LOGFILE" 2>&1

# 3) GCP
run_step "Lade GCP-Regionen" \
  "$SPLUNK_HOME/bin/splunk" cmd python3 "${APP_DIR}/regions_gcp.py" >> "$LOGFILE" 2>&1

# 4) Merge
run_step "Führe CSV-Dateien zusammen" \
  "$SPLUNK_HOME/bin/splunk" cmd python3 "${APP_DIR}/merge_regions.py" >> "$LOGFILE" 2>&1

# 5) Ergebnis prüfen
if [[ -f "$TARGET_LOOKUP" ]]; then
  echo "[✓] Erfolgreich erstellt: ${TARGET_LOOKUP}" >> "$LOGFILE"
else
  echo "[!] Fehler: ${TARGET_LOOKUP} wurde nicht erstellt!" >> "$LOGFILE"
  # kein 'exit 1', damit scripted input nicht hart fehlschlägt
fi

echo "[✓] Fertig. ($(date '+%Y-%m-%d %H:%M:%S'))" >> "$LOGFILE"
exit 0