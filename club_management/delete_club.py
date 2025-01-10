import discord
from discord.ext import commands
from database.history_queries import add_history  # Assurez-vous que cette fonction existe

@bot.command()
async def delete_club(ctx, club_id: int):
    """Supprimer un club et enregistrer l'action dans l'historique"""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()

            # Vérifie si le club existe avant de tenter la suppression
            cursor.execute("SELECT * FROM clubs WHERE club_id = %s", (club_id,))
            club = cursor.fetchone()
            if club:
                # Supprimer le club de la table clubs
                query = "DELETE FROM clubs WHERE club_id = %s"
                cursor.execute(query, (club_id,))
                conn.commit()

                # Enregistrement de l'action dans l'historique
                discord_id = ctx.author.id  # ID Discord de l'utilisateur ayant effectué l'action
                entity_type = "club"
                entity_id = club_id  # ID du club supprimé
                action_type = "suppression"
                action_details = f"Suppression du club {club_id} : Nom = {club[1]}, Propriétaire = {club[2]}"
                add_history(entity_type, entity_id, action_type, action_details, discord_id)

                await ctx.send(f"Le club '{club[1]}' (ID: {club_id}) a été supprimé avec succès.")
            else:
                await ctx.send(f"Club avec ID {club_id} introuvable.")
        except Exception as e:
            await ctx.send(f"Erreur lors de la suppression du club : {str(e)}")
        finally:
            cursor.close()
            conn.close()
    else:
        await ctx.send("Impossible de se connecter à la base de données.")