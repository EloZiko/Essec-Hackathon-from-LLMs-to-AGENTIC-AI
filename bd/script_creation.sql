CREATE TABLE Client (
   id_Client INT AUTO_INCREMENT,
   prenom VARCHAR(50) NOT NULL,
   date_de_naissance DATE NOT NULL,
   nom_client VARCHAR(50) NOT NULL,
   PRIMARY KEY(id_Client)
);

CREATE TABLE Passion (
   id_passion INT AUTO_INCREMENT,
   nom_passion VARCHAR(50) NOT NULL,
   PRIMARY KEY(id_passion)
);

CREATE TABLE type_activité (
   nom_type_activité VARCHAR(50),
   PRIMARY KEY(nom_type_activité)
);

CREATE TABLE Activites (
   id_Activites INT AUTO_INCREMENT,
   adresse TEXT NOT NULL,
   nom_lieu VARCHAR(50) NOT NULL,
   type_activité VARCHAR(50) NOT NULL,
   nom_type_activité VARCHAR(50) NOT NULL,
   PRIMARY KEY(id_Activites),
   FOREIGN KEY(nom_type_activité) REFERENCES type_activité(nom_type_activité)
);

CREATE TABLE est_catégorisé (
   id_Activites INT,
   id_passion INT,
   PRIMARY KEY(id_Activites, id_passion),
   FOREIGN KEY(id_Activites) REFERENCES Activites(id_Activites),
   FOREIGN KEY(id_passion) REFERENCES Passion(id_passion)
);

CREATE TABLE a_fait (
   id_Client INT,
   id_Activites INT,
   note TINYINT NOT NULL,
   commentaire TEXT NOT NULL,
   PRIMARY KEY(id_Client, id_Activites),
   FOREIGN KEY(id_Client) REFERENCES Client(id_Client),
   FOREIGN KEY(id_Activites) REFERENCES Activites(id_Activites)
);

CREATE TABLE aime (
   id_Client INT,
   id_passion INT,
   PRIMARY KEY(id_Client, id_passion),
   FOREIGN KEY(id_Client) REFERENCES Client(id_Client),
   FOREIGN KEY(id_passion) REFERENCES Passion(id_passion)
);

