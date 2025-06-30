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
    csv_war_list_all = [] # Liste aller Kriegsnamen aus der CSV
    csv_skipped_rows = 0

    print(f"Lese Kriege aus CSV-Datei: {CSV_FILE_PATH}")
    try:
        with open(CSV_FILE_PATH, mode='r', encoding='utf-8-sig') as csvfile:
            csv_reader = csv.reader(csvfile)
            header = next(csv_reader)

            for i, row in enumerate(csv_reader):
                current_row_num_in_file = i + 2
                if not any(field.strip() for field in row):
                    csv_skipped_rows +=1
                    continue
                if len(row) != EXPECTED_COLUMNS_IN_DATA:
                    print(f"Info CSV: Zeile {current_row_num_in_file} hat {len(row)} Spalten, erwartet {EXPECTED_COLUMNS_IN_DATA}. Übersprungen für diesen Vergleich.")
                    csv_skipped_rows +=1
                    continue
                try:
                    war_name = row[CSV_KRIEG_COLUMN_INDEX].strip()
                    if war_name: # Nur hinzufügen, wenn der Name nicht leer ist
                        csv_war_list_all.append(war_name)
                    else:
                        print(f"Info CSV: Kriegsname in Zeile {current_row_num_in_file} ist leer.")
                        csv_skipped_rows +=1
                except IndexError:
                    print(f"Fehler CSV: Zeile {current_row_num_in_file} hat nicht genügend Spalten für Kriegsnamen.")
                    csv_skipped_rows +=1
                    continue
    except FileNotFoundError:
        print(f"Fehler: CSV-Datei '{CSV_FILE_PATH}' nicht gefunden.")
        return
    except Exception as e:
        print(f"Fehler beim Lesen der CSV: {e}")
        return

    print(f"{len(csv_war_list_all)} Kriege (potenziell mit Duplikaten) aus CSV geladen (nach Überspringen von {csv_skipped_rows} Zeilen).")

    # Zähle Duplikate in der CSV
    csv_war_counts = Counter(csv_war_list_all)
    csv_unique_wars_set = set(csv_war_list_all)
    csv_duplicate_names = {name: count for name, count in csv_war_counts.items() if count > 1}

    print(f"{len(csv_unique_wars_set)} einzigartige Kriegsnamen in der CSV-Liste.")
    if csv_duplicate_names:
        print(f"{len(csv_duplicate_names)} Kriegsname(n) kommen in der CSV mehrfach vor:")
        for name, count in csv_duplicate_names.items():
            print(f"  - '{name}' (kommt {count} Mal vor)")
    else:
        print("Keine Duplikate (basierend auf Kriegsnamen) in der CSV-Liste gefunden.")

    # --- Aus der Datenbank lesen ---
    db_war_list_all = []
    db_row_count_actual = 0
    conn_db_count = None
    try:
        conn_db_count = sqlite3.connect(DB_FILE_PATH)
        cursor_db_count = conn_db_count.cursor()
        # Tatsächliche Zeilenzahl ermitteln
        cursor_db_count.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
        db_row_count_actual = cursor_db_count.fetchone()[0]

        # Alle Kriegsnamen aus der DB holen
        cursor_db_count.execute(f"SELECT \"{DB_KRIEG_COLUMN_NAME}\" FROM {TABLE_NAME}")
        for row in cursor_db_count:
            if row[0] is not None: # Ignoriere NULL-Werte für den Kriegsnamen, falls vorhanden
                 db_war_list_all.append(row[0].strip())
            else:
                print("Info DB: Ein Kriegsname in der DB ist NULL.")
        conn_db_count.close()
    except sqlite3.Error as e:
        print(f"SQLite Fehler beim Lesen der DB: {e}")
        if conn_db_count: conn_db_count.close()
        return

    print(f"\nDatenbank-Analyse:")
    print(f"Tatsächliche Zeilenanzahl in DB-Tabelle '{TABLE_NAME}' laut COUNT(*): {db_row_count_actual}")
    print(f"{len(db_war_list_all)} Kriegsnamen aus DB geladen (nach .strip() und ohne NULLs).")

    db_war_counts = Counter(db_war_list_all)
    db_unique_wars_set = set(db_war_list_all)
    db_duplicate_names = {name: count for name, count in db_war_counts.items() if count > 1}

    print(f"{len(db_unique_wars_set)} einzigartige Kriegsnamen in der DB-Liste (nach .strip()).")
    if db_duplicate_names:
        print(f"ACHTUNG: {len(db_duplicate_names)} Kriegsname(n) kommen in der DB-Liste MEHRFACH vor (sollte bei PRIMARY KEY nicht sein, es sei denn .strip() führt zu Kollisionen):")
        for name, count in db_duplicate_names.items():
            print(f"  - '{name}' (kommt {count} Mal vor in der DB-Liste nach .strip())")
    else:
        print("Keine Duplikate in der DB-Liste der Kriegsnamen gefunden (nach .strip()).")


    # --- Vergleiche die Sets ---
    print("\nVergleich der einzigartigen Kriegsnamen-Sets:")
    missing_in_db_set = csv_unique_wars_set - db_unique_wars_set
    missing_in_csv_set = db_unique_wars_set - csv_unique_wars_set

    if missing_in_db_set:
        print(f"\n{len(missing_in_db_set)} EINZIGARTIGE Kriege sind im CSV-Set, aber NICHT im DB-Set:")
        for war in sorted(list(missing_in_db_set)):
            print(f"  - '{war}'")
    else:
        print("\nAlle einzigartigen Kriege aus dem CSV-Set sind auch im DB-Set vorhanden.")

    if missing_in_csv_set:
        print(f"\n{len(missing_in_csv_set)} EINZIGARTIGE Kriege sind im DB-Set, aber NICHT im CSV-Set (sollte nicht passieren, wenn CSV die Quelle ist):")
        for war in sorted(list(missing_in_csv_set)):
            print(f"  - '{war}'")
    else:
        print("\nAlle einzigartigen Kriege aus dem DB-Set sind auch im CSV-Set vorhanden.")

    print("\n--- Zusammenfassung der Zählungen ---")
    print(f"CSV: {len(csv_war_list_all)} gelesene Namen (potenziell mit Duplikaten)")
    print(f"CSV: {len(csv_unique_wars_set)} einzigartige Namen")
    print(f"DB (COUNT(*)): {db_row_count_actual} Zeilen")
    print(f"DB: {len(db_war_list_all)} gelesene Namen (ignoriert NULLs, .strip() angewendet)")
    print(f"DB: {len(db_unique_wars_set)} einzigartige Namen (nach .strip())")

    if len(csv_unique_wars_set) == db_row_count_actual and not missing_in_db_set and not missing_in_csv_set and not csv_duplicate_names:
        print("\nPerfekte Übereinstimmung zwischen einzigartigen CSV-Namen und DB-Zeilenanzahl, keine Duplikate in CSV.")
    elif len(csv_war_list_all) - len(csv_duplicate_names) == db_row_count_actual and not missing_in_db_set and not missing_in_csv_set :
         # Diese Logik ist nicht ganz korrekt, wenn csv_duplicate_names die Anzahl der Namen ist, nicht die Anzahl der Duplikat-Instanzen
         num_lost_to_duplicates = sum(count - 1 for count in csv_duplicate_names.values())
         if len(csv_war_list_all) - num_lost_to_duplicates == db_row_count_actual:
            print(f"\nDie Differenz zwischen CSV-Rohdaten ({len(csv_war_list_all)}) und DB-Zeilen ({db_row_count_actual}) scheint durch {num_lost_to_duplicates} Duplikat-Instanzen in der CSV erklärt zu werden.")


if __name__ == '__main__':
    compare_csv_and_db_wars()