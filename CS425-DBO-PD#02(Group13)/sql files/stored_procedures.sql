DELIMITER //
CREATE PROCEDURE add_user(
    IN p_user_ID VARCHAR(10),
    IN p_user_name VARCHAR(100),
    IN p_user_email VARCHAR(100),
    IN p_user_contact_no VARCHAR(15),
    IN p_sub_status VARCHAR(10),
    IN p_subscription VARCHAR(20),
    IN p_profession VARCHAR(50)
)
BEGIN
    -- Validate subscription type
    IF p_subscription NOT IN ('Basic', 'Premium', 'None') THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid subscription type.';
    ELSE
        -- Insert new user if the subscription is valid
        INSERT INTO Users (user_ID, user_name, user_email, user_contact_no, sub_status, subscription, profession)
        VALUES (p_user_ID, p_user_name, p_user_email, p_user_contact_no, p_sub_status, p_subscription, p_profession);
    END IF;
END//
DELIMITER ;

-- CALL add_user('USR031', 'Alice Brown', 'alice.brown@example.com', '1234567890', 'Active', 'Premium', 'Researcher');


DELIMITER //
CREATE PROCEDURE add_publication(
    IN p_publication_ID VARCHAR(10),
    IN p_paper_name VARCHAR(255),
    IN p_publisher VARCHAR(100),
    IN p_DOI VARCHAR(50),
    IN p_print_ISSN VARCHAR(15),
    IN p_print_ISBN VARCHAR(20),
    IN p_conference_ID VARCHAR(10),
    IN p_date_of_publication DATE
)
BEGIN
    -- If the publication date is NULL, use the current date
    IF p_date_of_publication IS NULL THEN
        SET p_date_of_publication = CURDATE();
    END IF;

    -- Insert the new publication
    INSERT INTO Publications (publication_ID, paper_name, publisher, DOI, print_ISSN, print_ISBN, conference_ID, date_of_publication)
    VALUES (p_publication_ID, p_paper_name, p_publisher, p_DOI, p_print_ISSN, p_print_ISBN, p_conference_ID, p_date_of_publication);
END//
DELIMITER ;

-- CALL add_publication('PUB038', 'Photonics and Optoelectronics', 'Springer', '10.123/123', '5678-9101', '978-1-234567-9-0', 'CONF002', NULL);



DELIMITER //
CREATE PROCEDURE add_citation(
    IN p_citation_ID VARCHAR(10),
    IN p_citing_pub VARCHAR(255),
    IN p_cited_pub VARCHAR(255),
    IN p_cited_paper_links VARCHAR(255)
)
BEGIN
    -- Insert the citation
    INSERT INTO Citations (citation_ID, citing_pub, cited_pub, cited_paper_links)
    VALUES (p_citation_ID, p_citing_pub, p_cited_pub, p_cited_paper_links);

    -- Update the citation count for the cited publication
    UPDATE Publications
    SET citation_count = citation_count + 1
    WHERE paper_name = p_cited_pub;
END//
DELIMITER ;

-- CALL add_citation('CIT023', 'Wireless Networking in IoT', 'Photonics and Optoelectronics', 'http://example.com/paper');

DELIMITER //

CREATE PROCEDURE get_author_metrics(
    IN p_author_ID VARCHAR(10)
)
BEGIN
    -- Retrieve the author's metrics
    SELECT a.author_name, COUNT(pa.publication_ID) AS num_publications, 
           SUM(c.citation_count) AS total_citations
    FROM Authors a
    JOIN Pub_Author pa ON a.author_ID = pa.author_ID
    JOIN Pub_Cite pc ON pa.publication_ID = pc.publication_ID
    JOIN Citations c ON pc.citation_ID = c.citation_ID
    WHERE a.author_ID = p_author_ID
    GROUP BY a.author_name;
END//

DELIMITER ;

-- CALL get_author_metrics('AUTH002');

DELIMITER //

CREATE PROCEDURE get_popular_keywords(
    IN p_min_publications INT
)
BEGIN
    -- Retrieve keywords with more than a certain number of publications
    SELECT k.keyword, COUNT(pk.publication_ID) AS num_publications
    FROM Keywords k
    JOIN Pub_Key pk ON k.keyword_ID = pk.keyword_ID
    GROUP BY k.keyword
    HAVING num_publications > p_min_publications
    ORDER BY num_publications DESC;
END//

DELIMITER ;

-- CALL get_popular_keywords(2);


DELIMITER //

CREATE PROCEDURE get_conference_publications(
    IN p_conference_ID VARCHAR(10)
)
BEGIN
    -- Retrieve all publications for the given conference
    SELECT p.publication_ID, p.paper_name, p.publisher, p.date_of_publication
    FROM Publications p
    WHERE p.conference_ID = p_conference_ID;
END//

DELIMITER ;

-- CALL get_conference_publications('CONF001');

