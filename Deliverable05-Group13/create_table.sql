CREATE DATABASE IEEE_db;
USE IEEE_db;

CREATE TABLE Institutions (
    institution_ID VARCHAR(10),
    inst_name VARCHAR(100),
    inst_addr VARCHAR(50),
    inst_web_link VARCHAR(50),
    associated_authors INT,
    PRIMARY KEY (institution_ID)
);

CREATE TABLE Topics (
    topic_ID VARCHAR(10),
    topic_name VARCHAR(70),
    topic_pub_count INT,
    PRIMARY KEY (topic_ID)
);

CREATE TABLE Citations (
    citation_ID VARCHAR(10),
    citing_pub VARCHAR(70),
    cited_pub VARCHAR(70),
    cited_paper_links VARCHAR(50),
    citation_count INT,
    PRIMARY KEY (citation_ID)
);

CREATE TABLE Conferences (
    conference_ID VARCHAR(10),
    conference_name VARCHAR(120),
    conference_year INT,
    conference_location VARCHAR(50),
    PRIMARY KEY (conference_ID)
);

CREATE TABLE Users (
    user_ID VARCHAR(10),
    user_name VARCHAR(25),
    user_email VARCHAR(30),
    user_contact_no VARCHAR(12),
    sub_status VARCHAR(10),
    subscription VARCHAR(10),
    profession VARCHAR(25),
    PRIMARY KEY (user_ID)
);


CREATE TABLE Publications (
    publication_ID VARCHAR(10),
    paper_name VARCHAR(50),
    publisher VARCHAR(25),
    DOI VARCHAR(10),
    date_of_conference DATE,
    date_of_publication DATE,
    print_ISSN VARCHAR(10),
    print_ISBN VARCHAR(20),
    conference_ID VARCHAR(10),
    PRIMARY KEY (publication_ID),
    FOREIGN KEY (conference_ID) REFERENCES Conferences(conference_ID)
);

CREATE TABLE Authors (
    author_ID VARCHAR(10),
    author_name VARCHAR(25),
    no_of_publications INT,
    no_of_citations INT,
    institution_ID VARCHAR(10),
    topic_ID VARCHAR(10),
    PRIMARY KEY (author_ID),
    FOREIGN KEY (institution_ID) REFERENCES Institutions(institution_ID),
    FOREIGN KEY (topic_ID) REFERENCES Topics(topic_ID)
);


CREATE TABLE Keywords (
    keyword_ID VARCHAR(10),
    topic_ID VARCHAR(10),
    keyword VARCHAR(50),
    kw_pub_count INT,
    PRIMARY KEY (keyword_ID),
    FOREIGN KEY (topic_ID) REFERENCES Topics(topic_ID)
);

CREATE TABLE Members (
    member_ID VARCHAR(10),
    roles VARCHAR(25),
    memshp_status VARCHAR(10),
    memshp_start_date VARCHAR(10),
    user_ID VARCHAR(10),
    institution_ID VARCHAR(10),
    PRIMARY KEY (member_ID),
    FOREIGN KEY (user_ID) REFERENCES Users(user_ID),
    FOREIGN KEY (institution_ID) REFERENCES Institutions(institution_ID)
);


CREATE TABLE Author_Affiliation (
    author_ID VARCHAR(10),
    aff_start_date VARCHAR(10),
    aff_end_date VARCHAR(10),
    PRIMARY KEY (author_ID, aff_start_date),
    FOREIGN KEY (author_ID) REFERENCES Authors(author_ID)
);


CREATE TABLE Pub_Author (
    publication_ID VARCHAR(10),
    author_ID VARCHAR(10),
    PRIMARY KEY (publication_ID, author_ID),
    FOREIGN KEY (publication_ID) REFERENCES Publications(publication_ID),
    FOREIGN KEY (author_ID) REFERENCES Authors(author_ID)
);


CREATE TABLE Pub_Key (
    publication_ID VARCHAR(10),
    keyword_ID VARCHAR(10),
    PRIMARY KEY (publication_ID, keyword_ID),
    FOREIGN KEY (publication_ID) REFERENCES Publications(publication_ID),
    FOREIGN KEY (keyword_ID) REFERENCES Keywords(keyword_ID)
);


CREATE TABLE Pub_Cite (
    publication_ID VARCHAR(10),
    citation_ID VARCHAR(10),
    PRIMARY KEY (publication_ID, citation_ID),
    FOREIGN KEY (publication_ID) REFERENCES Publications(publication_ID),
    FOREIGN KEY (citation_ID) REFERENCES Citations(citation_ID)
);
