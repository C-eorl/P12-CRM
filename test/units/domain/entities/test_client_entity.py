from datetime import datetime

from src.domain.entities.value_objects import Email, Telephone



def test_client_create(client):

    assert client.id is None
    assert type(client.fullname) == str
    assert type(client.email) == Email
    assert type(client.telephone) == Telephone
    assert type(client.company_name) == str
    assert type(client.commercial_contact_id) == int
    assert type(client.created_at) == datetime
    assert type(client.updated_at) == datetime

def test_client_update_info(client):
    fullname = "futur test"
    email = Email('futur@test.fr')
    telephone = Telephone('0999999999')
    company_name = None
    client.update_info(fullname=fullname, email=email, telephone=telephone, company_name=company_name)

    assert client.fullname == fullname
    assert client.email == email
    assert client.telephone == telephone
    assert client.company_name == "company_test"
    assert client.updated_at != client.created_at


