
# **README**

## **Français**

### **Description du Projet**
Ce projet est une application web Flask qui permet de gérer et consulter des données sur les violations (contraventions) commises par des établissements. L'application offre des fonctionnalités pour rechercher des contraventions, soumettre des plaintes, et gérer des demandes d'inspection. Les données sont stockées dans une base de données SQLite et synchronisées quotidiennement à partir d'un fichier CSV fourni par la ville de Montréal.

---

### **Fonctionnalités Principales**
1. **Recherche de Contraventions**:
   - Recherche par nom d'établissement, propriétaire, ou rue.
   - Recherche rapide par plage de dates avec AJAX.

2. **API RESTful**:
   - Obtenir les contrevenants entre deux dates (`/contrevenants`).
   - Obtenir les infractions pour un établissement spécifique (`/infractions`).
   - Obtenir la liste des établissements ayant commis des infractions (`/etablissements-infraction`).

3. **Soumission de Plaintes**:
   - Formulaire pour soumettre une plainte avec validation des champs.
   - Confirmation de la plainte avant enregistrement.

4. **Demandes d'Inspection**:
   - API pour créer une demande d'inspection avec validation JSON.
   - Suppression d'une demande d'inspection via une API RESTful.

5. **Synchronisation Automatique**:
   - Les données sont synchronisées quotidiennement à minuit à partir du fichier CSV de la ville de Montréal.

6. **Gestion des Erreurs**:
   - Pages personnalisées pour les erreurs 404 et 500.

---

### **Installation et Configuration**

#### **Prérequis**
- Python 3.x
- Flask
- SQLite
- Bibliothèques Python nécessaires : `apscheduler`, `jsonschema`, `requests`

#### **Étapes d'Installation**
1. Clonez le dépôt :
   ```bash
   git clone https://github.com/votre-repo/contraventions.git
   cd contraventions
   ```

2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

3. Configurez la base de données :
   - Assurez-vous que le fichier `violations.db` existe ou exécutez la commande suivante pour charger les données initiales :
     ```bash
     python data_processor.py
     ```

4. Démarrez l'application :
   ```bash
   python app.py
   ```

5. Accédez à l'application dans votre navigateur :
   ```
   http://localhost:5000
   ```

---

### **Utilisation**
- **Page d'accueil** : Recherchez des contraventions par établissement, propriétaire, ou rue.
- **API** : Utilisez les endpoints RESTful pour interagir avec les données.
- **Soumission de Plaintes** : Remplissez le formulaire de plainte et confirmez les détails.
- **Demandes d'Inspection** : Utilisez les endpoints `/demande-inspection` pour créer ou supprimer des demandes.

---

## **English**

### **Project Description**
This project is a Flask-based web application designed to manage and query data on violations (infractions) committed by establishments. The application provides features for searching violations, submitting complaints, and managing inspection requests. Data is stored in an SQLite database and synchronized daily from a CSV file provided by the city of Montreal.

---

### **Key Features**
1. **Violation Search**:
   - Search by establishment name, owner, or street.
   - Quick search by date range using AJAX.

2. **RESTful API**:
   - Get offenders between two dates (`/contrevenants`).
   - Get infractions for a specific establishment (`/infractions`).
   - Get a list of establishments with infractions (`/etablissements-infraction`).

3. **Complaint Submission**:
   - Form to submit a complaint with field validation.
   - Confirmation page before saving the complaint.

4. **Inspection Requests**:
   - API to create an inspection request with JSON validation.
   - Delete an inspection request via a RESTful API.

5. **Automatic Synchronization**:
   - Data is synchronized daily at midnight from the Montreal city CSV file.

6. **Error Handling**:
   - Custom pages for 404 and 500 errors.

---

### **Installation and Setup**

#### **Prerequisites**
- Python 3.x
- Flask
- SQLite
- Required Python libraries: `apscheduler`, `jsonschema`, `requests`

#### **Installation Steps**
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/violations.git
   cd violations
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the database:
   - Ensure the `violations.db` file exists or run the following command to load initial data:
     ```bash
     python data_processor.py
     ```

4. Start the application:
   ```bash
   python app.py
   ```

5. Access the application in your browser:
   ```
   http://localhost:5000
   ```

---

### **Usage**
- **Homepage**: Search for violations by establishment, owner, or street.
- **API**: Use the RESTful endpoints to interact with the data.
- **Complaint Submission**: Fill out the complaint form and confirm the details.
- **Inspection Requests**: Use the `/demande-inspection` endpoints to create or delete requests.

---

### **API Endpoints**

#### **GET /contrevenants**
- **Description**: Returns a list of offenders with their number of violations between two dates.
- **Parameters**:
  - `du`: Start date (ISO 8601 format, e.g., `2023-01-01`).
  - `au`: End date (ISO 8601 format, e.g., `2023-12-31`).
- **Response**:
  ```json
  [
      {"etablissement": "Restaurant A", "nb_contraventions": 5},
      {"etablissement": "Restaurant B", "nb_contraventions": 3}
  ]
  ```

#### **GET /infractions**
- **Description**: Returns infractions for a specific establishment.
- **Parameters**:
  - `etablissement`: Name of the establishment.
- **Response**:
  ```json
  [
      {
          "date": "2023-01-15",
          "description": "Hygiene violation",
          "adresse": "123 Main St",
          "montant": 500,
          "statut": "Resolved"
      }
  ]
  ```

#### **POST /demande-inspection**
- **Description**: Creates an inspection request.
- **Request Body**:
  ```json
  {
      "nom_etablissement": "Restaurant C",
      "adresse": "456 Elm St",
      "ville": "Montreal",
      "date_visite": "2023-10-01",
      "nom_client": "John Doe",
      "description_probleme": "Food safety issue"
  }
  ```
- **Response**:
  ```json
  {
      "message": "Inspection request successfully registered.",
      "id": 1
  }
  ```

#### **DELETE /demande-inspection/{id}**
- **Description**: Deletes an inspection request by ID.
- **Response**:
  ```json
  {
      "message": "Inspection request with ID 1 successfully deleted."
  }
  ```

---

### **Contributing**
If you'd like to contribute to this project, please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a detailed description of your changes.

---

### **License**
This project is licensed under the MIT License. See the `LICENSE` file for more details.

---
