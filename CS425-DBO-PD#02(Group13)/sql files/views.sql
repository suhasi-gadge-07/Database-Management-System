CREATE VIEW active_users_contributions AS
SELECT u.user_ID, u.user_name, u.user_email, m.roles, i.inst_name, i.inst_addr
FROM Users u
JOIN Members m ON u.user_ID = m.user_ID
JOIN Institutions i ON m.institution_ID = i.institution_ID
WHERE u.sub_status = 'Active';

SELECT * FROM active_users_contributions
WHERE inst_name = 'Georgia Institute of Technology';


-- DROP VIEW high_impact_authors 
CREATE VIEW high_impact_authors AS
SELECT a.author_ID, a.author_name, COUNT(pa.publication_ID) AS num_publications, 
       SUM(c.citation_count) AS total_citations
FROM Authors a
JOIN Pub_Author pa ON a.author_ID = pa.author_ID
JOIN Pub_Cite pc ON pa.publication_ID = pc.publication_ID
JOIN Citations c ON pc.citation_ID = c.citation_ID
GROUP BY a.author_ID, a.author_name
HAVING total_citations > 50 AND num_publications > 5;

SELECT * FROM high_impact_authors
ORDER BY total_citations DESC;


CREATE VIEW popular_topics AS
SELECT t.topic_name, COUNT(p.publication_ID) AS num_publications
FROM Topics t
JOIN Authors a ON t.topic_ID = a.topic_ID
JOIN Pub_Author pa ON a.author_ID = pa.author_ID
JOIN Publications p ON pa.publication_ID = p.publication_ID
GROUP BY t.topic_name
ORDER BY num_publications DESC;

SELECT * FROM popular_topics
WHERE num_publications > 4;


-- DROP VIEW top_conferences 
CREATE VIEW top_conferences AS
SELECT c.conference_name, c.conference_year, COUNT(p.publication_ID) AS num_publications
FROM Conferences c
JOIN Publications p ON c.conference_ID = p.conference_ID
GROUP BY c.conference_name, c.conference_year
HAVING num_publications > 0
ORDER BY num_publications DESC;

SELECT * FROM top_conferences
WHERE num_publications = 1 ;


-- DROP VIEW top_cited_papers
CREATE VIEW top_cited_papers AS
SELECT p.publication_ID, p.paper_name, SUM(c.citation_count) AS total_citations
FROM Publications p
JOIN Pub_Cite pc ON p.publication_ID = pc.publication_ID
JOIN Citations c ON pc.citation_ID = c.citation_ID
GROUP BY p.publication_ID, p.paper_name
HAVING total_citations > 5 AND total_citations < 20
ORDER BY total_citations DESC;

SELECT tcp.*
FROM top_cited_papers tcp
JOIN Publications p ON tcp.publication_ID = p.publication_ID
WHERE p.conference_ID = 'CONF001';  


CREATE VIEW popular_keywords AS
SELECT k.keyword, COUNT(pk.publication_ID) AS num_publications
FROM Keywords k
JOIN Pub_Key pk ON k.keyword_ID = pk.keyword_ID
JOIN Publications p ON pk.publication_ID = p.publication_ID
GROUP BY k.keyword
ORDER BY num_publications DESC;

SELECT * FROM popular_keywords
WHERE num_publications =  1;


CREATE VIEW author_affiliations AS
SELECT a.author_ID, a.author_name, i.inst_name, aa.aff_start_date, aa.aff_end_date
FROM Authors a
JOIN Author_Affiliation aa ON a.author_ID = aa.author_ID
JOIN Institutions i ON a.institution_ID = i.institution_ID
ORDER BY a.author_name, aa.aff_start_date;

SELECT * FROM author_affiliations
WHERE author_name = 'Patrick Le Callet';

-- SELECT * FROM author_affiliations
-- WHERE inst_name = 'University College London';



SHOW FULL TABLES IN IEEE_db WHERE TABLE_TYPE = 'VIEW';
SELECT * FROM active_users_contributions;
SELECT * FROM high_impact_authors;
SELECT * FROM popular_topics;
SELECT * FROM top_conferences;
SELECT * FROM top_cited_papers;
SELECT * FROM popular_keywords;
SELECT * FROM author_affiliations;
