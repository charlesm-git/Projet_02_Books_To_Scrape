# Fonctionnement du programme ETL du site internet https://books.toscrape.com/

## Comment executer le code ?

- Télécharger en local l'ensemble des fichiers présents dans le repository GitHub 
- Configurer votre environnement virtuel avec l'ensemble des packages nécessaires. Vous pouvez pour cela utiliser le 
fichier `requirement.txt`
- Lancer l'execution du fichier Python `ETL.py`
- Et voila, l'ensemble du site books.toscrape.com va être analysé

## Données de sortie

Le programme va créer dans le projet Python un dossier nommé ./data_YYYYMMDD

Ce dossier contient l'ensemble des données extraites le jour de l'analyse :
* Un dossier CSV/ qui contient les données de tous les livres analysés, stockées au format CSV. Un fichier CSV par 
catégorie est créé.
* Un dossier image/ qui contient les couvertures de tous les livres, la aussi classé par catégorie.

Comme le programme crée un dossier daté, il est facile de le lancer à des dates différentes sans perdre le contenu des 
analyse précédentes. Vous pouvez donc suivre l'évolution du contenu du site facilement !