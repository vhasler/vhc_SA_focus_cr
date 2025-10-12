# vhc_SA_cloudprovider
---
## 🇩🇪 Deutsch
Die benötigten Python-Bibliotheken sind bereits in der App enthalten.
Falls eine Neuinstallation erforderlich ist (z. B. bei lokaler Entwicklung), können sie mit
```bash
pip install --no-binary :all: -r requirements.txt -t lib
```
erneut installiert werden.

## Cloud Region Builder (vhc_SA_cloudprovider)

### Automatische Aktualisierung
- Das Script `build_regions.sh` wird über `inputs.conf` einmal im Quartal ausgeführt.
- Ausgabe erscheint im Splunk `_internal` Index (`sourcetype=vhc:cloudprovider:regionbuilder`).

### Manuelle Aktualisierung
- Direkt über Search starten: 
  ```spl
  | build_regions
  ```
- Führt `build_regions.sh` aus und zeigt alle Logzeilen in der Search.

### Ergebnis
- Zusammengeführte Cloud-Regionen unter:
`$SPLUNK_HOME/etc/apps/vhc_SA_cloudprovider/lookups/cloud_regions.csv`

---

## 🇬🇧 English
The required Python libraries are already included in the app.
If reinstallation is needed (e.g., during local development), run:
```bash
pip install --no-binary :all: -r requirements.txt -t lib
```

## Cloud Region Builder (vhc_SA_cloudprovider)

### Automatic Update
- The script build_regions.sh is executed once per quarter via inputs.conf.
- Output appears in the Splunk _internal index (sourcetype=vhc:cloudprovider:regionbuilder).

### Manual Update
- Run directly from Splunk Search:
  ```spl
  | build_regions
  ```
- Executes build_regions.sh and displays all log lines in the Search UI.

### Result
- The merged cloud regions are stored at:
`$SPLUNK_HOME/etc/apps/vhc_SA_cloudprovider/lookups/cloud_regions.csv`