# Project README

Here's a README summarizing the contents and functionality of each Python file in this project:

---

# Project Overview

This project contains a set of Python scripts designed to handle data related to historical wars, their participants, and analyze such details for insights through database operations and visualizations. Below is a brief description of the functionality of each script within the project.

## File Summaries

### NormalizeCountries.py
This script processes and normalizes lists of country participants in wars, mapping country names from a database to standard canonical names to ensure consistency. It reads data on aggressors and defenders from a database, applies a mapping function to standardize names, and then saves the normalized data back into the database. The script also identifies which countries frequently appear as aggressors or defenders, and prepares additional data files for further analysis and visualization.

### analyze_import2.py
The script compares lists of wars from a CSV file and a SQLite database to ensure consistency and completeness. It identifies unique and duplicate war entries, checking if any wars are present in one source but not the other. This serves as a validation tool to ensure that data imported into the database matches the original CSV source.

### database_operations.py
This script defines essential database operations such as resetting the database, removing duplicates, and inserting new war entries. It provides functions for interacting with a SQLite database to manage war records, ensuring that duplicate entries do not exist and new data is correctly added.

### wars_barchartrace.py
Utilizing the `bar_chart_race` library, this script generates animations that visualize data over time. The primary focus of visualization is on countries’ involvement in wars by both number of wars and war-related deaths. These animations are saved as video files, providing a visual race-style display of data trends over the years.

---

These scripts, when combined, offer tools for data normalization, validation, database management, and dynamic data visualization concerning historical war data and analytics.

## Python File Summaries

### NormalizeCountries.py
**Full path:** `./SamplePy/NormalizeCountries.py`

import re
from database_operations import get_all_participants # Import database functions
from mapping import kriegsteilnehmer_mapping_red #import mapping table from a separate module
import pandas as pd
import numpy as np


def process_country_list(country_list_string, mapping_table):







# Example usage with your provided database strings:
#print("Before shape")
db_aggressors = get_all_participants('Parteien_Seite_Aggressor')  # Assuming this function returns a list of strings from your database
db_defenders = get_all_participants('Parteien_Seite_Verteidiger')  # Assuming this function returns a list of strings from your database
#print(db_strings.head())  # Display the first few rows of the DataFrame
#print("After shape")
#print(df.head()) #DEBUG first 5 rows

# Start with the original DataFrame (e.g. db_aggressors)
df = db_aggressors.copy()

# Map aggressors
df['mapped_Parteien_Seite_Aggressor'] = df['Parteien_Seite_Aggressor'].apply(lambda x: process_country_list(x, kriegsteilnehmer_mapping_red))
for idx, mapped_list in df['mapped_Parteien_Seite_Aggressor'].items():

# Map defenders (use the same DataFrame!)
df['mapped_Parteien_Seite_Verteidiger'] = db_defenders['Parteien_Seite_Verteidiger'].apply(lambda x: process_country_list(x, kriegsteilnehmer_mapping_red))
for idx, mapped_list in df['mapped_Parteien_Seite_Verteidiger'].items():

# Optional: fill NaN with False for all new columns (canonical country names)
#country_columns = set([country for sublist in df['mapped_Parteien_Seite_Aggressor'] for country in sublist])
#df[list(country_columns)] = df[list(country_columns)].fillna(False)

# Save the DataFrame to a CSV file
#df.to_csv("normalized_participants.csv", index=False)

# Open a connection to your existing database
# Convert lists to comma-separated strings for database storage
df['mapped_Parteien_Seite_Aggressor'] = df['mapped_Parteien_Seite_Aggressor'].apply(lambda x: ', '.join(x) if isinstance(x, list) else str(x))
df['mapped_Parteien_Seite_Verteidiger'] = df['mapped_Parteien_Seite_Verteidiger'].apply(lambda x: ', '.join(x) if isinstance(x, list) else str(x))
import sqlite3
conn = sqlite3.connect('kriege_datenbank.db')
# Write the DataFrame to a new table, e.g. "normalized_participants"
df.to_sql('KriegeGlobalTeilnehmer', conn, if_exists='replace', index=False)
conn.close()





# After both loops for aggressor and defender, collect all country columns
# (they are the columns that are not in the original db_defenders columns or mapped columns)
original_columns = set(db_defenders.columns) | {'mapped_Parteien_Seite_Aggressor', 'mapped_Parteien_Seite_Verteidiger'}
country_columns = [col for col in df.columns if col not in original_columns]

from itertools import permutations

max_count = 0
max_pair = (None, None)

for country1, country2 in permutations(country_columns, 2):

print(f"The pair of countries most often on different sides (Aggressor/Defender): {max_pair} ({max_count} rows)")

# Zähle für jedes Land, wie oft es "Agressor" oder "Defender" ist
aggressor_counts = {}
defender_counts = {}

for country in country_columns:

# Finde das Land mit den meisten "Agressor"- und "Defender"-Einträgen
most_aggressor = max(aggressor_counts, key=aggressor_counts.get)
most_defender = max(defender_counts, key=defender_counts.get)

print(f"Most frequent Aggressor: {most_aggressor} ({aggressor_counts[most_aggressor]} times)")
print(f"Most frequent Defender: {most_defender} ({defender_counts[most_defender]} times)")

both_counts = {}

for country in country_columns:

most_both = max(both_counts, key=both_counts.get)
print(f"Country most often involved as both Aggressor and Defender: {most_both} ({both_counts[most_both]} times)")


both_role_counts = {}

for country in country_columns:

# Sort and print the results
for country, count in sorted(both_role_counts.items(), key=lambda x: x[1], reverse=True):


# Bar_chart_race Kriegsteilnahmen
# 1. Wähle die relevanten Spalten aus
# Annahme: 'Startjahr' ist numerisch, country_columns enthält alle Länder-Spalten
df_bcr = df[['Startjahr'] + country_columns].copy()

# 2. Ersetze alle Nicht-NaN-Werte durch 1 (Beteiligung), sonst 0
for country in country_columns:

# 3. Gruppiere nach Jahr und summiere die Beteiligungen
df_bcr_grouped = df_bcr.groupby('Startjahr')[country_columns].sum()
df_bcr_cumulative = df_bcr_grouped.cumsum()

# Optional: Sortiere die Jahre aufsteigend
df_bcr_cumulative = df_bcr_cumulative.sort_index()

# 4. Speichere das Ergebnis für bar_chart_race
df_bcr_cumulative.to_csv("barchartrace_countries_by_year.csv")

#print(df_bcr_grouped.head())



# Bar_chart_race Kriegsopferzahlen
# 1. Prepare a DataFrame with Startjahr, Opferzahlen_Gesamt_bis, and country columns
df_opfer = df[['Startjahr', 'Opferzahlen_Gesamt_bis'] + country_columns].copy()

# 2. For each country, set value to Opferzahlen_Gesamt_bis if participating, else 0
for country in country_columns:

# 3. Group by year and sum
df_opfer_grouped = df_opfer.groupby('Startjahr')[country_columns].sum()

# 4. Cumulative sum over years
df_opfer_cumulative = df_opfer_grouped.cumsum().sort_index()

# 5. Save for bar_chart_race
df_opfer_cumulative.to_csv("barchartrace_countries_by_opferzahlen.csv")
#print(df_opfer_cumulative.head())

### analyze_import2.py
**Full path:** `./SamplePy/analyze_import2.py`

import csv
import sqlite3
from collections import Counter # Um Duplikate leicht zu zählen

# --- Konfiguration ---
CSV_FILE_PATH = 'China.csv'
DB_FILE_PATH = 'kriege_datenbank.db'
TABLE_NAME = 'KriegeChina'
CSV_KRIEG_COLUMN_INDEX = 0
DB_KRIEG_COLUMN_NAME = 'Krieg'
EXPECTED_COLUMNS_IN_DATA = 14 # Die Anzahl der Spalten in deinen Datenzeilen

def compare_csv_and_db_wars():


















if __name__ == '__main__':
    compare_csv_and_db_wars()

### database_operations.py
**Full path:** `./SamplePy/database_operations.py`

import sqlite3
import pandas as pd

def reset_database(table):

def delete_duplicates_from_wars():


def insert_war(Krieg_Name, Start_Jahr, End_Jahr):

def get_all_wars():


def get_all_participants(column_name):


    return df

### wars_barchartrace.py
**Full path:** `./SamplePy/wars_barchartrace.py`

import bar_chart_race as bcr
import pandas as pd

# Example dataframe (wide format, index = time, columns = categories)
#df = pd.read_csv('barchartrace_countries_by_year.csv', index_col='Startjahr', parse_dates=True)
df = pd.read_csv('barchartrace_countries_by_opferzahlen.csv', index_col='Startjahr', parse_dates=True)

bcr.bar_chart_race(
)
