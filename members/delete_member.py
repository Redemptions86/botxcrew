@bot.command()
async def delete_member(ctx, discord_id: int):
    """Supprimer un membre de la base de données"""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()

            # Vérifier si le membre existe
            cursor.execute("SELECT * FROM members WHERE discord_id = %s", (discord_id,))
            member_data = cursor.fetchone()
            if not member_data:
                await ctx.send(f"Aucun membre trouvé avec l'ID Discord {discord_id}.")
                return

            # Supprimer le membre de la base de données
            query = "DELETE FROM members WHERE discord_id = %s"
            cursor.execute(query, (discord_id,))
            conn.commit()

            # Enregistrer l'action dans l'historique
            history_query = """
            INSERT INTO history (entity_type, entity_id, action_type, action_details)
            VALUES (%s, %s, %s, %s)
            """
            action_details = f"Le membre avec ID {discord_id} a été supprimé de la base de données."
            cursor.execute(history_query, ("member", discord_id, "suppression", action_details))
            conn.commit()

            await ctx.send(f"Membre avec ID {discord_id} supprimé avec succès.")
        except Exception as e:
            await ctx.send(f"Erreur lors de la suppression du membre : {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        await ctx.send("Impossible de se connecter à la base de données.")