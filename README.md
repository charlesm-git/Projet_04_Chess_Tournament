# Logiciel de Gestion de tournoi d'échec

## Installation

* Importer l'ensemble du contenu du repository GitHub en local
* Créer votre environnement virtuel et à l'aide du fichier `requirement.txt`, installer l'ensemble des packages 
nécessaires au bon fonctionnement du programme
  * La commande à utiliser est : pip install -r requirements.txt

## Utilisation du programme
* Executer le fichier Python `main.py`
* A la première execution, l'arborescence de sauvegarde de données sera créé sous `.\data`
* Le programme se lance automatiquement et affiche le menu principal. Tout se passe dans la console !
* Vous n'avez plus qu'a quivre les indications du menu principal pour ajouter des joueurs à la base de données et 
créer votre premier tournoi !

## Génération d'un nouveau rapport flake8
Pour générer un nouveau rapport flake8 :
* Ouvrir un shell
* Se positionner dans le repertoire du projet Python
* Executer la commande : flake8 .\main.py .\Models\ .\Views\ .\Controllers\ .\Util\ --format=html --htmldir=flake_report

En faisant cela, l'ensemble des fichiers python du programme vont être analysés et un nouveau rapport html sera créé. 
Vous n'avez plus qu'a l'ouvrir !