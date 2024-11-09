import sqlite3
from fileinput import close
from sqlite3 import Error

from config.config import DATABASE_FILE
from debug.debug import debug


# Fonction pour créer une connexion à la base de données SQLite
def create_connection(db_file):
    """Crée une connexion à une base de données SQLite"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connexion réussie à la base de données : {db_file}")
    except Error as e:
        print(f"Erreur lors de la connexion à la base de données : {e}")
    return conn


# Fonction pour fermer la connexion à la base de données
def close_connection(conn):
    """Ferme la connexion à la base de données"""
    if conn:
        conn.close()
        print("Connexion fermée.")


# Fonction pour exécuter une requête SQL (sans retour de résultats)
def execute_query(query, params=None):
    """Exécute une requête SQL sans retour (ex: INSERT, UPDATE, DELETE)"""
    conn = None
    try:
        conn = create_connection(DATABASE_FILE)
    except Exception as e:
        print(f"[DATABASE] Erreur : {e}")

    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(query, params or [])
            print("Requête exécutée avec succès.")
    except Error as e:
        print(f"[DATABASE] Erreur lors de l'exécution de la requête : {e}")

    try:
        close_connection(conn)
    except Exception as e:
        print(f"[DATABASE] Erreur : {e}")


# Fonction pour exécuter une requête de sélection (avec retour de résultats)
def execute_read_query(query, params=None):
    """Exécute une requête de lecture SQL et retourne les résultats"""
    conn = None
    try:
        conn = create_connection(DATABASE_FILE)
    except Exception as e:
        print(f"[DATABASE] Erreur : {e}")

    try:
        cursor = conn.cursor()
        cursor.execute(query, params or [])
        rows = cursor.fetchall()
        close_connection(conn)
        return rows
    except Error as e:
        print(f"Erreur lors de l'exécution de la requête de lecture : {e}")
        
        try: 
            close_connection(conn)
        except Exception as e:
            print(f"[DATABASE] Erreur : {e}")
        return []


# Fonction pour insérer un message
def archive_message(message_id: int, channel_id: int, content: str, author_id: int):
    """Insérer un message dans la table"""
    conn = create_connection(DATABASE_FILE)
    query = """INSERT INTO history (id, content, channel_id, author_id) VALUES (?, ?, ?, ?);"""
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(query, (message_id, content, channel_id, author_id))
            debug("[DATABASE] Message inséré avec succès")
    except Error as e:
        print(f"[DATABASE] Erreur lors de l'insertion : {e}")