import re
from database_operations import get_all_participants # Import database functions
from mapping import kriegsteilnehmer_mapping_red #import mapping table from a separate module
import pandas as pd
import numpy as np


def process_country_list(country_list_string, mapping_table):
    """
    Processes a single string containing a list of countries and maps them
    to the keys in the provided mapping table.

    Args:
        country_list_string (str): The string from your database column (e.g., "Alliierte (USA,Großbritannien,Kanada,Freie Französische Streitkräfte,Polen u.a.)").
        mapping_table (dict): The mapping table (kriegsteilnehmer_mapping_red).

    Returns:
        list: A list of mapped "canonical" country names (keys from the mapping table)
              found in the input string.
    """
    mapped_countries = set()

    # 1. Extract individual country names from the string
    # This regex tries to capture names that are separated by commas,
    # or inside parentheses. It's a bit robust.
    # It also handles "u.a." by ignoring it.
    extracted_countries = re.findall(r'[\w\säöüÄÖÜß\.-]+', country_list_string)
    # Filter out common separators or indicators that aren't country names
    extracted_countries = [
        country.strip() for country in extracted_countries
        if country.strip() and country.strip().lower() not in ["u.a.", ""]
    ]
    # Further refinement for parenthetical content
    if '(' in country_list_string and ')' in country_list_string:
        parenthetical_content = re.search(r'\((.*?)\)', country_list_string)
        if parenthetical_content:
            inner_countries = [c.strip() for c in parenthetical_content.group(1).split(',')]
            extracted_countries.extend(inner_countries)
    # Remove duplicates and refine the list
    extracted_countries = list(set([re.sub(r'\s*\(.*\)\s*', '', c).strip() for c in extracted_countries]))
    extracted_countries = [c for c in extracted_countries if c] # Remove empty strings


    # 2. Iterate through your mapping table to find matches
    for canonical_name, aliases_str in mapping_table.items():
        aliases = [alias.strip() for alias in aliases_str.split(',')]
        for extracted in extracted_countries:
            if extracted in aliases:
                mapped_countries.add(canonical_name)
                break # Once a match is found for this canonical name, move to the next one

    return list(mapped_countries)

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
    for country in mapped_list:
        df.at[idx, country] = 'Agressor'

# Map defenders (use the same DataFrame!)
df['mapped_Parteien_Seite_Verteidiger'] = db_defenders['Parteien_Seite_Verteidiger'].apply(lambda x: process_country_list(x, kriegsteilnehmer_mapping_red))
for idx, mapped_list in df['mapped_Parteien_Seite_Verteidiger'].items():
    for country in mapped_list:
        # Create the column if it does not exist
        if country not in df.columns:
            df[country] = np.nan
        # If already 'Agressor', set to 'Both', else 'Defender'
        if df.at[idx, country] == 'Agressor':
            df.at[idx, country] = 'Both'
        else:
            df.at[idx, country] = 'Defender'

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
    # country1 ist Aggressor, country2 ist Defender in derselben Zeile
    count = ((df[country1] == 'Agressor') & (df[country2] == 'Defender')).sum()
    if count > max_count:
        max_count = count
        max_pair = (country1, country2)

print(f"The pair of countries most often on different sides (Aggressor/Defender): {max_pair} ({max_count} rows)")

# Zähle für jedes Land, wie oft es "Agressor" oder "Defender" ist
aggressor_counts = {}
defender_counts = {}

for country in country_columns:
    aggressor_counts[country] = (df[country] == 'Agressor').sum()
    defender_counts[country] = (df[country] == 'Defender').sum()

# Finde das Land mit den meisten "Agressor"- und "Defender"-Einträgen
most_aggressor = max(aggressor_counts, key=aggressor_counts.get)
most_defender = max(defender_counts, key=defender_counts.get)

print(f"Most frequent Aggressor: {most_aggressor} ({aggressor_counts[most_aggressor]} times)")
print(f"Most frequent Defender: {most_defender} ({defender_counts[most_defender]} times)")

both_counts = {}

for country in country_columns:
    both_counts[country] = aggressor_counts[country] + defender_counts[country]

most_both = max(both_counts, key=both_counts.get)
print(f"Country most often involved as both Aggressor and Defender: {most_both} ({both_counts[most_both]} times)")


both_role_counts = {}

for country in country_columns:
    both_role_counts[country] = (df[country] == 'Both').sum()

# Sort and print the results
for country, count in sorted(both_role_counts.items(), key=lambda x: x[1], reverse=True):
    if count > 0:
        print(f"{country}: {count} times as Both")


# Bar_chart_race Kriegsteilnahmen
# 1. Wähle die relevanten Spalten aus
# Annahme: 'Startjahr' ist numerisch, country_columns enthält alle Länder-Spalten
df_bcr = df[['Startjahr'] + country_columns].copy()

# 2. Ersetze alle Nicht-NaN-Werte durch 1 (Beteiligung), sonst 0
for country in country_columns:
    df_bcr[country] = df_bcr[country].notna().astype(int)

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
    df_opfer[country] = df_opfer[country].notna().astype(int) * df_opfer['Opferzahlen_Gesamt_bis'].fillna(0)

# 3. Group by year and sum
df_opfer_grouped = df_opfer.groupby('Startjahr')[country_columns].sum()

# 4. Cumulative sum over years
df_opfer_cumulative = df_opfer_grouped.cumsum().sort_index()

# 5. Save for bar_chart_race
df_opfer_cumulative.to_csv("barchartrace_countries_by_opferzahlen.csv")
#print(df_opfer_cumulative.head())