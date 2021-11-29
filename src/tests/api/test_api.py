import email

from jsf import JSF

from app.core.email import ACCOUNT_VERIFICATION_EMAIL_SUBJECT, fm
from app.models.users import UserCreate


def test_docs(client):
    response = client.get(
        "/docs",
    )
    assert response.ok
    assert response.status_code == 200


def test_register_user(client):
    user = JSF(UserCreate.schema()).generate()
    user.update({"phone_number": "0711223344"})
    response = client.post("/auth/register", json=user)
    assert response.status_code == 201
    assert not response.json()["is_verified"]
    assert response.json().get("name") == user.get("name")
    assert response.json().get("email") == user.get("email")


def test_login_jwt_not_verified(client):
    user = JSF(UserCreate.schema()).generate()
    user.update({"phone_number": "0711223344"})
    client.post(
        "/auth/register",
        json=user,
    )
    login_data = {"username": user["email"], "password": user["password"]}
    response = client.post(
        "/auth/jwt/login",
        data=login_data,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "LOGIN_USER_NOT_VERIFIED"


def test_login_jwt_verified(client, email_html_parser):
    # Create user account
    user = JSF(UserCreate.schema()).generate()
    user.update({"phone_number": "0711223344"})
    client.post(
        "/auth/register",
        json=user,
    )
    user_email = user["email"]

    # Request verification token, check in email
    fm.config.SUPPRESS_SEND = 1
    with fm.record_messages() as outbox:
        client.post(
            "/auth/request-verify-token",
            json={"email": user_email},
        )
        verification_email = outbox[0]

        assert verification_email["from"] == "admin@people.api"
        assert verification_email["to"] == user_email
        assert verification_email["subject"] == ACCOUNT_VERIFICATION_EMAIL_SUBJECT
        assert verification_email.is_multipart()

        for part in email.message_from_bytes(
            verification_email.get_payload(i=0).as_bytes()
        ).walk():
            assert part.get_content_type() == "text/html"
            email_html = part.get_payload(decode=True).decode("utf-8").replace("\n", "")
            email_html_parser.feed(email_html)

    verification_token = email_html_parser.html["data"].split(" ")[-1]

    verified_account_response = client.post(
        "/auth/verify",
        json={"token": verification_token},
    )

    assert verified_account_response.json()["email"] == user_email
    assert verified_account_response.json()["is_verified"]

    login_data = {"username": user_email, "password": user["password"]}

    response = client.post(
        "/auth/jwt/login",
        data=login_data,
    )

    assert response.status_code == 200
    assert response.json()["access_token"]
    assert response.json()["token_type"] == "bearer"
