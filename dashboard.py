from flask import Flask, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def accueil():
    connexion = sqlite3.connect("logs.db")
    curseur = connexion.cursor()

    curseur.execute("SELECT * FROM evenements ORDER BY id DESC")
    evenements = curseur.fetchall()

    curseur.execute("SELECT * FROM alertes ORDER BY id DESC")
    alertes = curseur.fetchall()

    connexion.close()

    total = len(evenements)
    reussies = len([e for e in evenements if e[2] == "Accepted"])
    echouees = len([e for e in evenements if e[2] == "Failed"])
    derniere_maj = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    compteur_par_minute = {}
    for e in evenements:
        date_obj = datetime.strptime(e[1], "%Y-%m-%d %H:%M:%S.%f")
        minute = date_obj.strftime("%Y-%m-%d %H:%M")
        if minute not in compteur_par_minute:
            compteur_par_minute[minute] = {"Accepted": 0, "Failed": 0}
        compteur_par_minute[minute][e[2]] += 1

    minutes_triees = sorted(compteur_par_minute.keys())
    labels_affiches = [datetime.strptime(m, "%Y-%m-%d %H:%M").strftime("%Hh%M") for m in minutes_triees]
    valeurs_reussies = [compteur_par_minute[m]["Accepted"] for m in minutes_triees]
    valeurs_echouees = [compteur_par_minute[m]["Failed"] for m in minutes_triees]

    return render_template(
        "index.html",
        evenements=evenements,
        alertes=alertes,
        total=total,
        reussies=reussies,
        echouees=echouees,
        heures=labels_affiches,
        valeurs_reussies=valeurs_reussies,
        valeurs_echouees=valeurs_echouees,
        derniere_maj=derniere_maj
    )

if __name__ == "__main__":
    app.run(debug=True)
