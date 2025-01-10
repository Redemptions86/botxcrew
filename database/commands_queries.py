def add_command(command_name, description):
    query = "INSERT INTO commands (command_name, description) VALUES (%s, %s)"
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query, (command_name, description))
        conn.commit()
        cursor.close()
        conn.close()

def get_command(command_id):
    query = "SELECT * FROM commands WHERE command_id = %s"
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query, (command_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result

def update_command(command_id, **kwargs):
    set_clause = ", ".join([f"{key} = %s" for key in kwargs])
    query = f"UPDATE commands SET {set_clause} WHERE command_id = %s"
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query, (*kwargs.values(), command_id))
        conn.commit()
        cursor.close()
        conn.close()

def delete_command(command_id):
    query = "DELETE FROM commands WHERE command_id = %s"
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query, (command_id,))
        conn.commit()
        cursor.close()
        conn.close()