def add_club_force(club_id, total_force):
    query = "INSERT INTO club_forces (club_id, total_force) VALUES (%s, %s)"
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query, (club_id, total_force))
        conn.commit()
        cursor.close()
        conn.close()

def get_club_force(club_id):
    query = "SELECT total_force FROM club_forces WHERE club_id = %s"
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query, (club_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result