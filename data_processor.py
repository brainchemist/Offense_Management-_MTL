import requests
import csv
import sqlite3

CSV_URL = "https://data.montreal.ca/dataset/05a9e718-6810-4e73-8bb9-5955efeb91a0/resource/7f939a08-be8a-45e1-b208-d8744dca8fc6/download/violations.csv"

def download_csv(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Erreur lors du téléchargement du fichier CSV: {response.status_code}")

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS violations (
            id_poursuite INTEGER PRIMARY KEY,
            business_id TEXT,
            date TEXT,
            description TEXT,
            adresse TEXT,
            date_jugement TEXT,
            etablissement TEXT,
            montant REAL,
            proprietaire TEXT,
            ville TEXT,
            statut TEXT,
            date_statut TEXT,
            categorie TEXT
        )
    """)
    conn.commit()

def insert_data(conn, csv_content):
    cursor = conn.cursor()
    reader = csv.DictReader(csv_content.splitlines())
    for row in reader:
        try:
            cursor.execute("""
                INSERT INTO violations (
                    id_poursuite, business_id, date, description, adresse, date_jugement,
                    etablissement, montant, proprietaire, ville, statut, date_statut, categorie
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row['id_poursuite'], row['business_id'], row['date'], row['description'],
                row['adresse'], row['date_jugement'], row['etablissement'], row['montant'],
                row['proprietaire'], row['ville'], row['statut'], row['date_statut'], row['categorie']
            ))
        except sqlite3.IntegrityError:
            # Skip les duplications
            continue
    conn.commit()

def load_data(db_path="violations.db"):
    csv_content = download_csv(CSV_URL)
    conn = sqlite3.connect(db_path)
    create_table(conn)
    insert_data(conn, csv_content)
    conn.close()

