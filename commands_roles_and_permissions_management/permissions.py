from discord.ext import commands
import mysql.connector
from mysql_connection import connect_to_db

class PermissionsCog(commands.Cog):
    """Cog pour gérer les permissions des commandes"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def example_command(self, ctx):
        """Commande exemple qui vérifie les permissions avant d'être exécutée."""
        member_id = ctx.author.id  # L'ID Discord du membre
        command_name = 'example_command'  # Le nom de la commande que vous vérifiez

        # Connexion à la base de données
        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                
                # Récupérer l'ID de la commande dans la base de données
                cursor.execute("SELECT command_id FROM commands WHERE command_name = %s", (command_name,))
                command = cursor.fetchone()
                if command:
                    command_id = command[0]
                    
                    # Vérifier les permissions spécifiques pour ce membre
                    cursor.execute("""
                        SELECT permission_level FROM command_permissions
                        WHERE command_id = %s AND discord_id = %s
                    """, (command_id, member_id))
                    permission = cursor.fetchone()

                    # Si aucune permission spécifique pour le membre, vérifier par rôle
                    if not permission:
                        cursor.execute("""
                            SELECT permission_level FROM command_permissions
                            WHERE command_id = %s AND role_id IN (
                                SELECT role_id FROM member_roles WHERE discord_id = %s
                            )
                        """, (command_id, member_id))
                        permission = cursor.fetchone()

                    if permission:
                        if permission[0] == 'allow':
                            await ctx.send("Vous avez la permission d'exécuter cette commande.")
                            # Exécuter la commande ici
                            # Placez le code de votre commande ici
                        else:
                            await ctx.send("Vous n'avez pas la permission d'exécuter cette commande.")
                    else:
                        await ctx.send("Aucune permission définie pour vous ou votre rôle.")
                else:
                    await ctx.send("Commande non trouvée.")
            except Exception as e:
                await ctx.send(f"Erreur lors de la vérification des permissions : {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            await ctx.send("Impossible de se connecter à la base de données.")

def setup(bot):
    bot.add_cog(PermissionsCog(bot))