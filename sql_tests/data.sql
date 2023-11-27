CREATE TABLE Artist(  
artistId INTEGER PRIMARY KEY,
name VARCHAR (50) NOT NULL,
yearBorn DATE,
yearDied DATE,
nationality VARCHAR(50),
birthplace VARCHAR(50));

CREATE TABLE Location(
locationId INTEGER PRIMARY KEY,
name VARCHAR (50) NOT NULL,
city VARCHAR(50),
country VARCHAR(50),
locationType VARCHAR(50));

CREATE TABLE Collection(
collectionId INTEGER PRIMARY KEY,
name VARCHAR (50) NOT NULL,
description VARCHAR(250),
locationId INTEGER REFERENCES Location(locationId),
isPrivateCollection INTEGER(1) NOT NULL);

CREATE TABLE ArtWork(
artworkId INTEGER PRIMARY KEY,
title VARCHAR(60) NOT NULL,
year VARCHAR(4),
price DECIMAL(30,2),
type VARCHAR(50),
material VARCHAR(50),
artistId INTEGER REFERENCES Artist(artistId),
collectionId INTEGER REFERENCES Collection(collectionId),
original_artworkId INTEGER REFERENCES ArtWork(artworkId)
);

CREATE TABLE Exhibition (
ExhibitionId INTEGER PRIMARY KEY,
title VARCHAR(100) NOT NULL,
startDate DATE,
endDate DATE,
isOnlineExhibition INTEGER(1) NOT NULL,
numberOfVisitors INTEGER,
numberOfOnlineVisitors INTEGER,
locationId INTEGER references Location(locationId));

CREATE TABLE On_Exhibition (
artworkId INTEGER REFERENCES Artwork(artworkId),
exhibitionId INTEGER REFERENCES Exhibition(exhibitionId),
numberOfLikes INTEGER,
numberOfOnlineLikes INTEGER,
PRIMARY KEY(artworkId, exhibitionId));

INSERT INTO Location VALUES(1, 'Ataneum Art Museum', 'Helsinki', 'Finland','museum');
INSERT INTO Location VALUES(2, 'Museum of Contemporary Art Kiasma', 'Helsinki', 'Finland','museum');
INSERT INTO Location VALUES(3, 'Oulu Museum of Art', 'Oulu', 'Finland','museum');
INSERT INTO Location VALUES(4, 'Rubens House', 'Antwerp', 'Belgium','museum');
INSERT INTO Location VALUES(5, 'Van Gogh Museum', 'Amsterdam', 'Netherlands','museum');
INSERT INTO Location VALUES(6, 'Louvre', 'Paris', 'France','museum');
INSERT INTO Location VALUES(7, 'Tate Modern', 'London', 'United Kingdom','museum');
INSERT INTO Location VALUES(8, 'Guggenheim Museum', 'Bilbao', 'Portugal','museum');
INSERT INTO Location VALUES(9, 'The Gemäldegalerie', 'Berlin', 'Germany','museum');
INSERT INTO Location VALUES(10, 'Prado National Museum', 'Madrid', 'Spain','museum');
INSERT INTO Location VALUES(11, 'The National Gallery', 'London', 'United Kingdom','museum');
INSERT INTO Location VALUES(12, 'The Hermitage', 'St. Petersburg', 'Russia','museum');
INSERT INTO Location VALUES(13, 'The National Museum', 'Oslo', 'Norway','museum');
INSERT INTO Location VALUES(14, 'The Gothenburg Museum of Art', 'Gothenburg', 'Sweden','museum');
INSERT INTO Location VALUES(15, 'MoMA - Museum of Modern Art', 'New York', 'USA','museum');
INSERT INTO Location VALUES(16, 'Helsinki Contemporary', 'Helsinki', 'Finland','art gallery');

INSERT INTO Collection VALUES(1, 'Finnish National Gallery Collection', 'Work of art, archival materials and artefacts', null, 0);
INSERT INTO Collection VALUES(2, 'Collection of the Oulu Museum of Art', 'Artwork from Oulu and Northern Ostrobothnia, also artworks from Finnish artists in general', 3, 0);
INSERT INTO Collection VALUES(3, 'Norwegian National Museum Collection', 'Older and modern art, contemporary art, architecture and design', 13, 0);
INSERT INTO Collection VALUES(4, 'City of Oulu Collection', '2000 artworks including paintings and sculptures covering different styles and techniques', 3, 0);
INSERT INTO Collection VALUES(5, 'Tate Museum Collection', null, 7, 0);
INSERT INTO Collection VALUES(6, 'Hermitage Museum Collection', null, 7, 0);
INSERT INTO Collection VALUES(7, 'MoMA Art Collection', null, 15, 0);
INSERT INTO Collection VALUES(8, 'The Hour of The Wolf', 'Selected work by Jarmo Mäkilä', null, 1);

INSERT INTO Artist VALUES(1, 'Edvard Munch', '1863', '1944','Norway', 'Loten');
INSERT INTO Artist VALUES(2, 'Vilho Lampi', '1898', '1936','Finland', 'Oulu');
INSERT INTO Artist VALUES(3, 'Elin Danielson-Gambogi', '1861', '1919','Finland', 'Noormarkku');
INSERT INTO Artist VALUES(4, 'Ivan Aivazovski', '1817', '1900','Russia', 'Feodosia');
INSERT INTO Artist VALUES(7, 'Claude Monet', '1840', '1926','France', 'Paris');
INSERT INTO Artist VALUES(5, 'Wassily Kandinsky', '1866', '1944','Russia', 'Moscow');
INSERT INTO Artist VALUES(6, 'Joan Miro', '1893', '1983','Spain', 'Barcelona');
INSERT INTO Artist VALUES(8, 'Salvador Dali', '1904', '1989','Spain', 'Figueres');
INSERT INTO Artist VALUES(9, 'Isak Wacklin', '1720', '1758','Finland', 'Oulu');
INSERT INTO Artist VALUES(10, 'Eeva-Riitta Eerola', '1980', null, 'Finland', 'Siilinjärvi');
INSERT INTO Artist VALUES(11, 'Jari Silomäki', '1975', null, 'Finland', 'Parkano');
INSERT INTO Artist VALUES(12, 'Hannaleena Hesika', '1973', null, 'Finland', 'Oulu');
INSERT INTO Artist VALUES(13, 'Miikka Vaskola', '1975', null, 'Finland', 'Helsinki');
INSERT INTO Artist VALUES(14, 'Helena Hietanen', '1963', null, 'Finland', 'Helsinki');
INSERT INTO Artist VALUES(15, 'Johanna Havimäki', '1978', null, 'Finland', 'Kuru');
INSERT INTO Artist VALUES(16, 'Jarmo Mäkilä', '1952', null, 'Finland', 'Rauma');

INSERT INTO Artwork VALUES(1001, 'Scream', '1983', null, 'drawing', 'pastel on cardboard', 1, null, null);
INSERT INTO Artwork VALUES(1002, 'Scream', '1983', null, 'painting', 'oil, tempera and pastel on cardboard', 1, 3, 1001);
INSERT INTO Artwork VALUES(1003, 'Scream', '1985', 120000000, 'drawing', 'pastel on cardboard', 1, 3, 1001);
INSERT INTO Artwork VALUES(1004, 'The Sick Child', '1984', 750000, 'painting', 'drypoint on paper',1, 3, null);
INSERT INTO Artwork VALUES(1005, 'The Sick Child', '1986', 500000, 'painting', 'oil on canvas', 1, 3, 1004);
INSERT INTO Artwork VALUES(1006, 'The Sick Child', '1907', null, 'painting', 'oil on canvas', 1, null, 1004);
INSERT INTO Artwork VALUES(1007, 'The Sick Child', '1925', 500000, 'painting', 'oil on canvas', 1, 5, 1004);

INSERT INTO Artwork VALUES(2001, 'Bridge dances', '1933', 34000, 'painting', 'oil on canvas',2, 2, null);
INSERT INTO Artwork VALUES(2002, 'Self-portrait', '1934', 14000, 'painting', 'oil on canvas', 2, 2, null);
INSERT INTO Artwork VALUES(2003, 'At the Mothers Grave', '1935', 900000, 'painting', 'oil on canvas',2, 2, null);

INSERT INTO Artwork VALUES(3001, 'Sisters', '1891', 43000,  'painting', 'oil on canvas', 3, null, null);
INSERT INTO Artwork VALUES(3002, 'La Merenda', '1904', 140000, 'painting', 'oil on canvas', 3, null, null);
INSERT INTO Artwork VALUES(3003, 'Sisters', '1891', 12000,  'drawing', 'charcoal', 3, null, 3001);

INSERT INTO Artwork VALUES(4001, 'On the Storm', '1872', 20000, 'painting', 'oil on canvas', 4, 5, null);
INSERT INTO Artwork VALUES(4002, 'The Ninth Wave', '1850', 99000, 'painting', 'oil on canvas', 4, 5, null);
INSERT INTO Artwork VALUES(4004, 'Stormy Sea at Night', '1849', 75000, 'painting', 'oil on canvas', 4, 5, null);

INSERT INTO Artwork VALUES(5001, 'Winter Landscape', '1909', 90000, 'painting', 'oil on canvas', 5, 5, null);
INSERT INTO Artwork VALUES(5002, 'Composition VI', '1913', 89000, 'painting', 'oil on canvas', 5, 5, null);

INSERT INTO Artwork VALUES(6001, 'Horse, Pipe and Red Flower', '1920', 340000, 'painting', 'oil on canvas', 6, null, null);
INSERT INTO Artwork VALUES(6002, 'Dog Barking at the Moon', '1926', 19000, 'painting', 'oil on canvas', 6, null, null);
INSERT INTO Artwork VALUES(6003, 'Dona i Ocell', '1982', null, 'sculpture', null, 6, null, null);

INSERT INTO Artwork VALUES(7001, 'Woman with a Umbrella', '1875', 1115000, 'painting', 'oil on canvas', 6, null, null);
INSERT INTO Artwork VALUES(7002, 'San Giorgio Maggiore at Dusk', '1908', 1078000, 'painting', 'oil on canvas', 6, null, null);
INSERT INTO Artwork VALUES(7004, 'Water Lilies', '1919', 1000000, 'painting', 'oil on canvas', 6, null, null);

INSERT INTO Artwork VALUES(8001, 'The persistence of Memory', '1931', 1780000, 'painting', 'oil on canvas', 8, 7, null);

INSERT INTO Artwork VALUES(9001, 'Dorothea Maria Losch', '1755', null, 'painting', 'oil on canvas', 9, 1, null); 
INSERT INTO Artwork VALUES(9002, 'Mrs. Heckford', '1757', null, 'painting', 'oil on canvas', 9, 1, null); 

INSERT INTO Artwork VALUES(10001, 'Act I', '2021', null, 'painting', 'oil on canvas',  10, null, null);
INSERT INTO Artwork VALUES(10002, 'Passage VI', '2021', null, 'painting', 'oil on canvas',  10, null, null);

INSERT INTO Artwork VALUES(12001, 'Stargazer', '2007', null, 'painting', 'oil on canvas',  12, null, null);
INSERT INTO Artwork VALUES(12002, 'Camouflage XXV', '2019', null, 'drawing', 'pastel',12, null, null);
INSERT INTO Artwork VALUES(12003, 'Ridestar', '2010', null, 'film', 'film',12, null, null);

INSERT INTO Artwork VALUES(13001, 'Wishlist', '2022', null, 'drawing', 'charcoal',  13, null, null);
INSERT INTO Artwork VALUES(13002, 'Another', '2015', null, 'painting', 'oil on canvas',  13, null, null);
INSERT INTO Artwork VALUES(13003, 'Instar IV', '2020', null, 'sculpture', 'plaster, wood and epoxy', 13, null, null);

INSERT INTO Artwork VALUES(14001, 'Nubes Tall SCulpture', '2022', null, 'sculpture', null, 14, null, null);

INSERT INTO Artwork VALUES(16001, 'Head Root', '2019', 55000, 'sculpture', null, 16, 8, null);
INSERT INTO Artwork VALUES(16002, 'Lord of the flies II', '2013', 2500, 'sculpture', null, 16,  8, null);
INSERT INTO Artwork VALUES(16003, 'Waiting For Christmas', '2012', 7500, 'painting', null, 16, 8, null);
INSERT INTO Artwork VALUES(16004, 'Jump', '2013', 5000, 'sculpture', null, 16 , 8, null);

INSERT INTO Exhibition VALUES(1, 'Finish Artists 2021', '2021-12-01', '2021-05-01', 1, 5598, 35432, 3);
INSERT INTO Exhibition VALUES(2, 'Nordic Artists', '2001-06-01', '2001-09-10', 0, 10077, 0, 11);
INSERT INTO Exhibition VALUES(3, 'Russia', '2001-11-01', '2002-05-15', 1, 43025, 54068, 1);
INSERT INTO Exhibition VALUES(4, 'Humans and nature', '2002-09-01', '2002-12-31', 0, 564089, 0, 7);
INSERT INTO Exhibition VALUES(5, 'Finish Artists 2022', '2022-01-15', '2022-06-31', 1, 15089, 10347, 3);
INSERT INTO Exhibition VALUES(6, 'Finish Artists 2000', '2020-05-07', '2020-09-30', 1, 1206, 25031, 3);
INSERT INTO Exhibition VALUES(7, 'Van Gogh in the Summer', '2022-05-07', '2022-08-31', 1, 205069, 3425031, 5);
INSERT INTO Exhibition VALUES(8, 'Lust For Life', '2022-09-09', '2022-12-31', 1, 12765, 25064, 16);
INSERT INTO Exhibition VALUES(9, 'Beyond', '2018-02-09', '2018-03-30', 1, 1567, 10574, 16);
INSERT INTO Exhibition VALUES(10, 'Locus', '2022-01-07', '2022-01-30', 1, 7832, 50574, 16);
INSERT INTO Exhibition VALUES(11, 'Navigating North', '2022-10-07', '2023-04-02', 1, null, null, 2);
INSERT INTO Exhibition VALUES(12, 'Another Exhibition in Kiasma', '2022-10-07', '2023-04-02', 1, null, null, 2);
INSERT INTO Exhibition VALUES(13, 'Navigating North', '2022-05-07', '2022-08-02', 1, null, null, 2);


INSERT INTO On_Exhibition VALUES(2001, 1, 10050, 20040);
INSERT INTO On_Exhibition VALUES(2002, 1, 10060, 20080);
INSERT INTO On_Exhibition VALUES(9001, 1, 10070, 20090);
INSERT INTO On_Exhibition VALUES(9002, 1, 10080, 20010);
INSERT INTO On_Exhibition VALUES(3001, 1, 15003, 25064);

INSERT INTO On_Exhibition VALUES(1001, 2, 10050, 0);
INSERT INTO On_Exhibition VALUES(1002, 2, 10060, 0);
INSERT INTO On_Exhibition VALUES(9001, 2, 10075, 0);
INSERT INTO On_Exhibition VALUES(9002, 2, 10086, 0);

INSERT INTO On_Exhibition VALUES(4001, 3, 100501, 200406);
INSERT INTO On_Exhibition VALUES(4002, 3, 100602, 200808);
INSERT INTO On_Exhibition VALUES(4004, 3, 10603, 28088);
INSERT INTO On_Exhibition VALUES(5001, 3, 100532, 200103);
INSERT INTO On_Exhibition VALUES(5002, 3, 10584, 300501);

INSERT INTO On_Exhibition VALUES(1006, 4, 100501, 0);
INSERT INTO On_Exhibition VALUES(1007, 4, 100602, 0);

INSERT INTO On_Exhibition VALUES(2001, 5, 10050, 20040);
INSERT INTO On_Exhibition VALUES(2003, 5, 10060, 20080);
INSERT INTO On_Exhibition VALUES(9001, 5, 10070, 20090);
INSERT INTO On_Exhibition VALUES(3002, 5, 2302, 5673);

INSERT INTO On_Exhibition VALUES(2002, 6, 1, 20040);
INSERT INTO On_Exhibition VALUES(2003, 6, 1, 20080);
INSERT INTO On_Exhibition VALUES(9002, 6, 1, 20090);
INSERT INTO On_Exhibition VALUES(3001, 6, 2302, 5673);
INSERT INTO On_Exhibition VALUES(3002, 6, 2302, 5673);

INSERT INTO On_Exhibition VALUES(5001, 7, 232302, 565673);
INSERT INTO On_Exhibition VALUES(5002, 7, 122302, 985673);

INSERT INTO On_Exhibition VALUES(12001, 8, 2387, 9346);
INSERT INTO On_Exhibition VALUES(12002, 8, 8972, 9375);
INSERT INTO On_Exhibition VALUES(13001, 8, 1274, 12890);
INSERT INTO On_Exhibition VALUES(13002, 8, 9375, 8753);

INSERT INTO On_Exhibition VALUES(13001, 9, 654, 2345);
INSERT INTO On_Exhibition VALUES(13002, 9, 132, 5318);
INSERT INTO On_Exhibition VALUES(13003, 9, 453, 4290);

INSERT INTO On_Exhibition VALUES(10001, 10, 1874, 19554);
INSERT INTO On_Exhibition VALUES(10002, 10, 2099, 43211);

INSERT INTO Artist(name, yearBorn, nationality, birthplace) VALUES('Juuso Noronkoski', '1983', 'Finland', 'Helsinki');
INSERT INTO Artist(name, yearBorn, yearDied, nationality, birthplace) VALUES('Ellen Thesleff', '1869', '1954', 'Finland', 'Helsinki');
INSERT INTO Artist(name, yearBorn, yearDied, nationality, birthplace) VALUES('Akseli Gallen-Kallela', '1869', '1931', 'Finland', 'Helsinki');
INSERT INTO Artist(name, yearBorn, yearDied, nationality, birthplace) VALUES('Helen Schjerfbeck', '1862', '1946', 'Finland', 'Helsinki');