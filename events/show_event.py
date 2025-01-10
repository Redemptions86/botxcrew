@bot.command()
async def show_event(ctx, event_id: int):
    """Afficher les détails d'un événement"""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            # Récupérer les informations de l'événement
            query = "SELECT * FROM events WHERE event_id = %s"
            cursor.execute(query, (event_id,))
            result = cursor.fetchone()

            if result:
                club_id, discord_id, total_points, start_date, end_date = result[1], result[2], result[3], result[4], result[5]
                await ctx.send(f"Événement {event_id}: Club {club_id} (Discord ID: {discord_id}) - {total_points} points\n"
                               f"Date de début: {start_date}\nDate de fin: {end_date}")
            else:
                await ctx.send(f"Événement avec l'ID {event_id} introuvable.")
        except Exception as e:
            await ctx.send(f"Erreur lors de l'affichage de l'événement : {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        await ctx.send("Impossible de se connecter à la base de données.")