import requests
import json

base_url = "http://localhost:5000/users"
create_url = base_url + "/create"
update_url = base_url + "/update/"
delete_url = base_url + "/delete/"
info_url = base_url + "/info/"

test_user_db = {}

test_user = {
        "first_name": "test_first",
        "last_name": "test_last",
        "email": "test_email"
    }


def cleanup_users():
    for user in list(test_user_db.values()):
        if 'id' in user:
            test_user_db.pop(user['id'])
            response = requests.delete(delete_url + user['id'])
            assert response.status_code == 200


# functional/unit tests
def test_create_info_user():
    response = requests.post(create_url, headers={"Content-Type": "application/json"},
                             data=json.dumps(test_user))
    assert response.status_code == 200
    data = response.json()
    assert 'data' in data
    user_id = data['data']
    response = requests.get(info_url + user_id)
    assert response.status_code == 200
    data = response.json()
    assert 'data' in data
    assert data['data'] == test_user
    test_user["id"] = user_id
    test_user_db[user_id] = test_user
    cleanup_users()
    assert not test_user_db
    test_user.pop("id")


def test_create_no_user():
    response = requests.post(create_url)
    assert response.status_code == 400


def test_update_no_user():
    none_id = '1234'
    response = requests.put(update_url + none_id)
    assert response.status_code == 404


def test_update_no_updates():
    response = requests.post(create_url, headers={"Content-Type": "application/json"},
                             data=json.dumps(test_user))
    assert response.status_code == 200
    data = response.json()
    assert 'data' in data
    user_id = data['data']
    test_user["id"] = user_id
    test_user_db[data['data']] = test_user
    response = requests.put(update_url + user_id)
    assert response.status_code == 400
    cleanup_users()
    assert not test_user_db
    test_user.pop("id")


def test_delete_invalid_user():
    none_id = '1234'
    response = requests.delete(delete_url + none_id)
    assert response.status_code == 404


def test_deleted_user():
    response = requests.post(create_url, headers={"Content-Type": "application/json"},
                             data=json.dumps(test_user))
    assert response.status_code == 200
    data = response.json()
    assert 'data' in data
    user_id = data['data']
    test_user["id"] = user_id
    response = requests.delete(delete_url + user_id)
    assert response.status_code == 200
    response = requests.delete(delete_url + user_id)
    assert response.status_code == 404


# integration test
def test_crud_user():
    response = requests.post(create_url, headers={"Content-Type": "application/json"},
                             data=json.dumps(test_user))
    assert response.status_code == 200
    data = response.json()
    assert 'data' in data
    user_id = data['data']

    test_user['first_name'] = 'real_first_name'
    test_user['last_name'] = 'real_last_name'
    test_user['email'] = 'real@email.com'
    response = requests.put(update_url + user_id, headers={"Content-Type": "application/json"},
                            data=json.dumps(test_user))
    assert response.status_code == 200
    response = requests.get(info_url + user_id)
    assert response.status_code == 200
    data = response.json()
    assert 'data' in data
    assert data['data'] == test_user
    test_user["id"] = user_id
    test_user_db[user_id] = test_user
    cleanup_users()
    assert not test_user_db


