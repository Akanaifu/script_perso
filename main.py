from utilitaire.fichiercsv import *
from utilitaire.utils import *
import os


def main():
    while True:
        print("Menu Principal")
        print("1. Fusionner les fichiers CSV")
        print("2. Sélection d'un fichier CSV")

        choix = int(input("Votre choix : "))

        if choix == 1:
            fusion_fichier_csv("stockDB")
        if choix == 2:
            liste_csv = os.listdir("stockDB")
            for idx, liste_csv in enumerate(liste_csv, 1):
                print(f"{idx}. {liste_csv}")
            choix_magasin = int(input("Quel magasin choississez-vous ? "))
            if 0 < choix_magasin <= len(liste_csv):
                chemin_fichier = f"stockDB/{liste_csv}"
                magasin = FichierCSV(chemin_fichier)
                print("Que faire : ")
                print("1. Afficher le contenu")
                print("2. Trier le fichier")
                print("3. Générer récapitulatif")
                choix_action = int(input("Votre choix : "))
                if choix_action == 1:
                    print("1. Affichage brut")
                    print("2. Avec des critères")
                    choix_affichage = int(input("Votre choix : "))
                    if choix_affichage == 1:
                        print(magasin.contenu_sans_header())
                    elif choix_affichage == 2:
                        min_souhaite = input("Entrez le minimum de tri : ")
                        max_souhaite = input("Entrez le maximum de tri : ")
                        print(magasin.afficher_categorie())
                        categ_shouhaite = input("Entrez la catégorie de tri : ")
                        print(
                            magasin.afficher_range_produit(
                                min_produit=min_souhaite,
                                max_produit=max_souhaite,
                                categ=categ_shouhaite,
                            )
                        )
                    else:
                        print("Choix non valide")


if __name__ == "__main__":
    main()
