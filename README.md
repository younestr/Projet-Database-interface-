# MySQL Interface en Python

MySQL Interface en Python
Ce programme Python fournit une interface graphique pour interagir avec une base de données MySQL. L'interface est conçue pour effectuer des opérations courantes telles que la sélection, l'insertion, la mise à jour et la suppression de données, ainsi que la création de nouvelles tables.

## Configuration de la Base de Données
Assurez-vous de remplacer les informations d'identification de la base de données dans la section suivante du code avec vos propres informations :

```python
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'projectDB'
}
```

## Utilisation de l'Interface
1-Sélection de la Table : Utilisez le menu déroulant pour sélectionner la table sur laquelle vous souhaitez effectuer des opérations.

2-Opérations SQL : Choisissez parmi les boutons disponibles pour effectuer des opérations telles que la sélection, l'insertion, la mise à jour, la suppression et la création de tables.

3-Exportation de Données : Exportez les données sélectionnées au format CSV en cliquant sur le bouton "Export Data". Vous serez invité à spécifier le fichier de destination.

4-Création de Nouvelles Tables : Utilisez le bouton "Create Table" pour spécifier le nom et le nombre de champs d'une nouvelle table, ainsi que leurs types.

5-Sélection de Données : Sélectionnez les colonnes et définissez des conditions pour afficher des données spécifiques.

6-Insertion de Données : Remplissez les champs appropriés et utilisez le bouton "Insert Data" pour insérer de nouvelles données dans la table sélectionnée.

7-Mise à Jour de Données : Sélectionnez des conditions pour identifier les lignes à mettre à jour, puis spécifiez les nouvelles valeurs dans les champs appropriés et utilisez le bouton "Update Data".

8-Suppression de Données : Supprimez des lignes spécifiques ou l'ensemble de la table en fonction des options choisies.

## Avertissement
Assurez-vous de comprendre les conséquences des opérations que vous effectuez, en particulier lors de la suppression de données ou de la création de nouvelles tables.

## Dépendances
Ce programme utilise la bibliothèque "mysql.connector" pour la connexion à la base de données et la bibliothèque "tkinter" pour l'interface graphique. Assurez-vous d'installer ces dépendances avant d'exécuter le programme.

```bash
pip install mysql-connector-python
```

## Exécution du Programme

Assurez-vous d'avoir Python installé sur votre machine. Exécutez le programme en utilisant la commande suivante dans le terminal :

```bash
python nom_du_programme.py
```
N'oubliez pas de personnaliser le nom du programme en conséquence.


