@bot.command()
async def delete_role(ctx, role_name: str):
    """Supprime un rôle de la base de données"""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            query = "DELETE FROM roles WHERE role_name = %s"
            cursor.execute(query, (role_name,))
            conn.commit()
            await ctx.send(f"Rôle '{role_name}' supprimé avec succès.")
        except Exception as e:
            await ctx.send(f"Erreur lors de la suppression du rôle : {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        await ctx.send("Impossible de se connecter à la base de données.")