import os
import csv


def fusion_fichier_csv(dossier_csv, fichier_sortie="fusion.csv"):
    """
    Fusionne toutes les données des fichiers CSV d'un dossier dans un seul fichier de sortie.

    Args:
        dossier_csv (str): Le chemin du dossier contenant les fichiers CSV.
        fichier_sortie (str): Le nom du fichier CSV fusionné (par défaut: "fusion.csv").

    Returns:
        str: Le chemin du fichier fusionné.
    """
    try:
        fichiers_csv = [f for f in os.listdir(dossier_csv) if f.endswith(".csv")]
        if not fichiers_csv:
            print("Aucun fichier CSV trouvé dans le dossier.")
            return

        chemin_sortie = os.path.join(dossier_csv, fichier_sortie)
        entetes_ecrits = False

        with open(chemin_sortie, mode="w", newline="", encoding="utf-8") as sortie:
            writer = csv.writer(sortie)

            for fichier in fichiers_csv:
                chemin_fichier = os.path.join(dossier_csv, fichier)

                with open(
                    chemin_fichier, mode="r", newline="", encoding="utf-8"
                ) as entree:
                    reader = csv.reader(entree)
                    entetes = next(reader)  # Lire les entêtes du fichier courant

                    # Écrire les entêtes seulement une fois
                    if not entetes_ecrits:
                        writer.writerow(entetes)
                        entetes_ecrits = True

                    # Écrire les lignes de données
                    for ligne in reader:
                        writer.writerow(ligne)

        print(f"Fusion terminée : {chemin_sortie}")
        return chemin_sortie

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        return


def recuperer_categorie_fichier(fichier):
    """
    Récupère toute la colonne catégorie d'un fichier CSV à partir de son nom.
    """
    try:
        with open(fichier, mode="r", newline="", encoding="utf-8") as entree:
            reader = csv.DictReader(entree)
            categorie = [row["categorie"] for row in reader]
            return categorie
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        return []
