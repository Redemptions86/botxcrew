from datetime import datetime

@bot.command()
async def add_club_match(ctx, club_id: int, opponent_club_id: int, score: str, match_type: str):
    """
    Ajouter un match de club et enregistrer l'action dans l'historique.
    - Enregistre automatiquement la date de début (création).
    - Ajoute un match avec club principal et adversaire.
    - Ajoute un enregistrement dans la table historique.
    """
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()

            # Vérifie si les clubs existent
            cursor.execute("SELECT * FROM clubs WHERE club_id = %s", (club_id,))
            club = cursor.fetchone()
            cursor.execute("SELECT * FROM clubs WHERE club_id = %s", (opponent_club_id,))
            opponent_club = cursor.fetchone()

            if not club:
                await ctx.send(f"Le club avec l'ID {club_id} n'a pas été trouvé.")
                return
            if not opponent_club:
                await ctx.send(f"Le club adverse avec l'ID {opponent_club_id} n'a pas été trouvé.")
                return

            # Ajouter le match de club dans la table club_match
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            query = """
            INSERT INTO club_match (club_id, opponent_club_id, score, match_type, start_date)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (club_id, opponent_club_id, score, match_type, created_at))
            conn.commit()

            # Récupérer l'ID du match ajouté
            match_id = cursor.lastrowid

            # Enregistrement de l'action dans l'historique
            history_query = """
            INSERT INTO history (entity_type, entity_id, action_type, action_details, action_date)
            VALUES (%s, %s, %s, %s, %s)
            """
            action_details = f"Match de club ajouté entre {club[1]} ({club_id}) et {opponent_club[1]} ({opponent_club_id}) avec le score {score} (Type: {match_type})"
            cursor.execute(history_query, ("club_match", match_id, "ajout", action_details, created_at))
            conn.commit()

            await ctx.send(f"Match de club ajouté avec succès. ID du match : {match_id}.")
        except Exception as e:
            await ctx.send(f"Erreur lors de l'ajout du match de club : {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        await ctx.send("Impossible de se connecter à la base de données.")