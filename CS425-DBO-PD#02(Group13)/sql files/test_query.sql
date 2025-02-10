WITH institution_citation_stats AS (
    SELECT i.inst_name, 
           COUNT(DISTINCT p.publication_ID) AS total_publications,
           SUM(c.citation_count) AS total_citations,
           CASE 
               WHEN COUNT(DISTINCT p.publication_ID) > 0 
               THEN SUM(c.citation_count) / COUNT(DISTINCT p.publication_ID)
               ELSE 0 
           END AS avg_citation_per_publication
    FROM Institutions i
    JOIN Authors a ON i.institution_ID = a.institution_ID
    JOIN Pub_Author pa ON a.author_ID = pa.author_ID
    JOIN Publications p ON pa.publication_ID = p.publication_ID
    JOIN Pub_Cite pc ON p.publication_ID = pc.publication_ID
    JOIN Citations c ON pc.citation_ID = c.citation_ID
    GROUP BY i.inst_name
)
SELECT inst_name, total_publications, total_citations, avg_citation_per_publication
FROM institution_citation_stats
ORDER BY avg_citation_per_publication DESC
LIMIT 10;


