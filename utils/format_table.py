def format_table(headers, rows):
    """
    Formate les données en tableau lisible pour Discord.
    Args:
        headers (list): Liste des en-têtes de colonnes.
        rows (list of tuples): Données à afficher.

    Returns:
        str: Tableau formaté en texte.
    """
    # Formater les en-têtes
    table = " | ".join(headers) + "\n" + "-" * (len(" | ".join(headers)) + 5)

    # Ajouter les lignes
    for row in rows:
        table += "\n" + " | ".join(str(col) for col in row)

    return f"```\n{table}\n```"