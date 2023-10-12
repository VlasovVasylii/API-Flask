# model.py


class User:
    """Создаёт класс пользователя платформы социальной сети"""

    def __init__(self, id, first_name, last_name, email):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.total_reactions = 0
        self.posts = []
