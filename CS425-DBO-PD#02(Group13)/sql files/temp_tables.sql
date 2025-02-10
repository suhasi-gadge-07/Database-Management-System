-- DROP TEMPORARY TABLE temp_pub_count_by_conference
CREATE TEMPORARY TABLE temp_pub_count_by_conference AS
SELECT conference_ID, COUNT(*) AS pub_count
FROM Publications
GROUP BY conference_ID;

SELECT *
FROM temp_pub_count_by_conference
WHERE pub_count < 2;


CREATE TEMPORARY TABLE temp_active_users AS
SELECT u.user_ID, u.user_name, i.inst_name
FROM Users u
JOIN Members m ON u.user_ID = m.user_ID
JOIN Institutions i ON m.institution_ID = i.institution_ID
WHERE u.sub_status = 'Active';

SELECT *
FROM temp_active_users
WHERE inst_name = 'Georgia Institute of Technology';



CREATE TEMPORARY TABLE temp_authors_metrics AS
SELECT a.author_ID, a.author_name, COUNT(pa.publication_ID) AS num_publications, 
       SUM(c.citation_count) AS total_citations
FROM Authors a
JOIN Pub_Author pa ON a.author_ID = pa.author_ID
JOIN Pub_Cite pc ON pa.publication_ID = pc.publication_ID
JOIN Citations c ON pc.citation_ID = c.citation_ID
GROUP BY a.author_ID, a.author_name;

SELECT author_name, num_publications, total_citations
FROM temp_authors_metrics
WHERE num_publications < 100 OR total_citations > 1000;



CREATE TEMPORARY TABLE temp_keyword_pub_count AS
SELECT k.keyword, COUNT(pk.publication_ID) AS pub_count
FROM Keywords k
JOIN Pub_Key pk ON k.keyword_ID = pk.keyword_ID
GROUP BY k.keyword;

SELECT keyword, pub_count
FROM temp_keyword_pub_count
WHERE pub_count > 1;



CREATE TEMPORARY TABLE temp_top_cited_pubs AS
SELECT p.publication_ID, p.paper_name, c.citation_count
FROM Publications p
JOIN Pub_Cite pc ON p.publication_ID = pc.publication_ID
JOIN Citations c ON pc.citation_ID = c.citation_ID
WHERE c.citation_count > 10;

SELECT t.publication_ID, t.paper_name, t.citation_count
FROM temp_top_cited_pubs t
JOIN Publications p ON t.publication_ID = p.publication_ID
WHERE p.publisher = 'IEEE';



CREATE TEMPORARY TABLE temp_authors_by_topic AS
SELECT a.author_ID, a.author_name, t.topic_name
FROM Authors a
JOIN Topics t ON a.topic_ID = t.topic_ID;

SELECT author_name, topic_name
FROM temp_authors_by_topic
WHERE topic_name = 'Bioengineering';



CREATE TEMPORARY TABLE temp_conference_participation AS
SELECT c.conference_year, COUNT(p.publication_ID) AS num_publications
FROM Conferences c
JOIN Publications p ON c.conference_ID = p.conference_ID
GROUP BY c.conference_year;

SELECT conference_year, num_publications
FROM temp_conference_participation
WHERE conference_year > 2020;
