def add_member_role(role_id, role_name):
    query = "INSERT INTO member_roles (role_id, role_name) VALUES (%s, %s)"
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query, (role_id, role_name))
        conn.commit()
        cursor.close()
        conn.close()

def get_member_role(role_id):
    query = "SELECT * FROM member_roles WHERE role_id = %s"
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query, (role_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result