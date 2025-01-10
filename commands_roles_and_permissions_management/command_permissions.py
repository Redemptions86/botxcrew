@commands.command()
async def command_permissions(self, ctx, command_name: str):
    """Affiche les permissions des rôles pour une commande spécifique"""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT r.role_name, cp.permission_level
                FROM command_permissions cp
                JOIN roles r ON cp.role_id = r.role_id
                JOIN commands c ON cp.command_id = c.command_id
                WHERE c.command_name = %s
            """, (command_name,))
            permissions = cursor.fetchall()

            if permissions:
                message = f"Permissions pour la commande {command_name} :\n"
                for permission in permissions:
                    message += f"Rôle: {permission[0]}, Permission: {permission[1]}\n"
                await ctx.send(message)
            else:
                await ctx.send(f"Aucune permission trouvée pour la commande {command_name}.")
        except Exception as e:
            await ctx.send(f"Erreur lors de la récupération des permissions : {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        await ctx.send("Impossible de se connecter à la base de données.")