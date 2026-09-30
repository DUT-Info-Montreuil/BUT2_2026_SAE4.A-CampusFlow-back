# API CampusFlow — contrat front ⇄ back

Source de vérité pour la communication entre le front et le back (voir `CLAUDE.md`).
Déduit des controllers, mappers et DTO du back ; à mettre à jour à chaque changement de route.

- **URL de base** : `http://127.0.0.1:5000` (Flask). Le front est autorisé via `CORS_ORIGIN` (`http://localhost:5173`).
- **Format** : JSON (`Content-Type: application/json`) sauf les exports CSV.
- **Dates** : `date_naissance` en chaîne (`YYYY-MM-DD`) ; `date` d'un événement au format ISO 8601.
- **Erreurs** : le corps est une simple chaîne JSON (message), pas un objet.
- **Authentification** : un jeton est délivré par `POST /config/authentificate`, mais **aucune route n'exige actuellement ce jeton** ; le front doit le gérer (voir `/config/verif-authentificate`).

## Santé

| Méthode | Route | Réponse |
|---|---|---|
| GET | `/` | `200` texte `CampusFlow` |

## Visiteurs (`/visiteurs`)

### Objets retournés

`GET /visiteurs` (résumé) :
```json
{ "id": 1, "nom": "Dupont", "prenom": "Jean",
  "bac": { "intitule": "Général", "annee": 2025, "matiere1": "Maths", "matiere2": null },
  "adresse": { "ville": "Montreuil", "codePostal": 93100 } }
```
`GET /visiteurs/{id}` (détail) : résumé + `date_naissance`, `lycee` (`{ "nom_lycee", "codePostal" }`),
`options` (`{ "handicap", "reorientation", "immersion" }` booléens), `email`, `telephone`,
`formation_actuelle` (`{ "intitule", "niveau_etudes" }` ou absent).

### Routes

| Méthode | Route | Description | Succès | Erreurs |
|---|---|---|---|---|
| GET | `/visiteurs` | Liste paginée filtrée | `200` `{ "data": [résumé…], "page", "limit" }` | — |
| GET | `/visiteurs/{id}` | Détail d'un visiteur | `200` détail | `404` |
| POST | `/visiteurs` | Créer un visiteur | `201` | `404` (validation, message d'erreur) |
| PUT | `/visiteurs/{id}` | Modifier un visiteur | `201` | `400` |
| DELETE | `/visiteurs/{id}` | Supprimer un visiteur | `204` | `404` |
| DELETE | `/visiteurs` | Supprimer tous les visiteurs | `204` | `404` (rien à supprimer) |
| GET | `/visiteurs/export` | Export CSV filtré (`visiteurs.csv`) | `200` `text/csv` | — |
| GET | `/visiteurs/export/email` | Export CSV des e-mails (`email.csv`) | `200` `text/csv` | — |
| GET | `/visiteurs/stat` | Toutes les statistiques | `200` `{ "bac", "reorientation", "immersion", "handicap" }` | — |
| GET | `/visiteurs/stat/bac` | Effectif par bac | `200` objet | — |
| GET | `/visiteurs/stat/handicap` | Effectif par valeur de `handicap` | `200` objet | — |
| GET | `/visiteurs/stat/immersion` | Effectif par valeur d'`immersion` | `200` objet | — |
| GET | `/visiteurs/stat/reorientation` | Effectif par valeur de `reorientation` | `200` objet | — |

Les statistiques sont des dictionnaires `valeur → effectif`, ex. `{ "Général": 12, "STI2D": 4 }` ou `{ "0": 10, "1": 3 }`.

### Filtres de `GET /visiteurs` (query string)

`nom`, `prenom`, `telephone`, `email`, `ville`, `bac`, `lycee`, `formation_actuelle`, `formation_visee`,
`reorientation`, `immersion`, `handicap` (`true` ou toute autre valeur = faux), `limit` (défaut `5`), `page` (défaut `1`).
`GET /visiteurs/export` accepte les mêmes filtres, sauf `formation_visee`, `limit` et `page`.

### Corps de `POST /visiteurs`

Corps **à plat** (pas d'objets imbriqués) :

| Champ | Type | Obligatoire | Règles |
|---|---|---|---|
| `nom`, `prenom` | string | oui | ≥ 2 caractères |
| `date_naissance` | string | oui | `YYYY-MM-DD` |
| `email` | string | non | au moins un de `email` / `telephone` (contrainte BDD) |
| `telephone` | string | non | exactement 10 caractères |
| `bac_intitule` | string | oui | ≥ 2 caractères |
| `bac_annee` | int | oui | |
| `bac_matiere1`, `bac_matiere2` | string | non | |
| `nom_lycee` | string | oui | |
| `code_postal_lycee` | int | oui | |
| `adresse_ville` | string | oui | ≥ 2 caractères |
| `adresse_codePostal` | int | oui | |
| `handicap`, `reorientation`, `immersion` | bool | non | défaut `false` |
| `formation_actuelle_intitule`, `formation_actuelle_niveau` | string | non | à fournir ensemble (niveau ≥ 5 caractères) |
| `formationSouhaite` | int | non | `id` d'une formation (`/config/formation`) |
| `evenementSouhaite` | int | non | `id` d'un événement (`/config/evenement`) |

### Corps de `PUT /visiteurs/{id}`

Mêmes champs à plat que le POST, avec ces différences : `bac_matiere1`/`bac_matiere2` s'appellent
`matiere1`/`matiere2` ; `email`, `telephone`, `nom_lycee`, `code_postal_lycee` sont **tous requis** (peuvent valoir `null` pour
`email`/`telephone`) ; `handicap` et `immersion` sont pris en compte (`reorientation` n'est pas modifiable) ;
la formation actuelle n'est pas modifiable.

## Configuration (`/config`)

### Événements

Objet : `{ "id": 1, "intitule": "JPO", "date": "2026-02-07T09:00:00", "lieu": { "ville": "Montreuil", "codePostal": 93100 } }`

| Méthode | Route | Corps | Succès | Erreurs |
|---|---|---|---|---|
| GET | `/config/evenement` | — | `200` liste d'événements | — |
| POST | `/config/evenement` | `intitule`, `date`, `adresse_ville`, `adresse_codePostal` | `201` | `400` |
| PUT | `/config/evenement/{id}` | `evenement_intitule`, `date`, `adresse_ville`, `adresse_codePostal` | `201` | `404` |
| DELETE | `/config/evenement/{id}` | — | `204` | `404` |
| DELETE | `/config/evenement` | — | `204` (supprime tout) | `404` |

### Formations de l'IUT

Objet : `{ "id": 1, "intitule": "BUT Informatique" }`

| Méthode | Route | Corps | Succès | Erreurs |
|---|---|---|---|---|
| GET | `/config/formation` | — | `200` liste de formations | — |
| POST | `/config/formation` | `intitule` | `201` | `404` |
| PUT | `/config/formation/{id}` | `formation_intitule`, `adresse_ville`, `adresse_codePostal` | `201` | `404` |
| DELETE | `/config/formation/{id}` | — | `204` | `404` |
| DELETE | `/config/formation` | — | `204` (supprime tout) | `404` |

### Authentification

| Méthode | Route | Corps | Succès | Erreurs |
|---|---|---|---|---|
| POST | `/config/authentificate` | `{ "password" }` | `200` `{ "token" }` | `400` |
| POST | `/config/verif-authentificate` | `{ "token" }` | `200` (jeton valide) | `400` |
| POST | `/config/logout` | `{ "token" }` | `200` | — |
| PUT | `/config/modif-password` | `{ "oldPassword", "newPassword", "confPassword" }` | `200` (toujours, même si refusé) | — |

Les jetons sont stockés en mémoire côté serveur : ils sont perdus au redémarrage.

## Points d'attention pour le front

- Les réponses `204` renvoient un message dans le corps côté serveur, mais un client HTTP l'ignore : ne pas s'y fier.
- Les codes d'erreur ne sont pas homogènes (`POST` visiteur/formation → `404`, événement → `400`) ; se fier au corps (message).
- `modif-password` répond `200` même si l'ancien mot de passe est faux ou si la confirmation diffère.
