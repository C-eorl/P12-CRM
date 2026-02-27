# Projet 12 - Développez une architecture back-end sécurisée avec Python et SQL
![logo Epic Events](https://user.oc-static.com/upload/2023/07/26/16903799358611_P12-02.png)
## 1. Présentation

Projet visant à mettre en place un CRM sécurisé en ligne de commande
pour l'entreprise Epic Events (entreprise de gestion / conseil dans l'évènementiel).

L'application permet de gérer :
- clients
- contrat
- évènements
- utilisateur
- authentification sécurisée

**Stack technique**
- python ≤ 3.13
- typer - CLI moderne et typée
- SQLAlcheny - ORM
- PostgreSQL - Base de donnée relationnelle
- bcrypt - hachage sécurisé des mots de passe

Le projet suit une Clean Architecture garantissant maintenabilité et testabilité.

          Sens des dépendances
        ┌───────────────────────┐
      ^ │       Entities        │ 
      | ├───────────────────────┤
      | │       Use Cases       │
      | ├───────────────────────┤
      | │   Interface Adapters  │
      | ├───────────────────────┤
      | │     Infrastructure    │
        └───────────────────────┘

Cela permet un découplage fort, une logique métier indépendante, une facilité pour les tests unitaire.
## 2. Installation
    
* cloner le githup
```bash
git clone git@github.com:C-eorl/P12-CRM.git
cd P12-CRM
```
* créer environnement virtuel & activer
```bash
python3 -m venv .venv
source .venv/bin/activate
```

* installer les dépendences
```bash
pip install -r requirements.txt
```
* initialiser la base de donnée et créer un utilisateur admin

Le projet necessite une base de donnée **PostgreSQL**.
Pendant le script, vos identifiants PostgreSQL vous seront demandés plus le nom de la base de donnée que vous allez créer.
Suivie de la création de l'utilisateur admin (nom, email, mot de passe)
```bash
python script_init.py
```
* démarrer l'application et connectez-vous à l'aide de vos identifiants admin 
```bash
python main.py auth login
```
## 3. Utilisation

- **Modèle de commande** `main.py [sub app] [command] [*parametre]`
1. **Acces à l'application**

    * Pour vous connecter, utilisez `auth login`
    * Pour vous déconnecter, utilisez `auth logout`
---
2. **Gestion des clients**

    * Créer un client, utilisez `client create`
    * Modifier un client, utilisez `client update [id client]`
    * Afficher un client, utilisez `client show [id client]`
    * Afficher tous les clients, utilisez `client list`, possibilité de filtrer `-f` ou `--filter`
    * Supprimer un client, utilisez `client delete [id client]`
---
3. **Gestion des contrats**

    * Créer un contrat, utilisez `contrat create`
    * Modifier un contrat, utilisez `contrat update [id contrat]`
    * Afficher un contrat, utilisez `contrat show [id contrat]`
    * Afficher tous les contrats, utilisez `contrat list`, possibilité de filtrer `-f [filtre]` ou `--filter [filtre]`
    * Signer un contrat, utilisez `contrat sign [id contrat]`
    * Effectuer un payement, utilisez `contrat pay [id contrat]`
    * Supprimer un contrat, utilisez `contrat delete [id contrat]`
---
4. **Gestion des events**

    * Créer un event, utilisez `event create`
    * Modifier un event, utilisez `event update [id event]`
    * Afficher un event, utilisez `event show [id event]`
    * Afficher tous les events, utilisez `event list`, possibilité de filtrer `-f [filtre]` ou `--filter [filtre]`
    * Assigner un utilisateur Support, utilisez `event assign [id event]`
    * Supprimer un event, utilisez `event delete [id event]`
---
5. **Gestion des users**

    * Créer un user, utilisez `user create`
    * Modifier un user, utilisez `user update [id user]`
    * Afficher un user, utilisez `user show [id user]`
    * Afficher tous les users, utilisez `user list`, possibilité de filtrer `-f` ou `--filter`
    * Supprimer un user, utilisez `user delete [id user]`
---

## 4. Test

Tests unitaires & intrégration

```bash
pytest
```


_Projet réalisé dans le contexte de la formation Developpeur Python - OpenClassRoom_