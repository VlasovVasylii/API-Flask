from uuid import uuid4


ENDPOINT = "http://127.0.0.1:5000"


def create_post_payload(number, text=True):
    if text:
        return {
            "author_id": number,
            "text": str(uuid4()),
        }
    return {
        "author_id": number,
    }


def create_reaction_payload(number):
    return {
        "user_id": number,
        "reaction": str(uuid4()),
    }


def create_user_payload():
    return {
        "first_name": "Vasya" + str(uuid4()),
        "last_name": "Pupkin" + str(uuid4()),
        "email": "test@test.ru" + str(uuid4()),
    }
