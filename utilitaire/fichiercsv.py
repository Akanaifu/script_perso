import csv
from collections import defaultdict
from tabulate import tabulate


class FichierCSV:
    """
    Classe pour gerer un fichier CSV.
    """

    def __init__(self, chemin_fichier: str):
        self.chemin_fichier = chemin_fichier

    def contenu_sans_header(self):
        """
        Retourne le contenu du fichier sans l'en-tête.
        """
        try:
            with open(self.chemin_fichier, "r", encoding="utf-8") as fichier:
                return fichier.readlines()[1:]  # Retourner les lignes sans l'en-tête
        except FileNotFoundError:
            print(f"Erreur : Le fichier '{self.chemin_fichier}' n'a pas ete trouve.")
            return []

    def afficher_solde_magasin(self):
        """
        Affiche le solde (qte * prix) du magasin.
        """
        solde = 0
        try:
            with open(
                self.chemin_fichier, mode="r", newline="", encoding="utf-8"
            ) as fichier:
                lecteur_csv = csv.DictReader(fichier)
                for ligne in lecteur_csv:
                    try:
                        solde += int(ligne["Quantite"]) * float(ligne["Prix unitaire"])
                    except ValueError:
                        print(f"Erreur de conversion dans la ligne : {ligne}")
            print(f"Le solde du magasin est de : {solde:.2f} euros")
        except FileNotFoundError:
            print(f"Erreur : Le fichier '{self.chemin_fichier}' n'a pas ete trouve.")

    def trier_fichier(self, colonne, croissant=False):
        """
        Trie le fichier par une colonne par ordre croissant ou decroissant.
        """
        try:
            with open(
                self.chemin_fichier, mode="r", newline="", encoding="utf-8"
            ) as fichier:
                reader = csv.DictReader(fichier)
                sorted_data = sorted(
                    reader, key=lambda row: row[colonne], reverse=not croissant
                )

            with open(
                self.chemin_fichier, mode="w", newline="", encoding="utf-8"
            ) as fichier_sortie:
                writer = csv.DictWriter(fichier_sortie, fieldnames=reader.fieldnames)
                writer.writeheader()
                writer.writerows(sorted_data)

            print(
                f"Le fichier a ete trie par '{colonne}' en ordre {'croissant' if croissant else 'decroissant'}."
            )
        except FileNotFoundError:
            print(f"Erreur : Le fichier '{self.chemin_fichier}' n'a pas ete trouve.")
        except KeyError:
            print(f"Erreur : La colonne '{colonne}' n'existe pas dans le fichier.")

    def afficher_range_produit(self, min_produit=0, max_produit=999, categ=None):
        """
        Affiche les produits d'une categorie dans un intervalle de prix.
        """
        try:
            with open(
                self.chemin_fichier, mode="r", newline="", encoding="utf-8"
            ) as fichier:
                lecteur_csv = csv.DictReader(fichier)
                for ligne in lecteur_csv:
                    try:
                        prix = float(ligne["Prix unitaire"])
                        if min_produit <= prix <= max_produit and (
                            categ is None or ligne["Categorie"] == categ
                        ):
                            print(ligne)
                    except ValueError:
                        print(f"Erreur de conversion dans la ligne : {ligne}")
        except FileNotFoundError:
            print(f"Erreur : Le fichier '{self.chemin_fichier}' n'a pas ete trouve.")

    def generer_recap_fichier(self):
        """
        Genère un recapitulatif du stock par categorie.
        """
        recap = defaultdict(lambda: {"quantite": 0, "valeur_totale": 0.0})

        try:
            with open(
                self.chemin_fichier, mode="r", newline="", encoding="utf-8"
            ) as fichier:
                reader = csv.DictReader(fichier)
                for ligne in reader:
                    try:
                        categorie = ligne["Categorie"]
                        quantite = int(ligne["Quantite"])
                        prix_unitaire = float(ligne["Prix unitaire"])
                        recap[categorie]["quantite"] += quantite
                        recap[categorie]["valeur_totale"] += quantite * prix_unitaire
                    except ValueError:
                        print(f"Erreur dans la ligne : {ligne}")
            tableau = [
                [categorie, donnees["quantite"], f"{donnees['valeur_totale']:.2f} €"]
                for categorie, donnees in recap.items()
            ]
            print(
                tabulate(
                    tableau,
                    headers=["Categorie", "Quantite totale", "Valeur totale"],
                    tablefmt="grid",
                )
            )

        except FileNotFoundError:
            print(f"Erreur : Le fichier '{self.chemin_fichier}' est introuvable.")

    def afficher_categorie(self):
        """
        Affiche les categories presentes dans le fichier.
        Returns:
            list: La liste des categories.
        """
        try:
            with open(
                self.chemin_fichier, mode="r", newline="", encoding="utf-8"
            ) as fichier:
                reader = csv.DictReader(fichier)
                categories = set(row["Categorie"] for row in reader)
                print(f"Categories presentes : {', '.join(categories)}")
                return list(categories)
        except FileNotFoundError:
            print(f"Erreur : Le fichier '{self.chemin_fichier}' n'a pas ete trouve.")
            return []

    def recuperer_noms_colonnes(self):
        """
        Récupère les noms des colonnes d'un fichier CSV.

        Args:
            chemin_fichier (str): Le chemin du fichier CSV.

        Returns:
            list: Une liste contenant les noms des colonnes.
        """
        try:
            with open(
                self.chemin_fichier, mode="r", newline="", encoding="utf-8"
            ) as fichier:
                lecteur_csv = csv.reader(fichier)
                noms_colonnes = next(
                    lecteur_csv
                )  # Lire uniquement la première ligne (en-tête)
                return noms_colonnes
        except FileNotFoundError:
            print(f"Erreur : Le fichier '{self.chemin_fichier}' n'a pas été trouvé.")
        return []  # Retourne une liste vide en cas d'erreur


if __name__ == "__main__":
    carrefour = FichierCSV("stockDB/carrefour.csv")
    carrefour.afficher_solde_magasin()
    carrefour.afficher_categorie()
    carrefour.generer_recap_fichier()
