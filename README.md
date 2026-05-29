```
pip3 install flask

```

```
python3 main.py
```

```
python -m app.init_db
```

RYTHMO est une application web complète de gestion et de diffusion musicale automatisée pour espaces commerciaux et publics. Le système permet de contrôler à distance des lecteurs audio (Raspberry Pi), de planifier des playlists par plages horaires et de gérer l'ensemble depuis une interface web centralisée.

🎧 Gestion des Lecteurs Audio

Contrôle à distance de lecteurs Raspberry Pi 5
Configuration volume, état (lecture/pause/arrêt)
Monitoring en temps réel de l'état des lecteurs
Gestion des emplacements et zones de diffusion

📅 Planification Hebdomadaire

Programmation automatique des playlists par jour et plage horaire
Interface intuitive de planification avec vue par jour
Basculement automatique entre playlists (ex: Matin, Midi, Soir)
Gestion des dates spécifiques pour événements

🎶 Bibliothèque de Playlists

Création et édition de playlists personnalisées
Calcul automatique de la durée totale
Association playlists-lecteurs-planning
Gestion des publicités et messages audio

🚨 Système d'Alertes

Activation/désactivation d'alertes en temps réel
Diffusion prioritaire sur tous les lecteurs
Enregistrement automatique dans les logs

👥 Gestion des Utilisateurs

Authentification sécurisée avec sessions
Système de rôles (Utilisateur, Administrateur, Superviseur)
Blocage automatique après 3 tentatives échouées
Réinitialisation de mot de passe par email
Gestion manuelle des comptes par administrateur

📊 Logs et Traçabilité

Enregistrement de toutes les actions système
Catégorisation (Infos, Avertissements, Erreurs)
Interface de visualisation avec statistiques en temps réel
Filtres et recherche dans l'historique

🎨 Interface Moderne

Design responsive (mobile, tablette, desktop)
Charte graphique noir/jaune/rouge
Dashboard personnalisé selon le rôle
Navigation intuitive et fluide
