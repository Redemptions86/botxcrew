from datetime import datetime

@bot.command()
async def end_club_match(ctx, match_id: int):
    """
    Terminer un match de club en enregistrant la date de fin et en mettant à jour l'état du match.
    """
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            # Vérifier si le match existe
            cursor.execute("SELECT * FROM club_match WHERE match_id = %s", (match_id,))
            match = cursor.fetchone()

            if match:
                # Vérifier si le match est déjà terminé
                if match[5]:  # Supposons que la colonne 5 est 'end_date'
                    await ctx.send(f"Le match ID {match_id} est déjà terminé.")
                    return

                # Mettre à jour la date de fin dans la table club_match
                end_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                query = "UPDATE club_match SET end_date = %s WHERE match_id = %s"
                cursor.execute(query, (end_date, match_id))
                conn.commit()

                # Enregistrement de l'action dans l'historique
                history_query = """
                INSERT INTO history (entity_type, entity_id, action_type, action_details, action_date)
                VALUES (%s, %s, %s, %s, %s)
                """
                action_details = f"Match terminé avec l'ID {match_id}. Date de fin : {end_date}."
                cursor.execute(history_query, ("club_match", match_id, "fin", action_details, end_date))
                conn.commit()

                await ctx.send(f"Match ID {match_id} terminé avec succès. Date de fin : {end_date}.")
            else:
                await ctx.send(f"Match avec l'ID {match_id} introuvable.")
        except Exception as e:
            await ctx.send(f"Erreur lors de la fin du match : {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        await ctx.send("Impossible de se connecter à la base de données.")