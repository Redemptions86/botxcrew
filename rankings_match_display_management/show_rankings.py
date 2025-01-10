@bot.command()
async def show_rankings(ctx, *club_ids: int):
    """
    Afficher le classement des clubs ou les détails d'un ou plusieurs clubs spécifiques sous forme de tableau lisible.
    """
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            
            # Si des club_ids sont spécifiés, limiter les résultats à ces clubs
            if club_ids:
                club_ids_placeholder = ", ".join(["%s"] * len(club_ids))
                query = f"""
                SELECT club_id, total_points, total_wins, total_losses, total_draws, average_force
                FROM rankings
                WHERE club_id IN ({club_ids_placeholder})
                ORDER BY total_points DESC
                """
                cursor.execute(query, club_ids)
            else:
                # Sinon, afficher le classement global
                query = """
                SELECT club_id, total_points, total_wins, total_losses, total_draws, average_force
                FROM rankings
                ORDER BY total_points DESC
                """
                cursor.execute(query)

            rankings = cursor.fetchall()

            if not rankings:
                await ctx.send("Aucun classement disponible pour les clubs spécifiés.")
                return

            # Construire un tableau lisible pour Discord
            header = f"{'Rang':<5} {'Club ID':<10} {'Points':<8} {'Victoires':<10} {'Défaites':<10} {'Nuls':<5} {'Force Moy.':<12}"
            separator = "-" * len(header)
            rows = []

            for rank, club in enumerate(rankings, start=1):
                rows.append(
                    f"{rank:<5} {club[0]:<10} {club[1]:<8} {club[2]:<10} {club[3]:<10} {club[4]:<5} {club[5]:<12.2f}"
                )

            # Construire le message final
            table = "```\n" + header + "\n" + separator + "\n" + "\n".join(rows) + "\n```"
            await ctx.send(table)

            # Enregistrement de l'action dans l'historique
            history_query = """
            INSERT INTO history (entity_type, action_type, action_details)
            VALUES (%s, %s, %s)
            """
            action_details = f"Affichage du classement des clubs. Clubs concernés : {', '.join(map(str, club_ids)) if club_ids else 'Tous les clubs'}."
            cursor.execute(history_query, ("ranking_display", "affichage", action_details))
            conn.commit()

            # Récupérer l'ID de l'historique
            history_id = cursor.lastrowid

            # Mettre à jour la table rankings avec l'ID de l'historique
            update_history_query = """
            UPDATE rankings
            SET history_id = %s
            WHERE club_id IN (%s)
            """
            cursor.execute(update_history_query, (history_id, ", ".join(map(str, club_ids))))
            conn.commit()

        except Exception as e:
            await ctx.send(f"Erreur lors de la récupération du classement : {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        await ctx.send("Impossible de se connecter à la base de données.")