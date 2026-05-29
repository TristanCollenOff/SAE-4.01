from datetime import datetime

class Lecteur:
    def __init__(self, id_lecteur, nom_lecteur, adresseIP, etat_lecteur, derniere_synchro, adresse_lecteur=None):
        self.id_lecteur = id_lecteur
        self.nom_lecteur = nom_lecteur
        self.adresseIP = adresseIP
        self.etat_lecteur = etat_lecteur      # "UP" ou "KO"
        self.derniere_synchro = derniere_synchro  # Texte "2025-01-16 15:30:00"
        self.adresse_lecteur = adresse_lecteur

    def est_en_ligne(self):
        if not self.derniere_synchro:
            return False

        fmt = '%Y-%m-%d %H:%M:%S'
        try:
            # On nettoie la date pour éviter les millisecondes qui font bugger strptime
            date_str = str(self.derniere_synchro)[:19]
            derniere_date = datetime.strptime(date_str, fmt)
            maintenant = datetime.now()
            
            difference = (maintenant - derniere_date).total_seconds()
            
            # Debug simple sans caractères spéciaux
            print(f"Check Lecteur {self.id_lecteur} - Ecart: {difference}s")

            # Si l'écart est moins de 15 secondes, c'est VERT
            return abs(difference) < 15
        except Exception as e:
            return False
        
    def get_etat_playlist_secours(self):
        """
        Logique métier : Si le lecteur est KO, sa playlist est sûrement obsolète.
        """
        if self.est_en_ligne():
            return "OK"
        else:
            return "Obsolète"