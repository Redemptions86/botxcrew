@bot.command()
async def end_round(ctx, match_id: int, round_number: int):
    """
    Terminer un round pour un match de ligue.
    """
    # Vérification que le round_number est un entier positif
    if round_number <= 0:
        await ctx.send("Le numéro de round doit être un entier positif.")
        return

    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()

            # Vérifier si le match existe
            cursor.execute("SELECT * FROM league_match WHERE match_id = %s", (match_id,))
            match = cursor.fetchone()

            if match:
                # Vérifier si la colonne pour le round spécifié existe
                cursor.execute(f"SHOW COLUMNS FROM league_match LIKE 'round{round_number}_end_date'")
                column_exists = cursor.fetchone()

                if not column_exists:
                    await ctx.send(f"Le round {round_number} n'existe pas pour ce match.")
                    return

                # Mettre à jour la date de fin pour le round
                end_column = f"round{round_number}_end_date"
                end_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                query = f"UPDATE league_match SET {end_column} = %s WHERE match_id = %s"
                cursor.execute(query, (end_date, match_id))
                conn.commit()

                # Enregistrement de l'action dans l'historique
                history_query = """
                INSERT INTO history (entity_type, entity_id, action_type, action_details, action_date)
                VALUES (%s, %s, %s, %s, %s)
                """
                action_details = f"Round {round_number} du match ID {match_id} terminé."
                cursor.execute(history_query, ("league_match", match_id, "round_end", action_details, end_date))
                conn.commit()

                await ctx.send(f"Round {round_number} du match ID {match_id} terminé avec succès.")
            else:
                await ctx.send(f"Match avec l'ID {match_id} introuvable.")
        except Exception as e:
            await ctx.send(f"Erreur lors de la fin du round : {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        await ctx.send("Impossible de se connecter à la base de données.")