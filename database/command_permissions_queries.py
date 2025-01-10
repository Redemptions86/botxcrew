def add_command_permission(command_id, role_id):
    query = "INSERT INTO command_permissions (command_id, role_id) VALUES (%s, %s)"
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query, (command_id, role_id))
        conn.commit()
        cursor.close()
        conn.close()

def get_command_permissions(command_id):
    query = "SELECT role_id FROM command_permissions WHERE command_id = %s"
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query, (command_id,))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result