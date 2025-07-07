from datetime import datetime

def test_create_materiel(client):
    response = client.post("/materiels/", json={
        "nom": "Scanner",
        "reference": "SC123",
        "date_installation": datetime.now().isoformat(),
        "statut": "actif",
        "site_id": 1
    })
    assert response.status_code == 200
    data = response.json()
    assert data["nom"] == "Scanner"
    assert data["statut"] == "actif"

def test_get_all_materiels(client):
    response = client.get("/materiels/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_update_materiel(client):
    response = client.put("/materiels/1", json={"statut": "en maintenance"})
    assert response.status_code == 200
    data = response.json()
    assert data["statut"] == "en maintenance"

def test_delete_materiel(client):
    response = client.delete("/materiels/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Matériel supprimé avec succès"}
