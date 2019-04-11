from app import db
from flask_login import UserMixin
from app.__init__ import lm
from hashlib import md5

ROLE_USER = 0
ROLE_ADMIN = 1



class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index=True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)

    @staticmethod
    #Этот метод просто добавляет счетчик к нику, пока он не станет уникальным.
    def make_unique_nickname(nickname):
        if User.query.filter_by(nickname = nickname).first() == None:
            return  nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(nickname = new_nickname).first() == None:
                break
            version+=1
        return new_nickname

    def __repr__(self):
        return '<User %r>' % (self.nickname)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)



class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)




# Для связи один-ко-многим поле db.relationship обычно определено
# на стороне «один». С помощью этой связи, мы получаем user.posts пользователя,
# который дает нам список всех записей пользователя.
# Первый аргумент db.relationship указывает на класс «многим» в этой связи.
# Аргумент backref определяет поле, которое будет добавленно к объектам класса «многим»,
# указывающее на объект «один». В нашем случае это означает, что мы можем
# использовать post.author для получения экземпляра User, которым эта запись была создана.



