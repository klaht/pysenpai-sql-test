SELECT name 
-- Testing with a single line comment
FROM Artist 
-- Another comment
/*
	Multiline
*/
WHERE artistId IN (SELECT artistId FROM ArtWork WHERE type == 'painting') ORDER BY name ASC;
