# CLAUDE.md

## Projet
**CampusFlow** – API back-end (SAÉ 4.A, BUT2 informatique, IUT de Montreuil) de gestion des visiteurs
d'événements IUT (portes ouvertes, salons) : fiches visiteurs, événements, formations visées, statistiques,
export CSV/e-mail. Auteurs : Lay, Quemener, Cai. Le front (Vite) tourne sur `http://localhost:5173`.

## Stack
- **Python 3.11** (version utilisée ici ; des `.pyc` 3.12 et 3.14 existent aussi)
- **Flask 3.1.3** + **flask-cors 6.0.2**, gevent 25.9.1
- **SQLite** via le module `sqlite3` (pas d'ORM), `row_factory = sqlite3.Row`, clés étrangères activées
- **Pydantic 2.12.5** pour la validation des DTO d'entrée
- **python-dotenv 1.2.2** pour la configuration (versions exactes dans `requirements.txt`)

## Structure
Tout le code est dans `BUT2_2026_SAE4.A-LayQuemenerCai-back/` :
- `app.py` – point d'entrée Flask, enregistre les blueprints, appelle `init_db()`
- `controllers/` – routes (`visiteurs_controller` → `/visiteurs`, `config_controller` → `/config`)
- `services/` – logique métier (filtrage, pagination, export CSV, stats)
- `repository/` – requêtes SQL (paramétrées avec `?`)
- `dtos/` – modèles Pydantic (`Creer*DTO`, `Get*DTO`)
- `mappers/` – conversion ligne BDD ⇄ DTO / JSON front
- `database.py` (connexion par requête via `flask.g`), `init_db.py` (schéma `CREATE TABLE IF NOT EXISTS`)
- `Token.py` – jetons d'authentification admin stockés en mémoire
- `../DocumentsARendre/` – livrables PDF (journal technique, RGPD)

## Commandes
Depuis `BUT2_2026_SAE4.A-LayQuemenerCai-back/` :
```bash
python -m venv .venv                # .venv est ignoré par git
source .venv/bin/activate          # Linux/macOS
.venv\Scripts\Activate.ps1         # Windows PowerShell (cmd : .venv\Scripts\activate.bat)
pip install -r requirements.txt
cp .env.exemple .env      # renseigner PASSWORD, DATABASE (chemin du .db), CORS_ORIGIN
flask --app app run       # ou: python app.py  (http://127.0.0.1:5000)
```
- **Tests** : aucun test automatisé ni CI pour l'instant ; vérifier à la main (`curl`/client HTTP) les routes,
  ex. `GET /visiteurs?limit=5&page=1`. Si vous ajoutez des tests, utilisez `pytest` + `app.test_client()`.

## Conventions observées
- Architecture en couches stricte : controller → service → repository ; les mappers/DTO font la transformation.
- Un fichier par domaine, suffixé `_controller`, `_service`, `_repository`, `_mapper` (`visiteurs`, `config`).
- Blueprints avec `url_prefix` ; routes REST (GET/POST/PUT/DELETE), filtres et pagination en query string
  (`limit`, `page`).
- Domaine et identifiants en **français** (`visiteurs`, `evenements`, `formations_iut`, `nom_lycee`…) ;
  colonnes SQL en `snake_case`, DTO JSON parfois en camelCase (`codePostal`).
- Fonctions de repository nommées de façon mixte (`get_allRepository`) : imiter le style local existant.
- Docstrings en français, placées dans un bloc de texte au-dessus des fonctions des mappers.
- Configuration uniquement via `.env` (jamais commité) ; `.env.exemple` documente les variables.
- ⚠️ Des `__pycache__/*.pyc` sont suivis par git malgré tout : ne pas les modifier ni les ajouter.

## Règles de travail
- Ne jamais committer de secret (`.env`, mots de passe, jetons) ; seul `.env.exemple` est versionné.
- Créer une branche et une PR par modification.
- Accompagner tout correctif de sécurité d'un test.
- Lancer les tests avant d'ouvrir une PR.
- Expliquer tout changement de dépendance (`requirements.txt`) dans la PR.
- Répondre en français.
