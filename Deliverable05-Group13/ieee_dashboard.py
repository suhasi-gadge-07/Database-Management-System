import streamlit as st
import mysql.connector
import pandas as pd
import datetime
import plotly.express as px


# Database connection
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="suhasi@1325",
        database="ieee_db"
    )

# User credentials (for demonstration purposes)
USER_CREDENTIALS = {
    "akshada": "aka123",
    "anuja": "anj123",
    "suhasi": "suh123"
}

# Function to validate login
def validate_user(username, password):
    if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
        return True
    return False

# Login page
def login(): 
    st.title("🔐 User Login")
    st.markdown("Please log in to access the **IEEE Database Management System**.")

    # Input fields
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Login button
    if st.button("Login"):
        if validate_user(username, password):
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.session_state["current_page"] = "🏠 Home"
            st.success(f"Welcome, {username}!")
            # After successful login
            st.experimental_set_query_params(logged_in="true")  # Reload the page to move to the main app
        else:
            st.error("Invalid username or password. Please try again.")


def home_page():
# Page Title
# Page Title
    st.title("🌐 Welcome to the IEEE Database Management System")

    # Introduction Section
    st.markdown(
        """
        The **IEEE Database Management System** is a comprehensive platform designed for academic researchers, 
        institutions, and enthusiasts to manage and analyze IEEE-related data. Whether you're managing publications, 
        exploring keywords, or tracking citation trends, this tool offers powerful and user-friendly functionalities.
        """
    )

    # Key Features Section
    st.header("🚀 Key Features")
    st.markdown(
        """
        - **🔍 Advanced Queries**: Perform complex queries like set operations, subqueries, OLAP queries, and more.
        - **📊 Visual Analytics**: View interactive charts and dashboards for better insights.
        - **📂 CRUD Operations**: Create, Read, Update, and Delete records for publications, authors, institutions, keywords, and more.
        - **🏆 Trend Analysis**: Discover publication trends, top authors, and highly cited keywords.
        """
    )

    # Application Pages Section
    st.header("📖 Explore Application Pages")
    st.markdown(
        """
        Navigate through the sidebar to explore the following pages:
        - **🏠 Home**: This overview page helps you understand the features and functionalities of the application.
        - **📖 Publications**: Manage and analyze publication records.
        - **🏫 Institutions**: Add, view, and update institution details.
        - **✍️ Authors**: Explore author data and their contribution to publications.
        - **🔑 Keywords**: Analyze keywords associated with various research topics.
        - **🔗 Citations**: Track citation trends and relations between publications.
        - **🎓 Conferences**: Manage conference data and explore their relation to publications.
        - **👤 Users**: Manage user records, including their details and interactions.
        - **📋 Members**: Explore membership details, roles, and related data.
        """
    )

    # CRUD Operations Guide
    st.header("📂 CRUD Operations")
    st.markdown(
        """
        This application allows you to perform the following CRUD operations on various data categories:
        - **Create**: Add new records for publications, authors, institutions, and more.
        - **Read**: View detailed data records with advanced query options.
        - **Update**: Modify existing data entries seamlessly.
        - **Delete**: Remove records that are no longer required.
        """
    )

    # Interactive Preview Section
    st.header("📈 Quick Insights")

        # Initialize variables with default values
    total_publications = 0
    top_keyword = "N/A"
    most_active_institution = "N/A"
    total_citations = 0

    # Connect to the database
    try:
        connection = connect_to_db()
        cursor = connection.cursor()

        # Total Publications
        cursor.execute("SELECT COUNT(*) FROM Publications;")
        result = cursor.fetchone()
        total_publications = result[0] if result else 0

        # Top Keyword by Usage
        cursor.execute("""
            SELECT K.keyword
            FROM Keywords K
            JOIN Pub_Key PK ON K.keyword_ID = PK.keyword_ID
            GROUP BY K.keyword
            ORDER BY COUNT(PK.publication_ID) DESC
            LIMIT 1;
        """)
        result = cursor.fetchone()
        top_keyword = result[0] if result else "N/A"

        # Most Active Institution
        cursor.execute("""
            SELECT I.inst_name
            FROM Institutions I
            JOIN Authors A ON I.institution_ID = A.institution_ID
            JOIN Pub_Author PA ON A.author_ID = PA.author_ID
            GROUP BY I.inst_name
            ORDER BY COUNT(PA.publication_ID) DESC
            LIMIT 1;
        """)
        result = cursor.fetchone()
        most_active_institution = result[0] if result else "N/A"

        # Total Citations
        cursor.execute("SELECT SUM(citation_count) FROM Citations;")
        result = cursor.fetchone()
        total_citations = result[0] if result and result[0] is not None else 0

    finally:
        cursor.close()
        connection.close()

    # Display Insights in Columns
    col1, col2 = st.columns(2)

    with col1:
        st.metric(label="Total Publications", value=f"{total_publications:,}")
        st.metric(label="Most Active Institution", value=most_active_institution)

    with col2:
        st.metric(label="Total Citations", value=f"{total_citations:,}")
        st.metric(label="Top Keyword", value=top_keyword)



# Institutions CRUD Operations
def institutions_crud():
    st.markdown("<h3 style='font-size:24px;'>Choose an Operation</h3>", unsafe_allow_html=True)
    crud_operation = st.selectbox("", ["🏢 Add Institution", "🔍 Explore Institutions", "✏️ Revise Institution Details", "❌ Remove Institution"])

    # CREATE Operation
    if crud_operation == "🏢 Add Institution":
        st.subheader("Add New Institution")
        institution_ID = st.text_input("Institution ID (e.g., INST001):")
        inst_name = st.text_input("Institution Name:")
        inst_addr = st.text_input("Institution Address:")
        inst_web_link = st.text_input("Institution Web Link:")
        associated_authors = st.text_input("Associated Authors (comma-separated):")

        if st.button("Submit"):
            try:
                connection = connect_to_db()
                cursor = connection.cursor()
                cursor.execute(
                    """INSERT INTO institutions 
                    (institution_ID, inst_name, inst_addr, inst_web_link, associated_authors) 
                    VALUES (%s, %s, %s, %s, %s)""",
                    (institution_ID, inst_name, inst_addr, inst_web_link, associated_authors)
                )
                connection.commit()
                st.success(f"Institution '{inst_name}' added successfully!")
            except mysql.connector.Error as error:
                st.error(f"Error: {error}")
            finally:
                cursor.close()
                connection.close()

    # READ Operation
    elif crud_operation == "🔍 Explore Institutions":
        st.subheader("View Institutions")
        view_option = st.selectbox("View Options", ["All Institutions", "Search by ID"])

        if view_option == "All Institutions":
            try:
                connection = connect_to_db()
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM institutions")
                records = cursor.fetchall()
                if records:
                    df = pd.DataFrame(records, columns=["ID", "Name", "Address", "Web Link", "Associated Authors"])
                    st.dataframe(df)
                else:
                    st.warning("No institutions found.")
            except mysql.connector.Error as error:
                st.error(f"Error: {error}")
            finally:
                cursor.close()
                connection.close()

        elif view_option == "Search by ID":
            search_id = st.text_input("Enter Institution ID:")
            if st.button("Search"):
                try:
                    connection = connect_to_db()
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM institutions WHERE institution_ID = %s", (search_id,))
                    record = cursor.fetchone()
                    if record:
                        df = pd.DataFrame([record], columns=["ID", "Name", "Address", "Web Link", "Associated Authors"])
                        st.table(df.transpose().rename(columns={0: "Value"}))
                    else:
                        st.warning("No institution found with that ID.")
                except mysql.connector.Error as error:
                    st.error(f"Error: {error}")
                finally:
                    cursor.close()
                    connection.close()

    # UPDATE Operation
    elif crud_operation == "✏️ Revise Institution Details":
        st.subheader("Update Institution")
        update_id = st.text_input("Enter Institution ID to Update:")

        if st.button("Fetch Details"):
            try:
                connection = connect_to_db()
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM institutions WHERE institution_ID = %s", (update_id,))
                record = cursor.fetchone()
                if record:
                    st.session_state['inst_name'] = record[1]
                    st.session_state['inst_addr'] = record[2]
                    st.session_state['inst_web_link'] = record[3]
                    st.session_state['associated_authors'] = record[4]
                    st.success("Details fetched successfully. You may update them below.")
                else:
                    st.warning("No institution found with that ID.")
            except mysql.connector.Error as error:
                st.error(f"Error: {error}")
            finally:
                cursor.close()
                connection.close()

        if 'inst_name' in st.session_state:
            inst_name = st.text_input("Institution Name:", st.session_state['inst_name'])
            inst_addr = st.text_input("Institution Address:", st.session_state['inst_addr'])
            inst_web_link = st.text_input("Institution Web Link:", st.session_state['inst_web_link'])
            associated_authors = st.text_input("Associated Authors (comma-separated):", st.session_state['associated_authors'])

            if st.button("Submit Update"):
                try:
                    connection = connect_to_db()
                    cursor = connection.cursor()
                    cursor.execute(
                        """UPDATE institutions SET inst_name = %s, inst_addr = %s, inst_web_link = %s, 
                        associated_authors = %s WHERE institution_ID = %s""",
                        (inst_name, inst_addr, inst_web_link, associated_authors, update_id)
                    )
                    connection.commit()
                    st.success("Institution updated successfully!")
                    del st.session_state['inst_name']
                    del st.session_state['inst_addr']
                    del st.session_state['inst_web_link']
                    del st.session_state['associated_authors']
                except mysql.connector.Error as error:
                    st.error(f"Error: {error}")
                finally:
                    cursor.close()
                    connection.close()

    # DELETE Operation
    elif crud_operation == "❌ Remove Institution":
        st.subheader("Delete Institution")
        delete_id = st.text_input("Enter Institution ID to Delete:")
        confirm_delete = st.checkbox("I confirm deletion of this institution.")

        if st.button("Confirm Delete") and confirm_delete:
            try:
                connection = connect_to_db()
                cursor = connection.cursor()
                cursor.execute("DELETE FROM institutions WHERE institution_ID = %s", (delete_id,))
                connection.commit()
                st.success(f"Institution ID {delete_id} deleted successfully!")
            except mysql.connector.Error as error:
                st.error(f"Error: {error}")
            finally:
                cursor.close()
                connection.close()

# Publications CRUD Operations
def publications_crud():
    st.markdown("<h3 style='font-size:24px;'>Choose an Operation</h3>", unsafe_allow_html=True)
    crud_operation = st.selectbox("", ["📝 Submit New Publication", "📖 Review Publications", "✏️ Update Publication Info", "❌ Withdraw Publication"])

    # CREATE Operation
    if crud_operation == "📝 Submit New Publication":
        st.subheader("Add New Publication")
        publication_ID = st.text_input("Publication ID (numeric):")
        paper_name = st.text_input("Paper Name:")
        publisher = st.text_input("Publisher:")
        DOI = st.text_input("DOI:")
        date_of_conference = st.date_input("Date of Conference:")
        date_of_publication = st.date_input("Date of Publication:")
        print_ISSN = st.text_input("Print ISSN:")
        print_ISBN = st.text_input("Print ISBN:")
        conference_ID = st.text_input("Conference ID:")

        if st.button("Submit"):
            try:
                connection = connect_to_db()
                cursor = connection.cursor()
                cursor.execute(
                    """INSERT INTO publications 
                    (publication_ID, paper_name, publisher, DOI, date_of_conference, date_of_publication, 
                     print_ISSN, print_ISBN, conference_ID) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (publication_ID, paper_name, publisher, DOI, date_of_conference, date_of_publication,
                     print_ISSN, print_ISBN, conference_ID)
                )
                connection.commit()
                st.success(f"Publication '{paper_name}' added successfully!")
            except mysql.connector.Error as error:
                st.error(f"Error: {error}")
            finally:
                cursor.close()
                connection.close()

    # READ Operation
    elif crud_operation == "📖 Review Publications":
        st.subheader("View Publications")
        view_option = st.selectbox("View Options", ["All Publications", "Search by ID"])

        if view_option == "All Publications":
            try:
                connection = connect_to_db()
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM publications")
                records = cursor.fetchall()
                if records:
                    df = pd.DataFrame(records, columns=["ID", "Name", "Publisher", "DOI", "Date of Conference", 
                                                        "Date of Publication", "Print ISSN", "Print ISBN", "Conference ID"])
                    st.dataframe(df)
                else:
                    st.warning("No publications found.")
            except mysql.connector.Error as error:
                st.error(f"Error: {error}")
            finally:
                cursor.close()
                connection.close()

        elif view_option == "Search by ID":
            search_id = st.text_input("Enter Publication ID:")
            if st.button("Search"):
                try:
                    connection = connect_to_db()
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM publications WHERE publication_ID = %s", (search_id,))
                    record = cursor.fetchone()
                    if record:
                        df = pd.DataFrame([record], columns=["ID", "Name", "Publisher", "DOI", "Date of Conference", 
                                                             "Date of Publication", "Print ISSN", "Print ISBN", "Conference ID"])
                        st.table(df.transpose().rename(columns={0: "Value"}))
                    else:
                        st.warning("No publication found with that ID.")
                except mysql.connector.Error as error:
                    st.error(f"Error: {error}")
                finally:
                    cursor.close()
                    connection.close()

    # UPDATE Operation
    elif crud_operation == "✏️ Update Publication Info":
        st.subheader("Update Publication")
        update_id = st.text_input("Enter Publication ID to Update:")

        if st.button("Fetch Details"):
            try:
                connection = connect_to_db()
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM publications WHERE publication_ID = %s", (update_id,))
                record = cursor.fetchone()
                if record:
                    st.session_state['paper_name'] = record[1]
                    st.session_state['publisher'] = record[2]
                    st.session_state['DOI'] = record[3]
                    st.session_state['date_of_conference'] = record[4]
                    st.session_state['date_of_publication'] = record[5]
                    st.session_state['print_ISSN'] = record[6]
                    st.session_state['print_ISBN'] = record[7]
                    st.session_state['conference_ID'] = record[8]
                    st.success("Details fetched successfully. You may update them below.")
                else:
                    st.warning("No publication found with that ID.")
            except mysql.connector.Error as error:
                st.error(f"Error: {error}")
            finally:
                cursor.close()
                connection.close()

        if 'paper_name' in st.session_state:
            paper_name = st.text_input("Paper Name:", st.session_state['paper_name'])
            publisher = st.text_input("Publisher:", st.session_state['publisher'])
            DOI = st.text_input("DOI:", st.session_state['DOI'])
            date_of_conference = st.date_input("Date of Conference:", st.session_state['date_of_conference'])
            date_of_publication = st.date_input("Date of Publication:", st.session_state['date_of_publication'])
            print_ISSN = st.text_input("Print ISSN:", st.session_state['print_ISSN'])
            print_ISBN = st.text_input("Print ISBN:", st.session_state['print_ISBN'])
            conference_ID = st.text_input("Conference ID:", st.session_state['conference_ID'])

            if st.button("Submit Update"):
                try:
                    connection = connect_to_db()
                    cursor = connection.cursor()
                    cursor.execute(
                        """UPDATE publications SET paper_name = %s, publisher = %s, DOI = %s, 
                        date_of_conference = %s, date_of_publication = %s, print_ISSN = %s, 
                        print_ISBN = %s, conference_ID = %s WHERE publication_ID = %s""",
                        (paper_name, publisher, DOI, date_of_conference, date_of_publication,
                         print_ISSN, print_ISBN, conference_ID, update_id)
                    )
                    connection.commit()
                    st.success("Publication updated successfully!")
                    for key in ['paper_name', 'publisher', 'DOI', 'date_of_conference', 
                                'date_of_publication', 'print_ISSN', 'print_ISBN', 'conference_ID']:
                        del st.session_state[key]
                except mysql.connector.Error as error:
                    st.error(f"Error: {error}")
                finally:
                    cursor.close()
                    connection.close()

    # DELETE Operation
    elif crud_operation == "❌ Withdraw Publication":
        st.subheader("Delete Publication")
        delete_id = st.text_input("Enter Publication ID to Delete:")
        confirm_delete = st.checkbox("I confirm deletion of this publication.")

        if st.button("Confirm Delete") and confirm_delete:
            try:
                connection = connect_to_db()
                cursor = connection.cursor()
                cursor.execute("DELETE FROM publications WHERE publication_ID = %s", (delete_id,))
                connection.commit()
                st.success(f"Publication ID {delete_id} deleted successfully!")
            except mysql.connector.Error as error:
                st.error(f"Error: {error}")
            finally:
                cursor.close()
                connection.close()


# Topics CRUD Operations
def topics_crud():
    st.markdown("<h3 style='font-size:24px;'>Choose an Operation</h3>", unsafe_allow_html=True)
    crud_operation = st.selectbox("", ["🆕 Add Research Topic","📂 Explore Topics", "✏️ Revise Topic Details", "❌ Remove Topic"])

    # CREATE Operation
    if crud_operation == "🆕 Add Research Topic":
        st.subheader("Add New Topic")
        topic_ID = st.text_input("Topic ID (up to 10 characters):")
        topic_name = st.text_input("Topic Name (up to 70 characters):")
        topic_pub_count = st.number_input("Topic Publication Count (numeric):", min_value=0, step=1)

        if st.button("Submit"):
            try:
                connection = connect_to_db()
                cursor = connection.cursor()
                cursor.execute(
                    """INSERT INTO Topics (topic_ID, topic_name, topic_pub_count) 
                    VALUES (%s, %s, %s)""",
                    (topic_ID, topic_name, topic_pub_count)
                )
                connection.commit()
                st.success(f"Topic '{topic_name}' added successfully!")
            except mysql.connector.Error as error:
                st.error(f"Error: {error}")
            finally:
                cursor.close()
                connection.close()

    # READ Operation
    elif crud_operation == "📂 Explore Topics":
        st.subheader("View Topics")
        view_option = st.selectbox("View Options", ["All Topics", "Search by ID"])

        if view_option == "All Topics":
            try:
                connection = connect_to_db()
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM Topics")
                records = cursor.fetchall()
                if records:
                    df = pd.DataFrame(records, columns=["ID", "Name", "Publication Count"])
                    st.dataframe(df)
                else:
                    st.warning("No topics found.")
            except mysql.connector.Error as error:
                st.error(f"Error: {error}")
            finally:
                cursor.close()
                connection.close()

        elif view_option == "Search by ID":
            search_id = st.text_input("Enter Topic ID:")
            if st.button("Search"):
                try:
                    connection = connect_to_db()
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM Topics WHERE topic_ID = %s", (search_id,))
                    record = cursor.fetchone()
                    if record:
                        df = pd.DataFrame([record], columns=["ID", "Name", "Publication Count"])
                        st.table(df.transpose().rename(columns={0: "Value"}))
                    else:
                        st.warning("No topic found with that ID.")
                except mysql.connector.Error as error:
                    st.error(f"Error: {error}")
                finally:
                    cursor.close()
                    connection.close()

    # UPDATE Operation
    elif crud_operation == "✏️ Revise Topic Details":
        st.subheader("Update Topic")
        update_id = st.text_input("Enter Topic ID to Update:")

        if st.button("Fetch Details"):
            try:
                connection = connect_to_db()
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM Topics WHERE topic_ID = %s", (update_id,))
                record = cursor.fetchone()
                if record:
                    st.session_state['topic_name'] = record[1]
                    st.session_state['topic_pub_count'] = record[2]
                    st.success("Details fetched successfully. You may update them below.")
                else:
                    st.warning("No topic found with that ID.")
            except mysql.connector.Error as error:
                st.error(f"Error: {error}")
            finally:
                cursor.close()
                connection.close()

        if 'topic_name' in st.session_state:
            topic_name = st.text_input("Topic Name (up to 70 characters):", st.session_state['topic_name'])
            topic_pub_count = st.number_input("Publication Count (numeric):", min_value=0, step=1, value=st.session_state['topic_pub_count'])

            if st.button("Submit Update"):
                try:
                    connection = connect_to_db()
                    cursor = connection.cursor()
                    cursor.execute(
                        """UPDATE Topics SET topic_name = %s, topic_pub_count = %s WHERE topic_ID = %s""",
                        (topic_name, topic_pub_count, update_id)
                    )
                    connection.commit()
                    st.success("Topic updated successfully!")
                    del st.session_state['topic_name']
                    del st.session_state['topic_pub_count']
                except mysql.connector.Error as error:
                    st.error(f"Error: {error}")
                finally:
                    cursor.close()
                    connection.close()

    # DELETE Operation
    elif crud_operation == "❌ Remove Topic":
        st.subheader("Delete Topic")
        delete_id = st.text_input("Enter Topic ID to Delete:")
        confirm_delete = st.checkbox("I confirm deletion of this topic.")

        if st.button("Confirm Delete") and confirm_delete:
            try:
                connection = connect_to_db()
                cursor = connection.cursor()
                cursor.execute("DELETE FROM Topics WHERE topic_ID = %s", (delete_id,))
                connection.commit()
                st.success(f"Topic ID {delete_id} deleted successfully!")
            except mysql.connector.Error as error:
                st.error(f"Error: {error}")
            finally:
                cursor.close()
                connection.close()


def citations_crud():
    st.markdown("<h3 style='font-size:24px;'>Choose an Operation</h3>", unsafe_allow_html=True)
    crud_operation = st.selectbox("", ["🔗 Add Citation", "📖 Review Citations", "✏️ Edit Citation Info", "❌ Remove Citation"])

    # CREATE Operation
    if crud_operation == "🔗 Add Citation":
        st.subheader("Add New Citation")
        citation_ID = st.text_input("Citation ID (up to 10 characters):")
        citing_pub = st.text_input("Citing Publication Name (up to 70 characters):")
        cited_pub = st.text_input("Cited Publication Name (up to 70 characters):")
        cited_paper_links = st.text_input("Cited Paper Links (up to 50 characters):")
        citation_count = st.number_input("Citation Count (numeric):", min_value=0, step=1)

        if st.button("Submit"):
            try:
                connection = connect_to_db()
                cursor = connection.cursor()
                cursor.execute(
                    """INSERT INTO Citations (citation_ID, citing_pub, cited_pub, cited_paper_links, citation_count) 
                    VALUES (%s, %s, %s, %s, %s)""",
                    (citation_ID, citing_pub, cited_pub, cited_paper_links, citation_count)
                )
                connection.commit()
                st.success(f"Citation '{citation_ID}' added successfully!")
            except mysql.connector.Error as error:
                st.error(f"Error: {error}")
            finally:
                cursor.close()
                connection.close()

    # READ Operation
    elif crud_operation == "📖 Review Citations":
        st.subheader("View Citations")
        view_option = st.selectbox("View Options", ["All Citations", "Search by ID"])

        if view_option == "All Citations":
            try:
                connection = connect_to_db()
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM Citations")
                records = cursor.fetchall()
                if records:
                    df = pd.DataFrame(records, columns=["ID", "Citing Publication", "Cited Publication", "Cited Paper Links", "Citation Count"])
                    st.dataframe(df)
                else:
                    st.warning("No citations found.")
            except mysql.connector.Error as error:
                st.error(f"Error: {error}")
            finally:
                cursor.close()
                connection.close()

        elif view_option == "Search by ID":
            search_id = st.text_input("Enter Citation ID:")
            if st.button("Search"):
                try:
                    connection = connect_to_db()
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM Citations WHERE citation_ID = %s", (search_id,))
                    record = cursor.fetchone()
                    if record:
                        df = pd.DataFrame([record], columns=["ID", "Citing Publication", "Cited Publication", "Cited Paper Links", "Citation Count"])
                        st.table(df.transpose().rename(columns={0: "Value"}))
                    else:
                        st.warning("No citation found with that ID.")
                except mysql.connector.Error as error:
                    st.error(f"Error: {error}")
                finally:
                    cursor.close()
                    connection.close()

    # UPDATE Operation
    elif crud_operation == "✏️ Edit Citation Info":
        st.subheader("Update Citation")
        update_id = st.text_input("Enter Citation ID to Update:")

        if st.button("Fetch Details"):
            try:
                connection = connect_to_db()
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM Citations WHERE citation_ID = %s", (update_id,))
                record = cursor.fetchone()
                if record:
                    st.session_state['citing_pub'] = record[1]
                    st.session_state['cited_pub'] = record[2]
                    st.session_state['cited_paper_links'] = record[3]
                    st.session_state['citation_count'] = record[4]
                    st.success("Details fetched successfully. You may update them below.")
                else:
                    st.warning("No citation found with that ID.")
            except mysql.connector.Error as error:
                st.error(f"Error: {error}")
            finally:
                cursor.close()
                connection.close()

        if 'citing_pub' in st.session_state:
            citing_pub = st.text_input("Citing Publication Name:", st.session_state['citing_pub'])
            cited_pub = st.text_input("Cited Publication Name:", st.session_state['cited_pub'])
            cited_paper_links = st.text_input("Cited Paper Links:", st.session_state['cited_paper_links'])
            citation_count = st.number_input("Citation Count (numeric):", min_value=0, step=1, value=st.session_state['citation_count'])

            if st.button("Submit Update"):
                try:
                    connection = connect_to_db()
                    cursor = connection.cursor()
                    cursor.execute(
                        """UPDATE Citations SET citing_pub = %s, cited_pub = %s, cited_paper_links = %s, 
                        citation_count = %s WHERE citation_ID = %s""",
                        (citing_pub, cited_pub, cited_paper_links, citation_count, update_id)
                    )
                    connection.commit()
                    st.success("Citation updated successfully!")
                    for key in ['citing_pub', 'cited_pub', 'cited_paper_links', 'citation_count']:
                        del st.session_state[key]
                except mysql.connector.Error as error:
                    st.error(f"Error: {error}")
                finally:
                    cursor.close()
                    connection.close()

    # DELETE Operation
    elif crud_operation == "❌ Remove Citation":
        st.subheader("Delete Citation")
        delete_id = st.text_input("Enter Citation ID to Delete:")
        confirm_delete = st.checkbox("I confirm deletion of this citation.")

        if st.button("Confirm Delete") and confirm_delete:
            try:
                connection = connect_to_db()
                cursor = connection.cursor()
                cursor.execute("DELETE FROM Citations WHERE citation_ID = %s", (delete_id,))
                connection.commit()
                st.success(f"Citation ID {delete_id} deleted successfully!")
            except mysql.connector.Error as error:
                st.error(f"Error: {error}")
            finally:
                cursor.close()
                connection.close()


def conferences_crud():
    st.markdown("<h3 style='font-size:24px;'>Choose an Operation</h3>", unsafe_allow_html=True)
    crud_operation = st.selectbox("", ["🎓 Add New Conference", "🔍 Explore Conferences", "✏️ Update Conference Details", "❌ Remove Conference"])

    # CREATE Operation
    if crud_operation == "🎓 Add New Conference":
        st.subheader("Add New Conference")
        conference_ID = st.text_input("Conference ID (up to 10 characters):")
        conference_name = st.text_input("Conference Name (up to 120 characters):")
        conference_year = st.number_input("Conference Year (numeric):", min_value=1900, max_value=2100, step=1)
        conference_location = st.text_input("Conference Location (up to 50 characters):")

        if st.button("Submit"):
            try:
                connection = connect_to_db()
                cursor = connection.cursor()
                cursor.execute(
                    """INSERT INTO Conferences (conference_ID, conference_name, conference_year, conference_location) 
                    VALUES (%s, %s, %s, %s)""",
                    (conference_ID, conference_name, int(conference_year), conference_location)
                )
                connection.commit()
                st.success(f"Conference '{conference_name}' added successfully!")
            except mysql.connector.Error as error:
                st.error(f"Error: {error}")
            finally:
                cursor.close()
                connection.close()

    # READ Operation
    elif crud_operation == "🔍 Explore Conferences":
        st.subheader("View Conferences")
        view_option = st.selectbox("View Options", ["All Conferences", "Search by ID"])

        if view_option == "All Conferences":
            try:
                connection = connect_to_db()
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM Conferences")
                records = cursor.fetchall()
                if records:
                    df = pd.DataFrame(records, columns=["ID", "Name", "Year", "Location"])
                    st.dataframe(df)
                else:
                    st.warning("No conferences found.")
            except mysql.connector.Error as error:
                st.error(f"Error: {error}")
            finally:
                cursor.close()
                connection.close()

        elif view_option == "Search by ID":
            search_id = st.text_input("Enter Conference ID:")
            if st.button("Search"):
                try:
                    connection = connect_to_db()
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM Conferences WHERE conference_ID = %s", (search_id,))
                    record = cursor.fetchone()
                    if record:
                        df = pd.DataFrame([record], columns=["ID", "Name", "Year", "Location"])
                        st.table(df.transpose().rename(columns={0: "Value"}))
                    else:
                        st.warning("No conference found with that ID.")
                except mysql.connector.Error as error:
                    st.error(f"Error: {error}")
                finally:
                    cursor.close()
                    connection.close()

    # UPDATE Operation
    elif crud_operation == "✏️ Update Conference Details":
        st.subheader("Update Conference")
        update_id = st.text_input("Enter Conference ID to Update:")

        if st.button("Fetch Details"):
            try:
                connection = connect_to_db()
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM Conferences WHERE conference_ID = %s", (update_id,))
                record = cursor.fetchone()
                if record:
                    st.session_state['conference_name'] = record[1]
                    st.session_state['conference_year'] = record[2]
                    st.session_state['conference_location'] = record[3]
                    st.success("Details fetched successfully. You may update them below.")
                else:
                    st.warning("No conference found with that ID.")
            except mysql.connector.Error as error:
                st.error(f"Error: {error}")
            finally:
                cursor.close()
                connection.close()

        if 'conference_name' in st.session_state:
            conference_name = st.text_input("Conference Name:", st.session_state['conference_name'])
            conference_year = st.number_input("Conference Year (numeric):", min_value=1900, max_value=2100, step=1, value=st.session_state['conference_year'])
            conference_location = st.text_input("Conference Location:", st.session_state['conference_location'])

            if st.button("Submit Update"):
                try:
                    connection = connect_to_db()
                    cursor = connection.cursor()
                    cursor.execute(
                        """UPDATE Conferences SET conference_name = %s, conference_year = %s, conference_location = %s 
                        WHERE conference_ID = %s""",
                        (conference_name, int(conference_year), conference_location, update_id)
                    )
                    connection.commit()
                    st.success("Conference updated successfully!")
                    for key in ['conference_name', 'conference_year', 'conference_location']:
                        del st.session_state[key]
                except mysql.connector.Error as error:
                    st.error(f"Error: {error}")
                finally:
                    cursor.close()
                    connection.close()

    # DELETE Operation
    elif crud_operation == "❌ Remove Conference":
        st.subheader("Delete Conference")
        delete_id = st.text_input("Enter Conference ID to Delete:")
        confirm_delete = st.checkbox("I confirm deletion of this conference.")

        if st.button("Confirm Delete") and confirm_delete:
            try:
                connection = connect_to_db()
                cursor = connection.cursor()
                cursor.execute("DELETE FROM Conferences WHERE conference_ID = %s", (delete_id,))
                connection.commit()
                st.success(f"Conference ID {delete_id} deleted successfully!")
            except mysql.connector.Error as error:
                st.error(f"Error: {error}")
            finally:
                cursor.close()
                connection.close()


def users_crud():
    st.markdown("<h3 style='font-size:24px;'>Choose an Operation</h3>", unsafe_allow_html=True)
    crud_operation = st.selectbox("", ["👤 Add New User", "📖 View User Info", "✏️ Update User Details", "❌ Delete User"])

    # CREATE Operation
    if crud_operation == "👤 Add New User":
        st.subheader("Add New User")
        user_ID = st.text_input("User ID (up to 10 characters):")
        user_name = st.text_input("User Name (up to 25 characters):")
        user_email = st.text_input("User Email (up to 30 characters):")
        user_contact_no = st.text_input("User Contact Number (up to 12 characters):")
        sub_status = st.text_input("Subscription Status (up to 10 characters):")
        subscription = st.text_input("Subscription Type (up to 10 characters):")
        profession = st.text_input("Profession (up to 25 characters):")

        if st.button("Submit"):
            try:
                connection = connect_to_db()
                cursor = connection.cursor()
                cursor.execute(
                    """INSERT INTO Users (user_ID, user_name, user_email, user_contact_no, sub_status, 
                    subscription, profession) VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    (user_ID, user_name, user_email, user_contact_no, sub_status, subscription, profession)
                )
                connection.commit()
                st.success(f"User '{user_name}' added successfully!")
            except mysql.connector.Error as error:
                st.error(f"Error: {error}")
            finally:
                cursor.close()
                connection.close()

    # READ Operation
    elif crud_operation == "📖 View User Info":
        st.subheader("View Users")
        view_option = st.selectbox("View Options", ["All Users", "Search by ID"])

        if view_option == "All Users":
            try:
                connection = connect_to_db()
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM Users")
                records = cursor.fetchall()
                if records:
                    df = pd.DataFrame(records, columns=["ID", "Name", "Email", "Contact No", "Subscription Status", 
                                                        "Subscription Type", "Profession"])
                    st.dataframe(df)
                else:
                    st.warning("No users found.")
            except mysql.connector.Error as error:
                st.error(f"Error: {error}")
            finally:
                cursor.close()
                connection.close()

        elif view_option == "Search by ID":
            search_id = st.text_input("Enter User ID:")
            if st.button("Search"):
                try:
                    connection = connect_to_db()
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM Users WHERE user_ID = %s", (search_id,))
                    record = cursor.fetchone()
                    if record:
                        df = pd.DataFrame([record], columns=["ID", "Name", "Email", "Contact No", "Subscription Status", 
                                                             "Subscription Type", "Profession"])
                        st.table(df.transpose().rename(columns={0: "Value"}))
                    else:
                        st.warning("No user found with that ID.")
                except mysql.connector.Error as error:
                    st.error(f"Error: {error}")
                finally:
                    cursor.close()
                    connection.close()

    # UPDATE Operation
    elif crud_operation == "✏️ Update User Details":
        st.subheader("Update User")
        update_id = st.text_input("Enter User ID to Update:")

        if st.button("Fetch Details"):
            try:
                connection = connect_to_db()
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM Users WHERE user_ID = %s", (update_id,))
                record = cursor.fetchone()
                if record:
                    st.session_state['user_name'] = record[1]
                    st.session_state['user_email'] = record[2]
                    st.session_state['user_contact_no'] = record[3]
                    st.session_state['sub_status'] = record[4]
                    st.session_state['subscription'] = record[5]
                    st.session_state['profession'] = record[6]
                    st.success("Details fetched successfully. You may update them below.")
                else:
                    st.warning("No user found with that ID.")
            except mysql.connector.Error as error:
                st.error(f"Error: {error}")
            finally:
                cursor.close()
                connection.close()

        if 'user_name' in st.session_state:
            user_name = st.text_input("User Name:", st.session_state['user_name'])
            user_email = st.text_input("User Email:", st.session_state['user_email'])
            user_contact_no = st.text_input("User Contact Number:", st.session_state['user_contact_no'])
            sub_status = st.text_input("Subscription Status:", st.session_state['sub_status'])
            subscription = st.text_input("Subscription Type:", st.session_state['subscription'])
            profession = st.text_input("Profession:", st.session_state['profession'])

            if st.button("Submit Update"):
                try:
                    connection = connect_to_db()
                    cursor = connection.cursor()
                    cursor.execute(
                        """UPDATE Users SET user_name = %s, user_email = %s, user_contact_no = %s, sub_status = %s, 
                        subscription = %s, profession = %s WHERE user_ID = %s""",
                        (user_name, user_email, user_contact_no, sub_status, subscription, profession, update_id)
                    )
                    connection.commit()
                    st.success("User updated successfully!")
                    for key in ['user_name', 'user_email', 'user_contact_no', 'sub_status', 'subscription', 'profession']:
                        del st.session_state[key]
                except mysql.connector.Error as error:
                    st.error(f"Error: {error}")
                finally:
                    cursor.close()
                    connection.close()

    # DELETE Operation
    elif crud_operation == "❌ Delete User":
        st.subheader("Delete User")
        delete_id = st.text_input("Enter User ID to Delete:")
        confirm_delete = st.checkbox("I confirm deletion of this user.")

        if st.button("Confirm Delete") and confirm_delete:
            try:
                connection = connect_to_db()
                cursor = connection.cursor()
                cursor.execute("DELETE FROM Users WHERE user_ID = %s", (delete_id,))
                connection.commit()
                st.success(f"User ID {delete_id} deleted successfully!")
            except mysql.connector.Error as error:
                st.error(f"Error: {error}")
            finally:
                cursor.close()
                connection.close()


def authors_crud():
    st.markdown("<h3 style='font-size:24px;'>Choose an Operation</h3>", unsafe_allow_html=True)
    crud_operation = st.selectbox("", ["✍️ Add New Author", "📖 Explore Authors", "✏️ Edit Author Info", "❌ Remove Author"])

    # CREATE Operation
    if crud_operation == "✍️ Add New Author":
        st.subheader("Add New Author")
        author_ID = st.text_input("Author ID (up to 10 characters):")
        author_name = st.text_input("Author Name (up to 25 characters):")
        no_of_publications = st.number_input("Number of Publications (numeric):", min_value=0, step=1)
        no_of_citations = st.number_input("Number of Citations (numeric):", min_value=0, step=1)
        institution_ID = st.text_input("Institution ID (up to 10 characters):")
        topic_ID = st.text_input("Topic ID (up to 10 characters):")

        if st.button("Submit"):
            try:
                connection = connect_to_db()
                cursor = connection.cursor()
                cursor.execute(
                    """INSERT INTO Authors (author_ID, author_name, no_of_publications, no_of_citations, 
                    institution_ID, topic_ID) VALUES (%s, %s, %s, %s, %s, %s)""",
                    (author_ID, author_name, int(no_of_publications), int(no_of_citations), institution_ID, topic_ID)
                )
                connection.commit()
                st.success(f"Author '{author_name}' added successfully!")
            except mysql.connector.Error as error:
                st.error(f"Error: {error}")
            finally:
                cursor.close()
                connection.close()

    # READ Operation
    elif crud_operation == "📖 Explore Authors":
        st.subheader("View Authors")
        view_option = st.selectbox("View Options", ["All Authors", "Search by ID"])

        if view_option == "All Authors":
            try:
                connection = connect_to_db()
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM Authors")
                records = cursor.fetchall()
                if records:
                    df = pd.DataFrame(records, columns=["ID", "Name", "Publications", "Citations", "Institution ID", "Topic ID"])
                    st.dataframe(df)
                else:
                    st.warning("No authors found.")
            except mysql.connector.Error as error:
                st.error(f"Error: {error}")
            finally:
                cursor.close()
                connection.close()

        elif view_option == "Search by ID":
            search_id = st.text_input("Enter Author ID:")
            if st.button("Search"):
                try:
                    connection = connect_to_db()
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM Authors WHERE author_ID = %s", (search_id,))
                    record = cursor.fetchone()
                    if record:
                        df = pd.DataFrame([record], columns=["ID", "Name", "Publications", "Citations", "Institution ID", "Topic ID"])
                        st.table(df.transpose().rename(columns={0: "Value"}))
                    else:
                        st.warning("No author found with that ID.")
                except mysql.connector.Error as error:
                    st.error(f"Error: {error}")
                finally:
                    cursor.close()
                    connection.close()

    # UPDATE Operation
    elif crud_operation == "✏️ Edit Author Info":
        st.subheader("Update Author")
        update_id = st.text_input("Enter Author ID to Update:")

        if st.button("Fetch Details"):
            try:
                connection = connect_to_db()
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM Authors WHERE author_ID = %s", (update_id,))
                record = cursor.fetchone()
                if record:
                    st.session_state['author_name'] = record[1]
                    st.session_state['no_of_publications'] = record[2]
                    st.session_state['no_of_citations'] = record[3]
                    st.session_state['institution_ID'] = record[4]
                    st.session_state['topic_ID'] = record[5]
                    st.success("Details fetched successfully. You may update them below.")
                else:
                    st.warning("No author found with that ID.")
            except mysql.connector.Error as error:
                st.error(f"Error: {error}")
            finally:
                cursor.close()
                connection.close()

        if 'author_name' in st.session_state:
            author_name = st.text_input("Author Name:", st.session_state['author_name'])
            no_of_publications = st.number_input("Number of Publications (numeric):", min_value=0, step=1, value=st.session_state['no_of_publications'])
            no_of_citations = st.number_input("Number of Citations (numeric):", min_value=0, step=1, value=st.session_state['no_of_citations'])
            institution_ID = st.text_input("Institution ID:", st.session_state['institution_ID'])
            topic_ID = st.text_input("Topic ID:", st.session_state['topic_ID'])

            if st.button("Submit Update"):
                try:
                    connection = connect_to_db()
                    cursor = connection.cursor()
                    cursor.execute(
                        """UPDATE Authors SET author_name = %s, no_of_publications = %s, no_of_citations = %s, 
                        institution_ID = %s, topic_ID = %s WHERE author_ID = %s""",
                        (author_name, no_of_publications, no_of_citations, institution_ID, topic_ID, update_id)
                    )
                    connection.commit()
                    st.success("Author updated successfully!")
                    for key in ['author_name', 'no_of_publications', 'no_of_citations', 'institution_ID', 'topic_ID']:
                        del st.session_state[key]
                except mysql.connector.Error as error:
                    st.error(f"Error: {error}")
                finally:
                    cursor.close()
                    connection.close()

    # DELETE Operation
    elif crud_operation == "❌ Remove Author":
        st.subheader("Delete Author")
        delete_id = st.text_input("Enter Author ID to Delete:")
        confirm_delete = st.checkbox("I confirm deletion of this author.")

        if st.button("Confirm Delete") and confirm_delete:
            try:
                connection = connect_to_db()
                cursor = connection.cursor()
                cursor.execute("DELETE FROM Authors WHERE author_ID = %s", (delete_id,))
                connection.commit()
                st.success(f"Author ID {delete_id} deleted successfully!")
            except mysql.connector.Error as error:
                st.error(f"Error: {error}")
            finally:
                cursor.close()
                connection.close()


def keywords_crud():
    st.markdown("<h3 style='font-size:24px;'>Choose an Operation</h3>", unsafe_allow_html=True)
    crud_operation = st.selectbox("", ["🔑 Add New Keyword", "🔍 Browse Keywords", "✏️ Revise Keyword Info", "❌ Remove Keyword"])

    # CREATE Operation
    if crud_operation == "🔑 Add New Keyword":
        st.subheader("Add New Keyword")
        keyword_ID = st.text_input("Keyword ID (up to 10 characters):")
        topic_ID = st.text_input("Topic ID (up to 10 characters):")
        keyword = st.text_input("Keyword (up to 50 characters):")
        kw_pub_count = st.number_input("Keyword Publication Count (numeric):", min_value=0, step=1)

        if st.button("Submit"):
            try:
                connection = connect_to_db()
                cursor = connection.cursor()
                cursor.execute(
                    """INSERT INTO Keywords (keyword_ID, topic_ID, keyword, kw_pub_count) 
                    VALUES (%s, %s, %s, %s)""",
                    (keyword_ID, topic_ID, keyword, int(kw_pub_count))
                )
                connection.commit()
                st.success(f"Keyword '{keyword}' added successfully!")
            except mysql.connector.Error as error:
                st.error(f"Error: {error}")
            finally:
                cursor.close()
                connection.close()

    # READ Operation
    elif crud_operation == "🔍 Browse Keywords":
        st.subheader("View Keywords")
        view_option = st.selectbox("View Options", ["All Keywords", "Search by ID"])

        if view_option == "All Keywords":
            try:
                connection = connect_to_db()
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM Keywords")
                records = cursor.fetchall()
                if records:
                    df = pd.DataFrame(records, columns=["ID", "Topic ID", "Keyword", "Publication Count"])
                    st.dataframe(df)
                else:
                    st.warning("No keywords found.")
            except mysql.connector.Error as error:
                st.error(f"Error: {error}")
            finally:
                cursor.close()
                connection.close()

        elif view_option == "Search by ID":
            search_id = st.text_input("Enter Keyword ID:")
            if st.button("Search"):
                try:
                    connection = connect_to_db()
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM Keywords WHERE keyword_ID = %s", (search_id,))
                    record = cursor.fetchone()
                    if record:
                        df = pd.DataFrame([record], columns=["ID", "Topic ID", "Keyword", "Publication Count"])
                        st.table(df.transpose().rename(columns={0: "Value"}))
                    else:
                        st.warning("No keyword found with that ID.")
                except mysql.connector.Error as error:
                    st.error(f"Error: {error}")
                finally:
                    cursor.close()
                    connection.close()

    # UPDATE Operation
    elif crud_operation == "✏️ Revise Keyword Info":
        st.subheader("Update Keyword")
        update_id = st.text_input("Enter Keyword ID to Update:")

        if st.button("Fetch Details"):
            try:
                connection = connect_to_db()
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM Keywords WHERE keyword_ID = %s", (update_id,))
                record = cursor.fetchone()
                if record:
                    st.session_state['topic_ID'] = record[1]
                    st.session_state['keyword'] = record[2]
                    st.session_state['kw_pub_count'] = record[3]
                    st.success("Details fetched successfully. You may update them below.")
                else:
                    st.warning("No keyword found with that ID.")
            except mysql.connector.Error as error:
                st.error(f"Error: {error}")
            finally:
                cursor.close()
                connection.close()

        if 'topic_ID' in st.session_state:
            topic_ID = st.text_input("Topic ID:", st.session_state['topic_ID'])
            keyword = st.text_input("Keyword:", st.session_state['keyword'])
            kw_pub_count = st.number_input("Publication Count (numeric):", min_value=0, step=1, value=st.session_state['kw_pub_count'])

            if st.button("Submit Update"):
                try:
                    connection = connect_to_db()
                    cursor = connection.cursor()
                    cursor.execute(
                        """UPDATE Keywords SET topic_ID = %s, keyword = %s, kw_pub_count = %s 
                        WHERE keyword_ID = %s""",
                        (topic_ID, keyword, kw_pub_count, update_id)
                    )
                    connection.commit()
                    st.success("Keyword updated successfully!")
                    for key in ['topic_ID', 'keyword', 'kw_pub_count']:
                        del st.session_state[key]
                except mysql.connector.Error as error:
                    st.error(f"Error: {error}")
                finally:
                    cursor.close()
                    connection.close()

    # DELETE Operation
    elif crud_operation == "❌ Remove Keyword":
        st.subheader("Delete Keyword")
        delete_id = st.text_input("Enter Keyword ID to Delete:")
        confirm_delete = st.checkbox("I confirm deletion of this keyword.")

        if st.button("Confirm Delete") and confirm_delete:
            try:
                connection = connect_to_db()
                cursor = connection.cursor()
                cursor.execute("DELETE FROM Keywords WHERE keyword_ID = %s", (delete_id,))
                connection.commit()
                st.success(f"Keyword ID {delete_id} deleted successfully!")
            except mysql.connector.Error as error:
                st.error(f"Error: {error}")
            finally:
                cursor.close()
                connection.close()


def members_crud():
    st.markdown("<h3 style='font-size:24px;'>Choose an Operation</h3>", unsafe_allow_html=True)
    crud_operation = st.selectbox("", ["📋 Register New Member", "🔍 Explore Members", "✏️ Update Member Details", "❌ Deregister Member"])

    # CREATE Operation
    if crud_operation == "📋 Register New Member":
        st.subheader("Add New Member")
        member_ID = st.text_input("Member ID (up to 10 characters):")
        roles = st.text_input("Role (up to 25 characters):")
        memshp_status = st.text_input("Membership Status (up to 10 characters):")
        memshp_start_date = st.date_input("Membership Start Date:")
        user_ID = st.text_input("User ID (up to 10 characters):")
        institution_ID = st.text_input("Institution ID (up to 10 characters):")

        if st.button("Submit"):
            try:
                connection = connect_to_db()
                cursor = connection.cursor()
                cursor.execute(
                    """INSERT INTO Members (member_ID, roles, memshp_status, memshp_start_date, user_ID, institution_ID) 
                    VALUES (%s, %s, %s, %s, %s, %s)""",
                    (member_ID, roles, memshp_status, memshp_start_date, user_ID, institution_ID)
                )
                connection.commit()
                st.success(f"Member '{member_ID}' added successfully!")
            except mysql.connector.Error as error:
                st.error(f"Error: {error}")
            finally:
                cursor.close()
                connection.close()

    # READ Operation
    elif crud_operation == "🔍 Explore Members":
        st.subheader("View Members")
        view_option = st.selectbox("View Options", ["All Members", "Search by ID"])

        if view_option == "All Members":
            try:
                connection = connect_to_db()
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM Members")
                records = cursor.fetchall()
                if records:
                    df = pd.DataFrame(records, columns=["ID", "Role", "Membership Status", "Start Date", "User ID", "Institution ID"])
                    st.dataframe(df)
                else:
                    st.warning("No members found.")
            except mysql.connector.Error as error:
                st.error(f"Error: {error}")
            finally:
                cursor.close()
                connection.close()

        elif view_option == "Search by ID":
            search_id = st.text_input("Enter Member ID:")
            if st.button("Search"):
                try:
                    connection = connect_to_db()
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM Members WHERE member_ID = %s", (search_id,))
                    record = cursor.fetchone()
                    if record:
                        df = pd.DataFrame([record], columns=["ID", "Role", "Membership Status", "Start Date", "User ID", "Institution ID"])
                        st.table(df.transpose().rename(columns={0: "Value"}))
                    else:
                        st.warning("No member found with that ID.")
                except mysql.connector.Error as error:
                    st.error(f"Error: {error}")
                finally:
                    cursor.close()
                    connection.close()


    # UPDATE Operation
    if crud_operation == "✏️ Update Member Details":
        st.subheader("Update Member")
        update_id = st.text_input("Enter Member ID to Update:")

        if st.button("Fetch Details"):
            try:
                connection = connect_to_db()
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM Members WHERE member_ID = %s", (update_id,))
                record = cursor.fetchone()
                if record:
                    st.session_state['roles'] = record[1]
                    st.session_state['memshp_status'] = record[2]

                    # Convert the fetched start date string to a datetime.date object
                    if isinstance(record[3], str):
                        st.session_state['memshp_start_date'] = datetime.datetime.strptime(record[3], "%Y-%m-%d").date()
                    else:
                        st.session_state['memshp_start_date'] = record[3]

                    st.session_state['user_ID'] = record[4]
                    st.session_state['institution_ID'] = record[5]
                    st.success("Details fetched successfully. You may update them below.")
                else:
                    st.warning("No member found with that ID.")
            except mysql.connector.Error as error:
                st.error(f"Error: {error}")
            finally:
                cursor.close()
                connection.close()

        if 'roles' in st.session_state:
            roles = st.text_input("Role:", st.session_state['roles'])
            memshp_status = st.text_input("Membership Status:", st.session_state['memshp_status'])
            memshp_start_date = st.date_input("Membership Start Date:", st.session_state['memshp_start_date'])
            user_ID = st.text_input("User ID:", st.session_state['user_ID'])
            institution_ID = st.text_input("Institution ID:", st.session_state['institution_ID'])

            if st.button("Submit Update"):
                try:
                    connection = connect_to_db()
                    cursor = connection.cursor()
                    cursor.execute(
                        """UPDATE Members SET roles = %s, memshp_status = %s, memshp_start_date = %s, 
                        user_ID = %s, institution_ID = %s WHERE member_ID = %s""",
                        (roles, memshp_status, memshp_start_date, user_ID, institution_ID, update_id)
                    )
                    connection.commit()
                    st.success("Member updated successfully!")
                    for key in ['roles', 'memshp_status', 'memshp_start_date', 'user_ID', 'institution_ID']:
                        del st.session_state[key]
                except mysql.connector.Error as error:
                    st.error(f"Error: {error}")
                finally:
                    cursor.close()
                    connection.close()


    # DELETE Operation
    elif crud_operation == "❌ Deregister Member":
        st.subheader("Delete Member")
        delete_id = st.text_input("Enter Member ID to Delete:")
        confirm_delete = st.checkbox("I confirm deletion of this member.")

        if st.button("Confirm Delete") and confirm_delete:
            try:
                connection = connect_to_db()
                cursor = connection.cursor()
                cursor.execute("DELETE FROM Members WHERE member_ID = %s", (delete_id,))
                connection.commit()
                st.success(f"Member ID {delete_id} deleted successfully!")
            except mysql.connector.Error as error:
                st.error(f"Error: {error}")
            finally:
                cursor.close()
                connection.close()




def advanced_queries():
    st.title("🔍 Advanced Data Analysis")
    st.markdown("Perform insightful operations on your data with user-friendly tools.")

    # Query Selection
    query_type = st.selectbox(
        "What would you like to do?",
        [
            "🔗 Combine Data Across Categories",
            "📖 Find Publications by Keywords",
            "📊 Compare Authors to Averages",
            "🕵️ Emerging Topics in Recent Publications",
            "📈 Analyze Publication Trends",
            "📊 Advanced Insights"
        ]
    )

    # Query: Combine Data Across Categories
    if query_type == "🔗 Combine Data Across Categories":
        st.subheader("Authors Contributing to Highly Cited Publications")

        # Dropdown for predefined analyses
        analysis_type = st.selectbox(
            "Select Analysis:",
            [
                "Authors Contributing to Highly Cited Publications",
                "Highly Cited Keywords",
            ]
        )

        # Input fields for thresholds and additional filters
        citation_threshold = st.number_input("Enter Citation Threshold (default: 30):", min_value=0, value=30)

        if st.button("Run Analysis"):
            try:
                connection = connect_to_db()
                cursor = connection.cursor()

                # Define hardcoded queries for different analyses
                if analysis_type == "Authors Contributing to Highly Cited Publications":
                    query = f"""
                        SELECT DISTINCT A.author_name
                        FROM Pub_Cite PC
                        JOIN Citations C ON PC.citation_ID = C.citation_ID
                        JOIN Pub_Author PA ON PC.publication_ID = PA.publication_ID
                        JOIN Authors A ON PA.author_ID = A.author_ID
                        WHERE C.citation_count > {citation_threshold};
                    """
                    result_columns = ["Author Name"]

                elif analysis_type == "Highly Cited Keywords":
                    query = f"""
                        SELECT K.keyword, SUM(C.citation_count) AS total_citation_count
                        FROM Pub_Cite PC
                        JOIN Citations C ON PC.citation_ID = C.citation_ID
                        JOIN Pub_Key PK ON PC.publication_ID = PK.publication_ID
                        JOIN Keywords K ON PK.keyword_ID = K.keyword_ID
                        GROUP BY K.keyword
                        HAVING SUM(C.citation_count) > {citation_threshold}
                        ORDER BY total_citation_count DESC;
                    """
                    result_columns = ["Keyword", "Total Citation Count"]

                # Execute and display results
                cursor.execute(query)
                results = cursor.fetchall()

                if results:
                    df = pd.DataFrame(results, columns=result_columns)
                    st.dataframe(df)
                else:
                    st.warning("No results found for the selected analysis.")

            except mysql.connector.Error as error:
                st.error(f"Error: {error}")
            finally:
                cursor.close()
                connection.close()

    # Query: Find Publications by Keywords
    elif query_type == "📖 Find Publications by Keywords":
        st.subheader("Publications Related to Specific Keywords")

        # Fetch keywords from the database dynamically
        try:
            connection = connect_to_db()
            cursor = connection.cursor()
            cursor.execute("SELECT DISTINCT keyword FROM Keywords;")
            keyword_results = cursor.fetchall()
            available_keywords = [row[0] for row in keyword_results]
        except mysql.connector.Error as error:
            st.error(f"Error fetching keywords: {error}")
            available_keywords = []
        finally:
            cursor.close()
            connection.close()

        # Dropdown for keywords and text input for custom keyword
        selected_keywords = st.multiselect("Select Keywords from the List:", available_keywords)
        custom_keyword = st.text_input("Or Enter a Custom Keyword:")

        if st.button("Search Publications"):
            try:
                connection = connect_to_db()
                cursor = connection.cursor()

                # Use a UNION approach for selected and custom keywords
                query_parts = []
                params = []

                if selected_keywords:
                    query_parts.append(
                        f"""
                        SELECT DISTINCT P.paper_name
                        FROM Pub_Key PK
                        JOIN Keywords K ON PK.keyword_ID = K.keyword_ID
                        JOIN Publications P ON PK.publication_ID = P.publication_ID
                        WHERE K.keyword IN ({','.join(['%s'] * len(selected_keywords))})
                        """
                    )
                    params.extend(selected_keywords)

                if custom_keyword:
                    query_parts.append(
                        """
                        SELECT DISTINCT P.paper_name
                        FROM Pub_Key PK
                        JOIN Keywords K ON PK.keyword_ID = K.keyword_ID
                        JOIN Publications P ON PK.publication_ID = P.publication_ID
                        WHERE K.keyword = %s
                        """
                    )
                    params.append(custom_keyword)

                # Combine all query parts with UNION
                query = " UNION ".join(query_parts)

                cursor.execute(query, params)
                results = cursor.fetchall()

                # Display results
                if results:
                    df = pd.DataFrame(results, columns=["Publication Name"])
                    st.dataframe(df)
                else:
                    st.info("No publications found for the selected keywords.")
            except mysql.connector.Error as error:
                st.error(f"Error: {error}")
            finally:
                cursor.close()
                connection.close()


    # Query: Compare Authors to Averages
    elif query_type == "📊 Compare Authors to Averages":
        st.subheader("Compare Authors Based on Citation Averages")

        # Step 1: Let the user choose the type of average for comparison
        average_type = st.radio(
            "Select the Average Type for Comparison:",
            options=[
                "Overall Average Across All Publications",
                "Average for Specific Author Groups",
                "Average for Specific Topics"
            ]
        )

        # Step 2: Provide input fields based on user selection
        additional_filter = ""
        if average_type == "Average for Specific Author Groups":
            author_group = st.multiselect("Select Author(s):", [
                "Alexandros Iosifidis", "Aljosa Smolic", "André Kaup", "Aris S. Lalos", "Esa Rahtu",
                "Evangelos Alexiou", "Farid Alijani", "Fengqing Zhu", "Frédéric Dufaux", "Giuseppe Valenzise",
                "Ismael Seidel", "José Luis Güntzel", "Jun Wang", "Konstantinos Moustakas", "Mateus Grellert",
                "Miska M. Hannuksela", "Patrick Le Callet", "Steve Göring", "Vanio Rodrigues Filho", "Zeman Shao"
            ])
            if author_group:
                # Use join with quotes added manually
                author_group_formatted = ', '.join([f"'{author}'" for author in author_group])
                additional_filter = f"AND A.author_name IN ({author_group_formatted})"

        elif average_type == "Average for Specific Topics":
            # Fetch topics dynamically from the database
            try:
                connection = connect_to_db()
                cursor = connection.cursor()
                cursor.execute("SELECT DISTINCT topic_name FROM Topics;")
                topic_results = cursor.fetchall()
                available_topics = [row[0] for row in topic_results]
            except mysql.connector.Error as error:
                st.error(f"Error fetching topics: {error}")
                available_topics = []
            finally:
                cursor.close()
                connection.close()

            # Create a dropdown for topics
            topic_filter = st.selectbox("Select a Topic:", available_topics)
            if topic_filter:
                additional_filter = f"AND T.topic_name = '{topic_filter}'"

        # Step 3: Allow dynamic threshold adjustment
        citation_threshold = st.number_input("Enter Citation Threshold (default: 30):", min_value=0, value=30)

        # Step 4: Query and display results
        if st.button("Analyze Authors"):
            try:
                connection = connect_to_db()
                cursor = connection.cursor()

                # Base Query
                base_query = f"""
                    WITH AvgCitations AS (
                        SELECT PC.publication_ID, AVG(C.citation_count) AS avg_citations
                        FROM Pub_Cite PC
                        JOIN Citations C ON PC.citation_ID = C.citation_ID
                        GROUP BY PC.publication_ID
                    )
                    SELECT A.author_name, T.topic_name, AVG(C.citation_count) AS author_avg
                    FROM Pub_Author PA
                    JOIN Authors A ON PA.author_ID = A.author_ID
                    JOIN Pub_Cite PC ON PA.publication_ID = PC.publication_ID
                    JOIN Citations C ON PC.citation_ID = C.citation_ID
                    LEFT JOIN Pub_Key PK ON PC.publication_ID = PK.publication_ID
                    LEFT JOIN Keywords K ON PK.keyword_ID = K.keyword_ID
                    LEFT JOIN Topics T ON K.topic_ID = T.topic_ID
                    WHERE 1=1
                    {additional_filter}
                    GROUP BY A.author_name, T.topic_name
                    HAVING AVG(C.citation_count) > (SELECT AVG(avg_citations) FROM AvgCitations)
                    AND AVG(C.citation_count) > {citation_threshold};
                """

                # Execute query
                cursor.execute(base_query)
                results = cursor.fetchall()

                # Display results
                if results:
                    df = pd.DataFrame(results, columns=["Author Name", "Topic Name", "Average Citation Count"])
                    st.dataframe(df)
                else:
                    st.info("No authors found matching the criteria.")

            except mysql.connector.Error as error:
                st.error(f"Error: {error}")
            finally:
                cursor.close()
                connection.close()




        # Query: Emerging Topics in Recent Publications
    elif query_type == "🕵️ Emerging Topics in Recent Publications":
        st.subheader("Analyze Emerging Topics in Recent Research")

        # Date range selection
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date for Analysis:")
        with col2:
            end_date = st.date_input("End Date for Analysis:", value=None)

        # Run the query
        if st.button("Analyze Topics"):
            try:
                connection = connect_to_db()
                cursor = connection.cursor()

                # Query for topics
                query = f"""
                    SELECT DISTINCT T.topic_name, COUNT(P.publication_ID) AS publication_count
                    FROM Topics T
                    JOIN Keywords K ON T.topic_ID = K.topic_ID
                    JOIN Pub_Key PK ON K.keyword_ID = PK.keyword_ID
                    JOIN Publications P ON PK.publication_ID = P.publication_ID
                    WHERE P.date_of_publication >= '{start_date}'
                """
                if end_date:
                    query += f" AND P.date_of_publication <= '{end_date}'"
                query += " GROUP BY T.topic_name ORDER BY publication_count DESC;"

                # Execute query
                cursor.execute(query)
                results = cursor.fetchall()

                # Display results
                if results:
                    df = pd.DataFrame(results, columns=["Topic", "Publication Count"])
                    st.dataframe(df)

                    # Visualization
                    # Within the function advanced_queries
                    import plotly.express as px

                    fig = px.bar(
                        df,
                        x="Topic",
                        y="Publication Count",
                        title="Emerging Topics in Recent Publications",
                        labels={"Topic": "Topic Name", "Publication Count": "Number of Publications"},
                        color="Publication Count",
                        height=500,
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No topics found for the selected date range.")

            except mysql.connector.Error as error:
                st.error(f"Error: {error}")
            finally:
                cursor.close()
                connection.close()


    # Query: Analyze Publication Trends
    elif query_type == "📈 Analyze Publication Trends":
        st.subheader("Keywords with Most Publications")

        # Fetch keywords from the database dynamically
        try:
            connection = connect_to_db()
            cursor = connection.cursor()
            cursor.execute("SELECT DISTINCT keyword FROM Keywords;")
            keyword_results = cursor.fetchall()
            available_keywords = [row[0] for row in keyword_results]  # Extract keywords
        except mysql.connector.Error as error:
            st.error(f"Error fetching keywords: {error}")
            available_keywords = []  # Fallback to empty list
        finally:
            cursor.close()
            connection.close()

        # Add a filter for specific keywords (optional)
        keyword_filter = st.multiselect(
            "Select Specific Keywords (Leave Blank for All):",
            available_keywords,
            default=[]
        )

        if st.button("Run Analysis"):
            try:
                connection = connect_to_db()
                cursor = connection.cursor()

                # Build query dynamically based on filter
                where_clause = ""
                if keyword_filter:
                    # Add WHERE clause for selected keywords
                    formatted_keywords = ', '.join([f"'{kw}'" for kw in keyword_filter])
                    where_clause = f"WHERE K.keyword IN ({formatted_keywords})"

                query = f"""
                    SELECT K.keyword, COUNT(PK.publication_ID) AS total_publications
                    FROM Pub_Key PK
                    JOIN Keywords K ON PK.keyword_ID = K.keyword_ID
                    {where_clause}
                    GROUP BY K.keyword
                    ORDER BY total_publications DESC;
                """
                cursor.execute(query)
                results = cursor.fetchall()

                # Display results
                if results:
                    df = pd.DataFrame(results, columns=["Keyword", "Total Publications"])

                    # Visualization with Plotly
                    import plotly.express as px

                    fig = px.bar(
                        df,
                        x="Keyword",
                        y="Total Publications",
                        title="Publication Trends by Keyword",
                        labels={"Keyword": "Keyword", "Total Publications": "Number of Publications"},
                        color="Total Publications",
                        text="Total Publications",
                        height=500,
                    )
                    fig.update_traces(textposition="outside")
                    fig.update_layout(
                        xaxis=dict(title="Keyword", tickangle=-45),
                        yaxis=dict(title="Total Publications"),
                        title_x=0.5,
                        template="plotly_white",
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No publications found for the selected keywords.")
            except mysql.connector.Error as error:
                st.error(f"Error: {error}")
            finally:
                cursor.close()
                connection.close()

   

    # Query: OLAP Queries Combined
    elif query_type == "📊 Advanced Insights":
        st.subheader("Perform OLAP Analysis")

        # Dropdown for predefined analyses
        olap_analysis_type = st.selectbox(
            "Select Analysis:",
            [
                "🏆 Rank Top Publications",
                "🏫 Institution-Wise Citations",
                "📆 Keyword Impact Over Time",
            ]
        )

        # Input fields for thresholds and filters (if applicable)
        if olap_analysis_type in ["🏆 Rank Top Publications", "🏫 Institution-Wise Citations"]:
            include_grand_total = st.checkbox("Include Grand Total (Enable OLAP Analysis)")
        if olap_analysis_type == "📆 Keyword Impact Over Time":
            start_year = st.number_input("Enter Start Year:", min_value=2000, max_value=2024, value=2015)

        # Button to execute the analysis
        if st.button("Run OLAP Analysis"):
            try:
                connection = connect_to_db()
                cursor = connection.cursor()

                # Define SQL queries for each analysis
                if olap_analysis_type == "🏆 Rank Top Publications":
                    if include_grand_total:
                        query = """
                            SELECT 
                                CASE 
                                    WHEN P.paper_name IS NULL THEN 'All Publications'
                                    ELSE P.paper_name
                                END AS paper_name,
                                SUM(C.citation_count) AS total_citations
                            FROM Pub_Cite PC
                            JOIN Citations C ON PC.citation_ID = C.citation_ID
                            JOIN Publications P ON PC.publication_ID = P.publication_ID
                            GROUP BY P.paper_name WITH ROLLUP
                            ORDER BY total_citations DESC;
                        """
                    else:
                        query = """
                            SELECT P.paper_name, SUM(C.citation_count) AS total_citations
                            FROM Pub_Cite PC
                            JOIN Citations C ON PC.citation_ID = C.citation_ID
                            JOIN Publications P ON PC.publication_ID = P.publication_ID
                            GROUP BY P.paper_name
                            ORDER BY total_citations DESC;
                        """
                    result_columns = ["Publication Name", "Total Citations"]

                elif olap_analysis_type == "🏫 Institution-Wise Citations":
                    if include_grand_total:
                        query = """
                            SELECT 
                                CASE 
                                    WHEN I.inst_name IS NULL THEN 'All Institutions'
                                    ELSE I.inst_name
                                END AS institution_name,
                                SUM(C.citation_count) AS total_citations
                            FROM Publications P
                            JOIN Pub_Author PA ON P.publication_ID = PA.publication_ID
                            JOIN Authors A ON PA.author_ID = A.author_ID
                            JOIN Institutions I ON A.institution_ID = I.institution_ID
                            JOIN Pub_Cite PC ON P.publication_ID = PC.publication_ID
                            JOIN Citations C ON PC.citation_ID = C.citation_ID
                            GROUP BY I.inst_name WITH ROLLUP
                            ORDER BY total_citations DESC;
                        """
                    else:
                        query = """
                            SELECT I.inst_name, SUM(C.citation_count) AS total_citations
                            FROM Publications P
                            JOIN Pub_Author PA ON P.publication_ID = PA.publication_ID
                            JOIN Authors A ON PA.author_ID = A.author_ID
                            JOIN Institutions I ON A.institution_ID = I.institution_ID
                            JOIN Pub_Cite PC ON P.publication_ID = PC.publication_ID
                            JOIN Citations C ON PC.citation_ID = C.citation_ID
                            GROUP BY I.inst_name
                            ORDER BY total_citations DESC;
                        """
                    result_columns = ["Institution Name", "Total Citations"]

                elif olap_analysis_type == "📆 Keyword Impact Over Time":
                    query = f"""
                        SELECT YEAR(P.date_of_publication) AS year, K.keyword, COUNT(P.publication_ID) AS total_publications
                        FROM Pub_Key PK
                        JOIN Keywords K ON PK.keyword_ID = K.keyword_ID
                        JOIN Publications P ON PK.publication_ID = P.publication_ID
                        WHERE YEAR(P.date_of_publication) >= {start_year}
                        GROUP BY YEAR(P.date_of_publication), K.keyword
                        ORDER BY year DESC, total_publications DESC;
                    """
                    result_columns = ["Year", "Keyword", "Total Publications"]

                # Execute query
                cursor.execute(query)
                results = cursor.fetchall()

                # Display results
                if results:
                    df = pd.DataFrame(results, columns=result_columns)
                    if olap_analysis_type == "📆 Keyword Impact Over Time":
                        # Line chart for keyword trends
                        import plotly.express as px
                        fig = px.line(
                            df,
                            x="Year",
                            y="Total Publications",
                            color="Keyword",
                            title="Keyword Impact Over Time",
                            labels={"Total Publications": "Number of Publications", "Year": "Year"},
                            height=600,
                            width=1200,
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        # Horizontal bar chart for rankings
                        import plotly.express as px
                        fig = px.bar(
                            df,
                            y=result_columns[0],
                            x=result_columns[1],
                            title=f"{olap_analysis_type} Analysis",
                            labels={result_columns[0]: "Category", result_columns[1]: "Total Citations"},
                            text=result_columns[1],
                            orientation="h",
                            height=800,
                            width=1200,
                        )
                        st.plotly_chart(fig, use_container_width=True)

                    # Data table
                    st.markdown("### Detailed Data")
                    st.dataframe(df)
                else:
                    st.info("No data found for the selected analysis.")

            except mysql.connector.Error as error:
                st.error(f"Error: {error}")
            finally:
                cursor.close()
                connection.close()





def main_app():
    # Set the current page in session state if not already set
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "🏠 Home"

    st.sidebar.title(f"Welcome, {st.session_state['username'].capitalize()}!")
    st.sidebar.title("Navigation")

    # General Section
    st.sidebar.markdown("### General")
    if st.sidebar.button("🏠 Home"):
        st.session_state["current_page"] = "🏠 Home"

    # Data Management Section
    st.sidebar.markdown("### Data Management")
    if st.sidebar.button("🏫 Institutions"):
        st.session_state["current_page"] = "🏫 Institutions"
    if st.sidebar.button("📖 Publications"):
        st.session_state["current_page"] = "📖 Publications"
    if st.sidebar.button("📂 Topics"):
        st.session_state["current_page"] = "📂 Topics"
    if st.sidebar.button("🔗 Citations"):
        st.session_state["current_page"] = "🔗 Citations"
    if st.sidebar.button("🎓 Conferences"):
        st.session_state["current_page"] = "🎓 Conferences"

    # User Management Section
    st.sidebar.markdown("### User Management")
    if st.sidebar.button("👤 Users"):
        st.session_state["current_page"] = "👤 Users"
    if st.sidebar.button("✍️ Authors"):
        st.session_state["current_page"] = "✍️ Authors"

    # Metadata Section
    st.sidebar.markdown("### Metadata")
    if st.sidebar.button("🔑 Keywords"):
        st.session_state["current_page"] = "🔑 Keywords"
    if st.sidebar.button("📋 Members"):
        st.session_state["current_page"] = "📋 Members"

    # Metadata Section
    st.sidebar.markdown("### Interactive Reports")
    if st.sidebar.button("🧠 Advanced Data Analysis"):
        st.session_state["current_page"] = "🧠 Advanced Data Analysis"

    # Render the current page
    if st.session_state["current_page"] == "🏠 Home":
        home_page()
    elif st.session_state["current_page"] == "🏫 Institutions":
        institutions_crud()
    elif st.session_state["current_page"] == "📖 Publications":
        publications_crud()
    elif st.session_state["current_page"] == "📂 Topics":
        topics_crud()
    elif st.session_state["current_page"] == "🔗 Citations":
        citations_crud()
    elif st.session_state["current_page"] == "🎓 Conferences":
        conferences_crud()
    elif st.session_state["current_page"] == "👤 Users":
        users_crud()
    elif st.session_state["current_page"] == "✍️ Authors":
        authors_crud()
    elif st.session_state["current_page"] == "🔑 Keywords":
        keywords_crud()
    elif st.session_state["current_page"] == "📋 Members":
        members_crud()
    elif st.session_state["current_page"] == "🧠 Advanced Data Analysis":
        advanced_queries()

# App logic
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    login()
else:
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "🏠 Home"  # Default to Home page
    main_app()