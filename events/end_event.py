from datetime import datetime

@bot.command()
async def end_event(ctx, event_id: int):
    """Terminer un événement et enregistrer la date de fin"""
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

            # Mettre à jour la date de fin de l'événement
            end_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            update_query = "UPDATE events SET end_date = %s WHERE event_id = %s"
            cursor.execute(update_query, (end_date, event_id))

            # Vérifier si la mise à jour a affecté une ligne
            if cursor.rowcount == 0:
                await ctx.send(f"Aucun changement effectué sur l'événement avec l'ID {event_id}.")
                return

            conn.commit()

            # Enregistrement de l'action dans l'historique
            history_query = """
            INSERT INTO history (entity_type, entity_id, action_type, action_details, action_date)
            VALUES (%s, %s, %s, %s, %s)
            """
            action_details = f"Événement {event_id} terminé. Date de fin : {end_date}."
            cursor.execute(history_query, ("event", event_id, "fin", action_details, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            conn.commit()

            await ctx.send(f"L'événement {event_id} a été terminé avec succès. Date de fin : {end_date}.")
        except Exception as e:
            await ctx.send(f"Erreur lors de la fin de l'événement : {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        await ctx.send("Impossible de se connecter à la base de données.")