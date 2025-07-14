# 📦 materiels_service

Microservice de gestion des matériels — Mini ERP MIF Maroc  
Développé avec **FastAPI**, **SQLModel**, **JWT**, et testé avec **pytest**.

---

## 🚀 Objectif

Ce service permet de gérer le **cycle de vie des matériels** dans le système Mini ERP : création, mise à jour, suppression, statut, suivi de maintenance, et statistiques.

---

## 🧩 Fonctionnalités

### ✅ Fonctionnalités de base

- 📥 **Créer un matériel**  
  `POST /materiels/`  
  → Ajouter un matériel avec nom, référence, site, prochaine maintenance, etc.

- 📄 **Lister tous les matériels**  
  `GET /materiels/`  
  → Filtrage possible par :
  - `statut` (`actif`, `en_maintenance`, `hors_service`, `en_panne`)
  - `site_id`
  - pagination (`skip`, `limit`)

- 🔍 **Rechercher un matériel**  
  `GET /materiels/search/?query=...`  
  → Recherche par `nom` ou `référence`.

- 📌 **Voir un matériel par ID**  
  `GET /materiels/{materiel_id}`

- ✏️ **Modifier un matériel**  
  `PUT /materiels/{materiel_id}`

- ♻️ **Changer uniquement le statut**  
  `PATCH /materiels/{materiel_id}/statut`

- ❌ **Supprimer un matériel**  
  `DELETE /materiels/{materiel_id}`

---

### 🔧 Fonctionnalités supplémentaires

- ⏰ **Lister les matériels en retard de maintenance**  
  `GET /materiels/en-retard/`  
  → Affiche tous les matériels dont `prochaine_maintenance < date actuelle`.

- 📊 **Statistiques globales**  
  `GET /materiels/stats`  
  → Exemple de sortie :
  ```json
  {
    "total": 15,
    "actifs": 10,
    "en_maintenance": 2,
    "hors_service": 2,
    "en_panne": 1
  }
````

---

## 🔐 Sécurité

* Authentification par **JWT** (via `auth_service`)
* Accès restreint pour les admins sur certaines routes :

  * Création
  * Suppression
  * Mise à jour
  * Changement de statut

---

## 🧪 Tests unitaires

* Framework : `pytest`, `httpx.AsyncClient`, `pytest-asyncio`
* Lancer les tests :

```bash
pytest -v
```

* Tous les tests **✅ PASSENT** :

  * Création, lecture, recherche, mise à jour, suppression
  * Fonctionnalités avancées testées : maintenance en retard, stats

---

## 🐳 Dockerisation

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 📎 Documentation

* Swagger UI : [http://localhost:8000/docs](http://localhost:8000/docs)
* Redoc : [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🛠️ Technologies

* FastAPI + SQLModel (Async)
* Pydantic v2
* SQLite / PostgreSQL
* httpx + pytest
* Docker

---

## ✅ Statut : `STABLE & TESTÉ`

```
✔️ 100% des tests unitaires réussis
✔️ Routes sécurisées
✔️ Dockerisé
✔️ Prêt à l'intégration
```

---

## 🔗 Auteur

Projet Mini ERP — MIF Maroc
Développé par \[Rochdi Sabir]

```
