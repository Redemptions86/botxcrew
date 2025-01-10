from datetime import datetime

@bot.command()
async def mod_match_club(ctx, match_id: int, new_score: str = None, new_match_type: str = None):
    """
    Modifier les informations d'un match en cours.
    - Modifie le score et/ou le type de match.
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
                    await ctx.send(f"Le match ID {match_id} est déjà terminé et ne peut pas être modifié.")
                    return

                # Préparer la mise à jour des informations
                updated = False
                if new_score:
                    query = "UPDATE club_match SET score = %s WHERE match_id = %s"
                    cursor.execute(query, (new_score, match_id))
                    updated = True

                if new_match_type:
                    query = "UPDATE club_match SET match_type = %s WHERE match_id = %s"
                    cursor.execute(query, (new_match_type, match_id))
                    updated = True

                if updated:
                    conn.commit()

                    # Enregistrement de l'action dans l'historique
                    history_query = """
                    INSERT INTO history (entity_type, entity_id, action_type, action_details, action_date)
                    VALUES (%s, %s, %s, %s, %s)
                    """
                    action_details = f"Match avec l'ID {match_id} modifié. Nouveau score : {new_score}, Nouveau type de match : {new_match_type}."
                    cursor.execute(history_query, ("club_match", match_id, "modification", action_details, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                    conn.commit()

                    await ctx.send(f"Match ID {match_id} modifié avec succès.")
                else:
                    await ctx.send("Aucune information n'a été modifiée.")
            else:
                await ctx.send(f"Match avec l'ID {match_id} introuvable.")
        except Exception as e:
            await ctx.send(f"Erreur lors de la modification du match : {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        await ctx.send("Impossible de se connecter à la base de données.")