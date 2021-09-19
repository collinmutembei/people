from app.models import ProfileCreate


def test_get_people(client):
    response = client.get(
        "/people",
    )
    assert response.status_code == 200
    # assert response.json() == []


def test_post_people(client):
    person = ProfileCreate(first_name="first", last_name="last", surname="surname")
    response = client.post("/people", json=person.dict())
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["first_name"] == person.first_name
    assert response.json()["last_name"] == person.last_name
    assert response.json()["surname"] == person.surname
