from flask import Flask
from flask_login import LoginManager    #настройки расширений для реализации регистрации
from flask_openid import OpenID


from config import basedir
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) #создаем объект приложения, наследуя Flask
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_object('config')    #подключаем конфиг
db = SQLAlchemy(app)    #создаем и инициализируем бд




#Представления — это обработчики, которые отвечают на запросы веб-браузера.
#Представления в Flask пишутся как Python функции.
#Каждая функция представления сопоставляется с одним
# или несколькими запросами URL




lm = LoginManager(app)
lm.init_app(app)
lm.login_view = 'index'

oid = OpenID(app, os.path.join(basedir, 'tmp')) #Расширению Flask-OpenID нужно где-то хранить
                                                # свои временные файлы, для этого при
                                                # инициализации ему передаётся путь до папки tmp.



from app import views, models #импортируем модули
from app.models import User

@lm.user_loader     #лоадер, в мануале его нет, но без него ничего не работало
def load_user(id):
    return User.query.get(int(id))
