DROP TABLE IF EXISTS Utilisateur;
CREATE TABLE Utilisateur(
   id_utilisateur INTEGER PRIMARY KEY AUTOINCREMENT,
   nom_utilisateur VARCHAR(50) UNIQUE,
   motdepasse VARCHAR(128),
   role VARCHAR(50),
   prenom VARCHAR(50),
   nom VARCHAR(50),
   age INTEGER,
   email VARCHAR(100) UNIQUE,
   login_attempts INTEGER DEFAULT 0,
   block_until DATETIME,
   last_login DATETIME
);

DROP TABLE IF EXISTS Organisation;
CREATE TABLE Organisation(
   id_organisation INTEGER PRIMARY KEY AUTOINCREMENT,
   nom_organisation VARCHAR(50) UNIQUE
);

DROP TABLE IF EXISTS Playlist;
CREATE TABLE Playlist(
   id_playlist INTEGER PRIMARY KEY AUTOINCREMENT,
   nom_playlist VARCHAR(50) UNIQUE,
   date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
   date_fin_playlist DATE,
   date_derniere_maj DATETIME,
   publie BOOLEAN DEFAULT 1
);

DROP TABLE IF EXISTS Fichier;
CREATE TABLE Fichier(
   id_fichier INTEGER PRIMARY KEY AUTOINCREMENT,
   nom VARCHAR(100) NOT NULL,
   emplacement VARCHAR(255),
   duree_fichier INTEGER,
   date_ajout DATETIME DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS Lecteur;
CREATE TABLE Lecteur(
   id_lecteur INTEGER PRIMARY KEY AUTOINCREMENT,
   nom_lecteur VARCHAR(50) NOT NULL UNIQUE,
   adresseIP VARCHAR(50) UNIQUE,
   etat_lecteur VARCHAR(50) DEFAULT 'Hors ligne',
   emplacement VARCHAR(50),
   derniere_synchro DATETIME,
   adresse_lecteur VARCHAR(50),
   id_organisation INTEGER NOT NULL,
   playlist_active_id INTEGER, 
   volume INTEGER DEFAULT 80,
   alerte_active BOOLEAN DEFAULT 0,
   FOREIGN KEY(id_organisation) REFERENCES Organisation(id_organisation),
   FOREIGN KEY(playlist_active_id) REFERENCES Playlist(id_playlist)
);

DROP TABLE IF EXISTS Planification;
CREATE TABLE Planification(
   id_planification INTEGER PRIMARY KEY AUTOINCREMENT,
   id_lecteur INTEGER NOT NULL,
   id_playlist INTEGER NOT NULL,
   jour_semaine VARCHAR(10), 
   heure_debut TIME,
   heure_fin TIME,
   date_specifique DATE, 
   FOREIGN KEY(id_lecteur) REFERENCES Lecteur(id_lecteur),
   FOREIGN KEY(id_playlist) REFERENCES Playlist(id_playlist)
);

DROP TABLE IF EXISTS FichierLog;
CREATE TABLE FichierLog (
    id_log INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    username VARCHAR(50), 
    type_log VARCHAR(50), 
    message VARCHAR(255),
    date_fichierlog DATETIME DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY(user_id) REFERENCES Utilisateur(id_utilisateur)
);

DROP TABLE IF EXISTS Conçoit_une;
CREATE TABLE Conçoit_une(
   id_utilisateur INT,
   id_playlist INT,
   PRIMARY KEY(id_utilisateur, id_playlist),
   FOREIGN KEY(id_utilisateur) REFERENCES Utilisateur(id_utilisateur),
   FOREIGN KEY(id_playlist) REFERENCES Playlist(id_playlist)
);

DROP TABLE IF EXISTS Est_composé_d_une;
CREATE TABLE Est_composé_d_une(
   id_playlist INT,
   id_fichier INT,
   PRIMARY KEY(id_playlist, id_fichier),
   FOREIGN KEY(id_playlist) REFERENCES Playlist(id_playlist),
   FOREIGN KEY(id_fichier) REFERENCES Fichier(id_fichier)
);

DROP TABLE IF EXISTS planifie_une;)
);

DROP TABLE IF EXISTS Travaille_ensemble;
CREATE TABLE Travaille_ensemble(
   id_utilisateur INT,
   id_organisation INT,
   PRIMARY KEY(id_utilisateur, id_organisation),
   FOREIGN KEY(id_utilisateur) REFERENCES Utilisateur(id_utilisateur),
   FOREIGN KEY(id_organisation) REFERENCES Organisation(id_organisation)
);