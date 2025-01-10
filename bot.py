import os
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv
from database.mysql_connection import connect_to_db

# S'assurer que le répertoire de travail est correct
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Configuration du journal
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Charger les variables d'environnement
load_dotenv()

# Variables de configuration
TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("PREFIX", "!")

# Création des intents
INTENTS = discord.Intents.default()
INTENTS.messages = True
INTENTS.guilds = True
INTENTS.members = True
INTENTS.message_content = True

# Création du bot
bot = commands.Bot(command_prefix=PREFIX, intents=INTENTS)

# Dossiers à explorer pour charger les fichiers Python
directories_to_search = ["cogs", "database", "config", "utils"]

# Charger les fichiers et autres cogs
async def load_files():
    """Charge les fichiers Python depuis les dossiers spécifiés, y compris les sous-dossiers."""
    loaded_files = []
    failed_files = []

    for directory in directories_to_search:
        folder_path = os.path.join(".", directory)
        
        # Vérifier si le dossier existe
        if os.path.isdir(folder_path):
            # Parcourir tous les fichiers et sous-dossiers dans le dossier
            for root, _, files in os.walk(folder_path):
                for filename in files:
                    # Vérifier que c'est un fichier Python (.py) et pas un dossier
                    if filename.endswith(".py") and filename != "__init__.py":
                        try:
                            # Calculer le chemin relatif pour le fichier à charger
                            relative_path = os.path.relpath(root, start=".")
                            cog_path = f"{relative_path.replace(os.sep, '.')}.{filename[:-3]}"  # Remplacer os.sep par .
                            
                            # Charger l'extension en fonction du chemin
                            await bot.load_extension(cog_path)  # Utilisation de load_extension ici
                            logging.info(f"✅ Fichier chargé : {cog_path}")
                            loaded_files.append(cog_path)
                        except Exception as e:
                            logging.error(f"❌ Erreur lors du chargement du fichier {filename}: {e}")
                            failed_files.append(filename)

    # Afficher un message en cas de succès ou d'échec
    if failed_files:
        logging.warning(f"⚠️ Fichiers échoués : {', '.join(failed_files)}")
    else:
        logging.info("✅ Tous les fichiers sont opérationnels.")

    return loaded_files, failed_files

# Charger les administrateurs depuis la base de données
def load_admins_from_db():
    """Charge les administrateurs depuis la base de données."""
    admins = []
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT discord_id FROM administrator")
        admins = [str(row[0]) for row in cursor.fetchall()]
    except Exception as err:
        logging.error(f"Erreur lors de la récupération des administrateurs : {err}")
    finally:
        cursor.close()
        conn.close()
    return admins

# Événement de démarrage
@bot.event
async def on_ready():
    logging.info(f"{bot.user} est prêt et en ligne !")

    # Charger les fichiers et vérifier leur état
    loaded_files, failed_files = await load_files()

    # Afficher un résumé des fichiers chargés
    if failed_files:
        logging.warning(f"⚠️ Certains fichiers n'ont pas été chargés : {', '.join(failed_files)}")
    else:
        logging.info("✅ Tous les fichiers sont opérationnels.")

# Vérification des permissions
@bot.check
async def check_command_permissions(ctx):
    admins = load_admins_from_db()
    if str(ctx.author.id) in admins:
        return True
    return await check_permissions_in_db(ctx.command.name, ctx.author)

# Vérification des permissions en base de données
async def check_permissions_in_db(command_name, user):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute(""" 
            SELECT role_id FROM command_permissions 
            WHERE command_id = (SELECT command_id FROM commands WHERE command_name = %s)
        """, (command_name,))
        required_roles = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()

        user_roles = [role.id for role in user.roles]
        return any(role_id in user_roles for role_id in required_roles)
    except Exception as e:
        logging.error(f"Erreur lors de la vérification des permissions pour la commande {command_name}: {e}")
        return False

# Commande pour lister les commandes
@bot.command(name="listcommands")
async def list_commands(ctx):
    """Liste toutes les commandes disponibles."""
    description = "**Commandes disponibles :**\n\n"
    for command in bot.commands:
        description += f"**Nom :** `{command.name}`\n"
        if command.help:
            description += f"**Description :** {command.help}\n"
        description += f"**Utilisation :** `{PREFIX}{command.name}`\n\n"

    for i in range(0, len(description), 2000):
        await ctx.send(description[i:i + 2000])

# Gestionnaire d'erreurs
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Commande inconnue. Utilisez `!help` pour voir la liste des commandes.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Vous n'avez pas les permissions nécessaires pour exécuter cette commande.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Argument manquant : {error.param.name}.")
    else:
        logging.error(f"Erreur : {error}")
        await ctx.send("Une erreur est survenue.")

# Lancer le bot
if __name__ == "__main__":
    try:
        bot.run(TOKEN)
    except Exception as e:
        logging.error(f"Erreur lors du lancement du bot : {e}")