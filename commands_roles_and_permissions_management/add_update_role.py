@bot.command()
async def add_update_role(ctx, role_name: str, permission_level: str):
    """Ajoute ou met à jour un rôle dans la base de données"""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO roles (role_name, permission_level)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE permission_level = %s
            """
            cursor.execute(query, (role_name, permission_level, permission_level))
            conn.commit()
            await ctx.send(f"Rôle '{role_name}' ajouté ou mis à jour avec succès.")
        except Exception as e:
            await ctx.send(f"Erreur lors de l'ajout ou de la mise à jour du rôle : {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        await ctx.send("Impossible de se connecter à la base de données.")