# Lister les version de python installées

# utiliser la version 3.12.10

  py -0

# Creer l'environnement virtuel

    py -3.12 -m venv venv

# Activer l'environnement virtuel

    .\venv\Scripts\activate

# Installer les dépendances

    pip install -r requirements.txt

# Creer la structure de base

    # Nous Allons definir une structure de base pour l'application 

# Pour creer les dossiers utiliser la commande

# Création des dossiers

New-Item -ItemType Directory -Path app
New-Item -ItemType Directory -Path app\models
New-Item -ItemType Directory -Path app\controllers
New-Item -ItemType Directory -Path app\routes
New-Item -ItemType Directory -Path app\utils

# Création des fichiers __init__.py

New-Item -ItemType File -Path app\__init__.py
New-Item -ItemType File -Path app\models\__init__.py
New-Item -ItemType File -Path app\controllers\__init__.py
New-Item -ItemType File -Path app\routes\__init__.py
New-Item -ItemType File -Path app\utils\__init__.py

# Création du point d’entrée et du fichier d’environnement

New-Item -ItemType File -Path main.py
New-Item -ItemType File -Path .env

# Configuration # Configuration de l'application Flask dans app/__init__.py

# Configuration de main.py

# Configuration de app/models/__init__.py

# Configuration du fichier .env

SECRET_KEY=3f8d$!kjsd8fjsd9fjsd9fjsd9fjsd9fjsd

# creer la database postgresql et la nommer todos_training

DATABASE_URL=postgresql://postgres:admin@localhost:5432/todo_db

# Initialisation de la base de données et des migrations

# Initialiser le répertoire de migrations

flask --app main db init

# Créer une migration initiale pour créer les tables définies dans les modèles

flask --app main db migrate -m "Initial migration"

# Ensuite appliquer la migration pour créer les tables dans la base de données

flask --app main db upgrade

# ################################################################################################

# Creer un fichiers dans utils Pour la gestion du token

New-Item -ItemType File -Path app\utils\jwt_utils.py

# Creer une methode pour generer le token

# Creer une methode pour decoder le token

# Creer un decorateur pour proteger les routes avec le token

# Creer un decorateur pour proteger les routes avec le role admin

# Creation du controlleur

New-Item -ItemType File -Path app\controllers\todo_controller.py
New-Item -ItemType File -Path app\controllers\user_controller.py

# Creation des routes

New-Item -ItemType File -Path app\routes\todo_routes.py
New-Item -ItemType File -Path app\routes\user_routes.py

# Lancer le serveur

flask --app main run
