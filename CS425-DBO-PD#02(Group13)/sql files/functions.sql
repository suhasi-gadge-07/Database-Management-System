DELIMITER //

CREATE FUNCTION get_author_total_citations(p_author_ID VARCHAR(10))
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE total_citations INT;
    
    SELECT SUM(c.citation_count)
    INTO total_citations
    FROM Pub_Author pa
    JOIN Pub_Cite pc ON pa.publication_ID = pc.publication_ID
    JOIN Citations c ON pc.citation_ID = c.citation_ID
    WHERE pa.author_ID = p_author_ID;
    
    RETURN IFNULL(total_citations, 0);  -- Return 0 if no citations exist
END//

DELIMITER ;

SELECT get_author_total_citations('AUTH003') AS total_citations;

DELIMITER //

CREATE FUNCTION validate_email_format(p_email VARCHAR(100))
RETURNS BOOLEAN
DETERMINISTIC
BEGIN
    IF p_email REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$' THEN
        RETURN TRUE;
    ELSE
        RETURN FALSE;
    END IF;
END//

DELIMITER ;

SELECT validate_email_format('nick.simpsons@example.com') AS is_valid_email;

DELIMITER //

CREATE FUNCTION calculate_age(p_birthdate DATE)
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE age INT;
    
    SET age = YEAR(CURDATE()) - YEAR(p_birthdate);
    
    IF MONTH(CURDATE()) < MONTH(p_birthdate) OR (MONTH(CURDATE()) = MONTH(p_birthdate) AND DAY(CURDATE()) < DAY(p_birthdate)) THEN
        SET age = age - 1;
    END IF;
    
    RETURN age;
END//

DELIMITER ;

SELECT calculate_age('1990-06-15') AS age;


DELIMITER //

CREATE FUNCTION get_publication_citation_count(p_publication_ID VARCHAR(10))
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE citation_count INT;
    
    SELECT citation_count INTO citation_count
    FROM Publications
    WHERE publication_ID = p_publication_ID;
    
    RETURN IFNULL(citation_count, 0);  -- Return 0 if no citations exist
END//

DELIMITER ;


SELECT get_publication_citation_count('PUB001') AS citation_count;


DELIMITER //

CREATE FUNCTION get_institution_author_count(p_institution_ID VARCHAR(10))
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE author_count INT;
    
    SELECT COUNT(*) INTO author_count
    FROM Authors
    WHERE institution_ID = p_institution_ID;
    
    RETURN author_count;
END//

DELIMITER ;

SELECT get_institution_author_count('INST001') AS author_count;


DELIMITER //

CREATE FUNCTION get_conference_publication_count(p_conference_ID VARCHAR(10))
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE publication_count INT;
    
    SELECT COUNT(*) INTO publication_count
    FROM Publications
    WHERE conference_ID = p_conference_ID;
    
    RETURN publication_count;
END//

DELIMITER ;

SELECT get_conference_publication_count('CONF001') AS publication_count;


DELIMITER //

CREATE FUNCTION get_most_popular_keyword()
RETURNS VARCHAR(100)
DETERMINISTIC
BEGIN
    DECLARE most_popular_keyword VARCHAR(100);
    
    SELECT k.keyword
    INTO most_popular_keyword
    FROM Keywords k
    JOIN Pub_Key pk ON k.keyword_ID = pk.keyword_ID
    GROUP BY k.keyword
    ORDER BY COUNT(pk.publication_ID) DESC
    LIMIT 1;
    
    RETURN most_popular_keyword;
END//

DELIMITER ;

SELECT get_most_popular_keyword() AS most_popular_keyword;

