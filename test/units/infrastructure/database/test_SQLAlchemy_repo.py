def test_save_client_create(client_SQLAlchemy_repository, client):
    saved_client = client_SQLAlchemy_repository.save(client)

    assert saved_client.id is not None
    assert saved_client.fullname == client.fullname
    assert saved_client.email.address == client.email.address


def test_save_client_update(client_SQLAlchemy_repository, client):
    saved_client = client_SQLAlchemy_repository.save(client)

    saved_client.fullname = "SQL test"
    updated_client = client_SQLAlchemy_repository.save(saved_client)

    assert updated_client.fullname == "SQL test"
    assert updated_client.id == saved_client.id