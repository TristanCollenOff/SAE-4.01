DROP TABLE IF EXISTS affilier;
DROP TABLE IF EXISTS Contenir;
DROP TABLE IF EXISTS connexion;
DROP TABLE IF EXISTS planification;
DROP TABLE IF EXISTS fichier;
DROP TABLE IF EXISTS lecteur;
DROP TABLE IF EXISTS fichier_log;
DROP TABLE IF EXISTS playlist;
DROP TABLE IF EXISTS utilisateur;
DROP TABLE IF EXISTS type_fichier;
DROP TABLE IF EXISTS role;
DROP TABLE IF EXISTS organisation;

CREATE TABLE organisation(
   id_organisation INTEGER PRIMARY KEY,
   nom_organisation VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE role(
   nom_role VARCHAR(50) PRIMARY KEY,
   description TEXT
);

CREATE TABLE type_fichier(
   type_fichier VARCHAR(50) PRIMARY KEY
);

CREATE TABLE utilisateur(
   id_utilisateur INTEGER UNIQUE NOT NULL,
   nom_utilisateur VARCHAR(50) UNIQUE NOT NULL,
   motdepasse VARCHAR(50) NOT NULL,
   prenom VARCHAR(50) NOT NULL,
   nom VARCHAR(50) NOT NULL,
   email VARCHAR(100) UNIQUE NOT NULL,
   nom_role VARCHAR(50) NOT NULL,
   FOREIGN KEY(nom_role) REFERENCES role(nom_role)
);

CREATE TABLE playlist(
   id_playlist INTEGER PRIMARY KEY,
   nom_playlist VARCHAR(50) UNIQUE NOT NULL,
   date_creation DATE NOT NULL,
   date_fin_playlist DATE NOT NULL,
   date_derniere_maj DATE NOT NULL,
   publie INTEGER NOT NULL,
   id_organisation INTEGER NOT NULL,
   FOREIGN KEY(id_organisation) REFERENCES organisation(id_organisation)
);

CREATE TABLE planification(
   id_planification INTEGER PRIMARY KEY,
   heure_debut TIME NOT NULL,
   heure_fin TIME NOT NULL,
   date_ DATE NOT NULL,
   id_playlist INT NOT NULL,
   FOREIGN KEY(id_playlist) REFERENCES playlist(id_playlist)
);

CREATE TABLE fichier_log(
   id_log INTEGER PRIMARY KEY,
   type_action VARCHAR(50) NOT NULL,
   message VARCHAR(50) NOT NULL,
   date_fichierlog DATE NOT NULL,
   id_organisation INT NOT NULL,
   FOREIGN KEY(id_organisation) REFERENCES organisation(id_organisation)
);

CREATE TABLE lecteur(
   id_lecteur INTEGER PRIMARY KEY,
   nom_lecteur VARCHAR(50) UNIQUE NOT NULL,
   adresseIP VARCHAR(50) UNIQUE NOT NULL,
   etat_lecteur VARCHAR(50) NOT NULL,
   emplacement VARCHAR(50) NOT NULL,
   derniere_synchro DATE NOT NULL,
   adresse_lecteur VARCHAR(50) NOT NULL,
   alerte INTEGER NOT NULL,
   id_organisation INTEGER NOT NULL,
   FOREIGN KEY(id_organisation) REFERENCES organisation(id_organisation)
);

CREATE TABLE fichier(
   id_fichier INTEGER PRIMARY KEY,
   nom VARCHAR(50) UNIQUE NOT NULL,
   chemin VARCHAR(50) NOT NULL,
   duree_fichier INTEGER NOT NULL,
   date_maj DATE NOT NULL,
   type_fichier VARCHAR(50) NOT NULL,
   FOREIGN KEY(type_fichier) REFERENCES type_fichier(type_fichier)
);

CREATE TABLE connexion(
   id_utilisateur INTEGER PRIMARY KEY,
   login_attempts INTEGER,
   block_until DATE,
   last_login DATE,
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
);

CREATE TABLE Contenir(
   id_playlist INTEGER,
   id_fichier INTEGER,
   PRIMARY KEY(id_playlist, id_fichier),
   FOREIGN KEY(id_playlist) REFERENCES playlist(id_playlist),
   FOREIGN KEY(id_fichier) REFERENCES fichier(id_fichier)
);

CREATE TABLE affilier(
   id_utilisateur INTEGER,
   id_organisation INTEGER,
   PRIMARY KEY(id_utilisateur, id_organisation),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(id_organisation) REFERENCES organisation(id_organisation)
);
