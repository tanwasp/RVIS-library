# code to update database

# call this in main.py
# from UpdateDB import update_db
#
# # Call the function
# update_db()

import pandas as pd
import sqlite3


def update_db():
    # Load the Excel file
    excel_data = pd.read_excel('FINALBOOKS.xlsx')

    # Connect to the SQLite database
    conn = sqlite3.connect('Storebooks.db')

    # Create a cursor object
    cur = conn.cursor()

    # Keep track of all titles in the Excel file
    excel_titles = set(excel_data['NAME OF BOOKS'])

    # Iterate over the rows in the Excel file
    for index, row in excel_data.iterrows():
        # Check if the data already exists in the database
        cur.execute("SELECT * FROM FinalBooks WHERE Title = ?", (row['NAME OF BOOKS'],))
        existing_data = cur.fetchone()

        if existing_data:
            # Data already exists, update the row
            sql_query = """
            UPDATE FinalBooks
            SET Title = ?, 
                Author = ?, 
                ISBN = ?, 
                Year = ?,  
                NumCopies = ?, 
                Category = ?
            WHERE Title = ?
            """
            cur.execute(sql_query, (row['NAME OF BOOKS'], row['AUTHOR'], row['ISBN#'], row['YEAR'], row['Num Copies'], row['CATEGORY'], row['NAME OF BOOKS']))

        else:
            # Data does not exist, insert a new row
            sql_query = """
            INSERT INTO FinalBooks (Title, Author, ISBN, Year, Availability, NumCopies, Category)
            VALUES  (?, ?, ?, ?, ?, ?, ?)
            """
            cur.execute(sql_query, (row['NAME OF BOOKS'], row['AUTHOR'], row['ISBN#'], row['YEAR'], row['AVAILABILITY'], row['Num Copies'], row['CATEGORY']))

    # Delete rows from the SQL database that are not in the Excel file
    cur.execute("SELECT Title FROM FinalBooks")
    db_titles = set(title for title, in cur.fetchall())
    titles_to_delete = db_titles - excel_titles

    for title in titles_to_delete:
        cur.execute("DELETE FROM FinalBooks WHERE Title = ?", (title,))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def delete_null_titles():
    # Connect to the SQLite database
    conn = sqlite3.connect('Storebooks.db')

    # Create a cursor object
    cur = conn.cursor()

    # Create an SQL query to delete rows where 'Title' is null
    sql_query = "DELETE FROM FinalBooks WHERE Title IS NULL"

    # Execute the SQL query
    cur.execute(sql_query)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Call the function
update_db()
# delete_null_titles()
