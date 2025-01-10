@bot.command()
async def league_next_round(ctx, match_id: int, club_id: int, score: str):
    """
    Démarrer le round suivant pour un match de ligue.
    Met à jour la position du club et des adversaires dans le match.
    """
    # Vérifier si le score est dans un format valide "X-Y"
    try:
        team1_score, team2_score = map(int, score.split('-'))
    except ValueError:
        await ctx.send("Le format du score est invalide. Utilisez le format 'X-Y'.")
        return

    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            # Vérifier si le match existe et récupérer les données du match
            cursor.execute("SELECT * FROM league_match WHERE match_id = %s", (match_id,))
            match = cursor.fetchone()

            if match:
                # Récupérer les positions actuelles du club principal et des adversaires
                current_position_club = match[2]  # club_position
                current_position_1 = match[10]  # position_1
                current_position_2 = match[11]  # position_2
                current_position_3 = match[12]  # position_3
                current_position_4 = match[13]  # position_4
                current_round = match[14]  # Round actuel du match (s'il existe)

                # Incrémenter le round actuel pour démarrer le round suivant
                new_round = current_round + 1 if current_round else 1

                # Déterminer les nouvelles positions
                if new_round == 1:  # Le round 1 est déjà passé
                    new_position_club = 1
                    new_position_1 = 2
                    new_position_2 = 3
                    new_position_3 = 4
                    new_position_4 = 5
                else:
                    new_position_club = current_position_club + 1
                    new_position_1 = current_position_1 + 1
                    new_position_2 = current_position_2 + 1
                    new_position_3 = current_position_3 + 1
                    new_position_4 = current_position_4 + 1

                # Mettre à jour les positions et démarrer le round suivant dans la table league_match
                query = """
                UPDATE league_match
                SET club_position = %s, position_1 = %s, position_2 = %s, position_3 = %s, position_4 = %s, 
                    round = %s, score = %s
                WHERE match_id = %s
                """
                cursor.execute(query, (new_position_club, new_position_1, new_position_2, new_position_3, new_position_4, new_round, score, match_id))
                conn.commit()

                # Enregistrement de l'action dans l'historique
                history_query = """
                INSERT INTO history (entity_type, entity_id, action_type, action_details, action_date)
                VALUES (%s, %s, %s, %s, %s)
                """
                action_details = f"Round {new_round} du match ID {match_id} démarré pour le club {club_id}. Score mis à jour : {score}."
                cursor.execute(history_query, ("league_match", match_id, "round_start", action_details, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                conn.commit()

                await ctx.send(f"Round {new_round} du match ID {match_id} démarré pour le club {club_id}. Score mis à jour : {score}.")
            else:
                await ctx.send(f"Match avec l'ID {match_id} introuvable.")
        except Exception as e:
            await ctx.send(f"Erreur lors du démarrage du round suivant : {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        await ctx.send("Impossible de se connecter à la base de données.")