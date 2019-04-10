
CSRF_ENABLE = True                      #активирует предотвращение поддельных межсайтовых запросов
SECRET_KEY = 'you-will-never-guess'     #используется для создания криптографического токена, который используется при валидации формы.
                                        # Когда вы пишете свое приложение, убедитесь,
                                        # что ваш секретный ключ сложно подобрать.
OPENID_PROVIDERS = [
    { 'name': 'Google', 'url': 'https://openid-provider.appspot.com/oleg.paukin'},
    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' +os.path.join(basedir,'app.db') #SQLALCHEMY_DATABASE_URI необходим для расширения Flask-SQLAlchemy. Это путь к файлу с нашей базой данных.
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')    #SQLALCHEMY_MIGRATE_REPO — это папка, где мы будем хранить файлы SQLAlchemy-migrate


#конфиг с настройками для расширений Flask