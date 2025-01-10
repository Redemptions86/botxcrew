import mysql.connector
import os
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

# Variables de connexion
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "botxcrew")

# Fonction pour obtenir la connexion
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Erreur de connexion : {err}")
        return None

def execute_query(query, params=None):
    """Exécute une requête SQL et retourne le résultat."""
    connection = get_connection()
    if connection is None:
        return None
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, params)
    if query.strip().lower().startswith('select'):
        result = cursor.fetchall()  # Récupère les résultats pour les requêtes SELECT
    else:
        connection.commit()  # Applique les modifications pour INSERT, UPDATE, DELETE
        result = None
    cursor.close()
    connection.close()
    return result

# Fonction pour fermer la connexion
def close_connection(connection):
    if connection and connection.is_connected():
        connection.close()
        print("Connexion fermée.")