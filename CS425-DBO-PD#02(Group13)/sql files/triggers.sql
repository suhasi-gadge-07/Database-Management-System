DELIMITER //
CREATE TRIGGER update_keyword_pub_count
AFTER INSERT ON Pub_Key
FOR EACH ROW
BEGIN
  UPDATE Keywords
  SET kw_pub_count = kw_pub_count + 1
  WHERE keyword_ID = NEW.keyword_ID;
END//
DELIMITER ;

SELECT * FROM Keywords WHERE keyword_ID = 'KW001';

SELECT * FROM Publications WHERE publication_ID = 'PUB036';
INSERT INTO Publications (publication_ID, paper_name, publisher, DOI, print_ISSN, print_ISBN, conference_ID)
VALUES ('PUB036', 'Sample Paper', 'IEEE', '10.10/123', '1234-5678', '978-1-234567-8-9', 'CONF001');

INSERT INTO Pub_Key (publication_ID, keyword_ID)
VALUES ('PUB036', 'KW001');

-- Check the updated keyword count
SELECT * FROM Keywords WHERE keyword_ID = 'KW001';


DELIMITER //
CREATE TRIGGER prevent_duplicate_email
BEFORE INSERT ON Users
FOR EACH ROW
BEGIN
  IF EXISTS (SELECT 1 FROM Users WHERE user_email = NEW.user_email) THEN
    SIGNAL SQLSTATE '45000' 
    SET MESSAGE_TEXT = 'Duplicate email not allowed.';
  END IF;
END//
DELIMITER ;


-- First insert a user with a unique email
INSERT INTO Users (user_ID, user_name, user_email, user_contact_no, sub_status, subscription, profession)
VALUES ('USR031', 'John Doe', 'john.doe@example.com', '3284108410', 'Active', 'Premium', 'Engineer');

-- Attempt to insert a duplicate email
INSERT INTO Users (user_ID, user_name, user_email, user_contact_no, sub_status, subscription, profession)
VALUES ('USR032', 'John Doe', 'john.doe@example.com', '9182374657', 'Active', 'Basic', 'Scientist');

DELIMITER //

CREATE TRIGGER validate_subscription
BEFORE INSERT ON Users
FOR EACH ROW
BEGIN
  IF NEW.subscription NOT IN ('Basic', 'Premium', 'None') THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Invalid subscription type.';
  END IF;
END//

DELIMITER ;

-- Attempt to insert a user with an invalid subscription type
INSERT INTO Users (user_ID, user_name, user_email, user_contact_no, sub_status, subscription, profession)
VALUES ('USR031', 'Alice Smith', 'alice.smith@example.com', '1872349190', 'Active', 'Gold', 'Engineer');


DELIMITER //

CREATE TRIGGER set_default_publication_date
BEFORE INSERT ON Publications
FOR EACH ROW
BEGIN
  IF NEW.date_of_publication IS NULL THEN
    SET NEW.date_of_publication = CURDATE();
  END IF;
END//

DELIMITER ;

-- Insert a publication without specifying the date_of_publication
INSERT INTO Publications (publication_ID, paper_name, publisher, DOI, print_ISSN, print_ISBN, conference_ID)
VALUES ('PUB037', 'Wireless Networking in IoT', 'IEEE', '10.10/23', '1234-5678', '97-8-1', 'CONF001');

-- Check the publication to see if the date_of_publication was set automatically
SELECT * FROM Publications WHERE publication_ID = 'PUB037';


DELIMITER //

CREATE TRIGGER prevent_negative_citations
BEFORE INSERT ON Citations
FOR EACH ROW
BEGIN
  IF NEW.citation_count < 0 THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Citation count cannot be negative.';
  END IF;
END//

DELIMITER ;

-- Try to insert a citation with a negative citation_count
INSERT INTO Citations (citation_ID, citing_pub, cited_pub, cited_paper_links, citation_count)
VALUES ('CIT022', 'Photonics and Optoelectronics', 'Cybersecurity Challenges in Healthcare', 'Another Pub', 'http://example.com', -10);


DELIMITER //

CREATE TRIGGER prevent_negative_authors
BEFORE UPDATE ON Institutions
FOR EACH ROW
BEGIN
  IF NEW.associated_authors < 0 THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'The number of associated authors cannot be negative.';
  END IF;
END//

DELIMITER ;

-- Try to update the associated_authors field with a negative value
UPDATE Institutions
SET associated_authors = -5
WHERE institution_ID = 'INST001';

DELIMITER //

CREATE TRIGGER validate_keyword_length
BEFORE INSERT ON Keywords
FOR EACH ROW
BEGIN
  IF LENGTH(NEW.keyword) > 100 THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Keyword length exceeds the allowed limit of 100 characters.';
  END IF;
END//

DELIMITER ;

-- Try inserting a keyword that exceeds the length limit
INSERT INTO Keywords (keyword_ID, keyword)
VALUES ('KW002', 'ThisIsAVeryLongKeywordThatExceedsTheAllowedLengthOfOneHundredCharactersAndShouldTriggerAnError');

