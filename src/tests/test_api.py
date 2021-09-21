from app.schemas import ProfileDetails


def test_get_people(client):
    response = client.get(
        "/profile",
    )
    assert response.status_code == 200


def test_create_profile(client):
    profile = ProfileDetails(name="first last", bio={"about": "tester", "other": "aob"})
    response = client.post("/profile", json=profile.dict())
    assert response.status_code == 200
    assert "id" in response.json()
    assert "active" in response.json()
    assert response.json()["name"] == profile.name
    assert response.json()["bio"] == profile.bio


def test_update_profile():
    pass


def test_delete_profile():
    pass
