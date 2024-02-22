from http import HTTPStatus
import requests
from app.tests.test_functions import (
    create_user_payload,
    create_post_payload,
    create_reaction_payload,
    ENDPOINT
)


def test_create_post():
    # создание пользователя
    payload_user = create_user_payload()
    create_response = requests.post(f"{ENDPOINT}/users/create", json=payload_user)
    assert create_response.status_code == HTTPStatus.OK

    user_data = create_response.json()
    user_id = user_data['id']
    assert user_data['first_name'] == payload_user['first_name']
    assert user_data['last_name'] == payload_user['last_name']
    assert user_data['email'] == payload_user['email']

    get_response = requests.get(f"{ENDPOINT}/users/{user_id}")
    assert get_response.json()['first_name'] == payload_user['first_name']
    assert get_response.json()['last_name'] == payload_user['last_name']
    assert get_response.json()['email'] == payload_user['email']

    # создание поста от имени пользователя выше
    payload_post = create_post_payload(user_id)
    create_response = requests.post(f"{ENDPOINT}/posts/create", json=payload_post)
    assert create_response.status_code == HTTPStatus.OK

    post_data = create_response.json()
    post_id = post_data['id']
    assert post_data['author_id'] == payload_post['author_id']
    assert post_data['text'] == payload_post['text']
    assert len(post_data['reactions']) == 0

    get_response = requests.get(f"{ENDPOINT}/posts/{post_id}")
    assert get_response.json()['author_id'] == payload_post['author_id']
    assert get_response.json()['text'] == payload_post['text']
    assert len(get_response.json()['reactions']) == 0

    # удаление поста и пользователя
    delete_response = requests.delete(f"{ENDPOINT}/user/{user_id}")
    assert delete_response.status_code == HTTPStatus.OK
    assert delete_response.json()['first_name'] == payload_user['first_name']
    assert delete_response.json()['last_name'] == payload_user['last_name']
    assert delete_response.json()['email'] == payload_user['email']
    assert delete_response.json()['status'] == "deleted"

    delete_response = requests.delete(f"{ENDPOINT}/post/{post_id}")
    assert delete_response.status_code == HTTPStatus.OK
    assert delete_response.json()['author_id'] == payload_post['author_id']
    assert delete_response.json()['text'] == payload_post['text']
    assert delete_response.json()['status'] == "deleted"


def test_create_post_bad_data():
    # создание пользователя
    payload_user = create_user_payload()
    create_response = requests.post(f"{ENDPOINT}/users/create", json=payload_user)
    assert create_response.status_code == HTTPStatus.OK

    user_data = create_response.json()
    user_id = user_data['id']
    assert user_data['first_name'] == payload_user['first_name']
    assert user_data['last_name'] == payload_user['last_name']
    assert user_data['email'] == payload_user['email']

    get_response = requests.get(f"{ENDPOINT}/users/{user_id}")
    assert get_response.json()['first_name'] == payload_user['first_name']
    assert get_response.json()['last_name'] == payload_user['last_name']
    assert get_response.json()['email'] == payload_user['email']

    # создание поста от имени пользователя выше
    payload_post = create_post_payload(user_id)
    payload_post['author_id'] = -1
    create_response = requests.post(f"{ENDPOINT}/posts/create", json=payload_post)
    assert create_response.status_code == HTTPStatus.BAD_REQUEST

    payload_post = create_post_payload(user_id, text=False)
    create_response = requests.post(f"{ENDPOINT}/posts/create", json=payload_post)
    assert create_response.status_code == HTTPStatus.BAD_REQUEST

    # удаление поста и пользователя
    delete_response = requests.delete(f"{ENDPOINT}/user/{user_id}")
    assert delete_response.status_code == HTTPStatus.OK
    assert delete_response.json()['first_name'] == payload_user['first_name']
    assert delete_response.json()['last_name'] == payload_user['last_name']
    assert delete_response.json()['email'] == payload_user['email']
    assert delete_response.json()['status'] == "deleted"


def test_put_a_reaction_to_the_post():
    # создание первого пользователя
    payload_user_one = create_user_payload()
    create_response = requests.post(f"{ENDPOINT}/users/create", json=payload_user_one)
    assert create_response.status_code == HTTPStatus.OK

    user_data = create_response.json()
    user_id_one = user_data['id']
    assert user_data['first_name'] == payload_user_one['first_name']
    assert user_data['last_name'] == payload_user_one['last_name']
    assert user_data['email'] == payload_user_one['email']

    get_response = requests.get(f"{ENDPOINT}/users/{user_id_one}")
    assert get_response.json()['first_name'] == payload_user_one['first_name']
    assert get_response.json()['last_name'] == payload_user_one['last_name']
    assert get_response.json()['email'] == payload_user_one['email']

    # создание второго пользователя
    payload_user_two = create_user_payload()
    create_response = requests.post(f"{ENDPOINT}/users/create", json=payload_user_two)
    assert create_response.status_code == HTTPStatus.OK

    user_data = create_response.json()
    user_id_two = user_data['id']
    assert user_data['first_name'] == payload_user_two['first_name']
    assert user_data['last_name'] == payload_user_two['last_name']
    assert user_data['email'] == payload_user_two['email']

    get_response = requests.get(f"{ENDPOINT}/users/{user_id_two}")
    assert get_response.json()['first_name'] == payload_user_two['first_name']
    assert get_response.json()['last_name'] == payload_user_two['last_name']
    assert get_response.json()['email'] == payload_user_two['email']

    # создание поста от имени пользователя выше
    payload_post = create_post_payload(user_id_two)
    create_response = requests.post(f"{ENDPOINT}/posts/create", json=payload_post)
    assert create_response.status_code == HTTPStatus.OK

    post_data = create_response.json()
    post_id = post_data['id']
    assert post_data['author_id'] == payload_post['author_id']
    assert post_data['text'] == payload_post['text']
    assert len(post_data['reactions']) == 0

    get_response = requests.get(f"{ENDPOINT}/posts/{post_id}")
    assert get_response.json()['author_id'] == payload_post['author_id']
    assert get_response.json()['text'] == payload_post['text']
    assert len(get_response.json()['reactions']) == 0

    # ставим реакцию на пост
    payload_reaction = create_reaction_payload(user_id_one)
    create_response = requests.post(f"{ENDPOINT}/posts/{post_id}/reaction", json=payload_reaction)
    print(post_id, user_id_one, payload_reaction)
    assert create_response.status_code == HTTPStatus.OK

    get_response = requests.get(f"{ENDPOINT}/posts/{post_id}")
    assert len(get_response.json()["reactions"]) == 1
    assert get_response.json()["reactions"][-1] == payload_reaction["reaction"]

    # удаление поста и пользователей
    delete_response = requests.delete(f"{ENDPOINT}/user/{user_id_one}")
    assert delete_response.status_code == HTTPStatus.OK
    assert delete_response.json()['first_name'] == payload_user_one['first_name']
    assert delete_response.json()['last_name'] == payload_user_one['last_name']
    assert delete_response.json()['status'] == "deleted"

    delete_response = requests.delete(f"{ENDPOINT}/user/{user_id_two}")
    assert delete_response.status_code == HTTPStatus.OK
    assert delete_response.json()['first_name'] == payload_user_two['first_name']
    assert delete_response.json()['last_name'] == payload_user_two['last_name']
    assert delete_response.json()['status'] == "deleted"

    delete_response = requests.delete(f"{ENDPOINT}/post/{post_id}")
    assert delete_response.status_code == HTTPStatus.OK
    assert delete_response.json()['author_id'] == payload_post['author_id']
    assert delete_response.json()['text'] == payload_post['text']
    assert delete_response.json()['status'] == "deleted"


def test_get_all_posts():
    # создание первого пользователя
    payload_user_one = create_user_payload()
    create_response = requests.post(f"{ENDPOINT}/users/create", json=payload_user_one)
    assert create_response.status_code == HTTPStatus.OK

    user_data_one = create_response.json()
    user_id_one = user_data_one['id']
    assert user_data_one['first_name'] == payload_user_one['first_name']
    assert user_data_one['last_name'] == payload_user_one['last_name']
    assert user_data_one['email'] == payload_user_one['email']

    get_response = requests.get(f"{ENDPOINT}/users/{user_id_one}")
    assert get_response.json()['first_name'] == payload_user_one['first_name']
    assert get_response.json()['last_name'] == payload_user_one['last_name']
    assert get_response.json()['email'] == payload_user_one['email']

    # создание второго пользователя
    payload_user_two = create_user_payload()
    create_response = requests.post(f"{ENDPOINT}/users/create", json=payload_user_two)
    assert create_response.status_code == HTTPStatus.OK

    user_data_two = create_response.json()
    user_id_two = user_data_two['id']
    assert user_data_two['first_name'] == payload_user_two['first_name']
    assert user_data_two['last_name'] == payload_user_two['last_name']
    assert user_data_two['email'] == payload_user_two['email']

    get_response = requests.get(f"{ENDPOINT}/users/{user_id_two}")
    assert get_response.json()['first_name'] == payload_user_two['first_name']
    assert get_response.json()['last_name'] == payload_user_two['last_name']
    assert get_response.json()['email'] == payload_user_two['email']

    # создание постов от имени второго пользователя
    # первый пост
    payload_post_one = create_post_payload(user_id_two)
    create_response = requests.post(f"{ENDPOINT}/posts/create", json=payload_post_one)
    assert create_response.status_code == HTTPStatus.OK

    post_data_one = create_response.json()
    post_id_one = post_data_one['id']
    assert post_data_one['author_id'] == payload_post_one['author_id']
    assert post_data_one['text'] == payload_post_one['text']
    assert len(post_data_one['reactions']) == 0

    get_response = requests.get(f"{ENDPOINT}/posts/{post_id_one}")
    assert get_response.json()['author_id'] == payload_post_one['author_id']
    assert get_response.json()['text'] == payload_post_one['text']
    assert len(get_response.json()['reactions']) == 0

    # второй пост
    payload_post_two = create_post_payload(user_id_two)
    create_response = requests.post(f"{ENDPOINT}/posts/create", json=payload_post_two)
    assert create_response.status_code == HTTPStatus.OK

    post_data_two = create_response.json()
    post_id_two = post_data_two['id']
    assert post_data_two['author_id'] == payload_post_two['author_id']
    assert post_data_two['text'] == payload_post_two['text']
    assert len(post_data_two['reactions']) == 0

    get_response = requests.get(f"{ENDPOINT}/posts/{post_id_two}")
    assert get_response.json()['author_id'] == payload_post_two['author_id']
    assert get_response.json()['text'] == payload_post_two['text']
    assert len(get_response.json()['reactions']) == 0

    # ставим реакцию на первый пост второго пользователя
    payload_reaction = create_reaction_payload(user_id_one)
    create_response = requests.post(f"{ENDPOINT}/posts/{post_id_one}/reaction", json=payload_reaction)
    assert create_response.status_code == HTTPStatus.OK

    get_response = requests.get(f"{ENDPOINT}/posts/{post_id_one}")
    assert len(get_response.json()["reactions"]) == 1
    assert get_response.json()["reactions"][-1] == payload_reaction["reaction"]

    # проверка возвращаемого значение из ручки get_all_posts
    get_response = requests.get(f"{ENDPOINT}/users/{user_id_two}/posts", json={"sort": "asc"})
    assert get_response.status_code == HTTPStatus.OK
    posts = get_response.json()['posts']

    print(posts)
    assert posts[1]['id'] == post_id_two
    assert posts[0]['id'] == post_id_one

    assert len(posts[1]['reactions']) == 0
    assert len(posts[0]['reactions']) == 1
    assert posts[0]['reactions'][0] == payload_reaction["reaction"]

    # удаление постов и пользователей
    delete_response = requests.delete(f"{ENDPOINT}/user/{user_id_one}")
    assert delete_response.status_code == HTTPStatus.OK
    assert delete_response.json()['first_name'] == payload_user_one['first_name']
    assert delete_response.json()['last_name'] == payload_user_one['last_name']
    assert delete_response.json()['status'] == "deleted"

    delete_response = requests.delete(f"{ENDPOINT}/user/{user_id_two}")
    assert delete_response.status_code == HTTPStatus.OK
    assert delete_response.json()['first_name'] == payload_user_two['first_name']
    assert delete_response.json()['last_name'] == payload_user_two['last_name']
    assert delete_response.json()['status'] == "deleted"

    delete_response = requests.delete(f"{ENDPOINT}/post/{post_id_one}")
    assert delete_response.status_code == HTTPStatus.OK
    assert delete_response.json()['author_id'] == payload_post_one['author_id']
    assert delete_response.json()['text'] == payload_post_one['text']
    assert delete_response.json()['status'] == "deleted"

    delete_response = requests.delete(f"{ENDPOINT}/post/{post_id_two}")
    assert delete_response.status_code == HTTPStatus.OK
    assert delete_response.json()['author_id'] == payload_post_two['author_id']
    assert delete_response.json()['text'] == payload_post_two['text']
    assert delete_response.json()['status'] == "deleted"
