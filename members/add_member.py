@bot.command()
async def add_member(ctx, member: discord.Member, club_id: int = None):
    """
    Ajouter un nouveau membre à la base de données.
    Récupère automatiquement le discord_id et le pseudo depuis le serveur Discord.
    """
    discord_id = member.id
    pseudo = member.name

    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()

            # Vérifier si le membre existe déjà
            cursor.execute("SELECT * FROM members WHERE discord_id = %s", (discord_id,))
            existing_member = cursor.fetchone()
            if existing_member:
                await ctx.send(f"Le membre {pseudo} existe déjà dans la base de données.")
                return

            # Si un club_id est fourni, vérifier si ce club existe
            if club_id:
                cursor.execute("SELECT * FROM clubs WHERE club_id = %s", (club_id,))
                club_exists = cursor.fetchone()
                if not club_exists:
                    await ctx.send(f"Le club avec l'ID {club_id} n'existe pas.")
                    return

            # Insérer le membre dans la base de données
            query = "INSERT INTO members (discord_id, pseudo, club_id) VALUES (%s, %s, %s)"
            cursor.execute(query, (discord_id, pseudo, club_id))
            conn.commit()

            # Récupérer le `history_id` du dernier ajout
            cursor.execute("SELECT LAST_INSERT_ID()")
            history_id = cursor.fetchone()[0]

            # Enregistrer l'action dans l'historique
            history_query = """
            INSERT INTO history (history_id, entity_type, entity_id, action_type, action_details)
            VALUES (%s, %s, %s, %s, %s)
            """
            action_details = f"Ajout du membre {pseudo} avec Discord ID {discord_id}."
            cursor.execute(history_query, (history_id, "member", discord_id, "ajout", action_details))
            conn.commit()

            club_message = f" et associé au club {club_id}" if club_id else ""
            await ctx.send(f"Membre {pseudo} ajouté avec succès{club_message}.")
        except Exception as e:
            await ctx.send(f"Erreur lors de l'ajout du membre : {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        await ctx.send("Impossible de se connecter à la base de données.")