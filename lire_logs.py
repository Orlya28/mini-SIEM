import subprocess
import json
import re
import sqlite3
from datetime import datetime

import subprocess
import json
import re
import sqlite3
from datetime import datetime

resultat = subprocess.run(
    ["journalctl", "-u", "ssh", "--since", "30 minutes ago", "-o", "json", "--no-pager"],
    capture_output=True,
    text=True
)

lignes = resultat.stdout.strip().split("\n")

evenements = []

connexion = sqlite3.connect("logs.db")
curseur = connexion.cursor()

for ligne in lignes:
    if not ligne:
        continue
    log = json.loads(ligne)
    message = log.get("MESSAGE", "")
    timestamp_brut = log.get("__REALTIME_TIMESTAMP")

    if timestamp_brut:
        timestamp_secondes = int(timestamp_brut) / 1_000_000
        date_lisible = datetime.fromtimestamp(timestamp_secondes)
    else:
        date_lisible = "date inconnue"

    match = re.search(r"(Accepted|Failed) password for (\w+) from ([\d.]+)", message)

    if match:
        statut = match.group(1)
        utilisateur = match.group(2)
        ip = match.group(3)

        evenement = {
            "date": date_lisible,
            "statut": statut,
            "utilisateur": utilisateur,
            "ip": ip
        }
        evenements.append(evenement)

        curseur.execute(
            "INSERT OR IGNORE INTO evenements (date, statut, utilisateur, ip) VALUES (?, ?, ?, ?)",
            (str(date_lisible), statut, utilisateur, ip)
        )

print(f"\n{len(evenements)} événement(s) de connexion détecté(s) :\n")
for e in evenements:
    print(e)

connexion.commit()
connexion.close()
print("\nÉvénements enregistrés dans logs.db")
