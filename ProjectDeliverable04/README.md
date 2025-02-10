# IEEE Database Management System

This project is a web-based **IEEE Database Management System (DMS)** designed to manage publication data and related entities, like authors, conferences, and topics. The front end is built with **Streamlit** for an easy-to-use interface, and **MySQL** serves as the database backend. Users can perform CRUD (Create, Read, Update, Delete) operations across different IEEE-related data tables, with a focus on making data handling straightforward.

## Project Structure

- **dashboard.py**: This main file contains the Streamlit code for the web app interface. Right now, CRUD operations are fully functional for the *Institutions* table, and we are working to expand these operations to the remaining tables for the final version.
- **ieee_database.py**: This file manages the MySQL database connection and provides helper functions for the CRUD operations.

## Key Features

- **CRUD Operations**: Complete set of operations across various tables (Publications, Authors, Institutions, Keywords, Topics, Citations, Conferences, Users, Members).
- **Streamlit Interface**: User-friendly interface for browsing and editing data with easy-to-navigate tabs and forms.
- **MySQL Integration**: Connects to a MySQL database to store and retrieve IEEE-related data securely.

## Requirements

- **Python** 3.7+ (preferably Python 3.10.11)
- **Streamlit**: Install with `pip install streamlit`
- **MySQL Connector for Python**: Install with `pip install mysql-connector-python`
- **MySQL Database Server**

## Database Setup

The application connects to a MySQL database called `ieee_db`, which should include these tables:

- **Institutions**
- **Publications**
- **Authors**
- **Keywords**
- **Topics**
- **Citations**
- **Conferences**
- **Users**
- **Members**

Make sure to add your MySQL credentials in the `connect_to_db()` function in both `dashboard.py` and `ieee_database.py`.

## How to Use

1. **Start MySQL Server**:
   ```bash
   sudo service mysql start  # Use the appropriate command for your OS
   ```

2. **Launch the Streamlit Dashboard**:
   ```bash
   streamlit run dashboard.py
   ```

3. **Performing CRUD Operations**:
   - Select the table you want to work with from the tabs.
   - Choose between Create, Read, Update, or Delete.
   - Enter the required details and execute the operation.

### Example

To add a new Institution, go to the *Institutions* tab, select "Create," and fill out the required information (Institutionn ID, Address, etc.).

For developers or database administrators, you can also use `ieee_database.py` directly from a terminal to test database functions and display output in a tabular format.

## Security Note

Ensure that database credentials in `dashboard.py` and `ieee_database.py` are protected, especially if deploying to a production environment.

## Planned Improvements

- Implement full CRUD functionality for all tables.
- Add data validation and error handling.
- Integrate basic analytics features to help with research insights.

