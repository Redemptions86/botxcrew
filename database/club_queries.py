import discord
from discord.ext import commands
from database.mysql_connection import execute_query  # Assurez-vous d'importer la fonction execute_query

class ClubManagementCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="get_club_by_name")
    async def get_club_by_name(self, ctx, club_name):
        """Récupère un club par son nom."""
        try:
            query = "SELECT * FROM clubs WHERE club_name = %s"
            result = execute_query(query, (club_name,))
            if result:
                await ctx.send(f"Club trouvé : {result[0]}")
            else:
                await ctx.send(f"Aucun club trouvé avec le nom '{club_name}'.")
        except Exception as e:
            await ctx.send(f"Erreur lors de la récupération du club : {e}")
    
    @commands.command(name="get_club_by_id")
    async def get_club_by_id(self, ctx, club_id):
        """Récupère un club par son ID."""
        try:
            query = "SELECT * FROM clubs WHERE club_id = %s"
            result = execute_query(query, (club_id,))
            if result:
                await ctx.send(f"Club trouvé : {result[0]}")
            else:
                await ctx.send(f"Aucun club trouvé avec l'ID '{club_id}'.")
        except Exception as e:
            await ctx.send(f"Erreur lors de la récupération du club : {e}")
    
    @commands.command(name="add_club")
    async def add_club(self, ctx, club_name, club_owner):
        """Ajoute un club dans la base de données."""
        try:
            query = "INSERT INTO clubs (club_name, club_owner) VALUES (%s, %s)"
            execute_query(query, (club_name, club_owner))  # Utilisation de execute_query pour l'insertion
            await ctx.send(f"Le club '{club_name}' a été ajouté avec succès.")
        except Exception as e:
            await ctx.send(f"Erreur lors de l'ajout du club : {e}")
    
    @commands.command(name="update_club")
    async def update_club(self, ctx, club_id, new_club_name, new_club_owner):
        """Met à jour un club dans la base de données."""
        try:
            query = "UPDATE clubs SET club_name = %s, club_owner = %s WHERE club_id = %s"
            execute_query(query, (new_club_name, new_club_owner, club_id))
            await ctx.send(f"Le club avec ID '{club_id}' a été mis à jour.")
        except Exception as e:
            await ctx.send(f"Erreur lors de la mise à jour du club : {e}")
    
    @commands.command(name="delete_club")
    async def delete_club(self, ctx, club_id):
        """Supprime un club de la base de données."""
        try:
            query = "DELETE FROM clubs WHERE club_id = %s"
            execute_query(query, (club_id,))
            await ctx.send(f"Le club avec ID '{club_id}' a été supprimé.")
        except Exception as e:
            await ctx.send(f"Erreur lors de la suppression du club : {e}")

    @commands.command(name="list_clubs")
    async def list_clubs(self, ctx):
        """Récupère la liste de tous les clubs."""
        try:
            query = "SELECT club_id, club_name, points FROM clubs"
            result = execute_query(query)
            if result:
                clubs_list = "\n".join([f"ID: {club['club_id']} | Nom: {club['club_name']} | Points: {club['points']}" for club in result])
                await ctx.send(f"Liste des clubs :\n{clubs_list}")
            else:
                await ctx.send("Aucun club trouvé.")
        except Exception as e:
            await ctx.send(f"Erreur lors de la récupération des clubs : {e}")
    
    @commands.command(name="add_club_with_validation")
    async def add_club_with_validation(self, ctx, club_name, club_owner):
        """Ajouter un club avec vérification de doublon et validation des données."""
        try:
            existing_club = get_club_by_name(club_name)
            if existing_club:
                await ctx.send(f"Un club avec le nom '{club_name}' existe déjà.")
                return
            
            if not club_name.strip() or not club_owner.strip():
                await ctx.send("Le nom du club et le nom du propriétaire ne peuvent pas être vides.")
                return
            
            add_club(club_name, club_owner)
            await ctx.send(f"Le club '{club_name}' a été ajouté avec succès.")
        except Exception as e:
            await ctx.send(f"Erreur lors de l'ajout du club avec validation : {e}")

def setup(bot):
    bot.add_cog(ClubManagementCog(bot))  # Ajoute le cog au bot