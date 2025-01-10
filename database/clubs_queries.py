from database.mysql_connection import execute_query  # Assurez-vous d'importer la fonction execute_query

def get_club_by_name(club_name):
    """Récupère un club par son nom."""
    try:
        query = "SELECT * FROM clubs WHERE club_name = %s"
        result = execute_query(query, (club_name,))
        return result[0] if result else None  # Retourne le premier résultat ou None si aucun club trouvé
    except Exception as e:
        print(f"Erreur lors de la récupération du club par nom : {e}")
        return None  # Retourne None en cas d'erreur

def get_club_by_id(club_id):
    """Récupère un club par son ID."""
    try:
        query = "SELECT * FROM clubs WHERE club_id = %s"
        result = execute_query(query, (club_id,))
        return result[0] if result else None  # Retourne le premier résultat ou None si aucun club trouvé
    except Exception as e:
        print(f"Erreur lors de la récupération du club par ID : {e}")
        return None

def add_club(club_name, club_owner):
    """Ajoute un club dans la base de données."""
    try:
        query = "INSERT INTO clubs (club_name, club_owner) VALUES (%s, %s)"
        execute_query(query, (club_name, club_owner))  # Utilisation de execute_query pour l'insertion
    except Exception as e:
        print(f"Erreur lors de l'ajout du club : {e}")

def update_club(club_id, new_club_name, new_club_owner):
    """Met à jour un club dans la base de données."""
    try:
        query = "UPDATE clubs SET club_name = %s, club_owner = %s WHERE club_id = %s"
        execute_query(query, (new_club_name, new_club_owner, club_id))  # Utilisation de execute_query pour la mise à jour
    except Exception as e:
        print(f"Erreur lors de la mise à jour du club : {e}")

def delete_club(club_id):
    """Supprime un club de la base de données."""
    try:
        query = "DELETE FROM clubs WHERE club_id = %s"
        execute_query(query, (club_id,))  # Utilisation de execute_query pour la suppression
    except Exception as e:
        print(f"Erreur lors de la suppression du club : {e}")

def list_clubs():
    """Récupère la liste de tous les clubs."""
    try:
        query = "SELECT club_id, club_name, points FROM clubs"
        result = execute_query(query)
        return result if result else []  # Retourne la liste des clubs ou une liste vide si aucun club trouvé
    except Exception as e:
        print(f"Erreur lors de la récupération des clubs : {e}")
        return []

def add_club_with_validation(club_name, club_owner):
    """Ajouter un club avec vérification de doublon et validation des données."""
    try:
        existing_club = get_club_by_name(club_name)
        if existing_club:
            return f"Un club avec le nom '{club_name}' existe déjà."
        
        if not club_name.strip() or not club_owner.strip():
            return "Le nom du club et le nom du propriétaire ne peuvent pas être vides."
        
        add_club(club_name, club_owner)
        return f"Le club '{club_name}' a été ajouté avec succès."
    except Exception as e:
        print(f"Erreur lors de l'ajout du club avec validation : {e}")
        return "Une erreur est survenue lors de l'ajout du club."