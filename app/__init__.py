from flask import Flask

app = Flask(__name__)

USERS = []  # лист для объектов типа пользователь будем хранить в runtime

from app import views
from app import models
