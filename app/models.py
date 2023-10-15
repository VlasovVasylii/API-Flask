# model.py
import json
import re


def get_sorted_users(users, key):
    sorted_users = sorted(users, key=lambda user: user.total_reactions)
    if key == "asc":
        return sorted_users
    elif key == "desc":
        return sorted_users[::-1]
    return None


class User:
    """Создаёт пользователя платформы социальной сети"""

    def __init__(self, user_id, first_name, last_name, email):
        self.id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.total_reactions = 0
        self.posts = []

    @staticmethod
    def is_valid_email(email):
        """Метод проверяет валидность почту у данного пользователя
        через регулярное выражения, но не проверяет её существование
        или кому она принадлежит"""

        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return True
        return False

    def put_reaction(self):
        self.total_reactions += 1

    def get_sorted_posts(self, key):
        posts = sorted(self.posts, key=lambda post: post.get_count_reactions())
        if key == "asc":
            return posts
        return posts[::-1]

    def add_post(self, post):
        self.posts.append(post)


class Post:
    """Создаёт текстовый пост"""

    def __init__(self, post_id, author_id, text):
        self.id = post_id
        self.author_id = author_id
        self.text = text
        self.reactions = []

    def add_reaction(self, reaction):
        self.reactions.append(reaction)

    def get_count_reactions(self):
        return len(self.reactions)


class MyEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__
