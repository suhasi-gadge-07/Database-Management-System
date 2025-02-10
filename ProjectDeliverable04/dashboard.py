# type: ignore
import streamlit as st 
import mysql.connector
import pandas as pd

# Title and Introduction
st.title("IEEE Database Management System")
st.markdown("Welcome to the **IEEE Database Management System**! This platform provides comprehensive CRUD functionality to manage and interact with an IEEE-related database. It serves as a centralized system for handling data on publications, authors, conferences, topics, citations, and more. The goal is to support efficient data management and analysis in academic and research contexts.")

# Navigation Guide
st.header("Navigation Guide")
st.write("""
To access the various sections of the IEEE Database Management System, use the navigation bar at the top of this page. Each section corresponds to a table in the database, allowing for specific CRUD operations:

- **Publications**: Create, read, update, and delete records related to publications.
- **Institutions**: Manage institution details where authors may be affiliated.
- **Topics**: Classify and manage various research topics.
- **Citations**: Track citations between different publications.
- **Conferences**: Record conference information for publications.
- **Users**: Handle user records and contact information.
- **Authors**: Add and manage authors and their respective details.
- **Keywords**: Organize keywords associated with various topics.
- **Members**: Track members, their roles, and status.
""")

# Database connection
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="suhasi@1325",
        database="ieee_db"
    )

# Exploring Through Database
st.header("Exploring Through Database!")

# Defining table names for tabs
table_names = ["Institutions", "Publications", "Authors", "Keywords", "Topics", "Citations", "Conferences", "Users", "Members"]

# Creating tabs for each table in table_names
tabs = st.tabs(table_names)


def institutions_crud():
    st.markdown("<h3 style='font-size:24px;'>Choose an Operation</h3>", unsafe_allow_html=True)
    crud_operation = st.selectbox("", ["Create", "Read", "Update", "Delete"])

    # CREATE Operation - To add a new institution
    if crud_operation == "Create":
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

    # READ Operation - To get details about institutions
    elif crud_operation == "Read":
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

    # UPDATE Operation - Modify institution details
    elif crud_operation == "Update":
        st.subheader("Update Institution")
        update_id = st.text_input("Enter Institution ID to Update:")

        # "Fetch Details" button for update operation only
        if st.button("Fetch Details"):
            try:
                connection = connect_to_db()
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM institutions WHERE institution_ID = %s", (update_id,))
                record = cursor.fetchone()
                if record:
                    # Store existing data in session state to allow editing
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

        # Show editable fields prefilled with fetched data
        if 'inst_name' in st.session_state:
            inst_name = st.text_input("Institution Name:", st.session_state['inst_name'])
            inst_addr = st.text_input("Institution Address:", st.session_state['inst_addr'])
            inst_web_link = st.text_input("Institution Web Link:", st.session_state['inst_web_link'])
            associated_authors = st.text_input("Associated Authors (comma-separated):", st.session_state['associated_authors'])

            # Update button to submit changes
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
                    # Clear session state after successful update
                    del st.session_state['inst_name']
                    del st.session_state['inst_addr']
                    del st.session_state['inst_web_link']
                    del st.session_state['associated_authors']
                except mysql.connector.Error as error:
                    st.error(f"Error: {error}")
                finally:
                    cursor.close()
                    connection.close()

    # DELETE Operation - Remove an institution by ID
    elif crud_operation == "Delete":
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

# Adding this function to the respective tab in the main code
for i, tab in enumerate(tabs):
    with tab:
        if table_names[i] == "Institutions":
            institutions_crud()
        else:
            st.write(f"CRUD operations for {table_names[i]} are not yet implemented.")











