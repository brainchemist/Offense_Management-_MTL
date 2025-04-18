
## **Introduction**
Ce document décrit les fonctionnalités développées dans le cadre du projet ainsi que les instructions pour tester chaque point. Chaque section correspond à un des points mentionnés dans l'énoncé.

---

## **A1 (10xp): Téléchargement des données CSV et insertion dans une base de données SQLite**
### **Description**
- Les données des contraventions sont téléchargées depuis l'URL suivante :  
  [https://data.montreal.ca/dataset/05a9e718-6810-4e73-8bb9-5955efeb91a0/resource/7f939a08-be8a-45e1-b208-d8744dca8fc6/download/violations.csv](https://data.montreal.ca/dataset/05a9e718-6810-4e73-8bb9-5955efeb91a0/resource/7f939a08-be8a-45e1-b208-d8744dca8fc6/download/violations.csv)
- Les données sont insérées dans une base de données SQLite (`violations.db`) via un script Python (`data_processor.py`).

### **Comment tester**
1. Exécutez le script Python manuellement :
   ```python
   from data_processor import load_data
   load_data()
   ```
2. Vérifiez que la base de données `violations.db` contient les données :
   ```bash
   sqlite3 violations.db
   SELECT COUNT(*) FROM violations;
   ```

---

## **A2 (10xp): Application Flask pour rechercher des contraventions**
### **Description**
- Une application Flask permet de rechercher des contraventions par :
  - Nom d'établissement
  - Propriétaire
  - Rue
- Les résultats sont affichés sur une nouvelle page (`results.html`).

### **Comment tester**
1. Démarrez l'application Flask :
   ```bash
   python app.py
   ```
2. Accédez à la page d'accueil (`http://localhost:5000`).
3. Utilisez le formulaire de recherche pour saisir des critères (nom d'établissement, propriétaire ou rue).
4. Vérifiez que les résultats s'affichent correctement.

---

## **A3 (5xp): Synchronisation quotidienne des données avec BackgroundScheduler**
### **Description**
- Un `BackgroundScheduler` est utilisé pour synchroniser les données de la ville de Montréal tous les jours à minuit.
- La tâche est planifiée avec `CronTrigger`.

### **Comment tester**
1. Déclenchez manuellement la synchronisation en utilisant l'endpoint `/load-data` :
   ```bash
   curl -X POST http://localhost:5000/load-data
   ```
2. Vérifiez que les données ont été mises à jour dans la base de données :
   ```bash
   sqlite3 violations.db
   SELECT COUNT(*) FROM violations;
   ```

---

## **A4 (10xp): API REST pour obtenir les contraventions entre deux dates**
### **Description**
- L'API retourne la liste des établissements ayant reçu des contraventions entre deux dates spécifiées.
- Endpoint : `/contrevenants?du=YYYY-MM-DD&au=YYYY-MM-DD`
- Format de réponse : JSON.

### **Comment tester**
1. Utilisez un outil comme `curl` ou Postman pour interroger l'API :
   ```bash
   curl "http://localhost:5000/contrevenants?du=2022-01-01&au=2022-12-31"
   ```
2. Vérifiez que la réponse contient les données attendues au format JSON.

---

## **A5 (10xp): Recherche rapide par dates avec AJAX**
### **Description**
- Un formulaire de recherche rapide permet de saisir deux dates et d'afficher les résultats via une requête AJAX.
- Les résultats sont affichés dans un tableau avec deux colonnes : nom de l'établissement et nombre de contraventions.

### **Comment tester**
1. Accédez à la page d'accueil (`http://localhost:5000`).
2. Utilisez le formulaire "Recherche rapide par dates" pour saisir deux dates.
3. Vérifiez que les résultats s'affichent dynamiquement sans recharger la page.

---

## **A6 (10xp): Recherche par nom d'établissement avec AJAX**
### **Description**
- Une liste déroulante contient tous les établissements distincts.
- L'utilisateur peut sélectionner un établissement et afficher ses infractions via une requête AJAX.

### **Comment tester**
1. Accédez à la page d'accueil (`http://localhost:5000`).
2. Utilisez le formulaire "Recherche par nom d'établissement".
3. Sélectionnez un établissement dans la liste déroulante et vérifiez que les résultats s'affichent dynamiquement.

---

## **C1 (10xp): API REST pour les établissements ayant commis des infractions**
### **Description**
- L'API retourne une liste d'établissements triée par nombre d'infractions en ordre décroissant.
- Endpoint : `/etablissements-infraction`
- Format de réponse : JSON.

### **Comment tester**
1. Utilisez un outil comme `curl` ou Postman pour interroger l'API :
   ```bash
   curl http://localhost:5000/etablissements-infraction
   ```
2. Vérifiez que la réponse contient les données attendues au format JSON.

---

## **D1 (15xp): API REST pour soumettre une demande d'inspection**
### **Description**
- L'API permet de soumettre une demande d'inspection via une requête POST.
- Le JSON doit être validé avec un schéma (`INSPECTION_SCHEMA`).
- Endpoint : `/demande-inspection`

### **Comment tester**
1. Utilisez un outil comme `curl` ou Postman pour envoyer une requête POST :
   ```bash
   curl -X POST http://localhost:5000/demande-inspection \
        -H "Content-Type: application/json" \
        -d '{"nom_etablissement": "Test", "adresse": "123 Rue Test", "ville": "Montreal", "date_visite": "2023-01-01", "nom_client": "John Doe", "description_probleme": "Problème test"}'
   ```
2. Vérifiez que la réponse contient un message de succès et l'ID de la demande.

---

## **D2 (5xp): API REST pour supprimer une demande d'inspection**
### **Description**
- L'API permet de supprimer une demande d'inspection via une requête DELETE.
- Endpoint : `/demande-inspection/<int:demande_id>`

### **Comment tester**
1. Utilisez un outil comme `curl` ou Postman pour envoyer une requête DELETE :
   ```bash
   curl -X DELETE http://localhost:5000/demande-inspection/1
   ```
2. Vérifiez que la réponse confirme la suppression.

---

## **F1 (15xp): Déploiement sur une plateforme infonuagique**
### **Description**
- L'application est entièrement déployée sur une plateforme infonuagique (par exemple, Heroku, AWS, ou Render).
- URL de l'application : [https://chaca425.pythonanywhere.com/supprimer-demande]

---

**Fin du fichier `correction.md`.**