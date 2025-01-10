from discord.ext import commands
import logging
from datetime import datetime
from .mysql_connection import connect_to_db

class HistoryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def log_action(self, entity_type, entity_id, action_type, action_details, discord_id):
        """Enregistre une action dans l'historique automatiquement."""
        query = """
        INSERT INTO history (entity_type, entity_id, action_type, action_details, action_date, discord_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        action_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Date actuelle
        conn = None
        cursor = None

        try:
            conn = connect_to_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute(query, (entity_type, entity_id, action_type, action_details, action_date, discord_id))
                conn.commit()
                logging.info(f"✅ Entrée ajoutée dans l'historique : {action_type} pour {entity_type} (ID: {entity_id}) par Discord ID: {discord_id}")
        except Exception as e:
            logging.error(f"❌ Erreur lors de l'ajout dans l'historique : {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @commands.command(name="add_role")
    async def add_role(self, ctx, user: discord.Member, role: discord.Role):
        """Ajoute un rôle à un utilisateur et enregistre l'action dans l'historique."""
        await user.add_roles(role)
        self.log_action("role", role.id, "ajout", f"Ajout du rôle {role.name} à {user.name}", ctx.author.id)
        await ctx.send(f"Le rôle {role.name} a été ajouté à {user.name}.")
        
    @commands.command(name="add_club")
    async def add_club(self, ctx, club_name):
        """Ajoute un club et enregistre l'action dans l'historique."""
        # Code pour ajouter un club à la base de données (simulé ici)
        club_id = 123  # Exemple d'ID généré
        self.log_action("club", club_id, "ajout", f"Ajout du club {club_name}", ctx.author.id)
        await ctx.send(f"Le club {club_name} a été ajouté avec succès.")
    
    @commands.command(name="get_history")
    async def get_history(self, ctx, discord_id):
        """Récupère l'historique d'un utilisateur."""
        query = "SELECT * FROM history WHERE discord_id = %s ORDER BY action_date DESC"
        conn = None
        cursor = None

        try:
            conn = connect_to_db()
            if conn:
                cursor = conn.cursor(dictionary=True)  # Récupérer les résultats sous forme de dictionnaire
                cursor.execute(query, (discord_id,))
                result = cursor.fetchall()
                logging.info(f"✅ Historique récupéré pour Discord ID: {discord_id}, {len(result)} entrées trouvées.")
                await ctx.send(f"Historique : {result}")
        except Exception as e:
            logging.error(f"❌ Erreur lors de la récupération de l'historique pour Discord ID {discord_id} : {e}")
            await ctx.send("❌ Erreur lors de la récupération de l'historique.")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

# Ajout du cog à l'extension
def setup(bot):
    bot.add_cog(HistoryCog(bot))