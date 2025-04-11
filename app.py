import json
from datetime import datetime
from flask import Flask, jsonify, render_template, request, redirect
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import sqlite3
from data_processor import load_data  # Import the load_data function
from jsonschema import validate, ValidationError
from urllib.parse import unquote
from urllib.parse import quote


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


@app.route('/contrevenants', methods=['GET'])
def get_contrevenants():
    """Retourne la liste des contrevenants avec leur nombre de contraventions entre deux dates."""
    try:
        # Récupérer les paramètres 'du' et 'au' depuis la requête
        date_du = request.args.get('du')
        date_au = request.args.get('au')

        # Valider que les deux paramètres sont présents
        if not date_du or not date_au:
            return jsonify({"error": "Les paramètres 'du' et 'au' sont requis."}), 400

        # Valider le format des dates (ISO 8601)
        try:
            datetime.fromisoformat(date_du)
            datetime.fromisoformat(date_au)
        except ValueError:
            return jsonify({"error": "Les dates doivent être au format ISO 8601 (YYYY-MM-DD)."}), 400

        # Construire la requête SQL pour regrouper par établissement
        query = """
            SELECT etablissement, COUNT(*) AS nb_contraventions
            FROM violations
            WHERE date BETWEEN ? AND ?
            GROUP BY etablissement
        """
        params = (date_du, date_au)

        # Exécuter la requête sur la base de données
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()

        # Convertir les résultats en format JSON
        data = [{"etablissement": row[0], "nb_contraventions": row[1]} for row in results]
        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/infractions', methods=['GET'])
def get_infractions():
    """Retourne les infractions pour un établissement spécifique."""
    try:
        # Récupérer le paramètre 'etablissement' depuis la requête
        etablissement = request.args.get('etablissement')

        # Valider que le paramètre est présent
        if not etablissement:
            return jsonify({"error": "Le paramètre 'etablissement' est requis."}), 400

        # Construire la requête SQL pour filtrer par établissement
        query = """
            SELECT * FROM violations
            WHERE etablissement = ?
        """
        params = (etablissement,)

        # Exécuter la requête sur la base de données
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()

        # Récupérer les noms des colonnes pour les inclure dans le JSON
        columns = [column[0] for column in cursor.description]

        # Convertir les résultats en format JSON
        data = [dict(zip(columns, row)) for row in results]
        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/etablissements', methods=['GET'])
def get_etablissements():
    """Retourne la liste distincte des établissements."""
    try:
        # Construire la requête SQL pour obtenir les établissements uniques
        query = """
            SELECT DISTINCT etablissement
            FROM violations
            ORDER BY etablissement
        """

        # Exécuter la requête sur la base de données
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()

        # Convertir les résultats en format JSON
        data = [{"etablissement": row[0]} for row in results]
        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/doc', methods=['GET'], endpoint="raml_doc")
def doc():
    """Affiche la documentation RAML du service web."""
    return render_template("doc.html")


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


INSPECTION_SCHEMA = {
    "type": "object",
    "properties": {
        "nom_etablissement": {"type": "string"},
        "adresse": {"type": "string"},
        "ville": {"type": "string"},
        "date_visite": {"type": "string", "format": "date"},
        "nom_client": {"type": "string"},
        "description_probleme": {"type": "string"},
    },
    "required": ["nom_etablissement", "adresse", "ville", "date_visite", "nom_client", "description_probleme"],
    "additionalProperties": False,
}

@app.route('/plainte', methods=['GET'])
def afficher_formulaire_plainte():
    """
    Affiche le formulaire de soumission de plainte.
    """
    return render_template("plainte.html")

@app.route('/plainte', methods=['POST'])
def plainte():
    """
    Traite la soumission d'une plainte et redirige vers une page de confirmation.
    """
    try:
        # Récupérer les données du formulaire
        nom_etablissement = request.form.get("nom_etablissement")
        adresse = request.form.get("adresse")
        ville = request.form.get("ville")
        date_visite = request.form.get("date_visite")
        nom_client = request.form.get("nom_client")
        description_probleme = request.form.get("description_probleme")

        # Valider les données (optionnel, mais recommandé)
        if not all([nom_etablissement, adresse, ville, date_visite, nom_client, description_probleme]):
            return jsonify({"error": "Tous les champs sont requis."}), 400

        # Créer un dictionnaire avec les détails de la plainte
        details = {
            "nom_etablissement": nom_etablissement,
            "adresse": adresse,
            "ville": ville,
            "date_visite": date_visite,
            "nom_client": nom_client,
            "description_probleme": description_probleme
        }

        # Rediriger vers la page de confirmation avec les détails encodés dans l'URL
        details_encoded = quote(json.dumps(details))
        return redirect(f"/confirmation?details={details_encoded}")

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/confirmation', methods=['GET'])
def confirmation():
    """
    Affiche les détails de la plainte pour confirmation.
    """
    try:
        # Récupérer les détails encodés dans l'URL
        details_encoded = request.args.get('details')
        if not details_encoded:
            return jsonify({"error": "Aucun détail de plainte trouvé."}), 400

        # Décoder et parser les détails JSON
        details = json.loads(unquote(details_encoded))

        # Rendre la page de confirmation avec les détails
        return render_template("confirmation.html", details=details)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/demande-inspection", methods=["POST"])
def demande_inspection():
    """Reçoit une demande d'inspection et valide le JSON."""
    try:
        # Récupérer les données JSON envoyées par le client
        data = request.get_json()

        # Valider le JSON avec le schéma défini
        validate(instance=data, schema=INSPECTION_SCHEMA)

        # Insérer les données dans la base de données
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO inspections (
                nom_etablissement, adresse, ville, date_visite, nom_client, description_probleme
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            data["nom_etablissement"],
            data["adresse"],
            data["ville"],
            data["date_visite"],
            data["nom_client"],
            data["description_probleme"]
        ))

        # Récupérer l'ID de la dernière insertion
        inserted_id = cursor.lastrowid

        conn.commit()
        conn.close()

        return jsonify({
            "message": "Demande d'inspection enregistrée avec succès.",
            "id": inserted_id  # Inclure l'ID dans la réponse
        }), 201

    except ValidationError as e:
        return jsonify({"error": f"Validation JSON échouée : {e.message}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/supprimer-demande', methods=['GET'])
def supprimer_demande():
    """Affiche la page pour supprimer une demande d'inspection."""
    return render_template("supprimer_demande.html")

@app.route('/demande-inspection/<int:demande_id>', methods=['DELETE'])
def supprimer_demande_inspection(demande_id):
    """Supprime une demande d'inspection par son ID."""
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Vérifier si l'ID existe
        cursor.execute("SELECT id FROM inspections WHERE id = ?", (demande_id,))
        result = cursor.fetchone()
        if not result:
            return jsonify({"error": "Aucune demande trouvée avec cet ID."}), 404

        # Supprimer la demande
        cursor.execute("DELETE FROM inspections WHERE id = ?", (demande_id,))
        conn.commit()
        conn.close()

        return jsonify({"message": f"Demande d'inspection avec l'ID {demande_id} supprimée avec succès."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    try:
        app.run(debug=True)
    finally:
        scheduler.shutdown()