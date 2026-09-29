import shutil
import os

if os.path.exists("logs_backup.db"):
    shutil.copy("logs_backup.db", "logs.db")
    print("Vraies donnees restaurees dans logs.db")
else:
    print("Aucune sauvegarde trouvee (logs_backup.db absent).")
