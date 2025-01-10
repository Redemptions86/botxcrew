from database.mysql_connection import connect_to_db

def create_tournament(club_id, club_position, opponent_club_ids, opponent_forces, positions, round, status, start_date, score):
    """Créer un tournoi dans la base de données."""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO tournaments (club_id, club_position, opponent_club_ids, opponent_forces, positions, round, status, start_date, score)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (club_id, club_position, opponent_club_ids, opponent_forces, positions, round, status, start_date, score))
            conn.commit()
        except Exception as e:
            raise Exception(f"Erreur lors de la création du tournoi : {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        raise Exception("Impossible de se connecter à la base de données.")

def add_club_with_validation(club_name, club_owner):
    """Ajouter un club à la base de données avec validation."""
    if not club_name or not club_owner:
        return "Le nom du club et le propriétaire ne peuvent pas être vides."

    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            # Vérifier si le club existe déjà
            cursor.execute("SELECT * FROM clubs WHERE name = %s", (club_name,))
            existing_club = cursor.fetchone()
            if existing_club:
                return f"Un club avec le nom '{club_name}' existe déjà."

            # Ajouter le club
            query = "INSERT INTO clubs (name, owner) VALUES (%s, %s)"
            cursor.execute(query, (club_name, club_owner))
            conn.commit()
            return "Le club a été ajouté avec succès."
        except Exception as e:
            raise Exception(f"Erreur lors de l'ajout du club : {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        raise Exception("Impossible de se connecter à la base de données.")

def get_club_by_name(club_name):
    """Récupérer un club par son nom."""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM clubs WHERE name = %s"
            cursor.execute(query, (club_name,))
            club = cursor.fetchone()
            return club
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération du club : {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        raise Exception("Impossible de se connecter à la base de données.")