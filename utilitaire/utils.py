import os
import csv
from collections import defaultdict


def fusion_fichier_csv(dossier_csv, fichier_sortie="fusion.csv"):
    """
    Fusionne toutes les donnees des fichiers CSV d'un dossier dans un seul fichier de sortie.
    Si un produit est present dans plusieurs fichiers, les quantites sont additionnees.

    Args:
        dossier_csv (str): Le chemin du dossier contenant les fichiers CSV.
        fichier_sortie (str): Le nom du fichier CSV fusionne (par defaut: "fusion.csv").

    Returns:
        str: Le chemin du fichier fusionne.
    """
    try:
        fichiers_csv = [f for f in os.listdir(dossier_csv) if f.endswith(".csv")]
        if not fichiers_csv:
            print("Aucun fichier CSV trouve dans le dossier.")
            return

        chemin_sortie = os.path.join(dossier_csv, fichier_sortie)
        donnees_fusionnees = defaultdict(
            lambda: {"Quantite": 0, "Prix unitaire": 0.0, "Categorie": ""}
        )

        # Parcourir chaque fichier CSV dans le dossier
        for fichier in fichiers_csv:
            chemin_fichier = os.path.join(dossier_csv, fichier)

            with open(chemin_fichier, mode="r", newline="", encoding="utf-8") as entree:
                reader = csv.DictReader(entree)
                for ligne in reader:
                    nom_produit = ligne["Nom du produit"]
                    quantite = int(ligne["Quantite"])
                    prix_unitaire = float(ligne["Prix unitaire"])
                    categorie = ligne["Categorie"]

                    # Mettre à jour les donnees fusionnees
                    if nom_produit in donnees_fusionnees:
                        donnees_fusionnees[nom_produit]["Quantite"] += quantite
                    else:
                        donnees_fusionnees[nom_produit] = {
                            "Quantite": quantite,
                            "Prix unitaire": prix_unitaire,
                            "Categorie": categorie,
                        }

        # ecriture des donnees fusionnees dans le fichier de sortie
        with open(chemin_sortie, mode="w", newline="", encoding="utf-8") as sortie:
            fieldnames = ["Nom du produit", "Quantite", "Prix unitaire", "Categorie"]
            writer = csv.DictWriter(sortie, fieldnames=fieldnames)

            writer.writeheader()
            for produit, donnees in donnees_fusionnees.items():
                writer.writerow(
                    {
                        "Nom du produit": produit,
                        "Quantite": donnees["Quantite"],
                        "Prix unitaire": donnees["Prix unitaire"],
                        "Categorie": donnees["Categorie"],
                    }
                )

        print(f"Fusion terminee avec sommation des quantites : {chemin_sortie}")
        return chemin_sortie

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        return
