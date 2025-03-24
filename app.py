from flask import Flask, jsonify, render_template, request
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import sqlite3
from data_processor import load_data  # Import the load_data function

app = Flask(__name__)

# Chemin vers la base de données SQLite
DB_PATH = "violations.db"

# Initialiser le BackgroundScheduler
scheduler = BackgroundScheduler()
scheduler.start()

# Planifier la tâche quotidienne à minuit pour charger les données
scheduler.add_job(
    load_data,  # Use the load_data function from data_processor.py
    trigger=CronTrigger(hour=0, minute=0),  # Exécution tous les jours à minuit
    id="sync_data",
    replace_existing=True
)

@app.route('/load-data', methods=['POST'])
def load_data_route():
    """Route pour déclencher manuellement le chargement des données."""
    try:
        load_data()  # Appel à la fonction du fichier data_processor.py
        return jsonify({"message": "Données chargées avec succès"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def index():
    """Page d'accueil avec un formulaire de recherche."""
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    """Traite la recherche et affiche les résultats."""
    # Récupérer les paramètres de recherche depuis le formulaire
    etablissement = request.form.get("etablissement")
    proprietaire = request.form.get("proprietaire")
    rue = request.form.get("rue")

    # Construire la requête SQL dynamique
    query = "SELECT * FROM violations WHERE 1=1"
    params = []

    if etablissement:
        query += " AND etablissement LIKE ?"
        params.append(f"%{etablissement}%")
    if proprietaire:
        query += " AND proprietaire LIKE ?"
        params.append(f"%{proprietaire}%")
    if rue:
        query += " AND adresse LIKE ?"
        params.append(f"%{rue}%")

    # Exécuter la requête sur la base de données
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()

    # Récupérer les noms des colonnes pour les afficher dans le template
    columns = [column[0] for column in cursor.description]

    # Passer les résultats au template
    return render_template("results.html", results=results, columns=columns)


if __name__ == "__main__":
    try:
        # Démarrer l'application Flask
        app.run(debug=True)
    finally:
        # Arrêter le scheduler lorsque l'application est arrêtée
        scheduler.shutdown()