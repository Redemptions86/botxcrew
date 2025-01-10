import discord
from discord.ext import commands
from database.history_queries import add_history  # Assurez-vous que cette fonction existe

@bot.command()
async def add_mod_club(ctx, club_id: int, new_club_name: str, new_club_owner: str):
    """Modifier un club et enregistrer l'action dans l'historique."""
    try:
        # Vérifie si le club existe avant de tenter la mise à jour
        club = get_club_by_id(club_id)
        if club:
            # Validation des nouvelles données
            if not new_club_name.strip() or not new_club_owner.strip():1244013791268835462
                await ctx.send("Le nom du club et le nom du propriétaire ne peuvent pas être vides.")
                return

            # Mise à jour du club avec les nouvelles informations
            update_club(club_id, new_club_name, new_club_owner)

            # Enregistrement de l'action dans l'historique
            discord_id = ctx.author.id  # ID Discord de l'utilisateur ayant effectué l'action
            entity_type = "club"
            entity_id = club_id  # Utilisation de l'ID du club
            action_type = "modification"
            action_details = f"Modification du club {club_id} : Nouveau nom = {new_club_name}, Nouveau propriétaire = {new_club_owner}"
            add_history(entity_type, entity_id, action_type, action_details, discord_id)

            await ctx.send(f"Le club '{new_club_name}' (ID: {club_id}) a été mis à jour avec succès.")
        else:
            await ctx.send(f"Club avec ID {club_id} introuvable.")
    except Exception as e:
        await ctx.send(f"Erreur lors de la mise à jour du club : {e}")