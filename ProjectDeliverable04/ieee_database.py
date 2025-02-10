# type: ignore
import mysql.connector
from tabulate import tabulate

# Database connection 
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="suhasi@1325",
        database="ieee_db"
    )

# CREATE Operation to add new tuple in Publications Table
def create_publication():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        # Input with validation
        publication_ID = input("Enter Publication ID (numeric): ")
        if not publication_ID.isdigit():
            print("Publication ID must be a number.")
            return
        
        paper_name = input("Enter Paper Name: ")
        publisher = input("Enter Publisher: ")
        DOI = input("Enter DOI: ")
        date_of_conference = input("Enter Date of Conference (YYYY-MM-DD): ")
        date_of_publication = input("Enter Date of Publication (YYYY-MM-DD): ")
        print_ISSN = input("Enter Print ISSN: ")
        print_ISBN = input("Enter Print ISBN: ")
        conference_ID = input("Enter Conference ID: ")
        
        # Insert data into database
        cursor.execute(
            """INSERT INTO publications 
            (publication_ID, paper_name, publisher, DOI, date_of_conference, date_of_publication, 
             print_ISSN, print_ISBN, conference_ID) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (publication_ID, paper_name, publisher, DOI, date_of_conference, date_of_publication, 
             print_ISSN, print_ISBN, conference_ID)
        )
        connection.commit()
        
        # Retrieve and display the newly added record
        cursor.execute("SELECT * FROM publications WHERE publication_ID = %s", (publication_ID,))
        new_record = cursor.fetchone()
        column_names = [i[0] for i in cursor.description]
        print("\nNew Publication Added Successfully:")
        print(tabulate([new_record], headers=column_names, tablefmt="grid"))
        
    except mysql.connector.Error as error:
        print(f"Error adding publication: {error}")
    finally:
        cursor.close()
        connection.close()


# Function to display one publication ID as an example
def show_sample_id():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        # Retrieve a single sample publication ID
        cursor.execute("SELECT publication_ID FROM publications LIMIT 1")
        sample_id = cursor.fetchone()
        
        if sample_id:
            print("Sample Publication ID:", sample_id[0])
        else:
            print("No publications found in the database.")
    except mysql.connector.Error as error:
        print(f"Error retrieving sample ID: {error}")
    finally:
        cursor.close()
        connection.close()

# READ operation to get the details about any and all Publication IDs
def read_publication():
    # Show a sample publication ID to guide the user
    show_sample_id()
    
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        publication_ID = input("Enter Publication ID to retrieve: ")
        cursor.execute("SELECT * FROM publications WHERE publication_ID = %s", (publication_ID,))
        
        record = cursor.fetchone()
        if record:
            # Fetch column names for table headers
            column_names = [i[0] for i in cursor.description]
            print(tabulate([record], headers=column_names, tablefmt="grid"))
        else:
            print("No record found with the given Publication ID.")
    except mysql.connector.Error as error:
        print(f"Error reading publication: {error}")
    finally:
        cursor.close()
        connection.close()


# UPDATE operation to make any changes in the existing records
def update_publication():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        publication_ID = input("Enter Publication ID to update: ")
        paper_name = input("Enter new Paper Name: ")
        publisher = input("Enter new Publisher: ")
        DOI = input("Enter new DOI: ")
        date_of_conference = input("Enter new Date of Conference (YYYY-MM-DD): ")
        date_of_publication = input("Enter new Date of Publication (YYYY-MM-DD): ")
        print_ISSN = input("Enter new Print ISSN: ")
        print_ISBN = input("Enter new Print ISBN: ")
        conference_ID = input("Enter new Conference ID: ")
        
        cursor.execute(
            """UPDATE publications SET paper_name = %s, publisher = %s, DOI = %s, 
               date_of_conference = %s, date_of_publication = %s, print_ISSN = %s, 
               print_ISBN = %s, conference_ID = %s WHERE publication_ID = %s""",
            (paper_name, publisher, DOI, date_of_conference, date_of_publication, 
             print_ISSN, print_ISBN, conference_ID, publication_ID)
        )
        connection.commit()
        
        # Fetch and display updated record
        cursor.execute("SELECT * FROM publications WHERE publication_ID = %s", (publication_ID,))
        updated_record = cursor.fetchone()
        
        if updated_record:
            column_names = [i[0] for i in cursor.description]
            print("\nPublication Updated Successfully:")
            print(tabulate([updated_record], headers=column_names, tablefmt="grid"))
        else:
            print("No record found with the given Publication ID.")
        
    except mysql.connector.Error as error:
        print(f"Error updating publication: {error}")
    finally:
        cursor.close()
        connection.close()


# DELETE operation to get rid of any unnecessary data
def delete_publication():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        publication_ID = input("Enter Publication ID to delete: ")
        
        # Display record before deletion
        cursor.execute("SELECT * FROM publications WHERE publication_ID = %s", (publication_ID,))
        record_to_delete = cursor.fetchone()
        
        if record_to_delete:
            column_names = [i[0] for i in cursor.description]
            print("\nPublication to be Deleted:")
            print(tabulate([record_to_delete], headers=column_names, tablefmt="grid"))
            
            confirm = input("Are you sure you want to delete this publication? (yes/no): ")
            if confirm.lower() == 'yes':
                cursor.execute("DELETE FROM publications WHERE publication_ID = %s", (publication_ID,))
                connection.commit()
                print(f"\nPublication {publication_ID} deleted successfully.")
            else:
                print("Deletion cancelled.")
        else:
            print("No record found with the given Publication ID.")
        
    except mysql.connector.Error as error:
        print(f"Error deleting publication: {error}")
    finally:
        cursor.close()
        connection.close()


# CREATE Operation to add new tuple in Institutions table
def create_institution():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        # Input with validation
        institution_ID = input("Enter Institution ID (numeric): ")
        if not institution_ID.isdigit():
            print("Institution ID must be a number.")
            return
        
        inst_name = input("Enter Institution Name: ")
        inst_addr = input("Enter Institution Address: ")
        inst_web_link = input("Enter Institution Web Link: ")
        associated_authors = input("Enter Associated Authors (comma-separated): ")
        
        # Insert data into database
        cursor.execute(
            """INSERT INTO institutions 
            (institution_ID, inst_name, inst_addr, inst_web_link, associated_authors) 
            VALUES (%s, %s, %s, %s, %s)""",
            (institution_ID, inst_name, inst_addr, inst_web_link, associated_authors)
        )
        connection.commit()
        
        # Retrieve and display the newly added record
        cursor.execute("SELECT * FROM institutions WHERE institution_ID = %s", (institution_ID,))
        new_record = cursor.fetchone()
        column_names = [i[0] for i in cursor.description]
        print("\nNew Institution Added Successfully:")
        print(tabulate([new_record], headers=column_names, tablefmt="grid"))
        
    except mysql.connector.Error as error:
        print(f"Error adding institution: {error}")
    finally:
        cursor.close()
        connection.close()

# Function to display one sample institution ID
def show_sample_institution_id():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        # Retrieve a single sample institution ID
        cursor.execute("SELECT institution_ID FROM institutions LIMIT 1")
        sample_id = cursor.fetchone()
        
        if sample_id:
            print("Sample Institution ID:", sample_id[0])
        else:
            print("No institutions found in the database.")
    except mysql.connector.Error as error:
        print(f"Error retrieving sample ID: {error}")
    finally:
        cursor.close()
        connection.close()

# READ operation - Retrieve institution by ID with table display
def read_institution():
    # Show a sample institution ID to guide the user
    show_sample_institution_id()
    
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        institution_ID = input("Enter Institution ID to retrieve: ")
        cursor.execute("SELECT * FROM institutions WHERE institution_ID = %s", (institution_ID,))
        
        record = cursor.fetchone()
        if record:
            # Fetch column names for table headers
            column_names = [i[0] for i in cursor.description]
            print(tabulate([record], headers=column_names, tablefmt="grid"))
        else:
            print("No record found with the given Institution ID.")
    except mysql.connector.Error as error:
        print(f"Error reading institution: {error}")
    finally:
        cursor.close()
        connection.close()

# UPDATE operation - Modify institution details
def update_institution():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        institution_ID = input("Enter Institution ID to update: ")
        inst_name = input("Enter new Institution Name: ")
        inst_addr = input("Enter new Institution Address: ")
        inst_web_link = input("Enter new Institution Web Link: ")
        associated_authors = input("Enter new Associated Authors (comma-separated): ")
        
        cursor.execute(
            """UPDATE institutions SET inst_name = %s, inst_addr = %s, inst_web_link = %s, 
               associated_authors = %s WHERE institution_ID = %s""",
            (inst_name, inst_addr, inst_web_link, associated_authors, institution_ID)
        )
        connection.commit()
        
        # Fetch and display updated record
        cursor.execute("SELECT * FROM institutions WHERE institution_ID = %s", (institution_ID,))
        updated_record = cursor.fetchone()
        
        if updated_record:
            column_names = [i[0] for i in cursor.description]
            print("\nInstitution Updated Successfully:")
            print(tabulate([updated_record], headers=column_names, tablefmt="grid"))
        else:
            print("No record found with the given Institution ID.")
        
    except mysql.connector.Error as error:
        print(f"Error updating institution: {error}")
    finally:
        cursor.close()
        connection.close()

# DELETE operation - Remove institution by ID
def delete_institution():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        institution_ID = input("Enter Institution ID to delete: ")
        
        # Display record before deletion
        cursor.execute("SELECT * FROM institutions WHERE institution_ID = %s", (institution_ID,))
        record_to_delete = cursor.fetchone()
        
        if record_to_delete:
            column_names = [i[0] for i in cursor.description]
            print("\nInstitution to be Deleted:")
            print(tabulate([record_to_delete], headers=column_names, tablefmt="grid"))
            
            confirm = input("Are you sure you want to delete this institution? (yes/no): ")
            if confirm.lower() == 'yes':
                cursor.execute("DELETE FROM institutions WHERE institution_ID = %s", (institution_ID,))
                connection.commit()
                print(f"\nInstitution {institution_ID} deleted successfully.")
            else:
                print("Deletion cancelled.")
        else:
            print("No record found with the given Institution ID.")
        
    except mysql.connector.Error as error:
        print(f"Error deleting institution: {error}")
    finally:
        cursor.close()
        connection.close()



# CREATE Operation to add new tuple in Topics Table
def create_topic():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        # Input with validation
        topic_ID = input("Enter Topic ID (up to 10 characters): ")
        if len(topic_ID) > 10:
            print("Topic ID must be 10 characters or fewer.")
            return
        
        topic_name = input("Enter Topic Name (up to 70 characters): ")
        if len(topic_name) > 70:
            print("Topic Name must be 70 characters or fewer.")
            return
        
        topic_pub_count = input("Enter Topic Publication Count (numeric): ")
        if not topic_pub_count.isdigit():
            print("Publication Count must be a number.")
            return
        
        # Insert data into database
        cursor.execute(
            """INSERT INTO Topics (topic_ID, topic_name, topic_pub_count) 
            VALUES (%s, %s, %s)""",
            (topic_ID, topic_name, int(topic_pub_count))
        )
        connection.commit()
        
        # Retrieve and display the newly added record
        cursor.execute("SELECT * FROM Topics WHERE topic_ID = %s", (topic_ID,))
        new_record = cursor.fetchone()
        column_names = [i[0] for i in cursor.description]
        print("\nNew Topic Added Successfully:")
        print(tabulate([new_record], headers=column_names, tablefmt="grid"))
        
    except mysql.connector.Error as error:
        print(f"Error adding topic: {error}")
    finally:
        cursor.close()
        connection.close()

# Function to display one sample topic ID
def show_sample_topic_id():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        # Retrieve a single sample topic ID
        cursor.execute("SELECT topic_ID FROM Topics LIMIT 1")
        sample_id = cursor.fetchone()
        
        if sample_id:
            print("Sample Topic ID:", sample_id[0])
        else:
            print("No topics found in the database.")
    except mysql.connector.Error as error:
        print(f"Error retrieving sample ID: {error}")
    finally:
        cursor.close()
        connection.close()

# READ operation - Retrieve topic by ID with table display
def read_topic():
    # Show a sample topic ID to guide the user
    show_sample_topic_id()
    
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        topic_ID = input("Enter Topic ID to retrieve: ")
        cursor.execute("SELECT * FROM Topics WHERE topic_ID = %s", (topic_ID,))
        
        record = cursor.fetchone()
        if record:
            # Fetch column names for table headers
            column_names = [i[0] for i in cursor.description]
            print(tabulate([record], headers=column_names, tablefmt="grid"))
        else:
            print("No record found with the given Topic ID.")
    except mysql.connector.Error as error:
        print(f"Error reading topic: {error}")
    finally:
        cursor.close()
        connection.close()

# UPDATE operation - Modify topic details
def update_topic():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        topic_ID = input("Enter Topic ID to update: ")
        topic_name = input("Enter new Topic Name (up to 70 characters): ")
        if len(topic_name) > 70:
            print("Topic Name must be 70 characters or fewer.")
            return
        
        topic_pub_count = input("Enter new Topic Publication Count (numeric): ")
        if not topic_pub_count.isdigit():
            print("Publication Count must be a number.")
            return
        
        cursor.execute(
            """UPDATE Topics SET topic_name = %s, topic_pub_count = %s WHERE topic_ID = %s""",
            (topic_name, int(topic_pub_count), topic_ID)
        )
        connection.commit()
        
        # Fetch and display updated record
        cursor.execute("SELECT * FROM Topics WHERE topic_ID = %s", (topic_ID,))
        updated_record = cursor.fetchone()
        
        if updated_record:
            column_names = [i[0] for i in cursor.description]
            print("\nTopic Updated Successfully:")
            print(tabulate([updated_record], headers=column_names, tablefmt="grid"))
        else:
            print("No record found with the given Topic ID.")
        
    except mysql.connector.Error as error:
        print(f"Error updating topic: {error}")
    finally:
        cursor.close()
        connection.close()

# DELETE operation - Remove topic by ID
def delete_topic():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        topic_ID = input("Enter Topic ID to delete: ")
        
        # Display record before deletion
        cursor.execute("SELECT * FROM Topics WHERE topic_ID = %s", (topic_ID,))
        record_to_delete = cursor.fetchone()
        
        if record_to_delete:
            column_names = [i[0] for i in cursor.description]
            print("\nTopic to be Deleted:")
            print(tabulate([record_to_delete], headers=column_names, tablefmt="grid"))
            
            confirm = input("Are you sure you want to delete this topic? (yes/no): ")
            if confirm.lower() == 'yes':
                cursor.execute("DELETE FROM Topics WHERE topic_ID = %s", (topic_ID,))
                connection.commit()
                print(f"\nTopic {topic_ID} deleted successfully.")
            else:
                print("Deletion cancelled.")
        else:
            print("No record found with the given Topic ID.")
        
    except mysql.connector.Error as error:
        print(f"Error deleting topic: {error}")
    finally:
        cursor.close()
        connection.close()


# CREATE Operation to add new tuple in Citations Table
def create_citation():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        # Input with validation
        citation_ID = input("Enter Citation ID (up to 10 characters): ")
        if len(citation_ID) > 10:
            print("Citation ID must be 10 characters or fewer.")
            return
        
        citing_pub = input("Enter Citing Publication Name (up to 70 characters): ")
        if len(citing_pub) > 70:
            print("Citing Publication Name must be 70 characters or fewer.")
            return
        
        cited_pub = input("Enter Cited Publication Name (up to 70 characters): ")
        if len(cited_pub) > 70:
            print("Cited Publication Name must be 70 characters or fewer.")
            return
        
        cited_paper_links = input("Enter Cited Paper Links (up to 50 characters): ")
        if len(cited_paper_links) > 50:
            print("Cited Paper Links must be 50 characters or fewer.")
            return
        
        citation_count = input("Enter Citation Count (numeric): ")
        if not citation_count.isdigit():
            print("Citation Count must be a number.")
            return
        
        # Insert data into database
        cursor.execute(
            """INSERT INTO Citations (citation_ID, citing_pub, cited_pub, cited_paper_links, citation_count) 
            VALUES (%s, %s, %s, %s, %s)""",
            (citation_ID, citing_pub, cited_pub, cited_paper_links, int(citation_count))
        )
        connection.commit()
        
        # Retrieve and display the newly added record
        cursor.execute("SELECT * FROM Citations WHERE citation_ID = %s", (citation_ID,))
        new_record = cursor.fetchone()
        column_names = [i[0] for i in cursor.description]
        print("\nNew Citation Added Successfully:")
        print(tabulate([new_record], headers=column_names, tablefmt="grid"))
        
    except mysql.connector.Error as error:
        print(f"Error adding citation: {error}")
    finally:
        cursor.close()
        connection.close()

# Function to display one sample citation ID
def show_sample_citation_id():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        # Retrieve a single sample citation ID
        cursor.execute("SELECT citation_ID FROM Citations LIMIT 1")
        sample_id = cursor.fetchone()
        
        if sample_id:
            print("Sample Citation ID:", sample_id[0])
        else:
            print("No citations found in the database.")
    except mysql.connector.Error as error:
        print(f"Error retrieving sample ID: {error}")
    finally:
        cursor.close()
        connection.close()

# READ operation - Retrieve citation by ID with table display
def read_citation():
    # Show a sample citation ID to guide the user
    show_sample_citation_id()
    
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        citation_ID = input("Enter Citation ID to retrieve: ")
        cursor.execute("SELECT * FROM Citations WHERE citation_ID = %s", (citation_ID,))
        
        record = cursor.fetchone()
        if record:
            # Fetch column names for table headers
            column_names = [i[0] for i in cursor.description]
            print(tabulate([record], headers=column_names, tablefmt="grid"))
        else:
            print("No record found with the given Citation ID.")
    except mysql.connector.Error as error:
        print(f"Error reading citation: {error}")
    finally:
        cursor.close()
        connection.close()

# UPDATE operation - Modify citation details
def update_citation():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        citation_ID = input("Enter Citation ID to update: ")
        citing_pub = input("Enter new Citing Publication Name (up to 70 characters): ")
        if len(citing_pub) > 70:
            print("Citing Publication Name must be 70 characters or fewer.")
            return
        
        cited_pub = input("Enter new Cited Publication Name (up to 70 characters): ")
        if len(cited_pub) > 70:
            print("Cited Publication Name must be 70 characters or fewer.")
            return
        
        cited_paper_links = input("Enter new Cited Paper Links (up to 50 characters): ")
        if len(cited_paper_links) > 50:
            print("Cited Paper Links must be 50 characters or fewer.")
            return
        
        citation_count = input("Enter new Citation Count (numeric): ")
        if not citation_count.isdigit():
            print("Citation Count must be a number.")
            return
        
        cursor.execute(
            """UPDATE Citations SET citing_pub = %s, cited_pub = %s, cited_paper_links = %s, 
               citation_count = %s WHERE citation_ID = %s""",
            (citing_pub, cited_pub, cited_paper_links, int(citation_count), citation_ID)
        )
        connection.commit()
        
        # Fetch and display updated record
        cursor.execute("SELECT * FROM Citations WHERE citation_ID = %s", (citation_ID,))
        updated_record = cursor.fetchone()
        
        if updated_record:
            column_names = [i[0] for i in cursor.description]
            print("\nCitation Updated Successfully:")
            print(tabulate([updated_record], headers=column_names, tablefmt="grid"))
        else:
            print("No record found with the given Citation ID.")
        
    except mysql.connector.Error as error:
        print(f"Error updating citation: {error}")
    finally:
        cursor.close()
        connection.close()

# DELETE operation - Remove citation by ID
def delete_citation():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        citation_ID = input("Enter Citation ID to delete: ")
        
        # Display record before deletion
        cursor.execute("SELECT * FROM Citations WHERE citation_ID = %s", (citation_ID,))
        record_to_delete = cursor.fetchone()
        
        if record_to_delete:
            column_names = [i[0] for i in cursor.description]
            print("\nCitation to be Deleted:")
            print(tabulate([record_to_delete], headers=column_names, tablefmt="grid"))
            
            confirm = input("Are you sure you want to delete this citation? (yes/no): ")
            if confirm.lower() == 'yes':
                cursor.execute("DELETE FROM Citations WHERE citation_ID = %s", (citation_ID,))
                connection.commit()
                print(f"\nCitation {citation_ID} deleted successfully.")
            else:
                print("Deletion cancelled.")
        else:
            print("No record found with the given Citation ID.")
        
    except mysql.connector.Error as error:
        print(f"Error deleting citation: {error}")
    finally:
        cursor.close()
        connection.close()


# CREATE Operation to add new tuple in Conferences Table
def create_conference():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        # Input with validation
        conference_ID = input("Enter Conference ID (up to 10 characters): ")
        if len(conference_ID) > 10:
            print("Conference ID must be 10 characters or fewer.")
            return
        
        conference_name = input("Enter Conference Name (up to 120 characters): ")
        if len(conference_name) > 120:
            print("Conference Name must be 120 characters or fewer.")
            return
        
        conference_year = input("Enter Conference Year (numeric): ")
        if not conference_year.isdigit():
            print("Conference Year must be a number.")
            return
        
        conference_location = input("Enter Conference Location (up to 50 characters): ")
        if len(conference_location) > 50:
            print("Conference Location must be 50 characters or fewer.")
            return
        
        # Insert data into database
        cursor.execute(
            """INSERT INTO Conferences (conference_ID, conference_name, conference_year, conference_location) 
            VALUES (%s, %s, %s, %s)""",
            (conference_ID, conference_name, int(conference_year), conference_location)
        )
        connection.commit()
        
        # Retrieve and display the newly added record
        cursor.execute("SELECT * FROM Conferences WHERE conference_ID = %s", (conference_ID,))
        new_record = cursor.fetchone()
        column_names = [i[0] for i in cursor.description]
        print("\nNew Conference Added Successfully:")
        print(tabulate([new_record], headers=column_names, tablefmt="grid"))
        
    except mysql.connector.Error as error:
        print(f"Error adding conference: {error}")
    finally:
        cursor.close()
        connection.close()

# Function to display one sample conference ID
def show_sample_conference_id():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        # Retrieve a single sample conference ID
        cursor.execute("SELECT conference_ID FROM Conferences LIMIT 1")
        sample_id = cursor.fetchone()
        
        if sample_id:
            print("Sample Conference ID:", sample_id[0])
        else:
            print("No conferences found in the database.")
    except mysql.connector.Error as error:
        print(f"Error retrieving sample ID: {error}")
    finally:
        cursor.close()
        connection.close()

# READ operation - Retrieve conference by ID with table display
def read_conference():
    # Show a sample conference ID to guide the user
    show_sample_conference_id()
    
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        conference_ID = input("Enter Conference ID to retrieve: ")
        cursor.execute("SELECT * FROM Conferences WHERE conference_ID = %s", (conference_ID,))
        
        record = cursor.fetchone()
        if record:
            # Fetch column names for table headers
            column_names = [i[0] for i in cursor.description]
            print(tabulate([record], headers=column_names, tablefmt="grid"))
        else:
            print("No record found with the given Conference ID.")
    except mysql.connector.Error as error:
        print(f"Error reading conference: {error}")
    finally:
        cursor.close()
        connection.close()

# UPDATE operation - Modify conference details
def update_conference():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        conference_ID = input("Enter Conference ID to update: ")
        conference_name = input("Enter new Conference Name (up to 120 characters): ")
        if len(conference_name) > 120:
            print("Conference Name must be 120 characters or fewer.")
            return
        
        conference_year = input("Enter new Conference Year (numeric): ")
        if not conference_year.isdigit():
            print("Conference Year must be a number.")
            return
        
        conference_location = input("Enter new Conference Location (up to 50 characters): ")
        if len(conference_location) > 50:
            print("Conference Location must be 50 characters or fewer.")
            return
        
        cursor.execute(
            """UPDATE Conferences SET conference_name = %s, conference_year = %s, conference_location = %s 
               WHERE conference_ID = %s""",
            (conference_name, int(conference_year), conference_location, conference_ID)
        )
        connection.commit()
        
        # Fetch and display updated record
        cursor.execute("SELECT * FROM Conferences WHERE conference_ID = %s", (conference_ID,))
        updated_record = cursor.fetchone()
        
        if updated_record:
            column_names = [i[0] for i in cursor.description]
            print("\nConference Updated Successfully:")
            print(tabulate([updated_record], headers=column_names, tablefmt="grid"))
        else:
            print("No record found with the given Conference ID.")
        
    except mysql.connector.Error as error:
        print(f"Error updating conference: {error}")
    finally:
        cursor.close()
        connection.close()

# DELETE operation - Remove conference by ID
def delete_conference():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        conference_ID = input("Enter Conference ID to delete: ")
        
        # Display record before deletion
        cursor.execute("SELECT * FROM Conferences WHERE conference_ID = %s", (conference_ID,))
        record_to_delete = cursor.fetchone()
        
        if record_to_delete:
            column_names = [i[0] for i in cursor.description]
            print("\nConference to be Deleted:")
            print(tabulate([record_to_delete], headers=column_names, tablefmt="grid"))
            
            confirm = input("Are you sure you want to delete this conference? (yes/no): ")
            if confirm.lower() == 'yes':
                cursor.execute("DELETE FROM Conferences WHERE conference_ID = %s", (conference_ID,))
                connection.commit()
                print(f"\nConference {conference_ID} deleted successfully.")
            else:
                print("Deletion cancelled.")
        else:
            print("No record found with the given Conference ID.")
        
    except mysql.connector.Error as error:
        print(f"Error deleting conference: {error}")
    finally:
        cursor.close()
        connection.close()


# CREATE Operation to add new tuple in Users Table
def create_user():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        # Input with validation
        user_ID = input("Enter User ID (up to 10 characters): ")
        if len(user_ID) > 10:
            print("User ID must be 10 characters or fewer.")
            return
        
        user_name = input("Enter User Name (up to 25 characters): ")
        if len(user_name) > 25:
            print("User Name must be 25 characters or fewer.")
            return
        
        user_email = input("Enter User Email (up to 30 characters): ")
        if len(user_email) > 30:
            print("User Email must be 30 characters or fewer.")
            return
        
        user_contact_no = input("Enter User Contact Number (up to 12 characters): ")
        if len(user_contact_no) > 12:
            print("User Contact Number must be 12 characters or fewer.")
            return
        
        sub_status = input("Enter Subscription Status (up to 10 characters): ")
        if len(sub_status) > 10:
            print("Subscription Status must be 10 characters or fewer.")
            return
        
        subscription = input("Enter Subscription Type (up to 10 characters): ")
        if len(subscription) > 10:
            print("Subscription Type must be 10 characters or fewer.")
            return
        
        profession = input("Enter Profession (up to 25 characters): ")
        if len(profession) > 25:
            print("Profession must be 25 characters or fewer.")
            return
        
        # Insert data into database
        cursor.execute(
            """INSERT INTO Users (user_ID, user_name, user_email, user_contact_no, sub_status, 
            subscription, profession) VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (user_ID, user_name, user_email, user_contact_no, sub_status, subscription, profession)
        )
        connection.commit()
        
        # Retrieve and display the newly added record
        cursor.execute("SELECT * FROM Users WHERE user_ID = %s", (user_ID,))
        new_record = cursor.fetchone()
        column_names = [i[0] for i in cursor.description]
        print("\nNew User Added Successfully:")
        print(tabulate([new_record], headers=column_names, tablefmt="grid"))
        
    except mysql.connector.Error as error:
        print(f"Error adding user: {error}")
    finally:
        cursor.close()
        connection.close()

# Function to display one sample user ID
def show_sample_user_id():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        # Retrieve a single sample user ID
        cursor.execute("SELECT user_ID FROM Users LIMIT 1")
        sample_id = cursor.fetchone()
        
        if sample_id:
            print("Sample User ID:", sample_id[0])
        else:
            print("No users found in the database.")
    except mysql.connector.Error as error:
        print(f"Error retrieving sample ID: {error}")
    finally:
        cursor.close()
        connection.close()

# READ operation - Retrieve user by ID with table display
def read_user():
    # Show a sample user ID to guide the user
    show_sample_user_id()
    
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        user_ID = input("Enter User ID to retrieve: ")
        cursor.execute("SELECT * FROM Users WHERE user_ID = %s", (user_ID,))
        
        record = cursor.fetchone()
        if record:
            # Fetch column names for table headers
            column_names = [i[0] for i in cursor.description]
            print(tabulate([record], headers=column_names, tablefmt="grid"))
        else:
            print("No record found with the given User ID.")
    except mysql.connector.Error as error:
        print(f"Error reading user: {error}")
    finally:
        cursor.close()
        connection.close()

# UPDATE operation - Modify user details
def update_user():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        user_ID = input("Enter User ID to update: ")
        user_name = input("Enter new User Name (up to 25 characters): ")
        if len(user_name) > 25:
            print("User Name must be 25 characters or fewer.")
            return
        
        user_email = input("Enter new User Email (up to 30 characters): ")
        if len(user_email) > 30:
            print("User Email must be 30 characters or fewer.")
            return
        
        user_contact_no = input("Enter new User Contact Number (up to 12 characters): ")
        if len(user_contact_no) > 12:
            print("User Contact Number must be 12 characters or fewer.")
            return
        
        sub_status = input("Enter new Subscription Status (up to 10 characters): ")
        if len(sub_status) > 10:
            print("Subscription Status must be 10 characters or fewer.")
            return
        
        subscription = input("Enter new Subscription Type (up to 10 characters): ")
        if len(subscription) > 10:
            print("Subscription Type must be 10 characters or fewer.")
            return
        
        profession = input("Enter new Profession (up to 25 characters): ")
        if len(profession) > 25:
            print("Profession must be 25 characters or fewer.")
            return
        
        cursor.execute(
            """UPDATE Users SET user_name = %s, user_email = %s, user_contact_no = %s, sub_status = %s, 
            subscription = %s, profession = %s WHERE user_ID = %s""",
            (user_name, user_email, user_contact_no, sub_status, subscription, profession, user_ID)
        )
        connection.commit()
        
        # Fetch and display updated record
        cursor.execute("SELECT * FROM Users WHERE user_ID = %s", (user_ID,))
        updated_record = cursor.fetchone()
        
        if updated_record:
            column_names = [i[0] for i in cursor.description]
            print("\nUser Updated Successfully:")
            print(tabulate([updated_record], headers=column_names, tablefmt="grid"))
        else:
            print("No record found with the given User ID.")
        
    except mysql.connector.Error as error:
        print(f"Error updating user: {error}")
    finally:
        cursor.close()
        connection.close()

# DELETE operation - Remove user by ID
def delete_user():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        user_ID = input("Enter User ID to delete: ")
        
        # Display record before deletion
        cursor.execute("SELECT * FROM Users WHERE user_ID = %s", (user_ID,))
        record_to_delete = cursor.fetchone()
        
        if record_to_delete:
            column_names = [i[0] for i in cursor.description]
            print("\nUser to be Deleted:")
            print(tabulate([record_to_delete], headers=column_names, tablefmt="grid"))
            
            confirm = input("Are you sure you want to delete this user? (yes/no): ")
            if confirm.lower() == 'yes':
                cursor.execute("DELETE FROM Users WHERE user_ID = %s", (user_ID,))
                connection.commit()
                print(f"\nUser {user_ID} deleted successfully.")
            else:
                print("Deletion cancelled.")
        else:
            print("No record found with the given User ID.")
        
    except mysql.connector.Error as error:
        print(f"Error deleting user: {error}")
    finally:
        cursor.close()
        connection.close()



# CREATE Operation to add new tuple in Authors Table
def create_author():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        # Input with validation
        author_ID = input("Enter Author ID (up to 10 characters): ")
        if len(author_ID) > 10:
            print("Author ID must be 10 characters or fewer.")
            return
        
        author_name = input("Enter Author Name (up to 25 characters): ")
        if len(author_name) > 25:
            print("Author Name must be 25 characters or fewer.")
            return
        
        no_of_publications = input("Enter Number of Publications (numeric): ")
        if not no_of_publications.isdigit():
            print("Number of Publications must be a number.")
            return
        
        no_of_citations = input("Enter Number of Citations (numeric): ")
        if not no_of_citations.isdigit():
            print("Number of Citations must be a number.")
            return
        
        institution_ID = input("Enter Institution ID (up to 10 characters): ")
        if len(institution_ID) > 10:
            print("Institution ID must be 10 characters or fewer.")
            return
        
        topic_ID = input("Enter Topic ID (up to 10 characters): ")
        if len(topic_ID) > 10:
            print("Topic ID must be 10 characters or fewer.")
            return
        
        # Insert data into database
        cursor.execute(
            """INSERT INTO Authors (author_ID, author_name, no_of_publications, no_of_citations, 
            institution_ID, topic_ID) VALUES (%s, %s, %s, %s, %s, %s)""",
            (author_ID, author_name, int(no_of_publications), int(no_of_citations), institution_ID, topic_ID)
        )
        connection.commit()
        
        # Retrieve and display the newly added record
        cursor.execute("SELECT * FROM Authors WHERE author_ID = %s", (author_ID,))
        new_record = cursor.fetchone()
        column_names = [i[0] for i in cursor.description]
        print("\nNew Author Added Successfully:")
        print(tabulate([new_record], headers=column_names, tablefmt="grid"))
        
    except mysql.connector.Error as error:
        print(f"Error adding author: {error}")
    finally:
        cursor.close()
        connection.close()

# Function to display one sample author ID
def show_sample_author_id():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        # Retrieve a single sample author ID
        cursor.execute("SELECT author_ID FROM Authors LIMIT 1")
        sample_id = cursor.fetchone()
        
        if sample_id:
            print("Sample Author ID:", sample_id[0])
        else:
            print("No authors found in the database.")
    except mysql.connector.Error as error:
        print(f"Error retrieving sample ID: {error}")
    finally:
        cursor.close()
        connection.close()

# READ operation - Retrieve author by ID with table display
def read_author():
    # Show a sample author ID to guide the user
    show_sample_author_id()
    
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        author_ID = input("Enter Author ID to retrieve: ")
        cursor.execute("SELECT * FROM Authors WHERE author_ID = %s", (author_ID,))
        
        record = cursor.fetchone()
        if record:
            # Fetch column names for table headers
            column_names = [i[0] for i in cursor.description]
            print(tabulate([record], headers=column_names, tablefmt="grid"))
        else:
            print("No record found with the given Author ID.")
    except mysql.connector.Error as error:
        print(f"Error reading author: {error}")
    finally:
        cursor.close()
        connection.close()

# UPDATE operation - Modify author details
def update_author():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        author_ID = input("Enter Author ID to update: ")
        author_name = input("Enter new Author Name (up to 25 characters): ")
        if len(author_name) > 25:
            print("Author Name must be 25 characters or fewer.")
            return
        
        no_of_publications = input("Enter new Number of Publications (numeric): ")
        if not no_of_publications.isdigit():
            print("Number of Publications must be a number.")
            return
        
        no_of_citations = input("Enter new Number of Citations (numeric): ")
        if not no_of_citations.isdigit():
            print("Number of Citations must be a number.")
            return
        
        institution_ID = input("Enter new Institution ID (up to 10 characters): ")
        if len(institution_ID) > 10:
            print("Institution ID must be 10 characters or fewer.")
            return
        
        topic_ID = input("Enter new Topic ID (up to 10 characters): ")
        if len(topic_ID) > 10:
            print("Topic ID must be 10 characters or fewer.")
            return
        
        cursor.execute(
            """UPDATE Authors SET author_name = %s, no_of_publications = %s, no_of_citations = %s, 
            institution_ID = %s, topic_ID = %s WHERE author_ID = %s""",
            (author_name, int(no_of_publications), int(no_of_citations), institution_ID, topic_ID, author_ID)
        )
        connection.commit()
        
        # Fetch and display updated record
        cursor.execute("SELECT * FROM Authors WHERE author_ID = %s", (author_ID,))
        updated_record = cursor.fetchone()
        
        if updated_record:
            column_names = [i[0] for i in cursor.description]
            print("\nAuthor Updated Successfully:")
            print(tabulate([updated_record], headers=column_names, tablefmt="grid"))
        else:
            print("No record found with the given Author ID.")
        
    except mysql.connector.Error as error:
        print(f"Error updating author: {error}")
    finally:
        cursor.close()
        connection.close()

# DELETE operation - Remove author by ID
def delete_author():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        author_ID = input("Enter Author ID to delete: ")
        
        # Display record before deletion
        cursor.execute("SELECT * FROM Authors WHERE author_ID = %s", (author_ID,))
        record_to_delete = cursor.fetchone()
        
        if record_to_delete:
            column_names = [i[0] for i in cursor.description]
            print("\nAuthor to be Deleted:")
            print(tabulate([record_to_delete], headers=column_names, tablefmt="grid"))
            
            confirm = input("Are you sure you want to delete this author? (yes/no): ")
            if confirm.lower() == 'yes':
                cursor.execute("DELETE FROM Authors WHERE author_ID = %s", (author_ID,))
                connection.commit()
                print(f"\nAuthor {author_ID} deleted successfully.")
            else:
                print("Deletion cancelled.")
        else:
            print("No record found with the given Author ID.")
        
    except mysql.connector.Error as error:
        print(f"Error deleting author: {error}")
    finally:
        cursor.close()
        connection.close()


# CREATE Operation to add new tuple in Keywords Table
def create_keyword():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        # Input with validation
        keyword_ID = input("Enter Keyword ID (up to 10 characters): ")
        if len(keyword_ID) > 10:
            print("Keyword ID must be 10 characters or fewer.")
            return
        
        topic_ID = input("Enter Topic ID (up to 10 characters): ")
        if len(topic_ID) > 10:
            print("Topic ID must be 10 characters or fewer.")
            return
        
        keyword = input("Enter Keyword (up to 50 characters): ")
        if len(keyword) > 50:
            print("Keyword must be 50 characters or fewer.")
            return
        
        kw_pub_count = input("Enter Keyword Publication Count (numeric): ")
        if not kw_pub_count.isdigit():
            print("Publication Count must be a number.")
            return
        
        # Insert data into database
        cursor.execute(
            """INSERT INTO Keywords (keyword_ID, topic_ID, keyword, kw_pub_count) 
            VALUES (%s, %s, %s, %s)""",
            (keyword_ID, topic_ID, keyword, int(kw_pub_count))
        )
        connection.commit()
        
        # Retrieve and display the newly added record
        cursor.execute("SELECT * FROM Keywords WHERE keyword_ID = %s", (keyword_ID,))
        new_record = cursor.fetchone()
        column_names = [i[0] for i in cursor.description]
        print("\nNew Keyword Added Successfully:")
        print(tabulate([new_record], headers=column_names, tablefmt="grid"))
        
    except mysql.connector.Error as error:
        print(f"Error adding keyword: {error}")
    finally:
        cursor.close()
        connection.close()

# Function to display one sample keyword ID
def show_sample_keyword_id():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        # Retrieve a single sample keyword ID
        cursor.execute("SELECT keyword_ID FROM Keywords LIMIT 1")
        sample_id = cursor.fetchone()
        
        if sample_id:
            print("Sample Keyword ID:", sample_id[0])
        else:
            print("No keywords found in the database.")
    except mysql.connector.Error as error:
        print(f"Error retrieving sample ID: {error}")
    finally:
        cursor.close()
        connection.close()

# READ operation - Retrieve keyword by ID with table display
def read_keyword():
    # Show a sample keyword ID to guide the user
    show_sample_keyword_id()
    
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        keyword_ID = input("Enter Keyword ID to retrieve: ")
        cursor.execute("SELECT * FROM Keywords WHERE keyword_ID = %s", (keyword_ID,))
        
        record = cursor.fetchone()
        if record:
            # Fetch column names for table headers
            column_names = [i[0] for i in cursor.description]
            print(tabulate([record], headers=column_names, tablefmt="grid"))
        else:
            print("No record found with the given Keyword ID.")
    except mysql.connector.Error as error:
        print(f"Error reading keyword: {error}")
    finally:
        cursor.close()
        connection.close()

# UPDATE operation - Modify keyword details
def update_keyword():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        keyword_ID = input("Enter Keyword ID to update: ")
        topic_ID = input("Enter new Topic ID (up to 10 characters): ")
        if len(topic_ID) > 10:
            print("Topic ID must be 10 characters or fewer.")
            return
        
        keyword = input("Enter new Keyword (up to 50 characters): ")
        if len(keyword) > 50:
            print("Keyword must be 50 characters or fewer.")
            return
        
        kw_pub_count = input("Enter new Keyword Publication Count (numeric): ")
        if not kw_pub_count.isdigit():
            print("Publication Count must be a number.")
            return
        
        cursor.execute(
            """UPDATE Keywords SET topic_ID = %s, keyword = %s, kw_pub_count = %s 
            WHERE keyword_ID = %s""",
            (topic_ID, keyword, int(kw_pub_count), keyword_ID)
        )
        connection.commit()
        
        # Fetch and display updated record
        cursor.execute("SELECT * FROM Keywords WHERE keyword_ID = %s", (keyword_ID,))
        updated_record = cursor.fetchone()
        
        if updated_record:
            column_names = [i[0] for i in cursor.description]
            print("\nKeyword Updated Successfully:")
            print(tabulate([updated_record], headers=column_names, tablefmt="grid"))
        else:
            print("No record found with the given Keyword ID.")
        
    except mysql.connector.Error as error:
        print(f"Error updating keyword: {error}")
    finally:
        cursor.close()
        connection.close()

# DELETE operation - Remove keyword by ID
def delete_keyword():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        keyword_ID = input("Enter Keyword ID to delete: ")
        
        # Display record before deletion
        cursor.execute("SELECT * FROM Keywords WHERE keyword_ID = %s", (keyword_ID,))
        record_to_delete = cursor.fetchone()
        
        if record_to_delete:
            column_names = [i[0] for i in cursor.description]
            print("\nKeyword to be Deleted:")
            print(tabulate([record_to_delete], headers=column_names, tablefmt="grid"))
            
            confirm = input("Are you sure you want to delete this keyword? (yes/no): ")
            if confirm.lower() == 'yes':
                cursor.execute("DELETE FROM Keywords WHERE keyword_ID = %s", (keyword_ID,))
                connection.commit()
                print(f"\nKeyword {keyword_ID} deleted successfully.")
            else:
                print("Deletion cancelled.")
        else:
            print("No record found with the given Keyword ID.")
        
    except mysql.connector.Error as error:
        print(f"Error deleting keyword: {error}")
    finally:
        cursor.close()
        connection.close()

# CREATE operation - Add a new member
def create_member():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        # Input with validation
        member_ID = input("Enter Member ID (up to 10 characters): ")
        if len(member_ID) > 10:
            print("Member ID must be 10 characters or fewer.")
            return
        
        roles = input("Enter Role (up to 25 characters): ")
        if len(roles) > 25:
            print("Role must be 25 characters or fewer.")
            return
        
        memshp_status = input("Enter Membership Status (up to 10 characters): ")
        if len(memshp_status) > 10:
            print("Membership Status must be 10 characters or fewer.")
            return
        
        memshp_start_date = input("Enter Membership Start Date (YYYY-MM-DD): ")
        if len(memshp_start_date) > 10:
            print("Start Date format should be YYYY-MM-DD.")
            return
        
        user_ID = input("Enter User ID (up to 10 characters): ")
        if len(user_ID) > 10:
            print("User ID must be 10 characters or fewer.")
            return
        
        institution_ID = input("Enter Institution ID (up to 10 characters): ")
        if len(institution_ID) > 10:
            print("Institution ID must be 10 characters or fewer.")
            return
        
        # Insert data into database
        cursor.execute(
            """INSERT INTO Members (member_ID, roles, memshp_status, memshp_start_date, user_ID, institution_ID) 
            VALUES (%s, %s, %s, %s, %s, %s)""",
            (member_ID, roles, memshp_status, memshp_start_date, user_ID, institution_ID)
        )
        connection.commit()
        
        # Retrieve and display the newly added record
        cursor.execute("SELECT * FROM Members WHERE member_ID = %s", (member_ID,))
        new_record = cursor.fetchone()
        column_names = [i[0] for i in cursor.description]
        print("\nNew Member Added Successfully:")
        print(tabulate([new_record], headers=column_names, tablefmt="grid"))
        
    except mysql.connector.Error as error:
        print(f"Error adding member: {error}")
    finally:
        cursor.close()
        connection.close()

# Function to display one sample member ID
def show_sample_member_id():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        # Retrieve a single sample member ID
        cursor.execute("SELECT member_ID FROM Members LIMIT 1")
        sample_id = cursor.fetchone()
        
        if sample_id:
            print("Sample Member ID:", sample_id[0])
        else:
            print("No members found in the database.")
    except mysql.connector.Error as error:
        print(f"Error retrieving sample ID: {error}")
    finally:
        cursor.close()
        connection.close()

# READ operation - Retrieve member by ID with table display
def read_member():
    # Show a sample member ID to guide the user
    show_sample_member_id()
    
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        member_ID = input("Enter Member ID to retrieve: ")
        cursor.execute("SELECT * FROM Members WHERE member_ID = %s", (member_ID,))
        
        record = cursor.fetchone()
        if record:
            # Fetch column names for table headers
            column_names = [i[0] for i in cursor.description]
            print(tabulate([record], headers=column_names, tablefmt="grid"))
        else:
            print("No record found with the given Member ID.")
    except mysql.connector.Error as error:
        print(f"Error reading member: {error}")
    finally:
        cursor.close()
        connection.close()

# UPDATE operation - Modify member details
def update_member():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        member_ID = input("Enter Member ID to update: ")
        roles = input("Enter new Role (up to 25 characters): ")
        if len(roles) > 25:
            print("Role must be 25 characters or fewer.")
            return
        
        memshp_status = input("Enter new Membership Status (up to 10 characters): ")
        if len(memshp_status) > 10:
            print("Membership Status must be 10 characters or fewer.")
            return
        
        memshp_start_date = input("Enter new Membership Start Date (YYYY-MM-DD): ")
        if len(memshp_start_date) > 10:
            print("Start Date format should be YYYY-MM-DD.")
            return
        
        user_ID = input("Enter new User ID (up to 10 characters): ")
        if len(user_ID) > 10:
            print("User ID must be 10 characters or fewer.")
            return
        
        institution_ID = input("Enter new Institution ID (up to 10 characters): ")
        if len(institution_ID) > 10:
            print("Institution ID must be 10 characters or fewer.")
            return
        
        cursor.execute(
            """UPDATE Members SET roles = %s, memshp_status = %s, memshp_start_date = %s, 
            user_ID = %s, institution_ID = %s WHERE member_ID = %s""",
            (roles, memshp_status, memshp_start_date, user_ID, institution_ID, member_ID)
        )
        connection.commit()
        
        # Fetch and display updated record
        cursor.execute("SELECT * FROM Members WHERE member_ID = %s", (member_ID,))
        updated_record = cursor.fetchone()
        
        if updated_record:
            column_names = [i[0] for i in cursor.description]
            print("\nMember Updated Successfully:")
            print(tabulate([updated_record], headers=column_names, tablefmt="grid"))
        else:
            print("No record found with the given Member ID.")
        
    except mysql.connector.Error as error:
        print(f"Error updating member: {error}")
    finally:
        cursor.close()
        connection.close()

# DELETE operation - Remove member by ID
def delete_member():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        member_ID = input("Enter Member ID to delete: ")
        
        # Display record before deletion
        cursor.execute("SELECT * FROM Members WHERE member_ID = %s", (member_ID,))
        record_to_delete = cursor.fetchone()
        
        if record_to_delete:
            column_names = [i[0] for i in cursor.description]
            print("\nMember to be Deleted:")
            print(tabulate([record_to_delete], headers=column_names, tablefmt="grid"))
            
            confirm = input("Are you sure you want to delete this member? (yes/no): ")
            if confirm.lower() == 'yes':
                cursor.execute("DELETE FROM Members WHERE member_ID = %s", (member_ID,))
                connection.commit()
                print(f"\nMember {member_ID} deleted successfully.")
            else:
                print("Deletion cancelled.")
        else:
            print("No record found with the given Member ID.")
        
    except mysql.connector.Error as error:
        print(f"Error deleting member: {error}")
    finally:
        cursor.close()
        connection.close()


# CREATE operation - Add an author affiliation
def create_author_affiliation():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        author_ID = input("Enter Author ID (up to 10 characters): ")
        aff_start_date = input("Enter Affiliation Start Date (YYYY-MM-DD): ")
        aff_end_date = input("Enter Affiliation End Date (YYYY-MM-DD): ")
        
        # Insert data into database
        cursor.execute(
            """INSERT INTO Author_Affiliation (author_ID, aff_start_date, aff_end_date)
            VALUES (%s, %s, %s)""",
            (author_ID, aff_start_date, aff_end_date)
        )
        connection.commit()
        print("\nAuthor affiliation added successfully.")
        
    except mysql.connector.Error as error:
        print(f"Error adding author affiliation: {error}")
    finally:
        cursor.close()
        connection.close()

# DELETE operation - Remove author affiliation by ID and start date
def delete_author_affiliation():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        author_ID = input("Enter Author ID: ")
        aff_start_date = input("Enter Affiliation Start Date (YYYY-MM-DD): ")
        
        # Delete data from database
        cursor.execute("DELETE FROM Author_Affiliation WHERE author_ID = %s AND aff_start_date = %s", 
                       (author_ID, aff_start_date))
        connection.commit()
        print("\nAuthor affiliation deleted successfully.")
        
    except mysql.connector.Error as error:
        print(f"Error deleting author affiliation: {error}")
    finally:
        cursor.close()
        connection.close()


# CREATE operation - Link publication to author
def create_pub_author():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        publication_ID = input("Enter Publication ID: ")
        author_ID = input("Enter Author ID: ")
        
        # Insert data into database
        cursor.execute(
            "INSERT INTO Pub_Author (publication_ID, author_ID) VALUES (%s, %s)",
            (publication_ID, author_ID)
        )
        connection.commit()
        print("\nPublication-Author link added successfully.")
        
    except mysql.connector.Error as error:
        print(f"Error adding publication-author link: {error}")
    finally:
        cursor.close()
        connection.close()

# DELETE operation - Unlink publication from author
def delete_pub_author():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        publication_ID = input("Enter Publication ID: ")
        author_ID = input("Enter Author ID: ")
        
        # Delete data from database
        cursor.execute("DELETE FROM Pub_Author WHERE publication_ID = %s AND author_ID = %s", 
                       (publication_ID, author_ID))
        connection.commit()
        print("\nPublication-Author link deleted successfully.")
        
    except mysql.connector.Error as error:
        print(f"Error deleting publication-author link: {error}")
    finally:
        cursor.close()
        connection.close()

# CREATE operation - Link publication to keyword
def create_pub_key():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        publication_ID = input("Enter Publication ID: ")
        keyword_ID = input("Enter Keyword ID: ")
        
        # Insert data into database
        cursor.execute(
            "INSERT INTO Pub_Key (publication_ID, keyword_ID) VALUES (%s, %s)",
            (publication_ID, keyword_ID)
        )
        connection.commit()
        print("\nPublication-Keyword link added successfully.")
        
    except mysql.connector.Error as error:
        print(f"Error adding publication-keyword link: {error}")
    finally:
        cursor.close()
        connection.close()

# DELETE operation - Unlink publication from keyword
def delete_pub_key():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        publication_ID = input("Enter Publication ID: ")
        keyword_ID = input("Enter Keyword ID: ")
        
        # Delete data from database
        cursor.execute("DELETE FROM Pub_Key WHERE publication_ID = %s AND keyword_ID = %s", 
                       (publication_ID, keyword_ID))
        connection.commit()
        print("\nPublication-Keyword link deleted successfully.")
        
    except mysql.connector.Error as error:
        print(f"Error deleting publication-keyword link: {error}")
    finally:
        cursor.close()
        connection.close()

# CREATE operation - Link publication to citation
def create_pub_cite():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        publication_ID = input("Enter Publication ID: ")
        citation_ID = input("Enter Citation ID: ")
        
        # Insert data into database
        cursor.execute(
            "INSERT INTO Pub_Cite (publication_ID, citation_ID) VALUES (%s, %s)",
            (publication_ID, citation_ID)
        )
        connection.commit()
        print("\nPublication-Citation link added successfully.")
        
    except mysql.connector.Error as error:
        print(f"Error adding publication-citation link: {error}")
    finally:
        cursor.close()
        connection.close()

# DELETE operation - Unlink publication from citation
def delete_pub_cite():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        publication_ID = input("Enter Publication ID: ")
        citation_ID = input("Enter Citation ID: ")
        
        # Delete data from database
        cursor.execute("DELETE FROM Pub_Cite WHERE publication_ID = %s AND citation_ID = %s", 
                       (publication_ID, citation_ID))
        connection.commit()
        print("\nPublication-Citation link deleted successfully.")
        
    except mysql.connector.Error as error:
        print(f"Error deleting publication-citation link: {error}")
    finally:
        cursor.close()
        connection.close()

# Menu for selecting CRUD operations for each table
def crud_operations(table_name):
    while True:
        print(f"\n--- {table_name} CRUD Operations ---")
        print("1. Create")
        print("2. Read All")
        print("3. Update")
        print("4. Delete")
        print("5. Back to Main Menu")
        
        choice = input("Select an option: ")
        
        if table_name == "Publications":
            if choice == '1':
                create_publication()
            elif choice == '2':
                read_publication()
            elif choice == '3':
                update_publication()
            elif choice == '4':
                delete_publication()
            elif choice == '5':
                break
        if table_name == "Institutions":
            if choice == '1':
                create_institution()
            elif choice == '2':
                read_institution()
            elif choice == '3':
                update_institution()
            elif choice == '4':
                delete_institution()
            elif choice == '5':
                break
        if table_name == "Topics":
            if choice == '1':
                create_topic()
            elif choice == '2':
                read_topic()
            elif choice == '3':
                update_topic()
            elif choice == '4':
                delete_topic()
            elif choice == '5':
                break
        if table_name == "Citations":
            if choice == '1':
                create_citation()
            elif choice == '2':
                read_citation()
            elif choice == '3':
                update_citation()
            elif choice == '4':
                delete_citation()
            elif choice == '5':
                break
        if table_name == "Conferences":
            if choice == '1':
                create_conference()
            elif choice == '2':
                read_conference()
            elif choice == '3':
                update_conference()
            elif choice == '4':
                delete_conference()
            elif choice == '5':
                break
        if table_name == "Users":
            if choice == '1':
                create_user()
            elif choice == '2':
                read_user()
            elif choice == '3':
                update_user()
            elif choice == '4':
                delete_user()
            elif choice == '5':
                break
        if table_name == "Authors":
            if choice == '1':
                create_author()
            elif choice == '2':
                read_author()
            elif choice == '3':
                update_author()
            elif choice == '4':
                delete_author()
            elif choice == '5':
                break
        if table_name == "Keywords":
            if choice == '1':
                create_keyword()
            elif choice == '2':
                read_keyword()
            elif choice == '3':
                update_keyword()
            elif choice == '4':
                delete_keyword()
            elif choice == '5':
                break
        if table_name == "Members":
            if choice == '1':
                create_member()
            elif choice == '2':
                read_member()
            elif choice == '3':
                update_member()
            elif choice == '4':
                delete_member()
            elif choice == '5':
                break
        if table_name == "Author_Affiliation":
            if choice == '1':
                create_author_affiliation()
            elif choice == '4':
                delete_author_affiliation()
            elif choice == '5':
                break
        if table_name == "Pub_Author":
            if choice == '1':
                create_pub_author()
            elif choice == '4':
                delete_pub_author()
            elif choice == '5':
                break
        if table_name == "Pub_Key":
            if choice == '1':
                create_pub_key()
            elif choice == '4':
                delete_pub_key()
            elif choice == '5':
                break
        if table_name == "Pub_Cite":
            if choice == '1':
                create_pub_cite()
            elif choice == '4':
                delete_pub_cite()
            elif choice == '5':
                break

# Main menu for selecting a table
def main():
    while True:
        print("\n--- Select Table for CRUD Operations ---")
        print("1. Publications")
        print("2. Institutions")
        print("3. Topics")
        print("4. Citations")
        print("5. Conferences")
        print("6. Users")
        print("7. Authors")
        print("8. Keywords")
        print("9. Members")
        print("10. Author_Affiliation")
        print("11. Pub_Author")
        print("12. Pub_Key")
        print("13. Pub_Cite")
        print("14. Exit")
        
        choice = input("Select a table: ")
        
        if choice == '1':
            crud_operations("Publications")
        elif choice == '2':
            crud_operations("Institutions")
        elif choice == '3':
            crud_operations("Topics")
        elif choice == '4':
            crud_operations("Citations")
        elif choice == '5':
            crud_operations("Conferences")
        elif choice == '6':
            crud_operations("Users")
        elif choice == '7':
            crud_operations("Authors")
        elif choice == '8':
            crud_operations("Keywords")
        elif choice == '9':
            crud_operations("Members")
        elif choice == '10':
            crud_operations("Author_Affiliation")
        elif choice == '11':
            crud_operations("Pub_Author")
        elif choice == '12':
            crud_operations("Pub_Key")
        elif choice == '13':
            crud_operations("Pub_Cite")
        elif choice == '14':
            print("Exiting...")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
