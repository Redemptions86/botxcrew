from discord.ext import commands
from decorators import format_as_table
from mysql_connection import connect_to_db

@commands.command()
@format_as_table(headers=["Discord ID", "Pseudo", "Force", "Rôle"])
async def list_members(ctx, club_id: int):
    """
    Liste les membres d'un club.
    """
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
            SELECT m.discord_id, m.pseudo, m.force, r.role_name
            FROM members m
            LEFT JOIN member_roles mr ON m.member_id = mr.member_id
            LEFT JOIN roles r ON mr.role_id = r.role_id
            WHERE m.club_id = %s
            """
            cursor.execute(query, (club_id,))
            members = cursor.fetchall()
            return members
        finally:
            cursor.close()
            conn.close()
    else:
        raise Exception("Impossible de se connecter à la base de données.")