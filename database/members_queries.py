from database.mysql_connection import connect_to_db

def add_member(discord_id, pseudo, club_id, force_team1, force_team2):
    query = """
    INSERT INTO members (discord_id, pseudo, club_id, force_team1, force_team2, creation_date)
    VALUES (%s, %s, %s, %s, %s, NOW())
    """
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query, (discord_id, pseudo, club_id, force_team1, force_team2))
        conn.commit()
        cursor.close()
        conn.close()

def get_member(discord_id):
    query = "SELECT * FROM members WHERE discord_id = %s"
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query, (discord_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result

def update_member(discord_id, pseudo=None, club_id=None, force_team1=None, force_team2=None):
    query = "UPDATE members SET "
    updates = []
    params = []

    if pseudo:
        updates.append("pseudo = %s")
        params.append(pseudo)
    if club_id:
        updates.append("club_id = %s")
        params.append(club_id)
    if force_team1:
        updates.append("force_team1 = %s")
        params.append(force_team1)
    if force_team2:
        updates.append("force_team2 = %s")
        params.append(force_team2)

    query += ", ".join(updates) + " WHERE discord_id = %s"
    params.append(discord_id)

    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query, tuple(params))
        conn.commit()
        cursor.close()
        conn.close()

def delete_member(discord_id):
    query = "DELETE FROM members WHERE discord_id = %s"
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query, (discord_id,))
        conn.commit()
        cursor.close()
        conn.close()