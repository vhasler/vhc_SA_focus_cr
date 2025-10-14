#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# build_regions_manually.py
# Splunk Custom Command: | build_regions
# Führt das Shell-Skript build_regions.sh aus, um Cloud-Region-CSV zu aktualisieren.
# -----------------------------------------------------------------------------
import os
import subprocess
import sys

def main():
    app_dir = os.path.dirname(__file__)
    script_path = os.path.join(app_dir, "build_cloudregions.sh")

    if not os.path.exists(script_path):
        print(f"[!] Fehler: {script_path} wurde nicht gefunden.")
        sys.exit(1)

    print("[*] Starte manuelles Cloud-Region-Update...")
    print(f"→ Führe Script aus: {script_path}")

    try:
        # run() mit Ausgabeerfassung
        result = subprocess.run(
            ["bash", script_path],
            capture_output=True,
            text=True,
            timeout=900  # 15 Minuten Sicherheitstimeout
        )

        # Standardausgabe
        if result.stdout:
            print(result.stdout.strip())

        # Fehlerausgabe
        if result.stderr:
            print(result.stderr.strip(), file=sys.stderr)

        if result.returncode == 0:
            print("[✓] Cloud-Regionen erfolgreich aktualisiert.")
        else:
            print(f"[!] Script beendet mit Fehlercode {result.returncode}.")

    except subprocess.TimeoutExpired:
        print("[!] Timeout: Das Script hat zu lange gebraucht und wurde beendet.")
    except Exception as e:
        print(f"[!] Unerwarteter Fehler: {e}")

if __name__ == "__main__":
    main()