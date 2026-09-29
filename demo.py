import sqlite3
import shutil
import random
from datetime import datetime, timedelta

shutil.copy("logs.db", "logs_backup.db")
print("Sauvegarde des vraies donnees faite dans logs_backup.db")

connexion = sqlite3.connect("logs.db")
curseur = connexion.cursor()

curseur.execute("DELETE FROM evenements")
curseur.execute("DELETE FROM alertes")
connexion.commit()
print("Base videe, generation des donnees simulees...")

ips_attaquantes = ["45.33.12.87", "185.220.101.4", "103.219.112.45"]
ip_legitime = "192.168.3.129"
utilisateurs = ["admin", "root", "test", "orlya"]

maintenant = datetime.now()
evenements_generes = []

for ip in ips_attaquantes:
    utilisateur_cible = random.choice(utilisateurs)
    heure_depart = maintenant - timedelta(minutes=random.randint(10, 120))
    nombre_tentatives = random.randint(4, 8)
    for i in range(nombre_tentatives):
        date_evenement = heure_depart + timedelta(seconds=i * 15)
        evenements_generes.append((date_evenement, "Failed", utilisateur_cible, ip))

for i in range(10):
    date_evenement = maintenant - timedelta(minutes=random.randint(1, 60))
    evenements_generes.append((date_evenement, "Accepted", "orlya", ip_legitime))

for date_evenement, statut, utilisateur, ip in evenements_generes:
    date_texte = date_evenement.strftime("%Y-%m-%d %H:%M:%S.%f")
    curseur.execute(
        "INSERT OR IGNORE INTO evenements (date, statut, utilisateur, ip) VALUES (?, ?, ?, ?)",
        (date_texte, statut, utilisateur, ip)
    )

connexion.commit()
connexion.close()
print(f"{len(evenements_generes)} evenements simules inseres.")
print("Lance maintenant : python3 detection.py")
