"""
Все роуты для взаимодействия пользователя
"""

from app import app, USERS, POSTS, models
from flask import request, Response, url_for
import json
from http import HTTPStatus
from matplotlib import pyplot as plt


@app.post("/users/create")
def user_create():
    data = request.get_json()
    user_id = len(USERS)
    try:
        first_name = data["first_name"]
        last_name = data["last_name"]
        email = data["email"]
    except KeyError:
        return Response("Не был передан один из параметров", status=HTTPStatus.BAD_REQUEST, mimetype="text")

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
        mimetype="text"
    )


@app.get("/users/<int:user_id>")
def get_user(user_id):
    if user_id < 0 or user_id >= len(USERS):
        return Response(
            "Такого пользователя не существует",
            status=HTTPStatus.NOT_FOUND,
            mimetype="text"
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


@app.post("/posts/create")
def create_post():

    data = request.get_json()
    post_id = len(POSTS)
    try:
        author_id = data["author_id"]
        text = data["text"]
    except KeyError:
        return Response(
            "Не был передан один из параметров",
            status=HTTPStatus.BAD_REQUEST,
            mimetype="text"
        )

    post = models.Post(post_id, author_id, text)
    POSTS.append(models.Post(post_id, author_id, text))
    USERS[author_id].add_post(post)

    response = Response(
        json.dumps(
            {
                "id": post.id,
                "author_id": post.author_id,
                "text": post.text,
                "reactions": post.reactions,
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.get("/posts/<int:post_id>")
def get_information_about_post(post_id):
    if post_id < 0 or post_id >= len(POSTS):
        return Response("Такого поста не существует", status=HTTPStatus.NOT_FOUND,
                        mimetype="text")
    post = POSTS[post_id]
    response = Response(
        json.dumps(
            {
                "id": post.id,
                "author_id": post.author_id,
                "text": post.text,
                "reactions": post.reactions,
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.post("/posts/<int:post_id>/reaction")
def put_a_reaction_to_the_post(post_id):

    data = request.get_json()
    try:
        user_id = data["user_id"]
        reaction = data["reaction"]
    except KeyError:
        return Response(
            "Не был передан один из параметров",
            status=HTTPStatus.BAD_REQUEST,
            mimetype="text"
    )
    if POSTS[post_id].author_id == user_id:
        return Response(
            "Автор поста не может ставить реакции на свой пост",
            status=HTTPStatus.BAD_REQUEST,
            mimetype="text"
        )
    if user_id < 0 or user_id >= len(USERS) or post_id < 0 or post_id >= len(POSTS):
        return Response("Такого пользователя или поста не существует", status=HTTPStatus.NOT_FOUND,
                        mimetype="text")
    POSTS[post_id].add_reaction(reaction)
    USERS[user_id].put_reaction()
    return Response(status=HTTPStatus.OK)


@app.get("/users/<int:user_id>/posts")
def get_all_posts(user_id):
    data = request.get_json()
    try:
        sort = data["sort"]
    except KeyError:
        return Response(
            "Не был передан один из параметров",
            status=HTTPStatus.BAD_REQUEST,
            mimetype="text"
        )
    if user_id < 0 or user_id >= len(USERS):
        return Response(status=HTTPStatus.NOT_FOUND)
    user = USERS[user_id]
    posts = user.get_sorted_posts(sort)
    response = Response(
        models.MyEncoder().encode(
            {
                "posts": [
                    get_information_about_post(post.id).get_json()
                    for post in posts
                ]
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
            "Не был передан один из параметров",
            status=HTTPStatus.BAD_REQUEST,
            mimetype="text"
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

        user_names = [f"{user.first_name} {user.last_name} ({user.id})" for user in sorted_users]
        user_count_reactions = [user.total_reactions for user in sorted_users]

        ax.bar(user_names, user_count_reactions)

        ax.set_ylabel("User's reactions")
        ax.set_title("User leaderboard by quantity reactions")
        plt.savefig("app/static/users_leaderboard.png")
        return Response(
            f'''<img src= "{url_for('static', filename='users_leaderboard.png')}">''',
            status=HTTPStatus.OK,
            mimetype="text/html"
        )
    return Response(status=HTTPStatus.BAD_REQUEST)
