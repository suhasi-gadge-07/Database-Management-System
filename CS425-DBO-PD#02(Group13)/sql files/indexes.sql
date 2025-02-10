CREATE INDEX idx_publications_conference_id ON Publications(conference_ID);
EXPLAIN SELECT * FROM Publications WHERE conference_ID = 'CONF001';

CREATE INDEX idx_publications_date_of_publication ON Publications(date_of_publication);
EXPLAIN SELECT * FROM Publications WHERE date_of_publication > '2020-01-01';

SHOW INDEX FROM PUBLICATIONS;

CREATE INDEX idx_authors_institution_id ON Authors(institution_ID);
EXPLAIN SELECT * FROM Authors WHERE institution_ID = 'INST001';

CREATE INDEX idx_authors_institution_topic ON Authors(institution_ID, topic_ID);
EXPLAIN SELECT * FROM Authors WHERE institution_ID = 'INST001' AND topic_ID = 'TOP001';

SHOW INDEX FROM Authors;

CREATE INDEX idx_authors_topic_id ON Authors(topic_ID);
EXPLAIN SELECT * FROM Authors WHERE topic_ID = 'TOP001';

CREATE INDEX idx_pub_author_author_id ON Pub_Author(author_ID);
EXPLAIN SELECT * FROM Pub_Author WHERE author_ID = 'AUTH001';
SHOW INDEX FROM Pub_Author;

CREATE INDEX idx_pub_author_publication_id ON Pub_Author(publication_ID);
EXPLAIN SELECT * FROM Pub_Author WHERE publication_ID = 'PUB001';

CREATE INDEX idx_pub_key_publication_id ON Pub_Key(publication_ID);
EXPLAIN SELECT * FROM Pub_Key WHERE publication_ID = 'PUB001';
SHOW INDEX FROM Pub_Key;

CREATE INDEX idx_pub_key_keyword_id ON Pub_Key(keyword_ID);
EXPLAIN SELECT * FROM Pub_Key WHERE keyword_ID = 'KW001';

CREATE INDEX idx_citations_citation_count ON Citations(citation_count);
EXPLAIN SELECT * FROM Pub_Cite WHERE publication_ID = 'PUB001';
EXPLAIN SELECT * FROM Pub_Cite WHERE citation_ID = 'CIT001';
EXPLAIN SELECT * FROM Citations WHERE citation_count > 5;
SHOW INDEX FROM Pub_Cite;
SHOW INDEX FROM citations;


