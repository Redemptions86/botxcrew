@bot.command()
async def show_club_events(ctx, club_id: int):
    """Afficher tous les événements associés à un club"""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            # Récupérer tous les événements du club
            query = "SELECT * FROM events WHERE club_id = %s"
            cursor.execute(query, (club_id,))
            results = cursor.fetchall()

            if results:
                response = f"Événements du club {club_id} :\n"
                for event in results:
                    event_id, _, discord_id, total_points, start_date, end_date = event
                    response += f"Événement {event_id} - Discord ID: {discord_id}, {total_points} points\n"
                    response += f"Du {start_date} au {end_date}\n"
                await ctx.send(response)
            else:
                await ctx.send(f"Aucun événement trouvé pour le club {club_id}.")
        except Exception as e:
            await ctx.send(f"Erreur lors de l'affichage des événements du club : {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        await ctx.send("Impossible de se connecter à la base de données.")