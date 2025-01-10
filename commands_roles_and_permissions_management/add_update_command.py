@bot.command()
async def add_update_command(ctx, command_name: str, description: str, permission_level: str):
    """Ajoute ou met à jour une commande dans la base de données"""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO commands (command_name, description, permission_level)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE description = %s, permission_level = %s
            """
            cursor.execute(query, (command_name, description, permission_level, description, permission_level))
            conn.commit()
            await ctx.send(f"Commande '{command_name}' ajoutée ou mise à jour avec succès.")
        except Exception as e:
            await ctx.send(f"Erreur lors de l'ajout ou de la mise à jour de la commande : {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        await ctx.send("Impossible de se connecter à la base de données.")