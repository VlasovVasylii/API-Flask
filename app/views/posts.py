"""
Все руты для работы с постами
"""

from app import app, USERS, POSTS, models
from flask import request, Response
import json
from http import HTTPStatus
from app.models import User, Post


@app.post("/posts/create")
def create_post():
    data = request.get_json()
    post_id = len(POSTS)
    try:
        author_id = data["author_id"]
        text = data["text"]
    except KeyError:
        return Response(
            "Были переданы не все параметры",
            status=HTTPStatus.BAD_REQUEST,
            mimetype="text",
        )
    if User.is_valid_id(author_id):
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
                    "status": post.status,
                }
            ),
            HTTPStatus.OK,
            mimetype="application/json",
        )
        return response
    return Response(
        "Некорректные данные",
        status=HTTPStatus.BAD_REQUEST,
        mimetype="text",
    )


@app.get("/posts/<int:post_id>")
def get_information_about_post(post_id):
    if not Post.is_valid_id(post_id):
        return Response(
            "Такого поста не существует", status=HTTPStatus.NOT_FOUND, mimetype="text"
        )
    post = POSTS[post_id]
    response = Response(
        json.dumps(
            {
                "id": post.id,
                "author_id": post.author_id,
                "text": post.text,
                "reactions": post.reactions,
                "status": post.status,
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
            "Были переданы не все параметры",
            status=HTTPStatus.BAD_REQUEST,
            mimetype="text",
        )
    if POSTS[post_id].author_id == user_id:
        return Response(
            "Автор поста не может ставить реакции на свой пост",
            status=HTTPStatus.BAD_REQUEST,
            mimetype="text",
        )
    if not User.is_valid_id(user_id) or not Post.is_valid_id(post_id):
        return Response(
            "Такого пользователя или поста не существует",
            status=HTTPStatus.NOT_FOUND,
            mimetype="text",
        )
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
            "Были переданы не все параметры",
            status=HTTPStatus.BAD_REQUEST,
            mimetype="text",
        )
    if not User.is_valid_id(user_id):
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


@app.delete("/post/<int:post_id>")
def delete_post(post_id):
    if not Post.is_valid_id(post_id):
        return Response(
            "Такого поста не существует",
            status=HTTPStatus.BAD_REQUEST,
            mimetype="text",
        )

    post = POSTS[post_id]
    post.status = "deleted"

    response = Response(
        json.dumps(
            {
                "id": post.id,
                "author_id": post.author_id,
                "text": post.text,
                "reactions": post.reactions,
                "status": post.status
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response
