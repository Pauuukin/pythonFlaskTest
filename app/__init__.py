from flask import Flask
from flask_login import LoginManager    #настройки расширений для реализации регистрации
from flask_openid import OpenID


from config import basedir, ADMINS, MAIL_PASSWORD, MAIL_PORT, MAIL_SERVER, MAIL_USERNAME
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



if not app.debug:
    #отправка ошибки по почте
    #Мы будем отправлять эти письма только в том случае, если выключен режим отладки.
    import logging
    from logging.handlers import SMTPHandler    #отладочный сервер SMTP, который нам предоставляет Python
    credentials = None
    if MAIL_USERNAME or MAIL_PASSWORD:
        credentials = (MAIL_USERNAME, MAIL_PASSWORD)
    mail_handler = SMTPHandler ((MAIL_SERVER, MAIL_PORT), 'no-reply@' + MAIL_SERVER, ADMINS, 'application failure', credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)
# запуск отладочного сервера: python -m smtpd -n -c DebuggingServer localhost:25

if not app.debug:
    #запись лога в файл
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/appVegworld.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('microblog startup')

# Лог будет сохраняться в папке tmp под именем microblog.log.
# Мы использовали RotatingFileHandler, что позволяет установить лимит на количество
# хранимых данных. В нашем случае размер файла ограничен одним мегабайтом, при этом
# сохраняются последние десять файлов.

# Класс logging.Formatter предоставляет возможность задавать произвольный формат
# записей в логе. Так как мы хотим получать как можно более подробную информацию,
# мы будем сохранять само сообщение, timestamp, статус записи,
# а также имя файла и номер строки, откуда была инициирована запись.