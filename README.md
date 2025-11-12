# vhc_SA_focus_cr
---
## 🇩🇪 Deutsch
Die benötigten Python-Bibliotheken sind bereits in der App enthalten.
Falls eine Neuinstallation erforderlich ist (z. B. bei lokaler Entwicklung), 
können sie mit folgendem Befehl neu installiert werden:

```bash
pip install --no-compile -r requirements.txt -t lib

# BeautifulSoup-Tests & Fuzz-Cases entfernen 
# (vermeidet "Binary without source")
rm -rf lib/bs4/tests || true
find lib -type f -name '*.testcase' -delete

# falls sich doch irgendwo .so verirrt haben: 
# (sollte nach obigem Pinning nicht nötig sein)
find lib -type f -name '*.so' -delete

# Permissions gemäß AppInspect-Empfehlung
find . -type d -exec chmod 755 {} +
find . -type f -exec chmod 644 {} +
find bin -type f -exec chmod 755 {} +
```

## Cloud Region Builder (vhc_SA_cloudprovider)

### Automatische Aktualisierung
- Das Script `build_cloudregions_command.sh` wird über `inputs.conf` einmal im Quartal ausgeführt.
- Ausgabe erscheint in Splunk unter:
```spl
index=_internal sourcetype="vhc:cloudregions"
```

### Manuelle Aktualisierung
- Kann direkt über die Search App ausgeführt werden:
```spl
| cloudregions
```
- Führt `build_cloudregions.sh` aus und zeigt alle Logzeilen in der Search-Ausgabe.

### Ergebnis
- Die zusammengeführten Cloud-Regionen werden gespeichert unter:
`$SPLUNK_HOME/etc/apps/vhc_SA_cloudprovider/lookups/cloudregions.csv`

- Zugriff über Lookup-Definition: 
```spl
| inputlookup cloudregions
```

- Output-Felder:
`city, country, lat, lon, provider, region_id`

- Beispiel für Verwendung in einer Karte:
```spl
| geostats latfield=lat longfield=lon count by provider
```

### Unterstützte Provider
- [Amazon](https://docs.aws.amazon.com/quicksuite/latest/userguide/regions.html)
- [Microsoft](https://learn.microsoft.com/en-us/azure/reliability/regions-list?view=azure-cloud)
- [Google](https://cloud.google.com/compute/docs/gpus/gpu-regions-zones)

```spl
| eval provider = case(
    ProviderName == "AWS", "Amazon",
    ProviderName == "Microsoft", "Microsoft",
    ProviderName == "Google Cloud","Google",
    1=1, ProviderName
)
```

---

## 🇬🇧 English
The required Python libraries are already included in the app.
If reinstallation is needed (e.g., for local development), run the following commands:
```bash
pip install --no-compile -r requirements.txt -t lib

# Remove BeautifulSoup test and fuzz files 
# (prevents "Binary without source" AppInspect errors)
rm -rf lib/bs4/tests || true
find lib -type f -name '*.testcase' -delete

# Remove any leftover .so binary files 
# (should not be necessary with pinned pure-Python versions)
find lib -type f -name '*.so' -delete

# Set permissions according to Splunk AppInspect recommendations
find . -type d -exec chmod 755 {} +
find . -type f -exec chmod 644 {} +
find bin -type f -exec chmod 755 {} +
```

## Cloud Region Builder (vhc_SA_cloudprovider)

### Automatic Update
- The script `build_cloudregions_command.sh` is executed once per quarter via `inputs.conf`.
- Output appears in Splunk:
```spl
index=_internal sourcetype="vhc:cloudregions"
```

### Manual Update
- Can be triggered directly from the Splunk Search app:
  ```spl
  | cloudregions
  ```
- Executes build_regions.sh internally and displays all log lines in the Search UI.

### Result
- The merged cloud region data is stored at:
`$SPLUNK_HOME/etc/apps/vhc_SA_cloudprovider/lookups/cloudregions.csv`

- Lookup Definition: 
```spl
| inputlookup cloudregions
```

- Output fields:
`city, country, lat, lon, provider, region_id`

- Example usage with maps:
```spl
| geostats latfield=lat longfield=lon count by provider
```

### Supported Provider
- [Amazon](https://docs.aws.amazon.com/quicksuite/latest/userguide/regions.html)
- [Microsoft](https://learn.microsoft.com/en-us/azure/reliability/regions-list?view=azure-cloud)
- [Google](https://cloud.google.com/compute/docs/gpus/gpu-regions-zones)

```spl
| eval provider = case(
    ProviderName == "AWS", "Amazon",
    ProviderName == "Microsoft", "Microsoft",
    ProviderName == "Google Cloud","Google",
    1=1, ProviderName
)
```