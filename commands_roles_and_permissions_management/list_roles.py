@commands.command()
async def list_roles(self, ctx):
    """Affiche la liste des rôles avec leurs ID"""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT role_id, role_name FROM roles")
            roles = cursor.fetchall()

            if roles:
                message = "Liste des rôles :\n"
                for role in roles:
                    message += f"ID: {role[0]}, Rôle: {role[1]}\n"
                await ctx.send(message)
            else:
                await ctx.send("Aucun rôle trouvé.")
        except Exception as e:
            await ctx.send(f"Erreur lors de la récupération des rôles : {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        await ctx.send("Impossible de se connecter à la base de données.")