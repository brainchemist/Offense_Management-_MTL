from flask import Flask, jsonify
from data_processor import load_data

app = Flask(__name__)

@app.route('/load-data', methods=['POST'])
def load_data_route():
    try:
        load_data()  # Appel à la fonction du fichier data_processor.py
        return jsonify({"message": "Données chargées avec succès"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)