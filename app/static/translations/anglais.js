// RYTHMO English translations.
// All English UI text is centralized here so templates stay language-neutral.
(function () {
  const STORAGE_KEY = "rythmo_language";
  const DEFAULT_LANGUAGE = "en";
  const currentLanguage = localStorage.getItem(STORAGE_KEY) || DEFAULT_LANGUAGE;

  const translations = {
  "-- Choisir un jour --": "-- Choose a day --",
  "-- Choisir une playlist --": "-- Choose a playlist --",
  "Acc\u00e9der \u00e0 l\u2019espace de gestion": "Go to the management area",
  "Actif": "Active",
  "Action": "Action",
  "Actions": "Actions",
  "Actions group\u00e9es": "Bulk actions",
  "Actions rapides": "Quick actions",
  "Administration": "Administration",
  "Administrez les comptes et les acc\u00e8s au syst\u00e8me": "Manage accounts and system access",
  "Adresse IP": "IP address",
  "Adresse IP (Cible)": "IP address (Target)",
  "Adresse email": "Email address",
  "Affectation": "Assignment",
  "Affecter": "Assign",
  "Affecter une playlist": "Assign a playlist",
  "Ajouter": "Add",
  "Ajouter Pub (Auto-Heure)": "Add Ad (Auto Time)",
  "Ajouter le lecteur": "Add player",
  "Ajouter un Lecteur": "Add a Player",
  "Ajouter un appareil": "Add a device",
  "Ajouter un commentaire...": "Add a comment...",
  "Ajouter une plage horaire": "Add a time slot",
  "Ajouter une publicit\u00e9 / annonce": "Add an advertisement / announcement",
  "Ajoutez des lecteurs pour commencer la surveillance": "Add players to start monitoring",
  "Alertes": "Alerts",
  "Al\u00e9atoire": "Shuffle",
  "Ambiance": "Mood",
  "Annonce": "Announcement",
  "Annonce urgente": "Urgent announcement",
  "Annuler": "Cancel",
  "Appareils audio configur\u00e9s": "Configured audio devices",
  "Assignation": "Assignment",
  "Assignez aux lecteurs, zones ou sites": "Assign to players, zones, or sites",
  "Assign\u00e9 \u00e0": "Assigned to",
  "Assign\u00e9 \u00e0 :": "Assigned to:",
  "Aucun commentaire": "No comments",
  "Aucun historique": "No history",
  "Aucun incident": "No incidents",
  "Aucun lecteur": "No players",
  "Aucun lecteur configur\u00e9": "No configured players",
  "Aucun log enregistr\u00e9 pour le moment": "No logs recorded yet",
  "Aucun utilisateur trouv\u00e9": "No users found",
  "Aucun \u00e9v\u00e9nement enregistr\u00e9": "No events recorded",
  "Aucune cible s\u00e9lectionn\u00e9e": "No target selected",
  "Aucune organisation associ\u00e9e \u00e0 votre compte.": "No organization is linked to your account.",
  "Aucune piste dans cette playlist": "No tracks in this playlist",
  "Aucune planification": "No schedule",
  "Aucune playlist": "No playlist",
  "Aucune playlist disponible.": "No playlist available.",
  "Avertissements": "Warnings",
  "Basculer secours": "Switch fallback",
  "Biblioth\u00e8que": "Library",
  "Biblioth\u00e8que musicale compl\u00e8te": "Complete music library",
  "Bloquer": "Block",
  "Bloqu\u00e9": "Blocked",
  "Bonjour": "Hello",
  "Bord": "Board",
  "Brouillon": "Draft",
  "Brouillons": "Drafts",
  "Brouillons et versions actives": "Drafts and active versions",
  "CONNECT\u00c9": "CONNECTED",
  "Cette action est irr\u00e9versible.": "This action cannot be undone.",
  "Changer de th\u00e8me": "Change theme",
  "Choisir un cr\u00e9neau ou une playlist": "Choose a time slot or playlist",
  "Choisir une organisation": "Choose an organization",
  "Choisis une ambiance pour adapter ton exp\u00e9rience musicale sur Rythmo": "Choose a mood to customize your Rythmo music experience",
  "Choisissez un mot de passe s\u00e9curis\u00e9": "Choose a secure password",
  "Choisissez un nom descriptif pour identifier facilement l'appareil": "Choose a descriptive name to identify the device easily",
  "Close": "Close",
  "Code de v\u00e9rification": "Verification code",
  "Commandes envoy\u00e9es au Raspberry Pi :": "Commands sent to the Raspberry Pi:",
  "Commencez par ajouter votre premier appareil audio": "Start by adding your first audio device",
  "Comment tu te sens aujourd'hui ?": "How are you feeling today?",
  "Commentaire de r\u00e9solution": "Resolution comment",
  "Commentaires": "Comments",
  "Configuration": "Configuration",
  "Configuration Administrative": "Administrative Configuration",
  "Configurer et surveiller les appareils": "Configure and monitor devices",
  "Configurez un nouvel appareil audio pour votre espace": "Configure a new audio device for your space",
  "Configur\u00e9": "Configured",
  "Connecter une plateforme": "Connect a platform",
  "Connect\u00e9": "Connected",
  "Connexion": "Login",
  "Consulter l'historique de diffusion": "View playback history",
  "Consulter le statut des appareils": "View device status",
  "Consulter le statut en temps r\u00e9el": "View real-time status",
  "Consulter les playlists publi\u00e9es": "View published playlists",
  "Contr\u00f4le Musical": "Music Control",
  "Critique": "Critical",
  "Critiques": "Critical",
  "Cr\u00e9er un compte": "Create an account",
  "Cr\u00e9er un compte - Rythmo": "Create an account - Rythmo",
  "Cr\u00e9er un site": "Create a site",
  "Cr\u00e9er une playlist": "Create a playlist",
  "Cr\u00e9er une zone": "Create a zone",
  "Cr\u00e9ez et g\u00e9rez vos biblioth\u00e8ques musicales": "Create and manage your music libraries",
  "Cr\u00e9ez votre premi\u00e8re playlist pour commencer": "Create your first playlist to get started",
  "Date": "Date",
  "Dernier contact": "Last contact",
  "Dernier contact :": "Last contact:",
  "Derni\u00e8re connexion": "Last login",
  "Derni\u00e8re sync :": "Last sync:",
  "Derni\u00e8re synchronisation": "Last synchronization",
  "Description": "Description",
  "Description d\u00e9taill\u00e9e": "Detailed description",
  "Diffuse imm\u00e9diatement une annonce sur le lecteur choisi.": "Immediately broadcast an announcement on the selected player.",
  "Dimanche": "Sunday",
  "Divisions au sein des sites": "Divisions within sites",
  "Down fr\u00e9quents": "Frequent outages",
  "Down fr\u00e9quents d\u00e9tect\u00e9s": "Frequent outages detected",
  "Dur\u00e9e totale": "Total duration",
  "D\u00c9CONNECT\u00c9": "DISCONNECTED",
  "D\u00e9bloquer": "Unblock",
  "D\u00e9but de l'incident": "Incident start",
  "D\u00e9clencher maintenant": "Trigger now",
  "D\u00e9connexion": "Logout",
  "D\u00e9crivez le probl\u00e8me rencontr\u00e9 en d\u00e9tail pour nous aider \u00e0 le r\u00e9soudre rapidement": "Describe the issue in detail so we can resolve it quickly",
  "D\u00e9finir comme playlist de secours (fallback)": "Set as fallback playlist",
  "D\u00e9rive sync": "Sync drift",
  "D\u00e9sactiver": "Disable",
  "D\u00e9tails": "Details",
  "EN LIGNE": "ONLINE",
  "Email": "Email",
  "Emplacement Physique": "Physical Location",
  "Emplacement physique": "Physical location",
  "En cours": "In progress",
  "En incident": "In incident",
  "En ligne": "Online",
  "Enregistrer": "Save",
  "Enregistrer le planning": "Save schedule",
  "Enregistrer les modifications": "Save changes",
  "Entrez le code re\u00e7u": "Enter the code you received",
  "Entrez le mot en MAJUSCULES": "Enter the word in UPPERCASE",
  "Entrez votre nom d'utilisateur et votre email": "Enter your username and email",
  "Envoyer le code": "Send code",
  "Envoyer le signalement": "Submit report",
  "Erreurs / Alertes": "Errors / Alerts",
  "Erreurs r\u00e9centes :": "Recent errors:",
  "Espace Commercial": "Commercial Area",
  "Espace client": "Client area",
  "Ex. Promo \u00e9t\u00e9": "E.g. Summer promo",
  "Ex: 192.168.1.50": "E.g. 192.168.1.50",
  "Ex: Couloir Nord, Salle de r\u00e9union A, etc.": "E.g. North corridor, Meeting room A, etc.",
  "Ex: Gare - Hall Principal": "E.g. Station - Main Hall",
  "Ex: Le lecteur ne r\u00e9pond plus": "E.g. The player no longer responds",
  "Explorer": "Explore",
  "Exporter l'historique en CSV": "Export history as CSV",
  "Exporter les logs": "Export logs",
  "Faible": "Low",
  "Fichier manquant": "Missing file",
  "Filtres avanc\u00e9s": "Advanced filters",
  "Filtres intelligents": "Smart filters",
  "Forcer la synchronisation": "Force synchronization",
  "Forcer sync": "Force sync",
  "Formulaire de signalement": "Report form",
  "For\u00eat, feuilles & calme vert": "Forest, leaves & green calm",
  "Gestion Lecteurs": "Player Management",
  "Gestion Op\u00e9rationnelle": "Operations Management",
  "Gestion des Alertes": "Alert Management",
  "Gestion des Lecteurs": "Player Management",
  "Gestion des Playlists": "Playlist Management",
  "Gestion des Utilisateurs": "User Management",
  "Gestion musicale professionnelle": "Professional music management",
  "Gravit\u00e9": "Severity",
  "Grille": "Grid",
  "G\u00e9rer le planning": "Manage schedule",
  "G\u00e9rer les membres et les acc\u00e8s": "Manage members and access",
  "G\u00e9rez toutes vos playlists en un seul endroit": "Manage all your playlists in one place",
  "HORS LIGNE": "OFFLINE",
  "Haute": "High",
  "Heure D\u00e9but": "Start Time",
  "Heure Fin": "End Time",
  "Historique": "History",
  "Historique complet des actions et \u00e9v\u00e9nements par organisation": "Complete history of actions and events by organization",
  "Hors ligne": "Offline",
  "ID Org": "Org ID",
  "INCONNU": "UNKNOWN",
  "Identification": "Identification",
  "Ignorer": "Ignore",
  "Ignor\u00e9s": "Ignored",
  "Importer des musiques": "Import music",
  "Info": "Info",
  "Informations": "Information",
  "Infos / Connexions": "Info / Connections",
  "Jeudi": "Thursday",
  "Jour de la semaine": "Day of the week",
  "Journal d'Activit\u00e9": "Activity Log",
  "Joyeux": "Happy",
  "L'adresse IP de l'appareil sur le r\u00e9seau local": "The device IP address on the local network",
  "L'emplacement r\u00e9el de l'appareil dans votre espace": "The actual location of the device in your space",
  "La playlist s\u00e9lectionn\u00e9e sera diffus\u00e9e automatiquement pendant la plage horaire d\u00e9finie.": "The selected playlist will play automatically during the defined time slot.",
  "Lecteur": "Player",
  "Lecteur cible": "Target player",
  "Lecteur concern\u00e9 (optionnel)": "Related player (optional)",
  "Lecteur hors ligne": "Player offline",
  "Lecteur s\u00e9lectionn\u00e9": "Selected player",
  "Lecteur unique": "Single player",
  "Lecteurs": "Players",
  "Lecteurs cibl\u00e9s": "Targeted players",
  "Lecteurs impact\u00e9s": "Impacted players",
  "Lecteurs impact\u00e9s :": "Impacted players:",
  "Lecture": "Playback",
  "Lecture / Pause": "Play / Pause",
  "Lecture en cours": "Now playing",
  "Lecture seule": "Read only",
  "Les actions seront appliqu\u00e9es \u00e0 tous les lecteurs de ce site": "Actions will apply to all players on this site",
  "Les actions seront appliqu\u00e9es \u00e0 tous les lecteurs de cette zone": "Actions will apply to all players in this zone",
  "Les incidents critiques sont trait\u00e9s en priorit\u00e9. Pour les autres, nous visons un d\u00e9lai de r\u00e9ponse sous 24-48h.": "Critical incidents are handled first. For others, we aim to respond within 24-48 hours.",
  "Les playlists changeront automatiquement aux heures d\u00e9finies.": "Playlists will switch automatically at the defined times.",
  "Les \u00e9v\u00e9nements syst\u00e8me appara\u00eetront ici": "System events will appear here",
  "Liste": "List",
  "Locale": "Local",
  "Login to Rythmo": "Login to Rythmo",
  "Lundi": "Monday",
  "Mardi": "Tuesday",
  "Mercredi": "Wednesday",
  "Message": "Message",
  "Mix Rythmo": "Rythmo Mix",
  "Mode": "Mode",
  "Mot cach\u00e9 requis pour continuer": "Hidden word required to continue",
  "Mot de passe (10+ caract\u00e8res)": "Password (10+ characters)",
  "Mot de passe oubli\u00e9": "Forgot password",
  "Mot de passe oubli\u00c3\u00a9 ?": "Forgot password?",
  "Mot de passe oubli\u00e9 ?": "Forgot password?",
  "Moyenne": "Medium",
  "Musique": "Music",
  "Nature": "Nature",
  "Navigation": "Navigation",
  "Nom": "Name",
  "Nom de l'appareil": "Device name",
  "Nom du lecteur": "Player name",
  "Nom ou ID du lecteur si applicable": "Player name or ID if applicable",
  "Notes de musique & identit\u00e9 signature": "Music notes & signature identity",
  "Nouveau Lecteur Audio": "New Audio Player",
  "Nouveau mot de passe": "New password",
  "Nouvelle Planification": "New Schedule",
  "Nuit": "Night",
  "OBSOL\u00c8TE": "OBSOLETE",
  "OK": "OK",
  "Organisez la diffusion des playlists pour :": "Organize playlist broadcasts for:",
  "Organisez vos espaces de mani\u00e8re hi\u00e9rarchique": "Organize your spaces hierarchically",
  "Ouverts": "Open",
  "Param\u00e8tres et contr\u00f4le avanc\u00e9": "Advanced settings and control",
  "Pas encore de compte ?": "No account yet?",
  "Password": "Password",
  "Permission refus\u00e9e": "Permission denied",
  "Personnalisation": "Personalization",
  "Pilotez la musique sur vos lecteurs en temps r\u00e9el": "Control music on your players in real time",
  "Piste :": "Track:",
  "Piste pr\u00e9c\u00e9dente": "Previous track",
  "Piste suivante": "Next track",
  "Pistes": "Tracks",
  "Planification Hebdomadaire": "Weekly Scheduling",
  "Planifier une diffusion": "Schedule a broadcast",
  "Planning des diffusions": "Broadcast schedule",
  "Playlist :": "Playlist:",
  "Playlist de secours": "Fallback playlist",
  "Playlist de secours active": "Active fallback playlist",
  "Playlist locale (active)": "Local playlist (active)",
  "Playlists": "Playlists",
  "Playlists de fallback automatiques": "Automatic fallback playlists",
  "Playlists disponibles": "Available playlists",
  "Pluie m\u00e9lancolique & bleu apaisant": "Melancholic rain & soothing blue",
  "Plus": "More",
  "Plus votre description est pr\u00e9cise, plus nous pourrons r\u00e9soudre le probl\u00e8me rapidement.": "The more precise your description is, the faster we can resolve the issue.",
  "Position :": "Position:",
  "Principales": "Main",
  "Priorit\u00e9": "Priority",
  "Probl\u00e8mes d\u00e9tect\u00e9s": "Detected issues",
  "Programmation automatique des playlists sur le Lecteur Principal": "Automatic playlist scheduling on the Main Player",
  "Pr\u00e9nom": "First name",
  "Pr\u00e9vu": "Scheduled",
  "Publication": "Publication",
  "Publicit\u00e9": "Advertisement",
  "Publicit\u00e9s, annonces et diffusion sur les lecteurs": "Advertisements, announcements and player broadcasts",
  "Publicit\u00e9s, annonces et diffusion urgente": "Advertisements, announcements and urgent broadcasting",
  "Publier": "Publish",
  "Publi\u00e9e": "Published",
  "Que se passe-t-il apr\u00e8s l'envoi ?": "What happens after submission?",
  "RYTHMO": "RYTHMO",
  "Rechercher dans les messages...": "Search messages...",
  "Rechercher une playlist...": "Search for a playlist...",
  "Reconna\u00eetre": "Acknowledge",
  "Red\u00e9marrer": "Restart",
  "Renseignez les informations de l'appareil": "Enter the device information",
  "Retour": "Back",
  "Retour au lecteur": "Back to player",
  "Retour au tableau de bord": "Back to dashboard",
  "Retour aux alertes": "Back to alerts",
  "Retour aux playlists": "Back to playlists",
  "Retour \u00e0 la connexion": "Back to login",
  "Retour \u00e0 la liste": "Back to list",
  "Romantique": "Romantic",
  "Rose, c\u0153urs & fleurs d\u00e9licates": "Pink, hearts & delicate flowers",
  "Rythmo": "Rythmo",
  "R\u00e9initialisation du mot de passe - Rythmo": "Password reset - Rythmo",
  "R\u00e9initialiser": "Reset",
  "R\u00e9p\u00e9ter": "Repeat",
  "R\u00e9solu le": "Resolved on",
  "R\u00e9solu le :": "Resolved on:",
  "R\u00e9solus": "Resolved",
  "R\u00e9soudre": "Resolve",
  "R\u00e9soudre l'incident": "Resolve incident",
  "R\u00f4le": "Role",
  "S'assigner": "Assign to me",
  "S'inscrire": "Sign up",
  "Samedi": "Saturday",
  "Sant\u00e9": "Health",
  "Se connecter": "Log in",
  "Secours": "Fallback",
  "Signalement d'Incident": "Incident Report",
  "Signaler un incident": "Report an incident",
  "Signalez un probl\u00e8me rencontr\u00e9 sur l'outil RYTHMO": "Report an issue encountered in the RYTHMO tool",
  "Site": "Site",
  "Sites": "Sites",
  "Sites & Zones": "Sites & Zones",
  "Soleil, confettis & \u00e9nergie positive": "Sun, confetti & positive energy",
  "Stabilit\u00e9": "Stability",
  "Stabilit\u00e9 :": "Stability:",
  "Statut :": "Status:",
  "Statut int\u00e9grit\u00e9 :": "Integrity status:",
  "Supervision Temps R\u00e9el": "Real-Time Supervision",
  "Supervision des incidents en temps r\u00e9el": "Real-time incident supervision",
  "Supervision et traitement des incidents en temps r\u00e9el": "Real-time incident monitoring and handling",
  "Support": "Support",
  "Supprimer ce lecteur": "Delete this player",
  "Surveillez et contr\u00f4lez tous vos appareils audio en temps r\u00e9el": "Monitor and control all your audio devices in real time",
  "Surveillez et maintenez vos appareils en temps r\u00e9el": "Monitor and maintain your devices in real time",
  "Surveillez toutes les actions et \u00e9v\u00e9nements du syst\u00e8me": "Monitor all system actions and events",
  "Sync": "Sync",
  "Synchroniser": "Synchronize",
  "Synchronis\u00e9": "Synchronized",
  "Syst\u00e8me de gestion et de diffusion musicale professionnel. Contr\u00f4lez vos lecteurs audio en temps r\u00e9el.": "Professional music management and broadcasting system. Control your audio players in real time.",
  "Syst\u00e8me s\u00e9curis\u00e9": "Secure system",
  "S\u00e9lectionner la Playlist": "Select Playlist",
  "S\u00e9lectionner la cible": "Select target",
  "S\u00e9lectionner la cible d'affectation": "Select assignment target",
  "S\u00e9lectionner un lecteur": "Select a player",
  "S\u00e9lectionner un site": "Select a site",
  "S\u00e9lectionner une zone": "Select a zone",
  "S\u00e9lectionnez l\u2019organisation sur laquelle vous souhaitez travailler. Les lecteurs, playlists et planifications seront filtr\u00e9s selon ce choix.": "Select the organization you want to work on. Players, playlists and schedules will be filtered accordingly.",
  "S\u00e9lectionnez un type": "Select a type",
  "S\u00e9lectionnez une section pour commencer votre gestion musicale": "Select a section to start managing your music",
  "Tableau de": "Dashboard",
  "Tableau de bord": "Dashboard",
  "Temps de r\u00e9ponse": "Response time",
  "Test": "Test",
  "Tester le volume": "Test volume",
  "Tester lecture": "Test playback",
  "Timeline": "Timeline",
  "Timeline des \u00e9v\u00e9nements": "Event timeline",
  "Titre": "Title",
  "Titre du probl\u00e8me": "Issue title",
  "Toggle navigation": "Toggle navigation",
  "Total incidents": "Total incidents",
  "Total lecteurs": "Total players",
  "Total logs": "Total logs",
  "Tous": "All",
  "Tous les syst\u00e8mes fonctionnent correctement": "All systems are operating normally",
  "Toutes": "All",
  "Triste": "Sad",
  "Type": "Type",
  "Type d'action": "Action type",
  "Type d'incident": "Incident type",
  "Type de contenu": "Content type",
  "Uptime": "Uptime",
  "Uptime :": "Uptime:",
  "Username": "Username",
  "Utilisateurs": "Users",
  "Utilisateurs inscrits": "Registered users",
  "Valider": "Confirm",
  "Vendredi": "Friday",
  "Version 1.0.0": "Version 1.0.0",
  "Version firmware": "Firmware version",
  "Vide": "Empty",
  "Voir": "View",
  "Voir d\u00e9tails": "View details",
  "Voir la playlist": "View playlist",
  "Voir le lecteur": "View player",
  "Voir les d\u00e9tails": "View details",
  "Voir tout": "View all",
  "Volume": "Volume",
  "Volume :": "Volume:",
  "Vos emplacements principaux": "Your main locations",
  "Votre signalement est automatiquement enregistr\u00e9 dans le syst\u00e8me. Notre \u00e9quipe technique l'examinera et vous contactera si n\u00e9cessaire.": "Your report is automatically saved in the system. Our technical team will review it and contact you if needed.",
  "Vous avez d\u00e9j\u00e0 un compte ?": "Already have an account?",
  "Vue hi\u00e9rarchique compl\u00e8te": "Full hierarchical view",
  "V\u00e9rification": "Verification",
  "V\u00e9rifier le code": "Verify code",
  "Warning": "Warning",
  "Zone": "Zone",
  "Zone de danger": "Danger zone",
  "Zone impact\u00e9e": "Impacted zone",
  "Zones": "Zones",
  "annonce": "announcement",
  "autre": "other",
  "bug": "bug",
  "create": "create",
  "critique": "critical",
  "en_cours": "in_progress",
  "faible": "low",
  "haute": "high",
  "ignore": "ignore",
  "incidents critiques": "critical incidents",
  "interface": "interface",
  "lecteur": "player",
  "moyenne": "medium",
  "ouvert": "open",
  "performance": "performance",
  "playlist": "playlist",
  "publicite": "advertisement",
  "resolu": "resolved",
  "synchronisation": "synchronization",
  "tous": "all",
  "\u00a9 2024 RYTHMO": "\u00a9 2024 RYTHMO",
  "\u00a9 2024 RYTHMO. Tous droits r\u00e9serv\u00e9s.": "\u00a9 2024 RYTHMO. All rights reserved.",
  "\u00c0 JOUR": "UP TO DATE",
  "\u00c0 propos": "About",
  "\u00c9tat": "Status",
  "\u00c9tat Temps R\u00e9el": "Real-Time Status",
  "\u00c9tat des lecteurs": "Player status",
  "\u00c9tat temps r\u00e9el": "Real-time status",
  "\u00c9toiles scintillantes & calme nocturne": "Twinkling stars & nighttime calm",
  "\u00c9v\u00e9nements syst\u00e8me": "System events",
  "\u25cf KO (Hors Ligne)": "\u25cf KO (Offline)",
  "\u25cf UP (En Ligne)": "\u25cf UP (Online)",
  "\u2600\ufe0f Joyeux": "\u2600\ufe0f Happy",
  "\u26a1 Probl\u00e8me de performance": "\u26a1 Performance issue",
  "\u2753 Autre": "\u2753 Other",
  "\ud83c\udf27\ufe0f Triste": "\ud83c\udf27\ufe0f Sad",
  "\ud83c\udf3f Nature": "\ud83c\udf3f Nature",
  "\ud83c\udfa7 V\u00e9rification Superviseur": "\ud83c\udfa7 Supervisor Verification",
  "\ud83c\udfa8 Probl\u00e8me d'interface": "\ud83c\udfa8 Interface issue",
  "\ud83c\udfb5 Mix": "\ud83c\udfb5 Mix",
  "\ud83c\udfb5 Mix (d\u00e9faut)": "\ud83c\udfb5 Mix (default)",
  "\ud83c\udfb5 Probl\u00e8me avec une playlist": "\ud83c\udfb5 Playlist issue",
  "\ud83d\udc1b Bug / Erreur technique": "\ud83d\udc1b Bug / Technical error",
  "\ud83d\udc95 Romantique": "\ud83d\udc95 Romantic",
  "\ud83d\udd04 Probl\u00e8me de synchronisation": "\ud83d\udd04 Synchronization issue",
  "\ud83d\udd0a Probl\u00e8me avec un lecteur": "\ud83d\udd0a Player issue"
  };

  const patternTranslations = [
    [/^(\d+)\s+lecteurs?$/i, "$1 players"],
    [/^(\d+)\s+incidents?$/i, "$1 incidents"],
    [/^(\d+)\s+logs?$/i, "$1 logs"],
    [/^(\d+)\s+utilisateurs?$/i, "$1 users"],
    [/^(\d+)\s+playlists?$/i, "$1 playlists"],
    [/^(\d+)\s+pistes?$/i, "$1 tracks"],
    [/^(\d+)\s+planifications?$/i, "$1 schedules"],
    [/^(\d+)\s+zones?$/i, "$1 zones"],
    [/^(\d+)\s+sites?$/i, "$1 sites"],
    [/^(.+)\s+au total$/i, "$1 total"]
  ];

  const attrNames = ["title", "placeholder", "aria-label", "value"];
  const ignoredTags = new Set(["SCRIPT", "STYLE", "NOSCRIPT", "TEXTAREA", "CODE", "PRE"]);

  function addLanguageSwitcher() {
    if (document.getElementById("rythmo-language-switcher")) return;

    const style = document.createElement("style");
    style.textContent = `
      .rythmo-language-switcher {
        position: fixed;
        right: 1rem;
        bottom: 1rem;
        z-index: 2000;
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        min-width: 76px;
        justify-content: center;
        padding: 0.55rem 0.75rem;
        border-radius: 999px;
        border: 1px solid rgba(255, 193, 7, 0.55);
        background: rgba(26, 6, 12, 0.9);
        color: #ffc107;
        font: 700 0.85rem/1 Manrope, system-ui, sans-serif;
        letter-spacing: 0;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
        backdrop-filter: blur(14px);
        cursor: pointer;
      }

      .rythmo-language-switcher:hover,
      .rythmo-language-switcher:focus {
        background: #ffc107;
        color: #1a060c;
        outline: none;
      }
    `;

    const button = document.createElement("button");
    button.id = "rythmo-language-switcher";
    button.className = "rythmo-language-switcher";
    button.type = "button";
    button.setAttribute("aria-label", currentLanguage === "en" ? "Passer en français" : "Switch to English");
    button.textContent = currentLanguage === "en" ? "FR" : "EN";
    button.addEventListener("click", () => {
      localStorage.setItem(STORAGE_KEY, currentLanguage === "en" ? "fr" : "en");
      window.location.reload();
    });

    document.head.appendChild(style);
    document.body.appendChild(button);
  }

  function normalize(text) {
    return String(text || "").replace(/\s+/g, " " ).trim();
  }

  function translateText(value) {
    const key = normalize(value);
    if (translations[key]) return translations[key];
    for (const [pattern, replacement] of patternTranslations) {
      if (pattern.test(key)) return key.replace(pattern, replacement);
    }
    return null;
  }

  function replaceTextNode(node) {
    const translated = translateText(node.nodeValue);
    if (!translated) return;
    const leading = (node.nodeValue.match(/^\s*/) || [""])[0];
    const trailing = (node.nodeValue.match(/\s*$/) || [""])[0];
    node.nodeValue = leading + translated + trailing;
  }

  function translateElementAttributes(element) {
    attrNames.forEach((attr) => {
      if (!element.hasAttribute(attr)) return;
      const translated = translateText(element.getAttribute(attr));
      if (translated) element.setAttribute(attr, translated);
    });
  }

  function translateRoot(root) {
    if (!root) return;
    if (root.nodeType === Node.ELEMENT_NODE) translateElementAttributes(root);

    const walker = document.createTreeWalker(
      root,
      NodeFilter.SHOW_TEXT | NodeFilter.SHOW_ELEMENT,
      {
        acceptNode(node) {
          const parent = node.nodeType === Node.TEXT_NODE ? node.parentElement : node;
          if (!parent || ignoredTags.has(parent.tagName)) return NodeFilter.FILTER_REJECT;
          return NodeFilter.FILTER_ACCEPT;
        }
      }
    );

    const textNodes = [];
    const elements = [];
    while (walker.nextNode()) {
      const node = walker.currentNode;
      if (node.nodeType === Node.TEXT_NODE) textNodes.push(node);
      if (node.nodeType === Node.ELEMENT_NODE) elements.push(node);
    }

    elements.forEach(translateElementAttributes);
    textNodes.forEach(replaceTextNode);
  }

  function translateDocument() {
    document.documentElement.lang = currentLanguage;
    addLanguageSwitcher();
    if (currentLanguage === "fr") return;

    if (document.title) {
      const translatedTitle = translateText(document.title);
      if (translatedTitle) document.title = translatedTitle;
    }
    translateRoot(document.body);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", translateDocument);
  } else {
    translateDocument();
  }

  const observer = new MutationObserver((mutations) => {
    if (currentLanguage === "fr") return;
    observer.disconnect();
    mutations.forEach((mutation) => {
      mutation.addedNodes.forEach((node) => {
        if (node.nodeType === Node.TEXT_NODE) replaceTextNode(node);
        if (node.nodeType === Node.ELEMENT_NODE) translateRoot(node);
      });
      if (mutation.type === "characterData") replaceTextNode(mutation.target);
    });
    observer.observe(document.body, { childList: true, subtree: true, characterData: true });
  });

  if (document.body) {
    observer.observe(document.body, { childList: true, subtree: true, characterData: true });
  }
})();
