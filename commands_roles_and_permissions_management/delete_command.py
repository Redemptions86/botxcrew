@bot.command()
async def delete_command(ctx, command_name: str):
    """Supprime une commande de la base de données"""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            query = "DELETE FROM commands WHERE command_name = %s"
            cursor.execute(query, (command_name,))
            conn.commit()
            await ctx.send(f"Commande '{command_name}' supprimée avec succès.")
        except Exception as e:
            await ctx.send(f"Erreur lors de la suppression de la commande : {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        await ctx.send("Impossible de se connecter à la base de données.")