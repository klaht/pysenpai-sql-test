SELECT title, startDate, endDate, numberofvisitors, name, city, country FROM exhibition, location WHERE numberofvisitors NOT NULL AND location.locationid == exhibition.locationid ORDER BY numberofvisitors DESC;