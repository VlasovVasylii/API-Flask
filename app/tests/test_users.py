from http import HTTPStatus
import requests
import re
from app.tests.test_functions import (
    create_user_payload,
    create_post_payload,
    create_reaction_payload,
    ENDPOINT
)


def test_user_create():
    payload = create_user_payload()
    create_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
    assert create_response.status_code == HTTPStatus.OK

    user_data = create_response.json()
    user_id = user_data['id']
    assert user_data['first_name'] == payload['first_name']
    assert user_data['last_name'] == payload['last_name']
    assert user_data['email'] == payload['email']

    get_response = requests.get(f"{ENDPOINT}/users/{user_id}")
    assert get_response.json()['first_name'] == payload['first_name']
    assert get_response.json()['last_name'] == payload['last_name']
    assert get_response.json()['email'] == payload['email']

    delete_response = requests.delete(f"{ENDPOINT}/user/{user_id}")
    assert delete_response.status_code == HTTPStatus.OK
    assert delete_response.json()['first_name'] == payload['first_name']
    assert delete_response.json()['last_name'] == payload['last_name']
    assert delete_response .json()['status'] == "deleted"


def test_user_create_bad_data():
    payload = create_user_payload()
    payload['email'] = "testtest.ru"
    create_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
    assert create_response.status_code == HTTPStatus.BAD_REQUEST


def test_get_users_leaderboard_list():
    n = 3
    test_users = []
    for _ in range(n):
        payload = create_user_payload()
        create_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
        assert create_response.status_code == HTTPStatus.OK
        test_users.append(create_response.json()['id'])

    get_response = requests.get(
        f"{ENDPOINT}/users/leaderboard",
        json={
            "type": "list",
            "sort": "asc"
        }
    )
    leaderboard = get_response.json()['users']
    assert isinstance(leaderboard, list)
    assert len(leaderboard) == n

    for user_id in test_users:
        delete_response = requests.delete(f"{ENDPOINT}/user/{user_id}")
        assert delete_response.status_code == HTTPStatus.OK


def test_get_users_leaderboard_graph():
    n = 3
    test_users = []
    for _ in range(n):
        payload = create_user_payload()
        create_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
        assert create_response.status_code == HTTPStatus.OK
        test_users.append(create_response.json()['id'])

    get_response = requests.get(
        f"{ENDPOINT}/users/leaderboard",
        json={
            "type": "graph",
        }
    )
    leaderboard = get_response.text
    print(leaderboard)
    assert re.match(r'<img src=".+">', leaderboard) is not None

    for user_id in test_users:
        delete_response = requests.delete(f"{ENDPOINT}/user/{user_id}")
        assert delete_response.status_code == HTTPStatus.OK
