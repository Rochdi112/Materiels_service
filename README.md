# 🛠️ Materiels Service - Mini ERP MIF Maroc

Microservice de gestion des matériels pour le projet **Mini ERP** de l'entreprise **MIF Maroc**.

Développé avec **FastAPI**, **SQLModel**, **SQLite**, et testé avec **Pytest**. Ce service gère les opérations CRUD pour les matériels techniques installés sur les différents sites.

---

## 📦 Fonctionnalités

- 📄 **Créer** un matériel (`POST /materiels/`)
- 📋 **Lister** tous les matériels (`GET /materiels/`)
- ✏️ **Mettre à jour** un matériel (`PUT /materiels/{id}`)
- 🗑️ **Supprimer** un matériel (`DELETE /materiels/{id}`)

---

## 🧱 Technologies

| Composant         | Version / Stack        |
|-------------------|------------------------|
| Python            | 3.10+                  |
| Framework         | FastAPI                |
| ORM               | SQLModel               |
| DB Dév            | SQLite                 |
| Test              | Pytest + TestClient    |
| Authentification  | (à intégrer via JWT)   |
| Déploiement       | Docker                 |

---

## 🚀 Lancer le service

### ▶️ En local (dev)

```bash
uvicorn app.main:app --reload
````

Accès docs :

* Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)
* ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

### 🐳 Docker

#### Dockerfile (inclus)

```bash
docker build -t materiels_service .
docker run -d -p 8000:8000 materiels_service
```

---

## 🧪 Tests unitaires

```bash
pytest -v
```

Tous les tests se trouvent dans :
`app/tests/test_materiels.py` ✅

---

## 🗃️ Structure du projet

```
materiels_service/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models/
│   │   └── materiel_model.py
│   ├── schemas/
│   │   └── materiel_schema.py
│   ├── routes/
│   │   └── materiels.py
│   ├── services/
│   │   └── materiel_service.py
│   └── tests/
│       ├── test_materiels.py
│       └── conftest.py
├── Dockerfile
└── requirements.txt
```

---

## 🔒 Sécurité

> Ce microservice peut être sécurisé via l'authentification JWT en intégrant un `Depends(get_current_user)` à chaque route critique. (non activé ici pour simplifier le développement)

---

## 📚 Auteurs

* Développé par **Rochdi** pour **MIF Maroc**
* Encadrant : Mr **Lahlou**

---

## ✅ Statut du service

| Testé | Déployable | Stable | Sécurisé (auth) |
| ----- | ---------- | ------ | --------------- |
| ✔️    | ✔️         | ✔️     | ❌ (à intégrer)  |

```