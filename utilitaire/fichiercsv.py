import csv


class FichierCSV:
    def __init__(self, chemin_fichier: str):
        self.chemin_fichier = chemin_fichier
        self.fichier = open(chemin_fichier, "r")

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

    def afficher_prod_categ(self, categ):
        """
        Affiche les produits d'une catégorie.
        """
        try:
            with open(
                self.chemin_fichier, mode="r", newline="", encoding="utf-8"
            ) as fichier:
                lecteur_csv = csv.reader(fichier)
                next(lecteur_csv)  # Ignorer l'en-tête
                for ligne in lecteur_csv:
                    if ligne[3] == categ:
                        print(ligne)
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

    def afficher_range_produit(self, min=0, max=999, categ=None):
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
                    if min <= float(ligne[2]) <= max and (
                        categ is None or ligne[3] == categ
                    ):
                        print(ligne)
        except FileNotFoundError:
            print(f"Erreur : Le fichier '{self.chemin_fichier}' n'a pas été trouvé.")
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")


if __name__ == "__main__":
    carrefour = FichierCSV("stockDB/carrefour.csv")
    carrefour.afficher_solde_magasin()
    carrefour.afficher_prod_categ("alimentaire")
