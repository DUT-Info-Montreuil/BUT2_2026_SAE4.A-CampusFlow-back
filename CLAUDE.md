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

## Domaines

Dépôt back uniquement : le front vit ailleurs, donc aucun domaine front ici. Chemins relatifs à `BUT2_2026_SAE4.A-LayQuemenerCai-back/`. Un domaine couvre soit le front, soit le back, jamais les deux, et correspond à une partie fonctionnelle précise.

| Domaine | Périmètre | Dossiers / fichiers |
|---|---|---|
| **Visiteurs** (back) | CRUD des visiteurs, exports (CSV, e-mails), statistiques (bac, handicap, immersion, réorientation) | `controllers/visiteurs_controller.py`, `services/visiteurs_service.py`, `repository/visiteurs_repository.py`, `mappers/visiteurs_mapper.py`, `dtos/CreerVisiteursDTO.py`, `dtos/GetVisiteursDTO.py` |
| **Configuration événements & formations** (back) | CRUD des événements et des formations de l'IUT | `controllers/config_controller.py` (routes `/evenement`, `/formation`), `services/config_service.py`, `repository/config_repository.py`, `mappers/config_mapper.py`, `dtos/CreerConfigDTO.py`, `dtos/GetConfigDTO.py` |
| **Authentification** (back) | Login, logout, vérification et changement de mot de passe, jetons | `Token.py`, routes `/authentificate`, `/verif-authentificate`, `/logout`, `/modif-password` de `controllers/config_controller.py` |
| **Socle technique** (back) | Démarrage de l'app, base SQLite, dépendances | `app.py`, `database.py`, `init_db.py`, `requirements.txt`, `.env.exemple` |
| **Documents projet** | Livrables (journal technique, RGPD) | `DocumentsARendre/` |

## Commandes
Depuis `BUT2_2026_SAE4.A-LayQuemenerCai-back/` :
```bash
rm -rf .venv && /usr/bin/python3 -m venv .venv   # .venv ignoré par git ; Python système, pas conda
source .venv/bin/activate                        # Windows : .venv\Scripts\Activate.ps1
# Si ensurepip échoue (Python conda) : sudo apt install python3-venv, ou utiliser conda :
# conda create -n campusflow python=3.11 && conda activate campusflow
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
- Ne travailler que dans un seul périmètre à la fois (un seul domaine du tableau ci-dessus). Il ne doit lire ni les dépendances installées (`.venv`, `site-packages`), ni les fichiers de verrouillage, ni les données (fichiers `.db`, `.env`), logs ou fichiers générés (`__pycache__`, etc.). Si le front et le back doivent communiquer, faites-les s'appuyer sur `docs/API.md` plutôt que sur une lecture complète de l'autre partie du projet.
- Ne jamais committer de secret (`.env`, mots de passe, jetons) ; seul `.env.exemple` est versionné.
- Créer une branche et une PR par modification.
- Accompagner tout correctif de sécurité d'un test.
- Lancer les tests avant d'ouvrir une PR.
- Expliquer tout changement de dépendance (`requirements.txt`) dans la PR.
- Répondre en français.
