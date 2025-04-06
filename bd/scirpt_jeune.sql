-- 🔸 Nouveaux Clients (jeunes adultes)
INSERT INTO Client (prenom, date_de_naissance, nom_client)
VALUES 
('Emma', '2003-08-12', 'Lemoine'),
('Lucas', '2000-04-25', 'Martin'),
('Chloé', '2001-11-05', 'Dubois');

-- 🔸 Nouvelles passions (jeunes adultes)
INSERT INTO Passion (nom_passion)
VALUES 
('Jeux vidéo'),
('Escape Game'),
('Café Chill');

-- 🔸 Nouveau type_activité si nécessaire
INSERT INTO type_activité (nom_type_activité)
VALUES 
('Divertissement');

-- 🔸 Nouvelles Activités
INSERT INTO Activites (adresse, nom_lieu, type_activité, nom_type_activité)
VALUES 
('15 Rue de la Liberté', 'Gaming Café Pixel', 'Jeux vidéo', 'Divertissement'),
('8 Place des Énigmes', 'Escape Room Orsay', 'Escape Game', 'Divertissement'),
('22 Avenue Relax', 'Café Cosy Chill', 'Boissons & Jeux de société', 'Divertissement');

-- 🔸 est_catégorisé : lien entre activités et passions
INSERT INTO est_catégorisé (id_Activites, id_passion)
VALUES 
(4, 5), -- Gaming Café - Jeux vidéo
(5, 6), -- Escape Room - Escape Game
(6, 7); -- Café Chill - Café Chill

-- 🔸 a_fait : les jeunes adultes ont fait les activités
INSERT INTO a_fait (id_Client, id_Activites, note, commentaire)
VALUES 
(4, 4, 9, 'J’ai adoré l’ambiance rétro du gaming café !'),
(5, 5, 10, 'Escape Game hyper immersif ! On a fini juste à temps.'),
(6, 6, 8, 'Parfait pour se détendre entre amis.');

-- 🔸 aime : les jeunes adultes aiment leurs passions
INSERT INTO aime (id_Client, id_passion)
VALUES 
(4, 5), -- Emma aime Jeux vidéo
(5, 6), -- Lucas aime Escape Game
(6, 7); -- Chloé aime Café Chill
