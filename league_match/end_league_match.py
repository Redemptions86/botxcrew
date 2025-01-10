@bot.command()
async def end_league_match(ctx, match_id: int):
    """
    Terminer un match de ligue et enregistrer la date de fin.
    """
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()

            # Vérifier si le match existe
            cursor.execute("SELECT * FROM league_match WHERE match_id = %s", (match_id,))
            match_data = cursor.fetchone()

            if not match_data:
                await ctx.send(f"Aucun match trouvé avec l'ID {match_id}.")
                return

            # Vérifier si le match a déjà une date de fin
            if match_data[4] is not None:  # Supposons que la date de fin est à l'index 4
                await ctx.send(f"Le match ID {match_id} est déjà terminé.")
                return

            # Mettre à jour la date de fin dans la table league_match
            end_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            query = "UPDATE league_match SET end_date = %s WHERE match_id = %s"
            cursor.execute(query, (end_date, match_id))
            conn.commit()

            # Enregistrement de l'action dans l'historique
            history_query = """
            INSERT INTO history (entity_type, entity_id, action_type, action_details, action_date)
            VALUES (%s, %s, %s, %s, %s)
            """
            action_details = f"Match de ligue terminé avec l'ID {match_id}. Date de fin : {end_date}."
            cursor.execute(history_query, ("league_match", match_id, "fin", action_details, end_date))
            conn.commit()

            await ctx.send(f"Match ID {match_id} terminé avec succès.")
        except Exception as e:
            await ctx.send(f"Erreur lors de la fin du match de ligue : {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        await ctx.send("Impossible de se connecter à la base de données.")