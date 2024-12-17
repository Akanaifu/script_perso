import csv
from collections import defaultdict
from tabulate import tabulate


class FichierCSV:
    def __init__(self, chemin_fichier: str):
        self.chemin_fichier = chemin_fichier
        self.fichier = open(chemin_fichier, "r")

    def contenu_sans_header(self):
        return self.fichier.readlines()[1:]

    def afficher_solde_magasin(self):
        """
        Affiche le solde (qte*prix) du magasin.
        """
        solde = 0
        try:
            with open(
                self.chemin_fichier, mode="r", newline="", encoding="utf-8"
            ) as fichier:
                lecteur_csv = csv.reader(fichier)
                next(lecteur_csv)  # Ignorer l'en-tête
                for ligne in lecteur_csv:
                    solde += float(float(ligne[1]) * float(ligne[2]))
            print(f"Le solde du magasin est de : {solde:.2f} euros")
        except FileNotFoundError:
            print(f"Erreur : Le fichier '{self.chemin_fichier}' n'a pas été trouvé.")
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")

    def trier_fichier(self, colonne, croissant=False):
        """
        Trie le fichier par une colonne par ordre croissant ou décroissant.
        """
        try:
            with open(
                self.chemin_fichier, mode="r", newline="", encoding="utf-8"
            ) as fichier:
                reader = csv.DictReader(fichier)
                sorted_data = sorted(
                    reader, key=lambda row: row[colonne], reverse=croissant
                )
                with open(
                    self.chemin_fichier, mode="w", newline="", encoding="utf-8"
                ) as f_output:
                    writer = csv.DictWriter(f_output, fieldnames=reader.fieldnames)
                    writer.writeheader()
                    writer.writerows(sorted_data)
            print(f"Le fichier a été trié par {colonne}.")
        except FileNotFoundError:
            print(f"Erreur : Le fichier '{self.chemin_fichier}' n'a pas été trouvé.")

    def afficher_range_produit(self, min_produit=0, max_produit=999, categ=None):
        """
        Affiche les produits d'une catégorie dans un intervalle de prix.
        """
        try:
            with open(
                self.chemin_fichier, mode="r", newline="", encoding="utf-8"
            ) as fichier:
                lecteur_csv = csv.reader(fichier)
                next(lecteur_csv)  # Ignorer l'en-tête
                for ligne in lecteur_csv:
                    if min_produit <= float(ligne[2]) <= max_produit and (
                        categ is None or ligne[3] == categ
                    ):
                        print(ligne)
        except FileNotFoundError:
            print(f"Erreur : Le fichier '{self.chemin_fichier}' n'a pas été trouvé.")
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")

    def generer_recap_fichier(self):
        """
        Génère un récapitulatif du stock par catégorie en sommant les quantités et calculant la valeur totale.
        Affiche les résultats sous forme de tableau.
        Retourne un dictionnaire contenant ces informations.
        """
        recap = defaultdict(lambda: {"quantite": 0, "valeur_totale": 0.0})

        try:
            with open(
                self.chemin_fichier, mode="r", newline="", encoding="utf-8"
            ) as fichier:
                reader = csv.DictReader(fichier)
                for ligne in reader:
                    categorie = ligne["Catégorie"]
                    quantite = int(ligne["Quantité"])
                    prix_unitaire = float(ligne["Prix unitaire"])

                    # Mise à jour des informations pour la catégorie
                    recap[categorie]["quantite"] += quantite
                    recap[categorie]["valeur_totale"] += quantite * prix_unitaire

            # Transformer les données pour affichage avec tabulate
            tableau = [
                [categorie, donnees["quantite"], f"{donnees['valeur_totale']:.2f} €"]
                for categorie, donnees in recap.items()
            ]

            # Afficher le tableau avec tabulate
            print(
                tabulate(
                    tableau,
                    headers=["Catégorie", "Quantité totale", "Valeur totale"],
                    tablefmt="grid",
                )
            )

            return recap

        except FileNotFoundError:
            print(f"Erreur : Le fichier '{self.chemin_fichier}' est introuvable.")
        except KeyError as e:
            print(f"Erreur : Colonne manquante dans le fichier CSV - {e}")
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")

    def afficher_categorie(self):
        try:
            with open(
                self.chemin_fichier, mode="r", newline="", encoding="utf-8"
            ) as entree:
                reader = csv.DictReader(entree)
                categorie = [row["categorie"] for row in reader]
                return categorie
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")
            return []


if __name__ == "__main__":
    carrefour = FichierCSV("stockDB/carrefour.csv")
    carrefour.afficher_solde_magasin()
    carrefour.afficher_prod_categ("alimentaire")
