"""
Все руты для работы с пользователями
"""

from app import app, USERS, models
from flask import request, Response, url_for
from http import HTTPStatus
from matplotlib import pyplot as plt
from app.views.posts import get_information_about_post


@app.post("/users/create")
def user_create():
    data = request.get_json()
    user_id = len(USERS)
    try:
        first_name = data["first_name"]
        last_name = data["last_name"]
        email = data["email"]
    except KeyError:
        return Response(
            "Были переданы не все параметры",
            status=HTTPStatus.BAD_REQUEST,
            mimetype="text",
        )

    if models.User.is_valid_email(email) and all(user.email != email for user in USERS):
        user = models.User(user_id, first_name, last_name, email)
        USERS.append(user)
        response = Response(
            models.MyEncoder().encode(
                {
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "total_reactions": user.total_reactions,
                    "posts": [
                        get_information_about_post(post.id).get_json()
                        for post in user.posts
                    ],
                }
            ),
            HTTPStatus.OK,
            mimetype="application/json",
        )
        return response
    return Response(
        "Пользователь с такой почтой уже существует или введён "
        "некорректный адрес электронной почты",
        status=HTTPStatus.BAD_REQUEST,
        mimetype="text",
    )


@app.get("/users/<int:user_id>")
def get_user(user_id):
    if user_id < 0 or user_id >= len(USERS):
        return Response(
            "Такого пользователя не существует",
            status=HTTPStatus.NOT_FOUND,
            mimetype="text",
        )

    user = USERS[user_id]

    response = Response(
        models.MyEncoder().encode(
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "total_reactions": user.total_reactions,
                "posts": [
                    get_information_about_post(post.id).get_json()
                    for post in user.posts
                ],
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.get("/users/leaderboard")
def get_users_leaderboard():
    data = request.get_json()
    try:
        response_type = data["type"]
    except KeyError:
        return Response(
            "Были переданы не все параметры",
            status=HTTPStatus.BAD_REQUEST,
            mimetype="text",
        )
    if response_type == "list":
        sort = data["sort"]
        sorted_list = models.get_sorted_users(USERS, sort)
        if sorted_list:
            response = Response(
                models.MyEncoder().encode(
                    {"users": [get_user(user.id).get_json() for user in sorted_list]}
                ),
                HTTPStatus.OK,
                mimetype="application/json",
            )
            return response
        else:
            return Response(status=HTTPStatus.BAD_REQUEST)
    elif response_type == "graph":
        sorted_users = models.get_sorted_users(USERS, "asc")
        fig, ax = plt.subplots()

        user_names = [
            f"{user.first_name} {user.last_name} ({user.id})" for user in sorted_users
        ]
        user_count_reactions = [user.total_reactions for user in sorted_users]

        ax.bar(user_names, user_count_reactions)

        ax.set_ylabel("User's reactions")
        ax.set_title("User leaderboard by quantity reactions")
        plt.savefig("app/static/users_leaderboard.png")
        return Response(
            f"""<img src= "{url_for('static', filename='users_leaderboard.png')}">""",
            status=HTTPStatus.OK,
            mimetype="text/html",
        )
    return Response(status=HTTPStatus.BAD_REQUEST)
