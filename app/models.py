# model.py
import re


class User:
    """Создаёт пользователя платформы социальной сети"""

    def __init__(self, id, first_name, last_name, email):
        self.id = id
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


class Post:
    """Создаёт текстовый пост"""

    def __init__(self, id, author_id, text):
        self.id = id
        self.author_id = author_id
        self.text = text
        self.reactions = []

    def add_reaction(self, reaction):
        self.reactions.append(reaction)
