@bot.command()
async def add_command(ctx, command_name: str, description: str):
    """Ajouter une nouvelle commande"""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO commands (command_name, description) VALUES (%s, %s)"
            cursor.execute(query, (command_name, description))
            conn.commit()
            await ctx.send(f"Commande {command_name} ajoutée avec succès.")
        except Exception as e:
            await ctx.send(f"Erreur lors de l'ajout de la commande : {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        await ctx.send("Impossible de se connecter à la base de données.")