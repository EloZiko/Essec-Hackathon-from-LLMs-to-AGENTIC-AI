-- Insertion dans la table Client
INSERT INTO Client (prenom, date_de_naissance, nom_client)
VALUES 
('John', '1990-05-15', 'Doe'),
('Alice', '1985-03-22', 'Smith'),
('Bob', '1992-07-10', 'Brown');

-- Insertion dans la table Passion
INSERT INTO Passion (nom_passion)
VALUES 
('Football'),
('Basketball'),
('Cyclisme'),
('Lecture');

-- Insertion dans la table type_activité
INSERT INTO type_activité (nom_type_activité)
VALUES 
('Sport'),
('Culture'),
('Loisirs');

-- Insertion dans la table Activites
INSERT INTO Activites (adresse, nom_lieu, type_activité, nom_type_activité)
VALUES 
('123 Rue Sportive', 'Stade Olympique', 'Football', 'Sport'),
('456 Avenue Culturelle', "Musée d'Art", 'Exposition', 'Culture'),
('789 Boulevard du Parc', 'Parc Central', 'Cyclisme', 'Loisirs');

-- Insertion dans la table est_catégorisé
INSERT INTO est_catégorisé (id_Activites, id_passion)
VALUES 
(1, 1),  -- Stade Olympique, Football
(2, 4),  -- Musée d'Art, Lecture
(3, 3);  -- Parc Central, Cyclisme

-- Insertion dans la table a_fait
INSERT INTO a_fait (id_Client, id_Activites, note, commentaire)
VALUES 
(1, 1, 8, 'Super expérience au stade, très excitant !'),
(2, 2, 9, 'Exposition impressionnante et très instructive.'),
(3, 3, 7, 'Bonne activité de cyclisme, mais un peu trop chaud ce jour-là.');

-- Insertion dans la table aime
INSERT INTO aime (id_Client, id_passion)
VALUES 
(1, 1),  -- John aime Football
(2, 4),  -- Alice aime Lecture
(3, 3);  -- Bob aime Cyclisme
