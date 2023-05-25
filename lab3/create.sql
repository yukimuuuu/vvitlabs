CREATE TABLE cafedra (id SERIAL PRIMARY KEY, nazvanie varchar NOT NULL, decanat varchar NOT NULL);
CREATE TABLE gruppa (id SERIAL PRIMARY KEY, nazvanie varchar NOT NULL, cafedra_id integer REFERENCES cafedra(id));
CREATE TABLE student (id SERIAL PRIMARY KEY, imya varchar NOT NULL, passport varchar NOT NULL, gruppa_id integer REFERENCES student(id));

VALUES 
(1, 'MathAn', 'IT'),
(2, 'Electr','RaT');
INSERT INTO gruppa
VALUES 
(1, 'BVT2202', 1),
(2, 'BVT2203', 1),
(3, 'BCT21', 2),
(4, 'BRT21', 2);
INSERT INTO student
VALUES 
(1, 'Artyom', '483742', 1),
(2, 'Kirill', '423244', 1),
(3, 'Roman', '645454', 1),
(4, 'Alexandr', '435323', 1),
(5, 'Andrey', '324421', 2),
(6, 'Anatoliy', '853485', 2),
(7, 'Nijika', '786542', 2),
(8, 'Hitori', '234248', 2),
(9, 'Ayaka', '958385', 3),
(10, 'Ayato', '535379', 3),
(11, 'Jennie', '809864', 3),
(12, 'Jisoo', '835834', 3),
(13, 'Wonyoung', '234424', 4),
(14, 'Itadori', '870535', 4),
(15, 'Tanjiro', '213147', 4),
(16, 'Kitagawa', '958472', 4);
