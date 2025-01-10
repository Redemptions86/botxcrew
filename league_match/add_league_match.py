@bot.command()
async def add_league_match(ctx, league_id: int, team1_id: int, team2_id: int, score: str):
    """Ajouter un match de ligue et enregistrer l'action dans l'historique"""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()

            # Vérifier si les équipes existent
            cursor.execute("SELECT * FROM teams WHERE team_id = %s", (team1_id,))
            team1_data = cursor.fetchone()
            cursor.execute("SELECT * FROM teams WHERE team_id = %s", (team2_id,))
            team2_data = cursor.fetchone()

            if not team1_data:
                await ctx.send(f"L'équipe {team1_id} n'existe pas dans la base de données.")
                return
            if not team2_data:
                await ctx.send(f"L'équipe {team2_id} n'existe pas dans la base de données.")
                return

            # Vérifier si la ligue existe
            cursor.execute("SELECT * FROM leagues WHERE league_id = %s", (league_id,))
            league_data = cursor.fetchone()

            if not league_data:
                await ctx.send(f"La ligue avec l'ID {league_id} n'existe pas.")
                return

            # Ajouter le match de ligue dans la table league_match
            query = "INSERT INTO league_match (league_id, team1_id, team2_id, score, start_date) VALUES (%s, %s, %s, %s, %s)"
            start_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(query, (league_id, team1_id, team2_id, score, start_date))
            conn.commit()

            # Enregistrement de l'action dans l'historique
            history_query = """
            INSERT INTO history (entity_type, entity_id, action_type, action_details, action_date)
            VALUES (%s, %s, %s, %s, %s)
            """
            action_details = f"Match de ligue entre {team1_id} et {team2_id} avec le score {score} (Ligue: {league_id})"
            cursor.execute(history_query, ("league_match", league_id, "ajout", action_details, start_date))
            conn.commit()

            await ctx.send(f"Match de ligue ajouté avec succès.")
        except Exception as e:
            await ctx.send(f"Erreur lors de l'ajout du match de ligue : {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        await ctx.send("Impossible de se connecter à la base de données.")