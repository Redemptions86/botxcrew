@bot.command()
async def add_update_member(ctx, discord_id: int, new_pseudo: str):
    """Ajouter ou modifier le pseudo d'un membre"""
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

            # Mettre à jour le pseudo du membre
            query = "UPDATE members SET pseudo = %s WHERE discord_id = %s"
            cursor.execute(query, (new_pseudo, discord_id))
            conn.commit()

            if cursor.rowcount > 0:
                # Récupérer le `history_id` du dernier ajout ou mise à jour
                cursor.execute("SELECT LAST_INSERT_ID()")
                history_id = cursor.fetchone()[0]

                # Enregistrer l'action dans l'historique
                history_query = """
                INSERT INTO history (history_id, entity_type, entity_id, action_type, action_details)
                VALUES (%s, %s, %s, %s, %s)
                """
                action_details = f"Le pseudo du membre avec ID {discord_id} a été modifié en {new_pseudo}."
                cursor.execute(history_query, (history_id, "member", discord_id, "modification du pseudo", action_details))
                conn.commit()

                await ctx.send(f"Pseudo du membre {discord_id} mis à jour avec succès.")
            else:
                await ctx.send(f"Aucun membre trouvé avec l'ID Discord {discord_id}.")
        except Exception as e:
            await ctx.send(f"Erreur lors de la mise à jour du pseudo : {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        await ctx.send("Impossible de se connecter à la base de données.")