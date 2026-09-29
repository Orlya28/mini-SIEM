import sqlite3
from datetime import datetime, timedelta

connexion = sqlite3.connect("logs.db")
curseur = connexion.cursor()

curseur.execute("SELECT date, ip FROM evenements WHERE statut = 'Failed'")
echecs = curseur.fetchall()

echecs_par_ip = {}
for date_texte, ip in echecs:
    date_obj = datetime.strptime(date_texte, "%Y-%m-%d %H:%M:%S.%f")
    if ip not in echecs_par_ip:
        echecs_par_ip[ip] = []
    echecs_par_ip[ip].append(date_obj)

SEUIL_TENTATIVES = 3
FENETRE_MINUTES = 2

for ip, dates in echecs_par_ip.items():
    dates.sort()

    for i in range(len(dates)):
        fenetre = [d for d in dates if dates[i] <= d <= dates[i] + timedelta(minutes=FENETRE_MINUTES)]

        if len(fenetre) >= SEUIL_TENTATIVES:
            date_detection = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            curseur.execute(
                "INSERT OR IGNORE INTO alertes (type, ip, nombre_tentatives, date_detection) VALUES (?, ?, ?, ?)",
                ("brute_force_ssh", ip, len(fenetre), date_detection)
            )
            print(f"ALERTE : {len(fenetre)} echecs depuis {ip} en moins de {FENETRE_MINUTES} minutes")
            break

connexion.commit()
connexion.close()
print("\nAnalyse terminee.")
