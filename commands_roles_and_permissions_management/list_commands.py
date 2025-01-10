@commands.command()
async def list_commands(self, ctx):
    """Affiche la liste des commandes avec leurs informations"""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT command_id, command_name, description FROM commands")
            commands = cursor.fetchall()

            if commands:
                message = "Liste des commandes :\n"
                for command in commands:
                    message += f"ID: {command[0]}, Commande: {command[1]}, Description: {command[2]}\n"
                await ctx.send(message)
            else:
                await ctx.send("Aucune commande trouvée.")
        except Exception as e:
            await ctx.send(f"Erreur lors de la récupération des commandes : {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        await ctx.send("Impossible de se connecter à la base de données.")