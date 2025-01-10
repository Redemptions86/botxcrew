@bot.command()
async def update_rankings(ctx):
    """
    Mettre à jour les données de la table 'rankings' en fonction des performances des clubs.
    """
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()

            # Recalculer les points et statistiques pour chaque club
            query_update = """
            INSERT INTO rankings (club_id, total_points, total_wins, total_losses, total_draws, average_force)
            SELECT 
                c.club_id,
                COALESCE(SUM(CASE WHEN cm.result = 'win' THEN 3 WHEN cm.result = 'draw' THEN 1 ELSE 0 END), 0) AS total_points,
                COALESCE(SUM(CASE WHEN cm.result = 'win' THEN 1 ELSE 0 END), 0) AS total_wins,
                COALESCE(SUM(CASE WHEN cm.result = 'loss' THEN 1 ELSE 0 END), 0) AS total_losses,
                COALESCE(SUM(CASE WHEN cm.result = 'draw' THEN 1 ELSE 0 END), 0) AS total_draws,
                COALESCE(AVG(f.force_value), 0) AS average_force
            FROM clubs c
            LEFT JOIN club_match cm ON c.club_id = cm.club_id
            LEFT JOIN forces f ON c.club_id = f.club_id
            GROUP BY c.club_id
            ON DUPLICATE KEY UPDATE
                total_points = VALUES(total_points),
                total_wins = VALUES(total_wins),
                total_losses = VALUES(total_losses),
                total_draws = VALUES(total_draws),
                average_force = VALUES(average_force);
            """
            cursor.execute(query_update)
            conn.commit()

            # Enregistrement de l'action dans l'historique
            history_query = """
            INSERT INTO history (entity_type, action_type, action_details)
            VALUES (%s, %s, %s)
            """
            action_details = "Mise à jour des classements des clubs en fonction des performances récentes."
            cursor.execute(history_query, ("ranking_update", "mise à jour", action_details))
            conn.commit()

            # Récupérer l'ID de l'historique
            history_id = cursor.lastrowid

            # Mettre à jour la table rankings avec l'ID de l'historique
            update_history_query = """
            UPDATE rankings
            SET history_id = %s
            WHERE club_id IN (SELECT club_id FROM rankings)
            """
            cursor.execute(update_history_query, (history_id,))
            conn.commit()

            await ctx.send("Table 'rankings' mise à jour avec succès.")
        except Exception as e:
            await ctx.send(f"Erreur lors de la mise à jour du classement : {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        await ctx.send("Impossible de se connecter à la base de données.")