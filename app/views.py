from app import app, USERS, POSTS, models
from flask import request, Response
import json
from http import HTTPStatus


@app.post("/users/create")
def user_create():
    try:
        data = request.get_json()
        user_id = len(USERS)
        first_name = data["first_name"]
        last_name = data["last_name"]
        email = data["email"]
    except Exception:
        return Response(status=HTTPStatus.BAD_REQUEST)

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
                    "posts": [get_information_about_post(post.id).get_json() for post in user.posts],
                }
            ),
            HTTPStatus.OK,
            mimetype="application/json",
        )
        return response
    return Response(status=HTTPStatus.BAD_REQUEST)


@app.get("/users/<int:user_id>")
def get_user(user_id):
    if user_id < 0 or user_id >= len(USERS):
        return Response(status=HTTPStatus.NOT_FOUND)
    user = USERS[user_id]
    response = Response(
        models.MyEncoder().encode({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "total_reactions": user.total_reactions,
                "posts": [get_information_about_post(post.id).get_json() for post in user.posts],
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.post("/posts/create")
def create_post():
    try:
        data = request.get_json()
        post_id = len(POSTS)
        author_id = data["author_id"]
        text = data["text"]
    except KeyError:
        return Response(status=HTTPStatus.BAD_REQUEST)
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
        return Response(status=HTTPStatus.NOT_FOUND)
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
    try:
        data = request.get_json()
        user_id = data["user_id"]
        reaction = data["reaction"]
    except Exception:
        return Response(status=HTTPStatus.BAD_REQUEST)
    if POSTS[post_id].author_id == user_id:
        return Response(status=HTTPStatus.BAD_REQUEST)
    if user_id < 0 or user_id >= len(USERS) or post_id < 0 or post_id >= len(POSTS):
        return Response(status=HTTPStatus.NOT_FOUND)
    POSTS[post_id].add_reaction(reaction)
    USERS[user_id].put_reaction()
    return Response(status=HTTPStatus.OK)


@app.get('/users/<int:user_id>/posts')
def get_all_posts(user_id):
    try:
        data = request.get_json()
        sort = data['sort']
    except Exception:
        return Response(status=HTTPStatus.BAD_REQUEST)
    if user_id < 0 or user_id >= len(USERS):
        return Response(status=HTTPStatus.NOT_FOUND)
    user = USERS[user_id]
    posts = user.get_sorted_posts(sort)
    response = Response(
        models.MyEncoder().encode({"posts": [get_information_about_post(post.id).get_json() for post in user.posts]}),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.get('/users/leaderboard')
def get_information_about_users():
    pass
