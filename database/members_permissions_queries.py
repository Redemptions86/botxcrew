def add_member_permission(member_id, permission_level):
    query = "INSERT INTO members_permissions (member_id, permission_level) VALUES (%s, %s)"
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query, (member_id, permission_level))
        conn.commit()
        cursor.close()
        conn.close()

def get_member_permissions(member_id):
    query = "SELECT permission_level FROM members_permissions WHERE member_id = %s"
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query, (member_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result