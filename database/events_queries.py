def add_event(event_name, event_date, description):
    query = "INSERT INTO events (event_name, event_date, description) VALUES (%s, %s, %s)"
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query, (event_name, event_date, description))
        conn.commit()
        cursor.close()
        conn.close()

def get_event(event_id):
    query = "SELECT * FROM events WHERE event_id = %s"
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query, (event_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result