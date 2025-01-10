from database.mysql_connection import connect_to_db

def add_club_match(club_id, opponent_club_1, opponent_club_2, opponent_club_3, opponent_club_4, start_date, end_date):
    query = """
    INSERT INTO club_match (club_id, opponent_club_1, opponent_club_2, opponent_club_3, opponent_club_4, start_date, end_date)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query, (club_id, opponent_club_1, opponent_club_2, opponent_club_3, opponent_club_4, start_date, end_date))
        conn.commit()
        cursor.close()
        conn.close()

def get_club_match(match_id):
    query = "SELECT * FROM club_match WHERE match_id = %s"
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query, (match_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result

def update_club_match(match_id, **kwargs):
    query = "UPDATE club_match SET "
    updates = []
    params = []

    for key, value in kwargs.items():
        updates.append(f"{key} = %s")
        params.append(value)

    query += ", ".join(updates) + " WHERE match_id = %s"
    params.append(match_id)

    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query, tuple(params))
        conn.commit()
        cursor.close()
        conn.close()

def delete_club_match(match_id):
    query = "DELETE FROM club_match WHERE match_id = %s"
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query, (match_id,))
        conn.commit()
        cursor.close()
        conn.close()