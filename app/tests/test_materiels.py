from datetime import datetime, timedelta
import pytest


@pytest.mark.asyncio
async def test_create_materiel(client):
    response = await client.post("/materiels/", json={
        "nom": "Scanner Epson",
        "reference": "EP123",
        "date_installation": datetime.utcnow().isoformat(),
        "prochaine_maintenance": (datetime.utcnow() + timedelta(days=30)).isoformat(),
        "site_id": 1,
        "statut": "actif"
    }, headers={"Authorization": "Bearer token_admin"})
    assert response.status_code == 201
    data = response.json()
    assert data["nom"] == "Scanner Epson"


@pytest.mark.asyncio
async def test_get_all_materiels(client):
    response = await client.get("/materiels/", headers={"Authorization": "Bearer token_admin"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_update_statut(client):
    response = await client.patch("/materiels/1/statut", json={
        "statut": "en_maintenance"
    }, headers={"Authorization": "Bearer token_admin"})
    assert response.status_code == 200
    assert response.json()["statut"] == "en_maintenance"


@pytest.mark.asyncio
async def test_get_by_id(client):
    response = await client.get("/materiels/1", headers={"Authorization": "Bearer token_admin"})
    assert response.status_code == 200
    assert response.json()["id"] == 1


@pytest.mark.asyncio
async def test_search_materiel(client):
    response = await client.get("/materiels/search/?query=Scanner", headers={"Authorization": "Bearer token_admin"})
    assert response.status_code == 200
    assert any("Scanner" in m["nom"] for m in response.json())


@pytest.mark.asyncio
async def test_en_retard(client):
    await client.post("/materiels/", json={
        "nom": "Onduleur APC",
        "reference": "APC500",
        "prochaine_maintenance": (datetime.utcnow() - timedelta(days=2)).isoformat(),
        "site_id": 2,
    }, headers={"Authorization": "Bearer token_admin"})

    response = await client.get("/materiels/en-retard/", headers={"Authorization": "Bearer token_admin"})
    assert response.status_code == 200
    assert len(response.json()) >= 1


@pytest.mark.asyncio
async def test_stats(client):
    response = await client.get("/materiels/stats", headers={"Authorization": "Bearer token_admin"})
    assert response.status_code == 200
    stats = response.json()
    assert "total" in stats
    assert "actifs" in stats


@pytest.mark.asyncio
async def test_delete_materiel(client):
    response = await client.delete("/materiels/1", headers={"Authorization": "Bearer token_admin"})
    assert response.status_code == 200
    assert response.json() == {"message": "Matériel supprimé avec succès"}
