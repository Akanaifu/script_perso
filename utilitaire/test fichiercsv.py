import unittest
import os
import csv
from fichiercsv import (
    FichierCSV,
)  # Assurez-vous que le fichier de classe est nommé fichier_csv.py


class TestFichierCSV(unittest.TestCase):
    def setUp(self):
        """
        Crée un fichier CSV temporaire pour les tests.
        """
        self.fichier_test = "test_stock.csv"
        self.donnees = [
            ["Categorie", "Quantite", "Prix unitaire"],
            ["Produits frais", "10", "2.5"],
            ["Boissons", "20", "1.5"],
            ["Produits secs", "15", "3.0"],
            ["Boissons", "5", "2.0"],
        ]
        with open(self.fichier_test, mode="w", newline="", encoding="utf-8") as fichier:
            writer = csv.writer(fichier)
            writer.writerows(self.donnees)
        self.objet_csv = FichierCSV(self.fichier_test)

    def tearDown(self):
        """
        Supprime le fichier CSV temporaire après chaque test.
        """
        if os.path.exists(self.fichier_test):
            os.remove(self.fichier_test)

    def test_contenu_sans_header(self):
        """
        Teste que le contenu sans l'en-tête est correct.
        """
        contenu = self.objet_csv.contenu_sans_header()
        attendu = [
            "Produits frais,10,2.5\n",
            "Boissons,20,1.5\n",
            "Produits secs,15,3.0\n",
            "Boissons,5,2.0\n",
        ]
        self.assertEqual(contenu, attendu)

    def test_afficher_solde_magasin(self):
        """
        Teste le calcul du solde total du magasin.
        """
        # Redirection de la sortie pour capturer le print
        from io import StringIO
        import sys

        output = StringIO()
        sys.stdout = output

        self.objet_csv.afficher_solde_magasin()
        sys.stdout = sys.__stdout__

        self.assertIn("Le solde du magasin est de : 110.00 euros", output.getvalue())

    def test_trier_fichier_croissant(self):
        """
        Teste le tri par prix unitaire en ordre croissant.
        """
        self.objet_csv.trier_fichier("Prix unitaire", croissant=True)
        with open(self.fichier_test, mode="r", newline="", encoding="utf-8") as fichier:
            lecteur_csv = list(csv.reader(fichier))
        attendu = [
            ["Categorie", "Quantite", "Prix unitaire"],
            ["Boissons", "20", "1.5"],
            ["Boissons", "5", "2.0"],
            ["Produits frais", "10", "2.5"],
            ["Produits secs", "15", "3.0"],
        ]
        self.assertEqual(lecteur_csv, attendu)

    def test_trier_fichier_decroissant(self):
        """
        Teste le tri par prix unitaire en ordre décroissant.
        """
        self.objet_csv.trier_fichier("Prix unitaire", croissant=False)
        with open(self.fichier_test, mode="r", newline="", encoding="utf-8") as fichier:
            lecteur_csv = list(csv.reader(fichier))
        attendu = [
            ["Categorie", "Quantite", "Prix unitaire"],
            ["Produits secs", "15", "3.0"],
            ["Produits frais", "10", "2.5"],
            ["Boissons", "5", "2.0"],
            ["Boissons", "20", "1.5"],
        ]
        self.assertEqual(lecteur_csv, attendu)

    def test_afficher_range_produit(self):
        """
        Teste l'affichage des produits dans une fourchette de prix et d'une catégorie.
        """
        from io import StringIO
        import sys

        output = StringIO()
        sys.stdout = output

        self.objet_csv.afficher_range_produit(
            min_produit=1.0, max_produit=2.0, categ="Boissons"
        )
        sys.stdout = sys.__stdout__

        self.assertIn("Boissons,20,1.5", output.getvalue())
        self.assertIn("Boissons,5,2.0", output.getvalue())

    def test_generer_recap_fichier(self):
        """
        Teste la génération du récapitulatif par catégorie.
        """
        recap = self.objet_csv.generer_recap_fichier()
        attendu = {
            "Produits frais": {"quantite": 10, "valeur_totale": 25.0},
            "Boissons": {"quantite": 25, "valeur_totale": 40.0},
            "Produits secs": {"quantite": 15, "valeur_totale": 45.0},
        }
        self.assertEqual(recap, attendu)

    def test_afficher_categorie(self):
        """
        Teste l'affichage et la récupération des catégories présentes.
        """
        categories = self.objet_csv.afficher_categorie()
        attendu = ["Produits frais", "Boissons", "Produits secs"]
        self.assertCountEqual(categories, attendu)

    def test_recuperer_noms_colonnes(self):
        """
        Teste la récupération des noms des colonnes.
        """
        colonnes = self.objet_csv.recuperer_noms_colonnes()
        attendu = ["Categorie", "Quantite", "Prix unitaire"]
        self.assertEqual(colonnes, attendu)


if __name__ == "__main__":
    unittest.main()
