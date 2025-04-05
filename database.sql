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
);

CREATE TABLE IF NOT EXISTS inspections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_etablissement TEXT NOT NULL,
    adresse TEXT NOT NULL,
    ville TEXT NOT NULL,
    date_visite TEXT NOT NULL,
    nom_client TEXT NOT NULL,
    description_probleme TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);