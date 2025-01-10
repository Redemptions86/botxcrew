from datetime import datetime

@bot.command()
async def update_event(ctx, event_id: int, total_points: int = None, start_date: str = None, end_date: str = None):
    """Modifier les informations d'un événement"""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()

            # Vérification de l'existence de l'événement
            cursor.execute("SELECT * FROM events WHERE event_id = %s", (event_id,))
            event = cursor.fetchone()
            if not event:
                await ctx.send(f"L'événement avec l'ID {event_id} n'existe pas.")
                return

            # Préparer les modifications
            update_query = "UPDATE events SET "
            params = []
            updated_fields = []

            if total_points is not None:
                update_query += "total_points = %s, "
                params.append(total_points)
                updated_fields.append(f"Points: {total_points}")
            if start_date is not None:
                update_query += "start_date = %s, "
                params.append(start_date)
                updated_fields.append(f"Date de début: {start_date}")
            if end_date is not None:
                update_query += "end_date = %s, "
                params.append(end_date)
                updated_fields.append(f"Date de fin: {end_date}")

            # Retirer la dernière virgule
            update_query = update_query.rstrip(", ") + " WHERE event_id = %s"
            params.append(event_id)

            # Exécuter la mise à jour
            cursor.execute(update_query, tuple(params))
            conn.commit()

            # Enregistrement de l'action dans l'historique
            history_query = """
            INSERT INTO history (entity_type, entity_id, action_type, action_details, action_date)
            VALUES (%s, %s, %s, %s, %s)
            """
            action_details = f"Événement {event_id} mis à jour avec les nouvelles valeurs : " + ", ".join(updated_fields) + "."
            cursor.execute(history_query, ("event", event_id, "modification", action_details, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            conn.commit()

            await ctx.send(f"Événement {event_id} mis à jour avec succès. Modifications : {', '.join(updated_fields)}.")
        except Exception as e:
            await ctx.send(f"Erreur lors de la mise à jour de l'événement : {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        await ctx.send("Impossible de se connecter à la base de données.")