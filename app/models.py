"""
Все модели использующиеся в проекте
"""

# model.py
import json
import re
from app import USERS, POSTS


def get_sorted_users(users, key):
    sorted_users = sorted(
        filter(lambda user: user.is_valid_id(user.id), users),
        key=lambda user: user.total_reactions,
    )
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
        self.status = "created"

    @staticmethod
    def is_valid_email(email):
        """Метод проверяет валидность почту у данного пользователя
        через регулярное выражения, но не проверяет её существование
        или кому она принадлежит"""

        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    def put_reaction(self):
        self.total_reactions += 1

    def get_sorted_posts(self, key):
        posts = list(filter(lambda p: p.status == 'created', self.posts))
        for i in range(len(posts)):
            for j in range(i + 1, len(posts)):
                if posts[i].get_count_reactions() < posts[j].get_count_reactions():
                    posts[i], posts[j] = posts[j], posts[i]
                    posts[i].id, posts[j].id = posts[j].id, posts[i].id
        if key == "asc":
            return posts
        elif key == 'desc':
            return posts[::-1]
        return None

    def add_post(self, post):
        self.posts.append(post)

    @staticmethod
    def is_valid_id(user_id):
        return 0 <= user_id < len(USERS) and USERS[user_id].status != "deleted"


class Post:
    """Создаёт текстовый пост"""

    def __init__(self, post_id, author_id, text):
        self.id = post_id
        self.author_id = author_id
        self.text = text
        self.reactions = []
        self.status = "created"

    def add_reaction(self, reaction):
        self.reactions.append(reaction)

    def get_count_reactions(self):
        return len(self.reactions)

    @staticmethod
    def is_valid_id(post_id):
        return 0 <= post_id < len(POSTS) and POSTS[post_id].status != "deleted"


class MyEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__
