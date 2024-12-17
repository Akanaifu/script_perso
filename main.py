import os
from utilitaire.fichiercsv import *
from utilitaire.utils import *


def main():
    while True:
        print("\nMenu Principal")
        print("1. Fusionner les fichiers CSV")
        print("2. Sélection d'un fichier CSV")
        print("3. Quitter")

        choix = int(input("Votre choix : "))

        if choix == 1:
            fusion_fichier_csv("stockDB")

        elif choix == 2:
            while True:
                liste_csv = os.listdir("stockDB")
                print("\nListe des fichiers CSV :")
                for idx, fichier_csv in enumerate(liste_csv, 1):
                    print(f"{idx}. {fichier_csv}")
                print(f"{len(liste_csv) + 1}. Retour au menu principal")
                print(f"{len(liste_csv) + 2}. Quitter")

                choix_magasin = int(input("Quel fichier choisissez-vous ? "))

                if 0 < choix_magasin <= len(liste_csv):
                    chemin_fichier = f"stockDB/{liste_csv[choix_magasin - 1]}"
                    magasin = FichierCSV(chemin_fichier)

                    while True:
                        print("\nQue faire avec le fichier ?")
                        print("1. Afficher le contenu")
                        print("2. Trier le fichier")
                        print("3. Générer récapitulatif")
                        print("4. Retour à la sélection des fichiers")
                        print("5. Quitter")

                        choix_action = int(input("Votre choix : "))

                        if choix_action == 1:
                            print("\n1. Affichage brut")
                            print("2. Avec des critères")
                            print("3. Retour")
                            choix_affichage = int(input("Votre choix : "))

                            if choix_affichage == 1:
                                print(magasin.contenu_sans_header())
                            elif choix_affichage == 2:
                                min_souhaite = int(input("Entrez le minimum de tri : "))
                                max_souhaite = int(input("Entrez le maximum de tri : "))
                                print(magasin.afficher_categorie())
                                categ_shouhaite = input("Entrez la catégorie de tri : ")
                                magasin.afficher_range_produit(
                                    min_produit=min_souhaite,
                                    max_produit=max_souhaite,
                                    categ=categ_shouhaite,
                                )
                            elif choix_affichage == 3:
                                continue
                            else:
                                print("Choix non valide.")

                        elif choix_action == 2:
                            print("\n1. Tri croissant")
                            print("2. Tri décroissant")
                            print("3. Retour")
                            choix_tri = int(input("Votre choix : "))

                            if choix_tri in [1, 2]:
                                ordre = (
                                    choix_tri == 2
                                )  # True pour décroissant, False pour croissant
                                listes_noms_colonnes = magasin.recuperer_noms_colonnes()

                                print("Choisissez une colonne pour le tri :")
                                for idx, nom in enumerate(listes_noms_colonnes, 1):
                                    print(f"{idx}. {nom}")
                                print(f"{len(listes_noms_colonnes) + 1}. Retour")

                                choix_colonne = int(
                                    input("Selon quelle colonne (index) ? ")
                                )
                                if 1 <= choix_colonne <= len(listes_noms_colonnes):
                                    magasin.trier_fichier(
                                        listes_noms_colonnes[choix_colonne - 1], ordre
                                    )
                                elif choix_colonne == len(listes_noms_colonnes) + 1:
                                    continue
                                else:
                                    print("Index de colonne invalide.")
                            elif choix_tri == 3:
                                continue
                            else:
                                print("Choix non valide.")

                        elif choix_action == 3:
                            magasin.generer_recap_fichier()
                        elif choix_action == 4:
                            break  # Retour à la sélection des fichiers
                        elif choix_action == 5:
                            print("Au revoir !")
                            exit()
                        else:
                            print("Choix non valide.")

                elif choix_magasin == len(liste_csv) + 1:
                    break  # Retour au menu principal
                elif choix_magasin == len(liste_csv) + 2:
                    print("Au revoir !")
                    exit()
                else:
                    print("Choix non valide.")

        elif choix == 3:
            print("Au revoir !")
            break

        else:
            print("Choix non valide.")


if __name__ == "__main__":
    main()
