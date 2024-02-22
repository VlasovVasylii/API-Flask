"""
Инициализирующий файл
"""

from flask import Flask

app = Flask(__name__)

USERS = []  # лист для объектов типа пользователь будем хранить в runtime
POSTS = []  # лист, хранящий посты в runtime

from app import views
from app import models
from app import views_all
from app import tests
