@bot.command()
async def end_tournament_match(ctx, tournament_id: int):
    """Terminer un match de tournoi et enregistrer la date de fin"""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            # Mettre à jour la date de fin dans la table tournaments
            end_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            update_query = "UPDATE tournaments SET end_date = %s, status = 'finished' WHERE tournament_id = %s"
            cursor.execute(update_query, (end_date, tournament_id))
            conn.commit()

            # Enregistrement de l'action dans l'historique
            history_query = """
            INSERT INTO history (entity_type, entity_id, action_type, action_details)
            VALUES (%s, %s, %s, %s)
            """
            action_details = f"Match de tournoi {tournament_id} terminé. Date de fin : {end_date}."
            cursor.execute(history_query, ("tournament_match", tournament_id, "fin", action_details))
            conn.commit()

            # Récupérer l'ID de l'historique
            history_id = cursor.lastrowid

            # Mettre à jour la table tournaments avec l'ID de l'historique
            update_history_query = """
            UPDATE tournaments
            SET history_id = %s
            WHERE tournament_id = %s
            """
            cursor.execute(update_history_query, (history_id, tournament_id))
            conn.commit()

            await ctx.send(f"Le match du tournoi {tournament_id} a été terminé avec succès.")
        except Exception as e:
            await ctx.send(f"Erreur lors de la fin du match du tournoi : {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        await ctx.send("Impossible de se connecter à la base de données.")