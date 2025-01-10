def add_command_translation(command_id, language, translation_text):
    query = """
    INSERT INTO command_translations (command_id, language, translation_text)
    VALUES (%s, %s, %s)
    """
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query, (command_id, language, translation_text))
        conn.commit()
        cursor.close()
        conn.close()

def get_command_translation(command_id, language):
    query = "SELECT translation_text FROM command_translations WHERE command_id = %s AND language = %s"
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query, (command_id, language))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result