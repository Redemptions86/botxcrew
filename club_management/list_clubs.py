from discord.ext import commands
from decorators import format_as_table
from mysql_connection import connect_to_db

@commands.command()
@format_as_table(headers=["Club ID", "Nom", "Points"])
async def list_clubs(ctx):
    """
    Liste tous les clubs.
    """
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            query = "SELECT club_id, name, points FROM clubs"
            cursor.execute(query)
            clubs = cursor.fetchall()
            return clubs
        finally:
            cursor.close()
            conn.close()
    else:
        raise Exception("Impossible de se connecter à la base de données.")