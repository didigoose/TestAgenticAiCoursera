import sqlite3
import pandas as pd

def reset_database(table):
    conn = sqlite3.connect("kriege_datenbank.db")
    cursor = conn.cursor()
    
    # Lösche die Tabelle, falls sie existiert
    cursor.execute("DROP TABLE IF EXISTS table")
    
    # Erstelle die Tabelle neu
    cursor.execute("""
        CREATE TABLE table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Krieg_Name TEXT NOT NULL,
            Start_Jahr INTEGER,
            End_Jahr INTEGER
        )
    """)
    
    conn.commit()
    conn.close()

def delete_duplicates_from_wars():
    conn = sqlite3.connect("kriege_datenbank.db")
    cursor = conn.cursor()

    # Lösche Duplikate basierend auf name, Start_Jahr und End_Jahr
    cursor.execute("""
        DELETE FROM kriege
        WHERE rowid NOT IN (
            SELECT MIN(rowid)
            FROM kriege
            GROUP BY Krieg_Name, Start_Jahr, End_Jahr
        )
    """)
    conn.commit()
    conn.close()

def insert_war(Krieg_Name, Start_Jahr, End_Jahr):
    conn = sqlite3.connect("kriege_datenbank.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO kriege (Krieg_Name, Start_Jahr, End_Jahr)
        VALUES (?, ?, ?)
    """, (Krieg_Name, Start_Jahr, End_Jahr))
    
    conn.commit()
    conn.close()

def get_all_wars():
    conn = sqlite3.connect("kriege_datenbank.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM kriege")
    wars = cursor.fetchall()
    
    conn.close()
    return wars


def get_all_participants(column_name):
    # Connect to the SQLite database
    conn = sqlite3.connect('kriege_datenbank.db')

    # Read a table into a DataFrame
    df = pd.read_sql_query(f"SELECT * FROM KriegeGesamt", conn)
    #print(df.shape)  # Display the first few rows of the DataFrame
    #print(df.head()) #DEBUG first 5 rows

    # Close the connection when done
    conn.close()
    return df